import os
import json
import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QDialog,
    QHeaderView, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from new_ticket_window import NewTicketDialog
from edit_ticket_window import EditTicketDialog

class MainWindow(QMainWindow):
    def __init__(self, ticket_service):
        super().__init__()
        self.ticket_service = ticket_service
        self.setWindowTitle("Gestion des Tickets")
        # Taille par défaut : ici 1000 x 700 px (modifiable)
        self.resize(1000, 700)

        # Conteneur principal
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # -- Zone pour la date de dernière modification (affichée en haut à droite) --
        self.top_layout = QHBoxLayout()
        self.mod_date_label = QLabel()
        self.mod_date_label.setStyleSheet("color: #555;")
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.mod_date_label)
        self.layout.addLayout(self.top_layout)
        self.update_mod_date_label()

        # Charger la configuration pour récupérer les listes de filtres
        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
        self.filter_mapping = {
            "Programme": self.config.get("programmes", []),
            "Statut": self.config.get("statuts", []),
            "Priorité": self.config.get("priorites", [])
        }

        # -- Zone de filtres (champs de recherche) --
        self.filter_layout = QHBoxLayout()
        self.filter_layout.setSpacing(8)
        self.filter_layout.setAlignment(Qt.AlignLeft)
        self.filters = {}
        # Largeurs fixes pour les champs de filtre
        filter_widths = {
            "N°": 50,
            "Nom": 120,
            "Description": 200,
            "Programme": 150,
            "Statut": 150,
            "Priorité": 150
        }
        # Pour chaque colonne, créer un label et le widget de filtre correspondant
        for header in self.ticket_service.columns:
            lbl = QLabel(header)
            # Appliquer la police de la fenêtre pour les labels
            font = lbl.font()
            font.setPointSize(self.table_font_size())
            lbl.setFont(font)
            lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            if header in self.filter_mapping:
                # Pour les colonnes avec des valeurs définies dans config.json, utiliser un QComboBox
                combo = QComboBox()
                combo.addItem("")  # Option vide pour ne pas filtrer
                combo.addItems(self.filter_mapping[header])
                combo.currentTextChanged.connect(self.apply_filters)
                if header in filter_widths:
                    combo.setFixedWidth(filter_widths[header])
                combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.filter_layout.addWidget(lbl)
                self.filter_layout.addWidget(combo)
                self.filters[header] = combo
            else:
                # Sinon, utiliser un QLineEdit
                edit = QLineEdit()
                edit.setPlaceholderText(f"Filtrer par {header}")
                edit.textChanged.connect(self.apply_filters)
                if header in filter_widths:
                    edit.setFixedWidth(filter_widths[header])
                edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.filter_layout.addWidget(lbl)
                self.filter_layout.addWidget(edit)
                self.filters[header] = edit

        # Ajout d'un stretch à la fin pour garder les widgets collés à gauche
        self.filter_layout.addStretch()
        self.layout.addLayout(self.filter_layout)

        # -- Table affichant les tickets --
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.ticket_service.columns))
        self.table.setHorizontalHeaderLabels(self.ticket_service.columns)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(True)
        self.table.setTextElideMode(Qt.ElideNone)
        # Définir l'alternate background color en bleu très clair
        self.table.setStyleSheet("QTableWidget { alternate-background-color: #E0F7FA; }")

        # Configuration du mode de redimensionnement des colonnes
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.Fixed)   # N°
        header_view.setSectionResizeMode(1, QHeaderView.Fixed)   # Nom
        header_view.setSectionResizeMode(2, QHeaderView.Fixed)   # Programme
        header_view.setSectionResizeMode(4, QHeaderView.Fixed)   # Statut
        header_view.setSectionResizeMode(5, QHeaderView.Fixed)   # Priorité
        header_view.setSectionResizeMode(3, QHeaderView.Stretch) # Description

        # Redimensionnement vertical automatique (hauteur de ligne)
        vertical_header = self.table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # Appliquer la police des entêtes pour qu'elle corresponde au contenu
        self.set_header_font(self.table.font())

        self.layout.addWidget(self.table)

        # -- Boutons d'action --
        self.button_layout = QHBoxLayout()
        self.btn_new = QPushButton("Nouveau Ticket")
        self.btn_new.clicked.connect(self.open_new_ticket)
        self.button_layout.addWidget(self.btn_new)
        self.btn_edit = QPushButton("Modifier Ticket")
        self.btn_edit.clicked.connect(self.edit_ticket)
        self.button_layout.addWidget(self.btn_edit)
        self.btn_delete = QPushButton("Supprimer Ticket")
        self.btn_delete.clicked.connect(self.delete_ticket)
        self.button_layout.addWidget(self.btn_delete)
        self.layout.addLayout(self.button_layout)

        self.load_table()

    def table_font_size(self):
        # Utilise la police par défaut de la fenêtre
        return self.font().pointSize()

    def set_header_font(self, font):
        header = self.table.horizontalHeader()
        header.setFont(font)

    def update_mod_date_label(self):
        # Met à jour le label avec la date de dernière modification du fichier Excel
        file_path = self.ticket_service.file_path
        if os.path.exists(file_path):
            mod_timestamp = os.path.getmtime(file_path)
            mod_date = datetime.datetime.fromtimestamp(mod_timestamp)
            formatted_date = mod_date.strftime("%d/%m/%Y %H:%M:%S")
            self.mod_date_label.setText(f"Derniére modification : {formatted_date}")
        else:
            self.mod_date_label.setText("Fichier non trouvé")

    def load_table(self):
        df = self.ticket_service.df
        self.table.setRowCount(0)
        for _, row in df.iterrows():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, col_name in enumerate(self.ticket_service.columns):
                text = str(row[col_name]).rstrip()
                item = QTableWidgetItem(text)
                # Centrer le contenu pour les colonnes "N°" et "Priorité"
                if col_name == "N°" or col_name == "Priorité":
                    item.setTextAlignment(Qt.AlignCenter)
                # Code couleur pour "Statut"
                if col_name == "Statut":
                    if text == "Ouvert":
                        item.setBackground(QColor("#82E0AA"))
                    elif text == "Fermé":
                        item.setBackground(QColor("#F1948A"))
                # Code couleur pour "Priorité"
                if col_name == "Priorité":
                    if text == "P1":
                        item.setBackground(QColor("#85C1E9"))
                    elif text == "P2":
                        item.setBackground(QColor("#F8C471"))
                    elif text == "P3":
                        item.setBackground(QColor("#E74C3C"))
                self.table.setItem(row_position, col, item)
        self.set_column_widths()
        self.table.resizeRowsToContents()
        self.table.repaint()
        self.update_mod_date_label()

    def set_column_widths(self):
        fixed_widths = {
            "N°": 50,
            "Nom": 120,
            "Programme": 100,
            "Description": 400,
            "Statut": 80,
            "Priorité": 60
        }
        for col, header in enumerate(self.ticket_service.columns):
            if header in fixed_widths:
                self.table.setColumnWidth(col, fixed_widths[header])

    def apply_filters(self):
        df = self.ticket_service.df.copy()
        for header, widget in self.filters.items():
            if isinstance(widget, QLineEdit):
                filter_text = widget.text().strip().lower()
            elif isinstance(widget, QComboBox):
                filter_text = widget.currentText().strip().lower()
            else:
                filter_text = ""
            if filter_text:
                df = df[df[header].astype(str).str.lower().str.contains(filter_text)]
        self.table.setRowCount(0)
        for _, row in df.iterrows():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, col_name in enumerate(self.ticket_service.columns):
                text = str(row[col_name]).rstrip()
                item = QTableWidgetItem(text)
                if col_name == "N°" or col_name == "Priorité":
                    item.setTextAlignment(Qt.AlignCenter)
                if col_name == "Statut":
                    if text == "Ouvert":
                        item.setBackground(QColor("#82E0AA"))
                    elif text == "Fermé":
                        item.setBackground(QColor("#F1948A"))
                if col_name == "Priorité":
                    if text == "P1":
                        item.setBackground(QColor("#85C1E9"))
                    elif text == "P2":
                        item.setBackground(QColor("#F8C471"))
                    elif text == "P3":
                        item.setBackground(QColor("#E74C3C"))
                self.table.setItem(row_position, col, item)
        self.set_column_widths()
        self.table.resizeRowsToContents()
        self.table.repaint()

    def open_new_ticket(self):
        dialog = NewTicketDialog(self.ticket_service, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.ticket_service.load_tickets()
            self.load_table()

    def edit_ticket(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner un ticket à modifier.")
            return
        row = selected_items[0].row()
        ticket_num_item = self.table.item(row, 0)
        try:
            ticket_num = int(ticket_num_item.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Ticket invalide.")
            return
        df = self.ticket_service.df
        ticket_data = df[df["N°"] == ticket_num].iloc[0].to_dict()
        dialog = EditTicketDialog(self.ticket_service, ticket_data, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.ticket_service.load_tickets()
            self.load_table()

    def delete_ticket(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner un ticket à supprimer.")
            return
        row = selected_items[0].row()
        ticket_num_item = self.table.item(row, 0)
        try:
            ticket_num = int(ticket_num_item.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Ticket invalide.")
            return
        reply = QMessageBox.question(
            self, "Confirmation",
            f"Confirmez-vous la suppression du ticket {ticket_num} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.ticket_service.delete_ticket(ticket_num)
            self.ticket_service.load_tickets()
            self.load_table()

    def showEvent(self, event):
        super().showEvent(event)
        self.table.resizeRowsToContents()
        self.table.repaint()