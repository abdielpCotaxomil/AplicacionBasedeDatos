from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QDateEdit,
    QFileDialog, QMessageBox, QHBoxLayout, QDialog
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap
import cv2
import psycopg2
import os
from tkinter import Tk, filedialog

class AddChoferForm(QWidget):
    def __init__(self, db, parent=None):
        super(AddChoferForm, self).__init__(parent)
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Agregar Chofer')
        self.resize(400, 600)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.nombre = QLineEdit(self)
        self.nombre.textChanged.connect(lambda text: self.nombre.setText(text.upper()))
        form_layout.addRow('Nombre:', self.nombre)

        self.apellido_paterno = QLineEdit(self)
        self.apellido_paterno.textChanged.connect(lambda text: self.apellido_paterno.setText(text.upper()))
        form_layout.addRow('Apellido Paterno:', self.apellido_paterno)

        self.apellido_materno = QLineEdit(self)
        self.apellido_materno.textChanged.connect(lambda text: self.apellido_materno.setText(text.upper()))
        form_layout.addRow('Apellido Materno:', self.apellido_materno)

        self.rfc = QLineEdit(self)
        self.rfc.setMaxLength(13)
        self.rfc.textChanged.connect(lambda text: self.rfc.setText(text.upper()))
        form_layout.addRow('RFC:', self.rfc)

        self.nss = QLineEdit(self)
        self.nss.setMaxLength(11)
        self.nss.textChanged.connect(lambda text: self.nss.setText(text.upper()))
        form_layout.addRow('NSS:', self.nss)

        self.curp = QLineEdit(self)
        self.curp.setMaxLength(18)
        self.curp.textChanged.connect(lambda text: self.curp.setText(text.upper()))
        form_layout.addRow('CURP:', self.curp)

        self.salario_base = QLineEdit(self)
        self.salario_base.textChanged.connect(lambda text: self.salario_base.setText(text.upper()))
        form_layout.addRow('Salario Base:', self.salario_base)

        self.tipo_jornada = QLineEdit(self)
        self.tipo_jornada.textChanged.connect(lambda text: self.tipo_jornada.setText(text.upper()))
        form_layout.addRow('Tipo de Jornada:', self.tipo_jornada)

        self.fecha_vencimiento_tarjeton = QDateEdit(self)
        self.fecha_vencimiento_tarjeton.setCalendarPopup(True)
        self.fecha_vencimiento_tarjeton.setDate(QDate.currentDate())
        form_layout.addRow('Fecha Vencimiento Tarjetón:', self.fecha_vencimiento_tarjeton)

        self.apodo = QLineEdit(self)
        self.apodo.textChanged.connect(lambda text: self.apodo.setText(text.upper()))
        form_layout.addRow('Apodo:', self.apodo)

        self.photos = {}
        self.photo_labels = {}

        self.create_photo_section(form_layout, 'Foto Credencial Frontal', 'foto_credencial_frontal')
        self.create_photo_section(form_layout, 'Foto Credencial Trasera', 'foto_credencial_trasera')
        self.create_photo_section(form_layout, 'Foto Tarjetón Frontal', 'foto_tarjeton_frontal')
        self.create_photo_section(form_layout, 'Foto Tarjetón Trasera', 'foto_tarjeton_trasera')
        self.create_photo_section(form_layout, 'Foto Chofer', 'foto_chofer')

        self.submit_btn = QPushButton('Agregar Chofer', self)
        self.submit_btn.clicked.connect(self.submit_form)
        form_layout.addRow(self.submit_btn)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def create_photo_section(self, form_layout, label, photo_type):
        container = QWidget()
        layout = QHBoxLayout()

        select_button = QPushButton('Seleccionar Archivo', self)
        select_button.clicked.connect(lambda: self.select_photo(photo_type))
        layout.addWidget(select_button)

        capture_button = QPushButton('Tomar Foto', self)
        capture_button.clicked.connect(lambda: self.capture_photo(photo_type))
        layout.addWidget(capture_button)

        self.photo_labels[photo_type] = QLabel(self)
        layout.addWidget(self.photo_labels[photo_type])

        container.setLayout(layout)
        form_layout.addRow(label, container)

    def select_photo(self, photo_type):
        root = Tk()
        root.withdraw()  # Oculta la ventana principal de tkinter
        filename = filedialog.askopenfilename(title="Seleccionar Foto", filetypes=[("Archivos de imagen", "*.png;*.jpeg")])
        root.destroy()  # Destruye la ventana principal de tkinter
        if filename:
            with open(filename, "rb") as file:
                self.photos[photo_type] = file.read()
            self.photo_labels[photo_type].setText(filename.split('/')[-1])

    def capture_photo(self, photo_type):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            root = Tk()
            root.withdraw()
            filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Archivos de imagen", "*.jpg")])
            root.destroy()
            if filename:
                cv2.imwrite(filename, frame)
                with open(filename, "rb") as file:
                    self.photos[photo_type] = file.read()
                self.photo_labels[photo_type].setText(filename.split('/')[-1])
        cap.release()

    def submit_form(self):
        try:
            nombre = self.nombre.text()
            apellido_paterno = self.apellido_paterno.text()
            apellido_materno = self.apellido_materno.text()
            rfc = self.rfc.text()
            nss = self.nss.text()
            curp = self.curp.text()
            salario_base = self.salario_base.text()
            tipo_jornada = self.tipo_jornada.text()
            fecha_vencimiento_tarjeton = self.fecha_vencimiento_tarjeton.date().toString('yyyy-MM-dd')
            apodo = self.apodo.text()

            if not all([nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton, apodo]):
                QMessageBox.critical(self, 'Error', 'Todos los campos deben estar llenos', QMessageBox.Ok)
                return

            fotos = {}
            for key in ['foto_credencial_frontal', 'foto_credencial_trasera', 'foto_tarjeton_frontal', 'foto_tarjeton_trasera', 'foto_chofer']:
                if key in self.photos:
                    fotos[key] = psycopg2.Binary(self.photos[key])
                else:
                    QMessageBox.critical(self, 'Error', f'{key} no está proporcionada', QMessageBox.Ok)
                    return

            query = """
            INSERT INTO empleado_chofer (nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton, foto_credencial_frontal, foto_credencial_trasera, foto_tarjeton_frontal, foto_tarjeton_trasera, foto_chofer)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_chofer
            """

            print("Ejecutando query")
            self.db.cursor.execute(query, (nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton, fotos['foto_credencial_frontal'], fotos['foto_credencial_trasera'], fotos['foto_tarjeton_frontal'], fotos['foto_tarjeton_trasera'], fotos['foto_chofer']))
            id_chofer = self.db.cursor.fetchone()[0]
                
            query_apodo = """
            INSERT INTO apodos (id_chofer, apodo)
            VALUES (%s, %s)
            """
            self.db.cursor.execute(query_apodo, (id_chofer, apodo))
                
            self.db.connection.commit()

            print("Query ejecutada correctamente")
            chofer_data = self.fetch_chofer_data(id_chofer)
            self.show_chofer_info(chofer_data)
        except psycopg2.Error as e:
            self.db.connection.rollback()
            print(f"Error durante la ejecución del query: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo agregar el chofer: {e}', QMessageBox.Ok)
        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)

    def fetch_chofer_data(self, id_chofer):
        try:
            query = """
            SELECT c.id_chofer, c.nombre, c.apellido_paterno, c.apellido_materno, c.rfc, c.nss, c.curp, c.salario_base, c.tipo_jornada, c.fecha_vencimiento_tarjeton, a.apodo
            FROM empleado_chofer c
            LEFT JOIN apodos a ON c.id_chofer = a.id_chofer
            WHERE c.id_chofer = %s
            """
            self.db.cursor.execute(query, (id_chofer,))
            chofer_data = self.db.cursor.fetchone()
            return chofer_data
        except psycopg2.Error as e:
            print(f"Error al obtener datos del chofer: {e}")
            return None

    def show_chofer_info(self, chofer_data):
        dialog = QDialog(self)
        dialog.setWindowTitle("Información del Chofer")
        dialog_layout = QFormLayout(dialog)
        
        labels = ['ID:', 'Nombre:', 'Apellido Paterno:', 'Apellido Materno:', 'RFC:', 'NSS:', 'CURP:', 'Salario Base:', 'Tipo de Jornada:', 'Fecha Vencimiento Tarjetón:', 'Apodo:']
        for label_text, data in zip(labels, chofer_data):
            label = QLabel(f"{label_text} {data}", dialog)
            dialog_layout.addRow(label)

        accept_button = QPushButton('Aceptar', dialog)
        accept_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(accept_button)

        dialog.exec_()
        self.close()
