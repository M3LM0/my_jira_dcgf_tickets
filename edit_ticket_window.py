from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QComboBox, QPushButton, QMessageBox
import json

class EditTicketDialog(QDialog):
    def __init__(self, ticket_service, ticket_data, config_path="config.json", parent=None):
        super().__init__(parent)
        self.ticket_service = ticket_service
        self.ticket_data = ticket_data
        self.setWindowTitle("Modifier Ticket")
        self.resize(500, 300)

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.programmes = self.config.get("programmes", [])
        self.statuts = self.config.get("statuts", [])
        self.priorites = self.config.get("priorites", [])

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.nom_edit = QLineEdit()
        self.nom_edit.setText(ticket_data.get("Nom", ""))
        form_layout.addRow("Nom :", self.nom_edit)

        self.programme_combo = QComboBox()
        self.programme_combo.addItems(self.programmes)
        current_programme = ticket_data.get("Programme", "")
        if current_programme in self.programmes:
            self.programme_combo.setCurrentIndex(self.programmes.index(current_programme))
        form_layout.addRow("Programme :", self.programme_combo)

        self.description_edit = QTextEdit()
        self.description_edit.setText(ticket_data.get("Description", ""))
        form_layout.addRow("Description :", self.description_edit)

        self.statut_combo = QComboBox()
        self.statut_combo.addItems(self.statuts)
        current_statut = ticket_data.get("Statut", "")
        if current_statut in self.statuts:
            self.statut_combo.setCurrentIndex(self.statuts.index(current_statut))
        form_layout.addRow("Statut :", self.statut_combo)

        self.priorite_combo = QComboBox()
        self.priorite_combo.addItems(self.priorites)
        current_priorite = ticket_data.get("Priorité", "")
        if current_priorite in self.priorites:
            self.priorite_combo.setCurrentIndex(self.priorites.index(current_priorite))
        form_layout.addRow("Priorité :", self.priorite_combo)

        layout.addLayout(form_layout)

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.save_ticket)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def save_ticket(self):
        nom = self.nom_edit.text().strip()
        programme = self.programme_combo.currentText()
        description = self.description_edit.toPlainText().strip()
        statut = self.statut_combo.currentText()
        priorite = self.priorite_combo.currentText()

        if not nom or not description:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs requis.")
            return

        ticket_number = self.ticket_data.get("N°")
        self.ticket_service.update_ticket(ticket_number, nom, programme, description, statut, priorite)
        self.accept()