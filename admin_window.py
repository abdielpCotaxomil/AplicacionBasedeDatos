import datetime
import os
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox, QInputDialog, QLabel, QDialog, QFormLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from add_chofer_form import AddChoferForm
from add_patio_form import AddPatioForm
from add_autobus_form import AddAutobusForm
from edit_cho_form import EditChoForm
from edit_pat_form import EditPatForm
from edit_aut_form import EditAutForm
from del_cho_form import DelChoForm
from del_pat_form import DelPatForm
from del_aut_form import DelAutForm
from info_cho import InfoCho
from info_pat import InfoPat

class AdminWindow(QMainWindow):
    def __init__(self, db):
        super(AdminWindow, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Administración')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        h_layout1 = QHBoxLayout()

        self.add_chofer_button = QPushButton('Agregar Chofer', self)
        self.add_chofer_button.clicked.connect(self.show_add_chofer_form)
        h_layout1.addWidget(self.add_chofer_button)

        self.edit_data_button = QPushButton('Editar Datos', self)
        self.edit_data_button.clicked.connect(self.show_edit_cho_form)
        self.edit_data_button.setStyleSheet("background-color: rgb(255, 165, 0);")
        self.edit_data_button.setFixedSize(120, 40)
        h_layout1.addWidget(self.edit_data_button)

        self.del_data_button = QPushButton('Eliminar Datos', self)
        self.del_data_button.clicked.connect(self.show_del_cho_form)
        self.del_data_button.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.del_data_button.setFixedSize(120, 40)
        h_layout1.addWidget(self.del_data_button)

        layout.addLayout(h_layout1)

        h_layout2 = QHBoxLayout()

        self.add_patio_button = QPushButton('Agregar Patio', self)
        self.add_patio_button.clicked.connect(self.show_add_patio_form)
        h_layout2.addWidget(self.add_patio_button)

        self.edit_patio_button = QPushButton('Editar Datos', self)
        self.edit_patio_button.clicked.connect(self.show_edit_pat_form)
        self.edit_patio_button.setStyleSheet("background-color: rgb(255, 165, 0);")
        self.edit_patio_button.setFixedSize(120, 40)
        h_layout2.addWidget(self.edit_patio_button)

        self.del_patio_button = QPushButton('Eliminar Datos', self)
        self.del_patio_button.clicked.connect(self.show_del_pat_form)
        self.del_patio_button.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.del_patio_button.setFixedSize(120, 40)
        h_layout2.addWidget(self.del_patio_button)

        layout.addLayout(h_layout2)

        h_layout3 = QHBoxLayout()

        self.add_bus_button = QPushButton('Agregar Autobus', self)
        self.add_bus_button.clicked.connect(self.show_add_autobus_form)
        h_layout3.addWidget(self.add_bus_button)

        self.edit_bus_button = QPushButton('Editar Datos', self)
        self.edit_bus_button.clicked.connect(self.show_edit_aut_form)
        self.edit_bus_button.setStyleSheet("background-color: rgb(255, 165, 0);")
        self.edit_bus_button.setFixedSize(120, 40)
        h_layout3.addWidget(self.edit_bus_button)

        self.del_bus_button = QPushButton('Eliminar Datos', self)
        self.del_bus_button.clicked.connect(self.show_del_aut_form)
        self.del_bus_button.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.del_bus_button.setFixedSize(120, 40)
        h_layout3.addWidget(self.del_bus_button)

        layout.addLayout(h_layout3)

        self.view_info_button = QPushButton('Ver Información', self)
        self.view_info_button.clicked.connect(self.show_info_options)
        layout.addWidget(self.view_info_button)

        self.check_tarjeton_button = QPushButton('Verificar Validez de Tarjetones', self)
        self.check_tarjeton_button.clicked.connect(self.check_tarjeton_validity)
        layout.addWidget(self.check_tarjeton_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)


    def show_add_chofer_form(self):
        self.add_chofer_form = AddChoferForm(self.db)
        self.add_chofer_form.show()

    def show_add_patio_form(self):
        self.add_patio_form = AddPatioForm(self.db)
        self.add_patio_form.show()

    def show_add_autobus_form(self):
        self.add_autobus_form = AddAutobusForm(self.db)
        self.add_autobus_form.show()

    def show_edit_cho_form(self):
        self.edit_cho_form = EditChoForm(self.db)
        self.edit_cho_form.show()

    def show_edit_pat_form(self):
        self.edit_pat_form = EditPatForm(self.db)
        self.edit_pat_form.show()

    def show_edit_aut_form(self):
        self.edit_aut_form = EditAutForm(self.db)
        self.edit_aut_form.show()

    def show_del_cho_form(self):
        self.del_cho_form = DelChoForm(self.db)
        self.del_cho_form.show()

    def show_del_pat_form(self):
        self.del_pat_form = DelPatForm(self.db)
        self.del_pat_form.show()

    def show_del_aut_form(self):
        self.del_aut_form = DelAutForm(self.db)
        self.del_aut_form.show()

    def show_info_options(self):
        info_type, ok = QInputDialog.getItem(self, "Ver Información", "Selecciona el tipo de información a ver:", ["Chofer", "Patio", "Autobus"], 0, False)
        if ok and info_type:
            if info_type == "Chofer":
                self.show_chofer_info()
            elif info_type == "Patio":
                self.show_pat_info()
            elif info_type == "Autobus":
                self.show_bus_info()

    def show_chofer_info(self):
        self.info_chofer_window = InfoCho(self.db)
        self.info_chofer_window.show()

    def show_pat_info(self):
        self.info_pat_window = InfoPat(self.db)
        self.info_pat_window.show()

    def show_bus_info(self):
        query = "SELECT * FROM autobus"
        try:
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            if results:
                info = "\n".join([str(result) for result in results])
                QMessageBox.information(self, "Información de Autobuses", info, QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Información de Autobuses", "No se encontraron registros.", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener la información de autobuses: {e}", QMessageBox.Ok)
    

    def check_tarjeton_validity(self):
        query = "SELECT nombre, apellido_paterno, apellido_materno, fecha_vencimiento_tarjeton FROM empleado_chofer"
        try:
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            if results:
                today = datetime.date.today()
                one_month_later = today + datetime.timedelta(days=30)
                valid_info = []
                for result in results:
                    nombre, apellido_paterno, apellido_materno, fecha_vencimiento = result
                    if today > fecha_vencimiento:
                        valid_info.append(f"Chofer: {nombre} {apellido_paterno} {apellido_materno}<br>Fecha de vencimiento: {fecha_vencimiento} - Tarjetón: <span style='color: red;'>Inválido</span>")
                    elif today <= fecha_vencimiento <= one_month_later:
                        valid_info.append(f"Chofer: {nombre} {apellido_paterno} {apellido_materno}<br>Fecha de vencimiento: {fecha_vencimiento} - Tarjetón: <span style='color: blue;'>Pendiente</span>")
                    else:
                        valid_info.append(f"Chofer: {nombre} {apellido_paterno} {apellido_materno}<br>Fecha de vencimiento: {fecha_vencimiento} - Tarjetón: <span style='color: green;'>Válido</span>")
                info_message = "<br><br>".join(valid_info)
                QMessageBox.information(self, "Validez de Tarjetones", info_message, QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Validez de Tarjetones", "No se encontraron registros.", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al verificar la validez de los tarjetones: {e}", QMessageBox.Ok)
