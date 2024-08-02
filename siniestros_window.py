from PyQt5.QtWidgets import QMainWindow, qApp, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit, QTimeEdit, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QDateTime
import os

class SiniestrosWindow(QDialog):
    def __init__(self, db, parent=None):
        super(SiniestrosWindow, self).__init__(parent)
        self.setWindowTitle('Siniestros')
        self.db = db

        layout = QVBoxLayout()

        self.registrar_btn = QPushButton('Registrar Siniestro', self)
        self.registrar_btn.clicked.connect(self.registrar_siniestro)
        layout.addWidget(self.registrar_btn)

        self.ver_activos_btn = QPushButton('Ver Siniestros Activos / Cambiar Estatus', self)
        self.ver_activos_btn.clicked.connect(self.ver_siniestros_activos)
        layout.addWidget(self.ver_activos_btn)

        self.ver_todos_btn = QPushButton('Ver Siniestros', self)
        self.ver_todos_btn.clicked.connect(self.ver_siniestros)
        layout.addWidget(self.ver_todos_btn)

        self.setLayout(layout)

    def registrar_siniestro(self):
        dialog = RegistrarSiniestroForm(self.db, self)
        dialog.exec_()

    def ver_siniestros_activos(self):
        dialog = VerSiniestrosActivosForm(self.db, self)
        dialog.exec_()

    def ver_siniestros(self):
        dialog = VerSiniestrosForm(self.db, self)
        dialog.exec_()

