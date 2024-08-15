import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, 
    QDateEdit, QFileDialog, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QPixmap, QRegExpValidator, QImage
from PyQt5.QtCore import QDate, Qt, QRegExp, QBuffer, QByteArray

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
        self.nombre.textChanged.connect(lambda: self.nombre.setText(self.nombre.text().upper()))
        form_layout.addRow('Nombre:', self.nombre)

        self.apellido_paterno = QLineEdit(self)
        self.apellido_paterno.textChanged.connect(lambda: self.apellido_paterno.setText(self.apellido_paterno.text().upper()))
        form_layout.addRow('Apellido Paterno:', self.apellido_paterno)

        self.apellido_materno = QLineEdit(self)
        self.apellido_materno.textChanged.connect(lambda: self.apellido_materno.setText(self.apellido_materno.text().upper()))
        form_layout.addRow('Apellido Materno:', self.apellido_materno)

        self.rfc = QLineEdit(self)
        self.rfc.setMaxLength(13)
        self.rfc.textChanged.connect(lambda: self.rfc.setText(self.rfc.text().upper()))
        form_layout.addRow('RFC:', self.rfc)

        self.nss = QLineEdit(self)
        self.nss.setMaxLength(11)
        self.nss.textChanged.connect(lambda: self.nss.setText(self.nss.text().upper()))
        form_layout.addRow('NSS:', self.nss)

        self.curp = QLineEdit(self)
        self.curp.setMaxLength(18)
        self.curp.textChanged.connect(lambda: self.curp.setText(self.curp.text().upper()))
        form_layout.addRow('CURP:', self.curp)

        self.salario_base = QLineEdit(self)
        self.salario_base.setMaxLength(12)
        self.salario_base.setPlaceholderText('99999999.99')
        self.salario_base.setValidator(QRegExpValidator(QRegExp(r'^\d{1,10}(\.\d{0,2})?$'), self))
        form_layout.addRow('Salario Base:', self.salario_base)

        self.tipo_jornada = QComboBox(self)
        self.tipo_jornada.addItems(['MATUTINO', 'VESPERTINO', 'MIXTO', 'COMPLETO'])
        form_layout.addRow('Tipo de Jornada:', self.tipo_jornada)

        self.fecha_vencimiento_tarjeton = QDateEdit(self)
        self.fecha_vencimiento_tarjeton.setCalendarPopup(True)
        self.fecha_vencimiento_tarjeton.setDate(QDate.currentDate())
        form_layout.addRow('Fecha Vencimiento Tarjetón:', self.fecha_vencimiento_tarjeton)

        self.apodo = QLineEdit(self)
        form_layout.addRow('Apodo:', self.apodo)

        self.photos = {}
        self.photo_labels = {}

        self.create_photo_section(form_layout, 'Foto Credencial Frontal', 'foto_credencial_frontal', self.take_foto_frontal)
        self.create_photo_section(form_layout, 'Foto Credencial Trasera', 'foto_credencial_trasera', self.take_foto_trasera)
        self.create_photo_section(form_layout, 'Foto Tarjetón Frontal', 'foto_tarjeton_frontal', self.take_foto_tarjeton_frontal)
        self.create_photo_section(form_layout, 'Foto Tarjetón Trasera', 'foto_tarjeton_trasera', self.take_foto_tarjeton_trasera)
        self.create_photo_section(form_layout, 'Foto Chofer', 'foto_chofer', self.take_foto_chofer)

        self.submit_btn = QPushButton('Agregar Chofer', self)
        self.submit_btn.clicked.connect(self.submit_form)
        form_layout.addRow(self.submit_btn)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def create_photo_section(self, form_layout, label, photo_type, capture_method):
        container = QWidget()
        layout = QHBoxLayout()

        select_button = QPushButton('Seleccionar Archivo', self)
        select_button.clicked.connect(lambda: self.select_photo(photo_type))
        layout.addWidget(select_button)

        capture_button = QPushButton('Tomar Foto', self)
        capture_button.clicked.connect(capture_method)
        layout.addWidget(capture_button)

        self.photo_labels[photo_type] = QLabel(self)
        layout.addWidget(self.photo_labels[photo_type])

        container.setLayout(layout)
        form_layout.addRow(label, container)

    def take_foto_frontal(self):
        self.take_photo_with_camera('foto_credencial_frontal')

    def take_foto_trasera(self):
        self.take_photo_with_camera('foto_credencial_trasera')

    def take_foto_tarjeton_frontal(self):
        self.take_photo_with_camera('foto_tarjeton_frontal')

    def take_foto_tarjeton_trasera(self):
        self.take_photo_with_camera('foto_tarjeton_trasera')

    def take_foto_chofer(self):
        self.take_photo_with_camera('foto_chofer')

    def take_photo_with_camera(self, photo_type):
        os.system('start microsoft.windows.camera:')

    def select_photo(self, photo_type):
        options = QFileDialog.Options()
        filters = "Images (*.jpg *.jpeg *.png)"
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto", "", filters, options=options)
        
        if filename:
            if not (filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png')):
                QMessageBox.critical(self, 'Error', 'El archivo seleccionado no es una imagen válida (debe ser JPG, JPEG o PNG).', QMessageBox.Ok)
                return
            
            pixmap = QPixmap(filename)
            self.photos[photo_type] = pixmap
            self.photo_labels[photo_type].setPixmap(pixmap)
            self.photo_labels[photo_type].setText(filename.split('/')[-1])

    def submit_form(self):
        try:
            nombre = self.nombre.text().upper()
            apellido_paterno = self.apellido_paterno.text().upper()
            apellido_materno = self.apellido_materno.text().upper()
            rfc = self.rfc.text().upper()
            nss = self.nss.text().upper()
            curp = self.curp.text().upper()
            salario_base = self.salario_base.text()
            tipo_jornada = self.tipo_jornada.currentText()
            fecha_vencimiento_tarjeton = self.fecha_vencimiento_tarjeton.date().toString('yyyy-MM-dd')
            apodo = self.apodo.text()

            if not all([nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton, apodo]):
                QMessageBox.critical(self, 'Error', 'Todos los campos deben estar llenos', QMessageBox.Ok)
                return

            fotos = {}
            for key in ['foto_credencial_frontal', 'foto_credencial_trasera', 'foto_tarjeton_frontal', 'foto_tarjeton_trasera', 'foto_chofer']:
                if key in self.photos:
                    image = self.photos[key].toImage()
                    buffer = QBuffer()
                    buffer.open(QBuffer.ReadWrite)
                    image.save(buffer, "JPEG")
                    fotos[key] = buffer.data().data()
                else:
                    QMessageBox.critical(self, 'Error', f'{key} no está proporcionada', QMessageBox.Ok)
                    return

            query = """
            INSERT INTO empleado_chofer (nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton, foto_credencial_frontal, foto_credencial_trasera, foto_tarjeton_frontal, foto_tarjeton_trasera, foto_chofer)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_chofer
            """
            data = (
                nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton,
                fotos.get('foto_credencial_frontal'), fotos.get('foto_credencial_trasera'), fotos.get('foto_tarjeton_frontal'),
                fotos.get('foto_tarjeton_trasera'), fotos.get('foto_chofer')
            )

            self.db.execute_query(query, data)
            id_chofer = self.db.cursor.fetchone()['id_chofer']

            QMessageBox.information(self, 'Éxito', f'Chofer agregado correctamente.\n\nID: {id_chofer}\nNombre: {nombre}\nApellido Paterno: {apellido_paterno}\nApellido Materno: {apellido_materno}', QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e), QMessageBox.Ok)
