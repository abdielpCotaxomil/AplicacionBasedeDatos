from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QFormLayout, QLineEdit, QDateEdit, QMessageBox, QHBoxLayout, QLabel, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDate
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

class InfoCho(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Lista de Choferes")
        self.resize(350, 350)

        self.layout = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.layout.addWidget(self.list_widget)

        self.load_data_btn = QPushButton('Cargar Datos', self)
        self.load_data_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_btn)

        self.setLayout(self.layout)

    def load_data(self):
        try:
            query = """
            SELECT e.id_chofer, e.nombre, e.apellido_paterno, e.apellido_materno, a.apodo
            FROM empleado_chofer e
            LEFT JOIN apodos a ON e.id_chofer = a.id_chofer
            """
            self.db.cursor.execute(query)
            rows = self.db.cursor.fetchall()

            self.list_widget.clear()
            for row in rows:
                item_widget = QWidget()
                item_layout = QHBoxLayout()
                item_layout.setContentsMargins(0, 0, 0, 0)
                
                item_text = f"{row[0]} - {row[1]} {row[2]} {row[3]}"
                if row[4]:
                    item_text += f" - \"<span style='color:red;'>{row[4]}</span>\""
                
                item_label = QLabel(item_text)
                item_label.setFixedHeight(25)
                item_label.setTextFormat(Qt.RichText)  # Para que el QLabel interprete el HTML

                view_btn = QPushButton("Ver")
                view_btn.setStyleSheet("background-color: rgb(255, 165, 0);")
                view_btn.setFixedSize(50, 16)
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
    def __init__(self, db, item_id, nombre, apellido_paterno, apellido_materno, parent=None):
        super().__init__(parent)
        self.db = db
        self.item_id = item_id
        self.nombre_str = nombre
        self.apellido_paterno_str = apellido_paterno
        self.apellido_materno_str = apellido_materno
        self.setWindowTitle("Ver Chofer")
        
        self.layout = QFormLayout()
        
        self.nombre = QLineEdit(self)
        self.nombre.setReadOnly(True)
        self.layout.addRow('Nombre:', self.nombre)

        self.apellido_paterno = QLineEdit(self)
        self.apellido_paterno.setReadOnly(True)
        self.layout.addRow('Apellido Paterno:', self.apellido_paterno)

        self.apellido_materno = QLineEdit(self)
        self.apellido_materno.setReadOnly(True)
        self.layout.addRow('Apellido Materno:', self.apellido_materno)

        self.rfc = QLineEdit(self)
        self.rfc.setReadOnly(True)
        self.layout.addRow('RFC:', self.rfc)

        self.nss = QLineEdit(self)
        self.nss.setReadOnly(True)
        self.layout.addRow('NSS:', self.nss)

        self.curp = QLineEdit(self)
        self.curp.setReadOnly(True)
        self.layout.addRow('CURP:', self.curp)

        self.salario_base = QLineEdit(self)
        self.salario_base.setReadOnly(True)
        self.layout.addRow('Salario Base:', self.salario_base)

        self.tipo_jornada = QLineEdit(self)
        self.tipo_jornada.setReadOnly(True)
        self.layout.addRow('Tipo de Jornada:', self.tipo_jornada)

        self.fecha_vencimiento_tarjeton = QDateEdit(self)
        self.fecha_vencimiento_tarjeton.setReadOnly(True)
        self.fecha_vencimiento_tarjeton.setCalendarPopup(True)
        self.layout.addRow('Fecha de Vencimiento del Tarjeton:', self.fecha_vencimiento_tarjeton)

        self.apodo = QLineEdit(self)
        self.apodo.setReadOnly(True)
        self.layout.addRow('Apodo:', self.apodo)

        self.foto_label = QLabel(self)
        self.layout.addRow('Foto:', self.foto_label)

        self.setLayout(self.layout)

        self.load_data()
        self.show_chofer_photo(nombre, apellido_paterno, apellido_materno)

    def load_data(self):
        try:
            query = """
            SELECT e.nombre, e.apellido_paterno, e.apellido_materno, e.rfc, e.nss, e.curp, e.salario_base, e.tipo_jornada, e.fecha_vencimiento_tarjeton, a.apodo
            FROM empleado_chofer e
            LEFT JOIN apodos a ON e.id_chofer = a.id_chofer
            WHERE e.id_chofer = %s
            """
            self.db.cursor.execute(query, (self.item_id,))
            row = self.db.cursor.fetchone()

            if row:
                self.nombre.setText(row[0])
                self.apellido_paterno.setText(row[1])
                self.apellido_materno.setText(row[2])
                self.rfc.setText(row[3])
                self.nss.setText(row[4])
                self.curp.setText(row[5])
                self.salario_base.setText(str(row[6]))  # Convertir decimal a string
                self.tipo_jornada.setText(row[7])
                self.fecha_vencimiento_tarjeton.setDate(QDate.fromString(str(row[8]), 'yyyy-MM-dd'))
                self.apodo.setText(row[9] if row[9] else "")
            else:
                QMessageBox.warning(self, 'Error', 'No se encontró el chofer con el ID proporcionado', QMessageBox.Ok)
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)

    def show_chofer_photo(self, nombre, apellido_paterno, apellido_materno):
        photo_dir = r"C:\Users\Cesar\Desktop\Fotos"
        photo_name = "foto_chofer_{}_{}_{}.jpg".format(nombre, apellido_paterno, apellido_materno)
        photo_path = os.path.join(photo_dir, photo_name)

        if os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(200)
                self.foto_label.setPixmap(pixmap)
            else:
                self.foto_label.setText("No se pudo cargar la foto")
        else:
            self.foto_label.setText("No disponible")
