from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QFormLayout, QLineEdit, QDateEdit, QMessageBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
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

class InfoAut(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Lista de Autobuses")
        self.resize(600, 600)

        self.layout = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.list_widget.setStyleSheet("font-size: 16px;")  # Ajustar el tamaño de la fuente
        self.layout.addWidget(self.list_widget)

        self.load_data_btn = QPushButton('Cargar Datos', self)
        self.load_data_btn.setStyleSheet("font-size: 16px; background-color: rgb(255, 165, 0);")  # Ajustar el tamaño de la fuente y color
        self.load_data_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_btn)

        self.setLayout(self.layout)

    def load_data(self):
        try:
            query = """
            SELECT eco, placa, numero_serie, numero_motor
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
                
                item_text = f"{row[0]} - {row[1]} - {row[2]} - {row[3]}"
                
                item_label = QLabel(item_text)
                item_label.setStyleSheet("font-size: 16px;")  # Ajustar el tamaño de la fuente
                item_label.setFixedHeight(25)

                view_btn = QPushButton("Ver")
                view_btn.setStyleSheet("background-color: rgb(255, 165, 0);")
                view_btn.setFixedSize(50, 36)
                view_btn.clicked.connect(lambda ch, row=row: self.view_item(row))
                
                item_layout.addWidget(item_label)
                item_layout.addWidget(view_btn)
                
                item_widget.setLayout(item_layout)
                
                list_item = QListWidgetItem(self.list_widget)
                list_item.setSizeHint(item_widget.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)
                
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)

    def view_item(self, row):
        self.view_window = ViewWindow(self.db, row[0], row[1], row[2], row[3])
        self.view_window.show()

class ViewWindow(QWidget):
    def __init__(self, db, eco, placa, numero_serie, numero_motor, parent=None):
        super().__init__(parent)
        self.db = db
        self.eco = eco
        self.placa = placa
        self.numero_serie = numero_serie
        self.numero_motor = numero_motor
        self.setWindowTitle("Ver Autobús")
        
        self.layout = QFormLayout()
        
        self.placa_line = QLineEdit(self)
        self.placa_line.setReadOnly(True)
        self.placa_line.setStyleSheet("font-size: 16px;")  # Ajustar el tamaño de la fuente
        self.layout.addRow('Placa:', self.placa_line)

        self.numero_serie_line = QLineEdit(self)
        self.numero_serie_line.setReadOnly(True)
        self.numero_serie_line.setStyleSheet("font-size: 16px;")  # Ajustar el tamaño de la fuente
        self.layout.addRow('Número de Serie:', self.numero_serie_line)

        self.numero_motor_line = QLineEdit(self)
        self.numero_motor_line.setReadOnly(True)
        self.numero_motor_line.setStyleSheet("font-size: 16px;")  # Ajustar el tamaño de la fuente
        self.layout.addRow('Número de Motor:', self.numero_motor_line)

        self.fecha_vigencia_seguro = QDateEdit(self)
        self.fecha_vigencia_seguro.setReadOnly(True)
        self.fecha_vigencia_seguro.setStyleSheet("font-size: 16px;")  # Ajustar el tamaño de la fuente
        self.layout.addRow('Fecha Vigencia Seguro:', self.fecha_vigencia_seguro)

        self.nombre_aseguradora_line = QLineEdit(self)
        self.nombre_aseguradora_line.setReadOnly(True)
        self.nombre_aseguradora_line.setStyleSheet("font-size: 16px;")  # Ajustar el tamaño de la fuente
        self.layout.addRow('Nombre Aseguradora:', self.nombre_aseguradora_line)

        self.setLayout(self.layout)

        self.load_data()

    def load_data(self):
        try:
            query = """
            SELECT placa, numero_serie, numero_motor, fecha_vigencia_seguro, nombre_aseguradora
            FROM autobus
            WHERE eco = %s
            """
            self.db.cursor.execute(query, (self.eco,))
            row = self.db.cursor.fetchone()

            if row:
                self.placa_line.setText(row[0])
                self.numero_serie_line.setText(row[1])
                self.numero_motor_line.setText(row[2])
                self.fecha_vigencia_seguro.setDate(row[3])
                self.nombre_aseguradora_line.setText(row[4])
            else:
                QMessageBox.warning(self, 'Error', 'No se encontró el autobús con el ID proporcionado', QMessageBox.Ok)
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)
