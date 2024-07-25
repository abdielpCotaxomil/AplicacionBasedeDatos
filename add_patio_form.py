from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, 
    QFileDialog, QMessageBox, QProgressDialog
)
from PyQt5.QtCore import Qt
import psycopg2
from empleado_info_window import EmpleadoInfoWindow

class AddPatioForm(QWidget):
    def __init__(self, db, parent=None):
        super(AddPatioForm, self).__init__(parent)
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Agregar Empleado')
        self.resize(400, 400)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.num_empleado = QLineEdit(self)
        form_layout.addRow('Num Empleado:', self.num_empleado)

        self.nombre = QLineEdit(self)
        form_layout.addRow('Nombre:', self.nombre)

        self.apellido_paterno = QLineEdit(self)
        form_layout.addRow('Apellido Paterno:', self.apellido_paterno)

        self.apellido_materno = QLineEdit(self)
        form_layout.addRow('Apellido Materno:', self.apellido_materno)

        self.puesto = QLineEdit(self)
        form_layout.addRow('Puesto:', self.puesto)

        self.salario = QLineEdit(self)
        form_layout.addRow('Salario:', self.salario)

        self.rfc = QLineEdit(self)
        form_layout.addRow('RFC:', self.rfc)

        self.nss = QLineEdit(self)
        form_layout.addRow('NSS:', self.nss)

        self.curp = QLineEdit(self)
        form_layout.addRow('CURP:', self.curp)

        self.submit_btn = QPushButton('Agregar Empleado', self)
        self.submit_btn.clicked.connect(self.submit_form)
        form_layout.addRow(self.submit_btn)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def submit_form(self):
        try:
            num_empleado = self.num_empleado.text()
            nombre = self.nombre.text()
            apellido_paterno = self.apellido_paterno.text()
            apellido_materno = self.apellido_materno.text()
            puesto = self.puesto.text()
            salario = self.salario.text()
            rfc = self.rfc.text()
            nss = self.nss.text()
            curp = self.curp.text()

            if not all([num_empleado, nombre, apellido_paterno, apellido_materno, puesto, salario, rfc, nss, curp]):
                QMessageBox.critical(self, 'Error', 'Todos los campos deben estar llenos', QMessageBox.Ok)
                return

            query = """
            INSERT INTO empleado_patio (num_empleado, nombre, apellido_paterno, apellido_materno, puesto, salario, rfc, nss, curp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING num_empleado
            """

            try:
                self.db.cursor.execute(query, (num_empleado, nombre, apellido_paterno, apellido_materno, puesto, salario, rfc, nss, curp))
                id_empleado = self.db.cursor.fetchone()[0]
                self.db.connection.commit()

                QMessageBox.information(self, 'Éxito', f'Empleado agregado correctamente con ID: {id_empleado}', QMessageBox.Ok)
                self.close()
            except psycopg2.Error as e:
                self.db.connection.rollback()
                QMessageBox.critical(self, 'Error', f'No se pudo agregar el empleado: {e}', QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error inesperado fuera del formulario: {e}', QMessageBox.Ok)
    
    def fetch_patio_data(self, num_empleado):
        try:
            query = """
            SELECT num_empleado, nombre, apellido_paterno, apellido_materno, puesto, salario, rfc, nss, curp
            FROM empleado_patio
            WHERE num_empleado = %s
            """
            self.db.cursor.execute(query, (num_empleado,))
            row = self.db.cursor.fetchone()

            empleado_data = {
                "num_empleado": row[0],
                "Nombre": row[1],
                "Apellido Paterno": row[2],
                "Apellido Materno": row[3],
                "puesto": row[4],
                "salario": row[5],
                "nss": row[6],
                "curp": row[7]
            }
            return empleado_data
        except Exception as e:
            print(f"Error obteniendo los datos del empleado: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo obtener los datos del empleado: {e}', QMessageBox.Ok)
            return {}

    def show_empleado_info(self, empleado_data):
        self.empleado_info_window = EmpleadoInfoWindow(empleado_data)
        self.empleado_info_window.exec_()