class RegistrarSiniestroForm(QDialog):
    def __init__(self, db, parent=None):
        super(RegistrarSiniestroForm, self).__init__(parent)
        self.setWindowTitle('Registrar Siniestro')
        self.db = db

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.eco = QComboBox(self)
        self.populate_autobuses()
        form_layout.addRow('Económico:', self.eco)

        self.id_chofer = QComboBox(self)
        self.populate_choferes()
        form_layout.addRow('Chofer:', self.id_chofer)

        self.culpable = QCheckBox(self)
        form_layout.addRow('Culpable:', self.culpable)

        self.tipo_pago = QLineEdit(self)
        form_layout.addRow('Tipo de Pago:', self.tipo_pago)

        self.foto_general_btn = QHBoxLayout()
        self.foto_general_select_btn = QPushButton('Seleccionar Foto General', self)
        self.foto_general_select_btn.clicked.connect(self.select_foto_general)
        self.foto_general_take_btn = QPushButton('Tomar Foto General', self)
        self.foto_general_take_btn.clicked.connect(self.take_foto_general)
        self.foto_general_btn.addWidget(self.foto_general_select_btn)
        self.foto_general_btn.addWidget(self.foto_general_take_btn)
        form_layout.addRow('Foto General:', self.foto_general_btn)

        self.foto_frontal_btn = QHBoxLayout()
        self.foto_frontal_select_btn = QPushButton('Seleccionar Foto Frontal', self)
        self.foto_frontal_select_btn.clicked.connect(self.select_foto_frontal)
        self.foto_frontal_take_btn = QPushButton('Tomar Foto Frontal', self)
        self.foto_frontal_take_btn.clicked.connect(self.take_foto_frontal)
        self.foto_frontal_btn.addWidget(self.foto_frontal_select_btn)
        self.foto_frontal_btn.addWidget(self.foto_frontal_take_btn)
        form_layout.addRow('Foto Frontal:', self.foto_frontal_btn)

        self.foto_trasera_btn = QHBoxLayout()
        self.foto_trasera_select_btn = QPushButton('Seleccionar Foto Trasera', self)
        self.foto_trasera_select_btn.clicked.connect(self.select_foto_trasera)
        self.foto_trasera_take_btn = QPushButton('Tomar Foto Trasera', self)
        self.foto_trasera_take_btn.clicked.connect(self.take_foto_trasera)
        self.foto_trasera_btn.addWidget(self.foto_trasera_select_btn)
        self.foto_trasera_btn.addWidget(self.foto_trasera_take_btn)
        form_layout.addRow('Foto Trasera:', self.foto_trasera_btn)

        self.foto_lateral_izquierdo_btn = QHBoxLayout()
        self.foto_lateral_izquierdo_select_btn = QPushButton('Seleccionar Foto Lateral Izquierdo', self)
        self.foto_lateral_izquierdo_select_btn.clicked.connect(self.select_foto_lateral_izquierdo)
        self.foto_lateral_izquierdo_take_btn = QPushButton('Tomar Foto Lateral Izquierdo', self)
        self.foto_lateral_izquierdo_take_btn.clicked.connect(self.take_foto_lateral_izquierdo)
        self.foto_lateral_izquierdo_btn.addWidget(self.foto_lateral_izquierdo_select_btn)
        self.foto_lateral_izquierdo_btn.addWidget(self.foto_lateral_izquierdo_take_btn)
        form_layout.addRow('Foto Lateral Izquierdo:', self.foto_lateral_izquierdo_btn)

        self.foto_lateral_derecho_btn = QHBoxLayout()
        self.foto_lateral_derecho_select_btn = QPushButton('Seleccionar Foto Lateral Derecho', self)
        self.foto_lateral_derecho_select_btn.clicked.connect(self.select_foto_lateral_derecho)
        self.foto_lateral_derecho_take_btn = QPushButton('Tomar Foto Lateral Derecho', self)
        self.foto_lateral_derecho_take_btn.clicked.connect(self.take_foto_lateral_derecho)
        self.foto_lateral_derecho_btn.addWidget(self.foto_lateral_derecho_select_btn)
        self.foto_lateral_derecho_btn.addWidget(self.foto_lateral_derecho_take_btn)
        form_layout.addRow('Foto Lateral Derecho:', self.foto_lateral_derecho_btn)

        self.descripcion = QTextEdit(self)
        form_layout.addRow('Descripción:', self.descripcion)

        self.submit_btn = QPushButton('Registrar', self)
        self.submit_btn.clicked.connect(self.registrar)
        form_layout.addRow(self.submit_btn)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def populate_autobuses(self):
        query = "SELECT eco FROM Autobus WHERE estatus = 'ACTIVO'"
        self.db.execute_query(query)
        autobuses = self.db.fetch_all()
        for autobus in autobuses:
            self.eco.addItem(str(autobus[0]), autobus[0])

    def populate_choferes(self):
        query = "SELECT id_chofer, nombre, apellido_paterno, apellido_materno FROM Empleado_Chofer WHERE estatus = 'ACTIVO'"
        self.db.execute_query(query)
        choferes = self.db.fetch_all()
        for chofer in choferes:
            self.id_chofer.addItem(f"{chofer[0]} - {chofer[1]} {chofer[2]} {chofer[3]}", chofer[0])

    def select_foto_general(self):
        self.foto_general_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto General", "", "Images (*.png *.xpm *.jpg)")

    def take_foto_general(self):
        os.system('start microsoft.windows.camera:')

    def select_foto_frontal(self):
        self.foto_frontal_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto Frontal", "", "Images (*.png *.xpm *.jpg)")

    def take_foto_frontal(self):
        os.system('start microsoft.windows.camera:')

    def select_foto_trasera(self):
        self.foto_trasera_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto Trasera", "", "Images (*.png *.xpm *.jpg)")

    def take_foto_trasera(self):
        os.system('start microsoft.windows.camera:')

    def select_foto_lateral_izquierdo(self):
        self.foto_lateral_izquierdo_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto Lateral Izquierdo", "", "Images (*.png *.xpm *.jpg)")

    def take_foto_lateral_izquierdo(self):
        os.system('start microsoft.windows.camera:')

    def select_foto_lateral_derecho(self):
        self.foto_lateral_derecho_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto Lateral Derecho", "", "Images (*.png *.xpm *.jpg)")

    def take_foto_lateral_derecho(self):
        os.system('start microsoft.windows.camera:')

    def registrar(self):
        eco = self.eco.currentText()
        id_chofer = self.id_chofer.currentData()
        culpable = self.culpable.isChecked()
        tipo_pago = self.tipo_pago.text()
        descripcion = self.descripcion.toPlainText()
        estatus = 'ACTIVA'

        # Load images
        foto_general = self.load_image(self.foto_general_path)
        foto_frontal = self.load_image(self.foto_frontal_path)
        foto_trasera = self.load_image(self.foto_trasera_path)
        foto_lateral_izquierdo = self.load_image(self.foto_lateral_izquierdo_path)
        foto_lateral_derecho = self.load_image(self.foto_lateral_derecho_path)

        query = """
        INSERT INTO Siniestros (fecha, hora, eco, id_chofer, culpable, tipo_pago, foto_general, foto_frontal, foto_trasera, foto_lateral_izquierdo, foto_lateral_derecho, descripcion, estatus)
        VALUES (CURRENT_DATE, CURRENT_TIME, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (eco, id_chofer, culpable, tipo_pago, foto_general, foto_frontal, foto_trasera, foto_lateral_izquierdo, foto_lateral_derecho, descripcion, estatus)

        try:
            self.db.execute_query(query, params)
            QMessageBox.information(self, 'Éxito', 'Siniestro registrado exitosamente.')
            self.close()
        except Exception as e:
            print(f"Error al registrar siniestro: {e}")
            QMessageBox.critical(self, 'Error', f'Error al registrar siniestro: {e}')

    def load_image(self, image_path):
        if image_path:
            with open(image_path, 'rb') as file:
                return file.read()
        return None

class VerSiniestrosActivosForm(QDialog):
    def __init__(self, db, parent=None):
        super(VerSiniestrosActivosForm, self).__init__(parent)
        self.setWindowTitle('Ver Siniestros Activos / Cambiar Estatus')
        self.db = db

        layout = QVBoxLayout()

        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        self.load_data()

        self.setLayout(layout)

    def load_data(self):
        query = "SELECT folio, eco, fecha FROM Siniestros WHERE estatus = 'ACTIVA'"
        self.db.execute_query(query)
        siniestros = self.db.fetch_all()

        self.table.setRowCount(len(siniestros))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Folio', 'Económico', 'Fecha'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row_num, siniestro in enumerate(siniestros):
            self.table.setItem(row_num, 0, QTableWidgetItem(str(siniestro[0])))
            self.table.setItem(row_num, 1, QTableWidgetItem(str(siniestro[1])))
            self.table.setItem(row_num, 2, QTableWidgetItem(str(siniestro[2])))

        self.table.cellDoubleClicked.connect(self.change_status)

    def change_status(self, row, column):
        folio = self.table.item(row, 0).text()
        new_status, ok = QInputDialog.getItem(self, 'Cambiar Estatus', 'Seleccionar nuevo estatus:', ['ACTIVA', 'RESUELTO'], editable=False)
        if ok:
            query = "UPDATE Siniestros SET estatus = %s WHERE folio = %s"
            params = (new_status, folio)
            try:
                self.db.execute_query(query, params)
                QMessageBox.information(self, 'Éxito', 'Estatus actualizado exitosamente.')
                self.load_data()
            except Exception as e:
                print(f"Error al actualizar estatus: {e}")
                QMessageBox.critical(self, 'Error', f'Error al actualizar estatus: {e}')

class VerSiniestrosForm(QDialog):
    def __init__(self, db, parent=None):
        super(VerSiniestrosForm, self).__init__(parent)
        self.setWindowTitle('Ver Siniestros')
        self.db = db

        layout = QVBoxLayout()

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(['ACTIVA', 'RESUELTO'])
        layout.addWidget(self.status_combo)

        self.load_btn = QPushButton('Cargar Siniestros', self)
        self.load_btn.clicked.connect(self.load_siniestros)
        layout.addWidget(self.load_btn)

        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_siniestros(self):
        estatus = self.status_combo.currentText()
        query = "SELECT folio, eco, fecha FROM Siniestros WHERE estatus = %s"
        self.db.execute_query(query, (estatus,))
        siniestros = self.db.fetch_all()

        self.table.setRowCount(len(siniestros))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Folio', 'Económico', 'Fecha'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row_num, siniestro in enumerate(siniestros):
            self.table.setItem(row_num, 0, QTableWidgetItem(str(siniestro[0])))
            self.table.setItem(row_num, 1, QTableWidgetItem(str(siniestro[1])))
            self.table.setItem(row_num, 2, QTableWidgetItem(str(siniestro[2])))

        self.table.cellDoubleClicked.connect(self.view_details)

    def view_details(self, row, column):
        folio = self.table.item(row, 0).text()
        query = """
        SELECT fecha, hora, eco, id_chofer, culpable, tipo_pago, foto_general, foto_frontal, foto_trasera, foto_lateral_izquierdo, foto_lateral_derecho, descripcion, estatus
        FROM Siniestros WHERE folio = %s
        """
        self.db.execute_query(query, (folio,))
        siniestro = self.db.fetch_all()[0]

        details_dialog = QDialog(self)
        details_dialog.setWindowTitle(f"Siniestro {folio}")

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow("Fecha:", QLabel(str(siniestro[0])))
        form_layout.addRow("Hora:", QLabel(str(siniestro[1])))
        form_layout.addRow("Económico:", QLabel(str(siniestro[2])))
        form_layout.addRow("ID Chofer:", QLabel(str(siniestro[3])))
        form_layout.addRow("Culpable:", QLabel("Sí" if siniestro[4] else "No"))
        form_layout.addRow("Tipo de Pago:", QLabel(str(siniestro[5])))
        form_layout.addRow("Descripción:", QLabel(siniestro[11]))
        form_layout.addRow("Estatus:", QLabel(siniestro[12]))

        layout.addLayout(form_layout)

        photo_layout = QHBoxLayout()
        photos = [siniestro[6], siniestro[7], siniestro[8], siniestro[9], siniestro[10]]
        for photo in photos:
            if photo:
                label = QLabel(self)
                pixmap = QPixmap()
                pixmap.loadFromData(photo)
                label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                label.mousePressEvent = lambda event, p=pixmap: self.show_full_image(p)
                photo_layout.addWidget(label)

        layout.addLayout(photo_layout)

        close_button = QPushButton('Cerrar', details_dialog)
        close_button.clicked.connect(details_dialog.accept)
        layout.addWidget(close_button)

        details_dialog.setLayout(layout)
        details_dialog.exec_()

    def show_full_image(self, pixmap):
        image_dialog = QDialog(self)
        image_dialog.setWindowTitle("Imagen Completa")

        layout = QVBoxLayout()
        label = QLabel(self)
        label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        layout.addWidget(label)

        close_button = QPushButton('Cerrar', image_dialog)
        close_button.clicked.connect(image_dialog.accept)
        layout.addWidget(close_button)

        image_dialog.setLayout(layout)
        image_dialog.exec_()
