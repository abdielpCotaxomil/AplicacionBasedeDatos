from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QFormLayout, QLineEdit, QDateEdit, QMessageBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QDate
import psycopg2
import sys
from datetime import date

class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="tu_db",
            user="tu_usuario",
            password="tu_contraseña",
            host="localhost"
        )
        self.cursor = self.connection.cursor()

class EditAutForm(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Lista de Autobuses")
        self.resize(600, 600)

        self.layout = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.list_widget.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
        self.layout.addWidget(self.list_widget)

        self.load_data_btn = QPushButton('Cargar Datos', self)
        self.load_data_btn.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
        self.load_data_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_btn)

        self.setLayout(self.layout)

    def load_data(self):
        try:
            query = """
            SELECT eco, placa, numero_serie, numero_motor, fecha_vigencia_seguro, nombre_aseguradora
            FROM autobus
            WHERE estatus = 'ACTIVO'
            """
            self.db.cursor.execute(query)
            rows = self.db.cursor.fetchall()

            self.list_widget.clear()
            for row in rows:
                item_widget = QWidget()
                item_layout = QHBoxLayout()
                item_layout.setContentsMargins(0, 0, 0, 0)
                
                item_text = f"{row[0]} - {row[1]} {row[2]} {row[3]}"
                item_label = QLabel(item_text)
                item_label.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
                item_label.setFixedHeight(40)  # Ajusta la altura si es necesario

                edit_btn = QPushButton("Editar")
                edit_btn.setStyleSheet("background-color: rgb(255, 165, 0); font-size: 16px;")  # Aumentar tamaño de fuente
                edit_btn.setFixedSize(80, 50)  # Ajusta el tamaño si es necesario
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
        self.setWindowTitle("Editar Autobus")
        
        self.layout = QFormLayout()
        
        self.placa = QLineEdit(self)
        self.placa.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
        self.layout.addRow('Placa:', self.placa)

        self.numero_serie = QLineEdit(self)
        self.numero_serie.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
        self.layout.addRow('Numero de Serie:', self.numero_serie)

        self.numero_motor = QLineEdit(self)
        self.numero_motor.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
        self.layout.addRow('Numero Motor:', self.numero_motor)

        self.fecha_vigencia_seguro = QDateEdit(self)
        self.fecha_vigencia_seguro.setCalendarPopup(True)
        self.fecha_vigencia_seguro.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
        self.layout.addRow('Fecha de Vigencia de Seguro:', self.fecha_vigencia_seguro)

        self.nombre_aseguradora = QLineEdit(self)
        self.nombre_aseguradora.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
        self.layout.addRow('Nombre de Aseguradora:', self.nombre_aseguradora)

        self.update_btn = QPushButton('Actualizar Datos', self)
        self.update_btn.setStyleSheet("font-size: 16px;")  # Aumentar tamaño de fuente
        self.update_btn.clicked.connect(self.update_data)
        self.layout.addWidget(self.update_btn)

        self.setLayout(self.layout)

        self.load_data()

    def load_data(self):
        try:
            query = """
            SELECT eco, placa, numero_serie, numero_motor, fecha_vigencia_seguro, nombre_aseguradora
            FROM autobus
            WHERE eco = %s
            """
            self.db.cursor.execute(query, (self.item_id,))
            row = self.db.cursor.fetchone()

            if row:
                self.placa.setText(str(row[1]))
                self.numero_serie.setText(str(row[2]))
                self.numero_motor.setText(str(row[3]))
                fecha_vigencia_str = row[4].strftime('%Y-%m-%d')
                fecha_vigencia = QDate.fromString(fecha_vigencia_str, 'yyyy-MM-dd')
                self.fecha_vigencia_seguro.setDate(fecha_vigencia)
                self.nombre_aseguradora.setText(str(row[5]))

            else:
                QMessageBox.warning(self, 'Error', 'No se encontró el Autobus con el ID proporcionado', QMessageBox.Ok)
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)
            
    def update_data(self):
        try:
            placa = self.placa.text()
            numero_serie = self.numero_serie.text()
            numero_motor = self.numero_motor.text()
            fecha_vigencia_seguro = self.fecha_vigencia_seguro.text()
            nombre_aseguradora = self.nombre_aseguradora.text()

            if not all([placa, numero_serie, numero_motor, fecha_vigencia_seguro, nombre_aseguradora]):
                QMessageBox.critical(self, 'Error', 'Todos los campos deben estar llenos', QMessageBox.Ok)
                return

            query = """
            UPDATE autobus
            SET placa = %s, numero_serie = %s, numero_motor = %s, fecha_vigencia_seguro = %s, nombre_aseguradora = %s
            WHERE eco = %s
            """

            self.db.cursor.execute(query, (placa, numero_serie, numero_motor, fecha_vigencia_seguro, nombre_aseguradora, self.item_id))
            self.db.connection.commit()
            QMessageBox.information(self, 'Éxito', 'Datos actualizados correctamente', QMessageBox.Ok)
            self.close()
        except psycopg2.Error as e:
            self.db.connection.rollback()
            print(f"Error durante la actualización del query: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo actualizar el Autobus: {e}', QMessageBox.Ok)
        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
