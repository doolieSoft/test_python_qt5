import sys
import urllib

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QPushButton, QTableWidgetItem, QLineEdit, QAction, \
    QDialog, QLabel

CURRENT_VERSION = "1.0.0"


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle("Add Line to Table")

        # Définir les variables des éléments de la fenêtre
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.button = self.findChild(QPushButton, "pushButton")
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.action_verifier_mise_jour = self.findChild(QAction, "action_verifier_mise_jour")

        # Prendre toute la largeur du tableau
        self.table.horizontalHeader().setStretchLastSection(True)

        # Mapper les événements aux fonctions
        self.button.clicked.connect(self.add_line_to_table)
        self.action_verifier_mise_jour.triggered.connect(self.verifier_mise_jour)
        self.lineEdit.returnPressed.connect(self.add_line_to_table)
        self.lineEdit.setFocusPolicy(Qt.StrongFocus)
        self.show()

    def add_line_to_table(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition, 0, QTableWidgetItem(self.lineEdit.text()))
        self.lineEdit.setText("")
        self.lineEdit.setFocus()

    def verifier_mise_jour(self):
        with open('c:/temp/repository/main/version.txt', 'r') as fichier:
            repo_version = fichier.readline()

            if CURRENT_VERSION < repo_version:
                print(
                    f"La version de main n'est pas à jour : Votre version {CURRENT_VERSION} => Version actuelle {repo_version}")
                update_dialog = UpdateDialog(current_version=CURRENT_VERSION, repo_version=repo_version)
                update_dialog.exec_()
            else:
                up_to_date_dialog = UpToDateDialog()
                up_to_date_dialog.exec_()


class UpToDateDialog(QDialog):
    def __init__(self):
        super(UpToDateDialog, self).__init__()
        uic.loadUi('up_to_date_dialog.ui', self)
        self.setWindowTitle("Application à jour")


class UpdateDialog(QDialog):
    def __init__(self, current_version, repo_version):
        super(UpdateDialog, self).__init__()
        uic.loadUi('update_dialog.ui', self)
        self.setWindowTitle("Verifier mise à jour")

        self.current_version = current_version
        self.repo_version = repo_version

        self.label_current_version = self.findChild(QLabel, "current_version")
        self.label_repo_version = self.findChild(QLabel, "repo_version")
        self.button_update = self.findChild(QPushButton, "button_update")
        self.button_dont_update = self.findChild(QPushButton, "button_dont_update")

        self.button_update.clicked.connect(self.do_update)
        self.button_dont_update.clicked.connect(self.dont_update)

        self.label_current_version.setText(self.current_version)
        self.label_repo_version.setText(self.repo_version)

    def do_update(self):
        print("Mise à jour en cours...")
        self.close()

    def dont_update(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
