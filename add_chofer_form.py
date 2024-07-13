from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QDateEdit,
    QFileDialog, QMessageBox, QHBoxLayout, QProgressDialog
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap
import cv2
from chofer_info_window import ChoferInfoWindow
import psycopg2

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
        form_layout.addRow('Nombre:', self.nombre)

        self.apellido_paterno = QLineEdit(self)
        form_layout.addRow('Apellido Paterno:', self.apellido_paterno)

        self.apellido_materno = QLineEdit(self)
        form_layout.addRow('Apellido Materno:', self.apellido_materno)

        self.rfc = QLineEdit(self)
        form_layout.addRow('RFC:', self.rfc)

        self.nss = QLineEdit(self)
        form_layout.addRow('NSS:', self.nss)

        self.curp = QLineEdit(self)
        form_layout.addRow('CURP:', self.curp)

        self.salario_base = QLineEdit(self)
        form_layout.addRow('Salario Base:', self.salario_base)

        self.tipo_jornada = QLineEdit(self)
        form_layout.addRow('Tipo de Jornada:', self.tipo_jornada)

        self.fecha_vencimiento_tarjeton = QDateEdit(self)
        self.fecha_vencimiento_tarjeton.setCalendarPopup(True)
        self.fecha_vencimiento_tarjeton.setDate(QDate.currentDate())
        form_layout.addRow('Fecha Vencimiento Tarjetón:', self.fecha_vencimiento_tarjeton)

        self.photos = {}
        self.photo_labels = {}  # Inicializar el diccionario photo_labels

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
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto", "", "Images (.jpg)", options=options)
        if filename:
            pixmap = QPixmap(filename)
            self.photos[photo_type] = pixmap
            self.photo_labels[photo_type].setText(filename.split('/')[-1])

    def capture_photo(self, photo_type):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            filename, _ = QFileDialog.getSaveFileName(self, "Guardar Foto", "", "Images (*.png *.xpm *.jpg)")
            if filename:
                cv2.imwrite(filename, frame)
                pixmap = QPixmap(filename)
                self.photos[photo_type] = pixmap
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

            if not all([nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton]):
                QMessageBox.critical(self, 'Error', 'Todos los campos deben estar llenos', QMessageBox.Ok)
                return

            fotos = {}
            for key in ['foto_credencial_frontal', 'foto_credencial_trasera', 'foto_tarjeton_frontal', 'foto_tarjeton_trasera', 'foto_chofer']:
                if key in self.photos:
                    fotos[key] = self.photos[key].toImage().bits().asstring(self.photos[key].toImage().byteCount())
                else:
                    QMessageBox.critical(self, 'Error', f'{key} no está proporcionada', QMessageBox.Ok)
                    return

            query = """
            INSERT INTO empleado_chofer (nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton, foto_credencial_frontal, foto_credencial_trasera, foto_tarjeton_frontal, foto_tarjeton_trasera, foto_chofer)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_chofer
            """

            progress_dialog = QProgressDialog("Guardando...", None, 0, 0, self)
            progress_dialog.setWindowTitle("Guardando")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()

            try:
                print("Ejecutando query")
                self.db.cursor.execute(query, (nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton, fotos['foto_credencial_frontal'], fotos['foto_credencial_trasera'], fotos['foto_tarjeton_frontal'], fotos['foto_tarjeton_trasera'], fotos['foto_chofer']))
                id_chofer = self.db.cursor.fetchone()[0]
                self.db.connection.commit()

                progress_dialog.close()
                print("Query ejecutada correctamente")
                chofer_data = self.fetch_chofer_data(id_chofer)
                self.show_chofer_info(chofer_data)
                self.close()
            except psycopg2.Error as e:
                progress_dialog.close()
                self.db.connection.rollback()
                print(f"Error durante la ejecución del query: {e}")
                QMessageBox.critical(self, 'Error', f'No se pudo agregar el chofer: {e}', QMessageBox.Ok)
            except Exception as e:
                progress_dialog.close()
                print(f"Error inesperado: {e}")
                QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
        except Exception as e:
            print(f"Error inesperado fuera de la consulta: {e}")
            QMessageBox.critical(self, 'Error', f'Error inesperado fuera de la consulta: {e}', QMessageBox.Ok)

    def fetch_chofer_data(self, id_chofer):
        try:
            query = """
            SELECT id_chofer, nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton
            FROM empleado_chofer
            WHERE id_chofer = %s
            """
            self.db.cursor.execute(query, (id_chofer,))
            row = self.db.cursor.fetchone()

            chofer_data = {
                "ID": row[0],
                "Nombre": row[1],
                "Apellido Paterno": row[2],
                "Apellido Materno": row[3],
                "RFC": row[4],
                "NSS": row[5],
                "CURP": row[6],
                "Salario Base": row[7],
                "Tipo de Jornada": row[8],
                "Fecha Vencimiento Tarjetón": row[9]
            }
            return chofer_data
        except Exception as e:
            print(f"Error obteniendo los datos del chofer: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo obtener los datos del chofer: {e}', QMessageBox.Ok)
            return {}

    def show_chofer_info(self, chofer_data):
        self.chofer_info_window = ChoferInfoWindow(chofer_data)
        self.chofer_info_window.exec_()
