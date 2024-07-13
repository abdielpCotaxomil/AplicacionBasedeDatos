from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QInputDialog, QLabel, QDialog, QFormLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from add_chofer_form import AddChoferForm
from PIL import Image
from io import BytesIO
import os

class AdminWindow(QMainWindow):
    def __init__(self, db):
        super(AdminWindow, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Administración')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.add_chofer_button = QPushButton('Agregar Chofer', self)
        self.add_chofer_button.clicked.connect(self.show_add_chofer_form)
        layout.addWidget(self.add_chofer_button)

        self.add_patio_button = QPushButton('Agregar Patio', self)
        layout.addWidget(self.add_patio_button)

        self.add_bus_button = QPushButton('Agregar Autobus', self)
        layout.addWidget(self.add_bus_button)

        self.edit_data_button = QPushButton('Editar Datos', self)
        layout.addWidget(self.edit_data_button)

        self.view_info_button = QPushButton('Ver Información', self)
        self.view_info_button.clicked.connect(self.show_info_options)
        layout.addWidget(self.view_info_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def show_add_chofer_form(self):
        self.add_chofer_form = AddChoferForm(self.db)
        self.add_chofer_form.show()

    def show_info_options(self):
        info_type, ok = QInputDialog.getItem(self, "Ver Información", "Selecciona el tipo de información a ver:", ["Chofer", "Patio", "Autobus"], 0, False)
        if ok and info_type:
            if info_type == "Chofer":
                self.show_chofer_list()
            elif info_type == "Patio":
                self.show_patio_info()
            elif info_type == "Autobus":
                self.show_bus_info()

    def show_chofer_list(self):
        query = "SELECT id_chofer, nombre FROM empleado_chofer"
        try:
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            if results:
                chofer_list = [f"{result[0]} - {result[1]}" for result in results]
                chofer, ok = QInputDialog.getItem(self, "Seleccionar Chofer", "Selecciona un chofer:", chofer_list, 0, False)
                if ok and chofer:
                    chofer_id = int(chofer.split(" - ")[0])
                    self.show_chofer_info(chofer_id)
            else:
                QMessageBox.information(self, "Información de Choferes", "No se encontraron registros.", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener la lista de choferes: {e}", QMessageBox.Ok)

    def show_chofer_info(self, chofer_id):
        query = """
        SELECT nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton,
               foto_credencial_frontal, foto_credencial_trasera, foto_tarjeton_frontal, foto_tarjeton_trasera, foto_chofer
        FROM empleado_chofer
        WHERE id_chofer = %s
        """
        try:
            self.db.cursor.execute(query, (chofer_id,))
            result = self.db.cursor.fetchone()
            if result:
                info = f"""
                Nombre: {result[0]}
                Apellido Paterno: {result[1]}
                Apellido Materno: {result[2]}
                RFC: {result[3]}
                NSS: {result[4]}
                CURP: {result[5]}
                Salario Base: {result[6]}
                Tipo de Jornada: {result[7]}
                Fecha Vencimiento Tarjetón: {result[8]}
                """
                QMessageBox.information(self, "Información del Chofer", info, QMessageBox.Ok)

                self.show_chofer_photos(result[9:])
            else:
                QMessageBox.information(self, "Información del Chofer", "No se encontraron registros.", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener la información del chofer: {e}", QMessageBox.Ok)

    def show_chofer_photos(self, photos):
        dialog = QDialog(self)
        dialog.setWindowTitle("Fotos del Chofer")
        layout = QFormLayout()

        labels = [
            "Foto Credencial Frontal",
            "Foto Credencial Trasera",
            "Foto Tarjetón Frontal",
            "Foto Tarjetón Trasera",
            "Foto Chofer"
        ]

        for idx, (label, photo) in enumerate(zip(labels, photos)):
            if photo:
                print(f"Tamaño de la foto para {label}: {len(photo)} bytes")  # Añadir mensaje de depuración
                try:
                    # Escribir a un archivo temporal para verificar los datos de la imagen
                    file_path = f"temp_image_{idx}.jpg"
                    with open(file_path, "wb") as file:
                        file.write(photo)

                    # Intentar cargar la imagen desde el archivo
                    image = Image.open(file_path)
                    buffer = BytesIO()
                    image.save(buffer, format="PNG")
                    pixmap = QPixmap()
                    if not pixmap.loadFromData(buffer.getvalue(), "PNG"):
                        print(f"Error al cargar la foto para {label}")
                    else:
                        photo_label = QLabel()
                        photo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                        layout.addRow(label, photo_label)
                except Exception as e:
                    print(f"Excepción al procesar la foto para {label}: {e}")
            else:
                print(f"Foto para {label} es nula")

        dialog.setLayout(layout)
        dialog.exec_()

    def show_patio_info(self):
        query = "SELECT * FROM empleado_patio"
        try:
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            if results:
                info = "\n".join([str(result) for result in results])
                QMessageBox.information(self, "Información de Patios", info, QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Información de Patios", "No se encontraron registros.", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener la información de patios: {e}", QMessageBox.Ok)

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
