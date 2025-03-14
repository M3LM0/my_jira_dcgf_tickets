import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from ticket_service import TicketService
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # 1) Utilisation du style "Fusion" plus moderne
    app.setStyle("Fusion")

    # 2) Personnalisation de la palette (couleurs principales)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 245, 245))         # Fond des fenêtres
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))           # Texte
    palette.setColor(QPalette.Base, QColor(255, 255, 255))           # Fond des champs (LineEdit, etc.)
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))  # Fond alterné dans les tableaux
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 225))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(230, 230, 230))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(51, 153, 255))       # Couleur de surbrillance (sélection)
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    app.setPalette(palette)

    # Initialisation du service et de la fenêtre principale
    ticket_service = TicketService()
    window = MainWindow(ticket_service)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()