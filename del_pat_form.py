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

class DelPatForm(QWidget):
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

                delete_btn = QPushButton("Eliminar")
                delete_btn.setStyleSheet("background-color: rgb(255, 0, 0);")
                delete_btn.setFixedSize(60, 16)
                delete_btn.clicked.connect(lambda ch, row=row: self.delete_item(row[0]))
                
                item_layout.addWidget(item_label)
                item_layout.addWidget(delete_btn)
                
                item_widget.setLayout(item_layout)
                
                list_item = QListWidgetItem(self.list_widget)
                list_item.setSizeHint(item_widget.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)
                
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)


    def delete_item(self, item_id):
        try:
            reply = QMessageBox.question(self, 'Eliminar Empleado', 
                                         '¿Estás seguro de que quieres eliminar este Empleado?', 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                query = "DELETE FROM empleado_patio WHERE num_empleado = %s"
                self.db.cursor.execute(query, (item_id,))
                self.db.connection.commit()
                QMessageBox.information(self, 'Éxito', 'Empleado eliminado correctamente', QMessageBox.Ok)
                self.load_data()  # Recargar los datos después de la eliminación

        except psycopg2.Error as e:
            self.db.connection.rollback()
            print(f"Error durante la eliminación del Empleado: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo eliminar el Empleado: {e}', QMessageBox.Ok)
        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
