from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QMessageBox
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

class DelAutForm(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Lista de Autobuses")
        self.resize(600, 600)

        self.layout = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.layout.addWidget(self.list_widget)

        self.load_data_btn = QPushButton('Cargar Datos', self)
        self.load_data_btn.setStyleSheet("font-size: 16px;")  # Establecer tamaño de fuente para el botón
        self.load_data_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_btn)

        self.setLayout(self.layout)

    def load_data(self):
        try:
            # Consulta actualizada para filtrar solo los camiones activos
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
                item_label.setFixedHeight(25)
                item_label.setStyleSheet("font-size: 16px;")  # Establecer tamaño de fuente para la etiqueta

                deactivate_btn = QPushButton("ELIMINAR")
                deactivate_btn.setStyleSheet("background-color: rgb(255, 0, 0); font-size: 16px;")  # Establecer tamaño de fuente para el botón
                deactivate_btn.setFixedSize(100, 50)  # Ajustar tamaño del botón para el texto más grande
                deactivate_btn.clicked.connect(lambda ch, row=row: self.deactivate_item(row[0]))
                
                item_layout.addWidget(item_label)
                item_layout.addWidget(deactivate_btn)
                
                item_widget.setLayout(item_layout)
                
                list_item = QListWidgetItem(self.list_widget)
                list_item.setSizeHint(item_widget.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)
                
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)

    def deactivate_item(self, item_id):
        try:
            reply = QMessageBox.question(self, 'Desactivar Autobus', 
                                         '¿Estás seguro de que quieres desactivar este Autobus?', 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                query = "UPDATE autobus SET estatus = 'INACTIVO' WHERE eco = %s"
                self.db.cursor.execute(query, (item_id,))
                self.db.connection.commit()
                QMessageBox.information(self, 'Éxito', 'Autobus desactivado correctamente', QMessageBox.Ok)
                self.load_data()  # Recargar los datos después de la actualización

        except psycopg2.Error as e:
            self.db.connection.rollback()
            print(f"Error durante la desactivación del Autobus: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo desactivar el Autobus: {e}', QMessageBox.Ok)
        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
