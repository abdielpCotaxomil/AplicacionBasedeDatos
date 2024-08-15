from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
import psycopg2
import sys
import os

class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="tu_db",
            user="tu_usuario",
            password="tu_contraseña",
            host="localhost"
        )
        self.cursor = self.connection.cursor()

class DelChoForm(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Lista de Choferes")
        self.setStyleSheet("font-size: 16px;")  # Aplicar el tamaño de fuente general
        self.resize(600, 600)

        self.layout = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.list_widget.setStyleSheet("font-size: 16px;")  # Tamaño de fuente en la lista
        self.layout.addWidget(self.list_widget)

        self.load_data_btn = QPushButton('Cargar Datos', self)
        self.load_data_btn.setStyleSheet("font-size: 16px;")  # Tamaño de fuente en el botón
        self.load_data_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_btn)

        self.setLayout(self.layout)

    def load_data(self):
        try:
            # Cambiar la consulta SQL para mostrar solo choferes activos
            query = """
            SELECT ec.id_chofer, ec.nombre, ec.apellido_paterno, ec.apellido_materno, a.apodo
            FROM empleado_chofer ec
            LEFT JOIN apodos a ON ec.id_chofer = a.id_chofer
            WHERE ec.estatus = 'ACTIVO'
            """
            self.db.cursor.execute(query)
            rows = self.db.cursor.fetchall()

            self.list_widget.clear()
            for row in rows:
                item_widget = QWidget()
                item_layout = QHBoxLayout()
                item_layout.setContentsMargins(0, 0, 0, 0)
                
                chofer_text = f"{row[0]} - {row[1]} {row[2]} {row[3]}"
                apodo_text = f'"{row[4]}"' if row[4] else ''  # Agregar apodo entre comillas si existe

                chofer_label = QLabel(chofer_text)
                chofer_label.setStyleSheet("font-size: 16px;")  # Tamaño de fuente en la etiqueta
                chofer_label.setFixedHeight(25)

                apodo_label = QLabel(apodo_text)
                apodo_label.setStyleSheet("color: red; font-size: 16px;")  # Tamaño de fuente y color rojo para el apodo
                apodo_label.setFixedHeight(25)

                delete_btn = QPushButton("ELIMINAR")
                delete_btn.setStyleSheet("background-color: rgb(255, 0, 0); font-size: 16px;")  # Tamaño de fuente en el botón
                delete_btn.setFixedSize(100, 50)
                delete_btn.clicked.connect(lambda ch, row=row: self.inactivate_item(row[0], row[1], row[2], row[3]))
                
                item_layout.addWidget(chofer_label)
                item_layout.addWidget(apodo_label)
                item_layout.addWidget(delete_btn)
                
                item_widget.setLayout(item_layout)
                
                list_item = QListWidgetItem(self.list_widget)
                list_item.setSizeHint(item_widget.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)
                
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)

    def inactivate_item(self, item_id, nombre, apellido_paterno, apellido_materno):
        try:
            reply = QMessageBox.question(self, 'Inactivar Chofer', 
                                         '¿Estás seguro de que quieres inactivar este Chofer?', 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # Actualizar el estatus del chofer a 'INACTIVO'
                query_update = "UPDATE empleado_chofer SET estatus = 'INACTIVO' WHERE id_chofer = %s"
                self.db.cursor.execute(query_update, (item_id,))
                
                self.db.connection.commit()

                # Eliminar las fotos del chofer
                target_folder = r'C:\Users\Cesar\Desktop\Fotos'
                photo_types = ['foto_credencial_frontal', 'foto_credencial_trasera', 'foto_tarjeton_frontal', 'foto_tarjeton_trasera', 'foto_chofer']
                for photo_type in photo_types:
                    filename = os.path.join(target_folder, f"{photo_type}_{nombre}_{apellido_paterno}_{apellido_materno}.jpg")
                    if os.path.exists(filename):
                        os.remove(filename)

                QMessageBox.information(self, 'Éxito', 'Chofer inactivado correctamente', QMessageBox.Ok)
                self.load_data()  # Recargar los datos después de la inactivación

        except psycopg2.Error as e:
            self.db.connection.rollback()
            print(f"Error durante la inactivación del Chofer: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo inactivar el Chofer: {e}', QMessageBox.Ok)
        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
