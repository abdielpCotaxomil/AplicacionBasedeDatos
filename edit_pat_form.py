from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QFormLayout, QLineEdit, QDateEdit, QMessageBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QDate
import psycopg2
import sys

class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="tu_db",
            user="tu_usuario",
            password="tu_contraseña",
            host="localhost"
        )
        self.cursor = self.connection.cursor()

class EditPatForm(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Lista de Empleados")

        self.layout = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.layout.addWidget(self.list_widget)

        self.load_data_btn = QPushButton('Cargar Datos', self)
        self.load_data_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_btn)

        self.setLayout(self.layout)

    def load_data(self):
        try:
            query = "SELECT num_empleado, nombre, apellido_paterno, apellido_materno FROM empleado_patio"
            self.db.cursor.execute(query)
            rows = self.db.cursor.fetchall()

            self.list_widget.clear()
            for row in rows:
                item_widget = QWidget()
                item_layout = QHBoxLayout()
                item_layout.setContentsMargins(0, 0, 0, 0)
                
                item_text = f"{row[0]} - {row[1]} {row[2]} {row[3]}"
                item_label = QLabel(item_text)
                item_label.setFixedHeight(25)

                edit_btn = QPushButton("Editar")
                edit_btn.setStyleSheet("background-color: rgb(255, 165, 0);")
                edit_btn.setFixedSize(50, 16)
                edit_btn.clicked.connect(lambda ch, row=row: self.edit_item(row[0]))
                
                item_layout.addWidget(item_label)
                item_layout.addWidget(edit_btn)
                
                item_widget.setLayout(item_layout)
                
                list_item = QListWidgetItem(self.list_widget)
                list_item.setSizeHint(item_widget.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)
                
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)

    def edit_item(self, item_id):
        self.edit_window = EditWindow(self.db, item_id)
        self.edit_window.show()

class EditWindow(QWidget):
    def __init__(self, db, item_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.item_id = item_id
        self.setWindowTitle("Editar Empleado")
        
        self.layout = QFormLayout()
        
        self.nombre = QLineEdit(self)
        self.layout.addRow('Nombre:', self.nombre)

        self.apellido_paterno = QLineEdit(self)
        self.layout.addRow('Apellido Paterno:', self.apellido_paterno)

        self.apellido_materno = QLineEdit(self)
        self.layout.addRow('Apellido Materno:', self.apellido_materno)

        self.puesto = QLineEdit(self)
        self.layout.addRow('Puesto:', self.puesto)

        self.salario = QLineEdit(self)
        self.layout.addRow('Salario:', self.salario)

        self.rfc = QLineEdit(self)
        self.layout.addRow('RFC:', self.rfc)

        self.nss = QLineEdit(self)
        self.layout.addRow('NSS:', self.nss)

        self.curp = QLineEdit(self)
        self.layout.addRow('CURP:', self.curp)

        self.update_btn = QPushButton('Actualizar Datos', self)
        self.update_btn.clicked.connect(self.update_data)
        self.layout.addWidget(self.update_btn)

        self.setLayout(self.layout)

        self.load_data()

    def load_data(self):
        try:
            query = """
            SELECT nombre, apellido_paterno, apellido_materno, puesto, salario, rfc, nss, curp
            FROM empleado_patio
            WHERE num_empleado = %s
            """
            self.db.cursor.execute(query, (self.item_id,))
            row = self.db.cursor.fetchone()

            if row:
                self.nombre.setText(row[0])
                self.apellido_paterno.setText(row[1])
                self.apellido_materno.setText(row[2])
                self.puesto.setText(row[3])
                self.salario.setText(str(row[4]))
                self.rfc.setText(row[5])
                self.nss.setText(row[6])
                self.curp.setText(row[7])

            else:
                QMessageBox.warning(self, 'Error', 'No se encontró el chofer con el ID proporcionado', QMessageBox.Ok)
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)

    def update_data(self):
        try:
            nombre = self.nombre.text()
            apellido_paterno = self.apellido_paterno.text()
            apellido_materno = self.apellido_materno.text()
            puesto = self.puesto.text()
            salario = self.salario.text()
            rfc = self.rfc.text()
            nss = self.nss.text()
            curp = self.curp.text()

            if not all([nombre, apellido_paterno, apellido_materno, puesto, salario, rfc, nss, curp]):
                QMessageBox.critical(self, 'Error', 'Todos los campos deben estar llenos', QMessageBox.Ok)
                return

            query = """
            UPDATE empleado_patio
            SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, puesto = %s, salario = %s, rfc = %s, nss = %s, curp = %s
            WHERE num_empleado = %s
            """

            self.db.cursor.execute(query, (nombre, apellido_paterno, apellido_materno, puesto, salario, rfc, nss, curp, self.item_id))
            self.db.connection.commit()
            QMessageBox.information(self, 'Éxito', 'Datos actualizados correctamente', QMessageBox.Ok)
            self.close()
        except psycopg2.Error as e:
            self.db.connection.rollback()
            print(f"Error durante la actualización del query: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo actualizar el chofer: {e}', QMessageBox.Ok)
        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
