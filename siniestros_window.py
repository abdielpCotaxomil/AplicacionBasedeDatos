from PyQt5.QtWidgets import QMainWindow, qApp, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit, QTimeEdit, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QDateTime
import os
import sys
import tempfile
import subprocess
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os
import tempfile
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from PyQt5.QtWidgets import QMainWindow, qApp, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit, QTimeEdit, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QDateTime,QDate
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QComboBox, QDateEdit, QTextEdit, QLabel
from PyQt5.QtCore import Qt, QDate

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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

        # Botón para imprimir formato
        self.imprimir_formato_btn = QPushButton('Imprimir Formato', self)
        self.imprimir_formato_btn.clicked.connect(self.imprimir_formato)
        layout.addWidget(self.imprimir_formato_btn)

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

    def imprimir_formato(self):
        dialog = SeleccionarFormatoDialog(self)
        dialog.exec_()

class SeleccionarFormatoDialog(QDialog):
    def __init__(self, parent=None):
        super(SeleccionarFormatoDialog, self).__init__(parent)
        self.setWindowTitle('Seleccionar Formato')
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.formato_combo = QComboBox(self)
        self.formato_combo.addItems(['Pago', 'Reparación'])
        layout.addWidget(QLabel('Selecciona el tipo de formato:'))
        layout.addWidget(self.formato_combo)

        self.siguiente_btn = QPushButton('Siguiente', self)
        self.siguiente_btn.clicked.connect(self.siguiente)
        layout.addWidget(self.siguiente_btn)

        self.setLayout(layout)

    def siguiente(self):
        tipo_formato = self.formato_combo.currentText()
        if tipo_formato == 'Pago':
            dialog = FormatoPagoDialog(self)
        else:
            dialog = FormatoReparacionDialog(self)
        dialog.exec_()
        self.close()

class SeleccionarFormatoDialog(QDialog):
    def __init__(self, parent=None):
        super(SeleccionarFormatoDialog, self).__init__(parent)
        self.setWindowTitle('Seleccionar Formato')
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.formato_combo = QComboBox(self)
        self.formato_combo.addItems(['Pago', 'Reparación'])
        layout.addWidget(QLabel('Selecciona el tipo de formato:'))
        layout.addWidget(self.formato_combo)

        self.siguiente_btn = QPushButton('Siguiente', self)
        self.siguiente_btn.clicked.connect(self.siguiente)
        layout.addWidget(self.siguiente_btn)

        self.setLayout(layout)

    def siguiente(self):
        tipo_formato = self.formato_combo.currentText()
        if tipo_formato == 'Pago':
            dialog = FormatoPagoDialog(self)
        else:
            dialog = FormatoReparacionDialog(self)
        dialog.exec_()
        self.close()

class SeleccionarFormatoDialog(QDialog):
    def __init__(self, parent=None):
        super(SeleccionarFormatoDialog, self).__init__(parent)
        self.setWindowTitle('Seleccionar Formato')
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.formato_combo = QComboBox(self)
        self.formato_combo.addItems(['Pago', 'Reparación'])
        layout.addWidget(QLabel('Selecciona el tipo de formato:'))
        layout.addWidget(self.formato_combo)

        self.siguiente_btn = QPushButton('Siguiente', self)
        self.siguiente_btn.clicked.connect(self.siguiente)
        layout.addWidget(self.siguiente_btn)

        self.setLayout(layout)

    def siguiente(self):
        tipo_formato = self.formato_combo.currentText()
        if tipo_formato == 'Pago':
            dialog = FormatoPagoDialog(self)
        else:
            dialog = FormatoReparacionDialog(self)
        dialog.exec_()
        self.close()

class SeleccionarFormatoDialog(QDialog):
    def __init__(self, parent=None):
        super(SeleccionarFormatoDialog, self).__init__(parent)
        self.setWindowTitle('Seleccionar Formato')
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.formato_combo = QComboBox(self)
        self.formato_combo.addItems(['Pago', 'Reparación'])
        layout.addWidget(QLabel('Selecciona el tipo de formato:'))
        layout.addWidget(self.formato_combo)

        self.siguiente_btn = QPushButton('Siguiente', self)
        self.siguiente_btn.clicked.connect(self.siguiente)
        layout.addWidget(self.siguiente_btn)

        self.setLayout(layout)

    def siguiente(self):
        tipo_formato = self.formato_combo.currentText()
        if tipo_formato == 'Pago':
            dialog = FormatoPagoDialog(self)
        else:
            dialog = FormatoReparacionDialog(self)
        dialog.exec_()
        self.close()

class FormatoPagoDialog(QDialog):
    def __init__(self, parent=None):
        super(FormatoPagoDialog, self).__init__(parent)
        self.setWindowTitle('Recibo de Pago por Reparación de Daños')
        self.resize(400, 600)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.fecha_pago = QDateEdit(self)
        self.fecha_pago.setCalendarPopup(True)
        self.fecha_pago.setDate(QDate.currentDate())
        form_layout.addRow('Fecha del Pago:', self.fecha_pago)

        self.nombre_receptor = QLineEdit(self)
        form_layout.addRow('Nombre Afectado:', self.nombre_receptor)

        self.rol_receptor = QLineEdit(self)
        form_layout.addRow('Rol/Cargo:', self.rol_receptor)

        self.nombre_pagador = QLineEdit(self)
        form_layout.addRow('Nombre del Ejecutivo:', self.nombre_pagador)

        self.monto_letras = QLineEdit(self)
        form_layout.addRow('Monto en Letras:', self.monto_letras)

        self.monto_numeros = QLineEdit(self)
        form_layout.addRow('Monto en Números:', self.monto_numeros)

        self.fecha_incidente = QDateEdit(self)
        self.fecha_incidente.setCalendarPopup(True)
        self.fecha_incidente.setDate(QDate.currentDate())
        form_layout.addRow('Fecha del Incidente:', self.fecha_incidente)

        self.descripcion_dano = QTextEdit(self)
        form_layout.addRow('Descripción del Daño:', self.descripcion_dano)

        self.metodo_pago_combo = QComboBox(self)
        self.metodo_pago_combo.addItems(['Efectivo', 'Transferencia Bancaria'])
        form_layout.addRow('Método de Pago:', self.metodo_pago_combo)

        self.banco = QLineEdit(self)
        form_layout.addRow('Banco:', self.banco)

        self.numero_cuenta = QLineEdit(self)
        form_layout.addRow('Número de Cuenta:', self.numero_cuenta)

        self.fecha_transferencia = QDateEdit(self)
        self.fecha_transferencia.setCalendarPopup(True)
        self.fecha_transferencia.setDate(QDate.currentDate())
        form_layout.addRow('Fecha de la Transferencia:', self.fecha_transferencia)

        self.referencia_transferencia = QLineEdit(self)
        form_layout.addRow('Referencia de la Transferencia:', self.referencia_transferencia)

        self.observaciones = QTextEdit(self)
        form_layout.addRow('Observaciones:', self.observaciones)

        self.nombre_responsable_pago = QLineEdit(self)
        form_layout.addRow('Nombre del Ejecutivo a Pagar:', self.nombre_responsable_pago)

        layout.addLayout(form_layout)

        self.imprimir_btn = QPushButton('Imprimir', self)
        self.imprimir_btn.clicked.connect(self.imprimir)
        layout.addWidget(self.imprimir_btn)

        self.setLayout(layout)

    def imprimir(self):
        # Generar PDF con reportlab en tamaño de ticket 58mm
        ticket_width = 58 * mm  # 58 mm de ancho para el ticket
        ticket_height = 200 * mm  # Altura estimada del ticket, ajustable según necesidad
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            c = canvas.Canvas(temp_file.name, pagesize=(ticket_width, ticket_height))

            logo_path = resource_path('resources/cotaxomil.jpg')
            if os.path.exists(logo_path):
                try:
                    c.drawImage(logo_path, 5 * mm, ticket_height - 30 * mm, width=48 * mm, height=20 * mm)
                except Exception as e:
                    print(f"Error al dibujar la imagen: {e}")

            y = ticket_height - 100
            c.setFont("Helvetica-Bold", 7)
            c.drawString(4, y, "RECIBO DE PAGO SINIESTRO COTAXOMIL")
            y -= 20

            c.setFont("Helvetica", 6)
            c.drawString(6, y, f"Fecha: {self.fecha_pago.date().toString('dd/MM/yyyy')}")
            y -= 15

            c.drawString(6, y, f"Nombre del afectado: {self.nombre_receptor.text()}")
            y -= 15

            c.drawString(6, y, f"Rol del Ejecutivo: {self.rol_receptor.text()}")
            y -= 15

            c.drawString(6, y, f"Nombre del Pagador: {self.nombre_pagador.text()}")
            y -= 15

            c.drawString(6, y, f"Monto en Letras: {self.monto_letras.text()}")
            y -= 15

            c.drawString(6, y, f"Monto en Números: {self.monto_numeros.text()}")
            y -= 15

            c.drawString(6, y, f"Fecha del Incidente: {self.fecha_incidente.date().toString('dd/MM/yyyy')}")
            y -= 15

            # Ajustar el texto de la descripción del daño al tamaño del ticket
            descripcion_dano = self.descripcion_dano.toPlainText()
            max_width = ticket_width - 20  # Margen de 10 mm a cada lado
            styles = getSampleStyleSheet()
            styleN = ParagraphStyle('Normal', fontSize=8)
            p = Paragraph(descripcion_dano, styleN)
            width, height = p.wrap(max_width, y)
            p.drawOn(c, 10, y - height)
            y -= height + 15

            c.drawString(6, y, f"Método de Pago: {self.metodo_pago_combo.currentText()}")
            y -= 15

            if self.metodo_pago_combo.currentText() == 'Transferencia Bancaria':
                c.drawString(6, y, f"Banco: {self.banco.text()}")
                y -= 15
                c.drawString(6, y, f"Número de cuenta: {self.numero_cuenta.text()}")
                y -= 15
                c.drawString(6, y, f"Fecha de la Transferencia: {self.fecha_transferencia.date().toString('dd/MM/yyyy')}")
                y -= 15
                c.drawString(6, y, f"Referencia de la Transferencia: {self.referencia_transferencia.text()}")
                y -= 15

            c.drawString(6, y, f"Observaciones: {self.observaciones.toPlainText()}")
            y -= 15

            c.drawString(6, y, f"Nombre del Afectado: {self.nombre_responsable_pago.text()}")
            y -= 15

            c.drawString(6, y, "Firma: ____________________________")
            y -= 30

            c.drawString(6, y, f"PAGO COTAXOMIL:")
            y -= 15
            c.drawString(6, y, f"Nombre: {self.nombre_receptor.text()}")
            y -= 30
            c.drawString(6, y, "Firma: ____________________________")
            y -= 30

            c.drawString(6, y, "Dirección de la Empresa:")
            y -= 15
            c.drawString(6, y, "Camino antiguo a San Lucas 533 Talas de San Lorenzo")
            y -= 15
            c.drawString(6, y, "Xochimilco, Ciudad de México, CP:16090, México")
            y -=15
            c.drawString(6, y, "Teléfono: 00-00-00-00-00")

            c.save()

        subprocess.run(["start", temp_file.name], shell=True)

class FormatoReparacionDialog(QDialog):
    def __init__(self, parent=None):
        super(FormatoReparacionDialog, self).__init__(parent)
        self.setWindowTitle('Acta de Compromiso de Reparación de Daños')
        self.resize(400, 600)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.fecha_redaccion = QDateEdit(self)
        self.fecha_redaccion.setCalendarPopup(True)
        self.fecha_redaccion.setDate(QDate.currentDate())
        form_layout.addRow('Fecha de Redacción:', self.fecha_redaccion)

        self.nombre_responsable = QLineEdit(self)
        form_layout.addRow('Nombre del ejecutivo:', self.nombre_responsable)

        self.rol_responsable = QLineEdit(self)
        form_layout.addRow('Rol/Cargo:', self.rol_responsable)

        self.fecha_incidente = QDateEdit(self)
        self.fecha_incidente.setCalendarPopup(True)
        self.fecha_incidente.setDate(QDate.currentDate())
        form_layout.addRow('Fecha del Incidente:', self.fecha_incidente)

        self.descripcion_dano = QTextEdit(self)
        form_layout.addRow('Descripción del Daño:', self.descripcion_dano)

        self.descripcion_reparacion = QTextEdit(self)
        form_layout.addRow('Descripción de la Reparación:', self.descripcion_reparacion)

        self.plazo_reparacion = QDateEdit(self)
        self.plazo_reparacion.setCalendarPopup(True)
        self.plazo_reparacion.setDate(QDate.currentDate().addDays(7))
        form_layout.addRow('Plazo para la Reparación:', self.plazo_reparacion)

        self.condiciones_especificas = QTextEdit(self)
        form_layout.addRow('Condiciones Específicas:', self.condiciones_especificas)

        self.observaciones = QTextEdit(self)
        form_layout.addRow('Observaciones:', self.observaciones)

        layout.addLayout(form_layout)

        self.imprimir_btn = QPushButton('Imprimir', self)
        self.imprimir_btn.clicked.connect(self.imprimir)
        layout.addWidget(self.imprimir_btn)

        self.setLayout(layout)

    def imprimir(self):
        # Generar PDF con reportlab en tamaño de ticket 58mm
        ticket_width = 58 * mm  # 58 mm de ancho para el ticket
        ticket_height = 200 * mm  # Altura fija para el ticket
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            c = canvas.Canvas(temp_file.name, pagesize=(ticket_width, ticket_height))

            # Añadir logo
            logo_path = resource_path('resources/cotaxomil.jpg')
            if os.path.exists(logo_path):
                try:
                    c.drawImage(logo_path, 5 * mm, ticket_height - 30 * mm, width=48 * mm, height=20 * mm)
                except Exception as e:
                    print(f"Error al dibujar la imagen: {e}")

            y = ticket_height - 40 * mm
            c.setFont("Helvetica-Bold", 7)
            c.drawString(3 * mm, y, "COMPROMISO DE REPARACIÓN DE DAÑOS")
            y -= 20

            c.setFont("Helvetica", 5)
            c.drawString(5 * mm, y, f"Fecha: {self.fecha_redaccion.date().toString('dd/MM/yyyy')}")
            y -= 15

            c.drawString(5 * mm, y, f"Nombre del Afectado: {self.nombre_responsable.text()}")
            y -= 15

            c.drawString(5 * mm, y, f"Rol/Cargo: {self.rol_responsable.text()}")
            y -= 15

            c.drawString(5 * mm, y, f"Fecha del Incidente: {self.fecha_incidente.date().toString('dd/MM/yyyy')}")
            y -= 15

            # Ajustar el texto de la descripción del daño al tamaño del ticket
            descripcion_dano = self.descripcion_dano.toPlainText()
            max_width = ticket_width - 10 * mm  # Margen de 5 mm a cada lado
            styles = getSampleStyleSheet()
            styleN = ParagraphStyle('Normal', fontSize=8)
            p = Paragraph(descripcion_dano, styleN)
            width, height = p.wrap(max_width, y)
            p.drawOn(c, 5 * mm, y - height)
            y -= height + 15

            # Ajustar el texto de la descripción de la reparación al tamaño del ticket
            descripcion_reparacion = self.descripcion_reparacion.toPlainText()
            p = Paragraph(descripcion_reparacion, styleN)
            width, height = p.wrap(max_width, y)
            p.drawOn(c, 5 * mm, y - height)
            y -= height + 15

            c.drawString(5 * mm, y, f"Plazo para la Reparación: {self.plazo_reparacion.date().toString('dd/MM/yyyy')}")
            y -= 15

            c.drawString(5 * mm, y, f"Condiciones Específicas: {self.condiciones_especificas.toPlainText()}")
            y -= 15

            c.drawString(5 * mm, y, f"Observaciones: {self.observaciones.toPlainText()}")
            y -= 15

            c.drawString(5 * mm, y, "Firma: ____________________________")
            y -= 30

            c.drawString(5 * mm, y, f"Ejecutivo Responsable:")
            y -= 15
            c.drawString(5 * mm, y, f"Nombre: {self.nombre_responsable.text()}")
            y -= 30
            c.drawString(5 * mm, y, "Firma: ____________________________")
            y -= 30

            c.drawString(5 * mm, y, "Dirección de la Empresa:")
            y -= 15
            c.drawString(5 * mm, y, "Camino antiguo a San Lucas 533 Talas de San Lorenzo")
            y -= 15
            c.drawString(5 * mm, y, "Xochimilco, Ciudad de México, CP:16090, México")
            y -= 15
            c.drawString(5 * mm, y, "Teléfono:00-00-00-00-00")

            c.save()

        subprocess.run(["start", temp_file.name], shell=True)


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
        self.foto_general_label = QLabel('No seleccionada')
        self.foto_general_select_btn = QPushButton('Seleccionar Foto General', self)
        self.foto_general_select_btn.clicked.connect(self.select_foto_general)
        self.foto_general_take_btn = QPushButton('Tomar Foto General', self)
        self.foto_general_take_btn.clicked.connect(self.take_foto_general)
        self.foto_general_btn.addWidget(self.foto_general_select_btn)
        self.foto_general_btn.addWidget(self.foto_general_take_btn)
        self.foto_general_btn.addWidget(self.foto_general_label)
        form_layout.addRow('Foto General:', self.foto_general_btn)

        self.foto_frontal_btn = QHBoxLayout()
        self.foto_frontal_label = QLabel('No seleccionada')
        self.foto_frontal_select_btn = QPushButton('Seleccionar Foto Frontal', self)
        self.foto_frontal_select_btn.clicked.connect(self.select_foto_frontal)
        self.foto_frontal_take_btn = QPushButton('Tomar Foto Frontal', self)
        self.foto_frontal_take_btn.clicked.connect(self.take_foto_frontal)
        self.foto_frontal_btn.addWidget(self.foto_frontal_select_btn)
        self.foto_frontal_btn.addWidget(self.foto_frontal_take_btn)
        self.foto_frontal_btn.addWidget(self.foto_frontal_label)
        form_layout.addRow('Foto Frontal:', self.foto_frontal_btn)

        self.foto_trasera_btn = QHBoxLayout()
        self.foto_trasera_label = QLabel('No seleccionada')
        self.foto_trasera_select_btn = QPushButton('Seleccionar Foto Trasera', self)
        self.foto_trasera_select_btn.clicked.connect(self.select_foto_trasera)
        self.foto_trasera_take_btn = QPushButton('Tomar Foto Trasera', self)
        self.foto_trasera_take_btn.clicked.connect(self.take_foto_trasera)
        self.foto_trasera_btn.addWidget(self.foto_trasera_select_btn)
        self.foto_trasera_btn.addWidget(self.foto_trasera_take_btn)
        self.foto_trasera_btn.addWidget(self.foto_trasera_label)
        form_layout.addRow('Foto Trasera:', self.foto_trasera_btn)

        self.foto_lateral_izquierdo_btn = QHBoxLayout()
        self.foto_lateral_izquierdo_label = QLabel('No seleccionada')
        self.foto_lateral_izquierdo_select_btn = QPushButton('Seleccionar Foto Lateral Izquierdo', self)
        self.foto_lateral_izquierdo_select_btn.clicked.connect(self.select_foto_lateral_izquierdo)
        self.foto_lateral_izquierdo_take_btn = QPushButton('Tomar Foto Lateral Izquierdo', self)
        self.foto_lateral_izquierdo_take_btn.clicked.connect(self.take_foto_lateral_izquierdo)
        self.foto_lateral_izquierdo_btn.addWidget(self.foto_lateral_izquierdo_select_btn)
        self.foto_lateral_izquierdo_btn.addWidget(self.foto_lateral_izquierdo_take_btn)
        self.foto_lateral_izquierdo_btn.addWidget(self.foto_lateral_izquierdo_label)
        form_layout.addRow('Foto Lateral Izquierdo:', self.foto_lateral_izquierdo_btn)

        self.foto_lateral_derecho_btn = QHBoxLayout()
        self.foto_lateral_derecho_label = QLabel('No seleccionada')
        self.foto_lateral_derecho_select_btn = QPushButton('Seleccionar Foto Lateral Derecho', self)
        self.foto_lateral_derecho_select_btn.clicked.connect(self.select_foto_lateral_derecho)
        self.foto_lateral_derecho_take_btn = QPushButton('Tomar Foto Lateral Derecho', self)
        self.foto_lateral_derecho_take_btn.clicked.connect(self.take_foto_lateral_derecho)
        self.foto_lateral_derecho_btn.addWidget(self.foto_lateral_derecho_select_btn)
        self.foto_lateral_derecho_btn.addWidget(self.foto_lateral_derecho_take_btn)
        self.foto_lateral_derecho_btn.addWidget(self.foto_lateral_derecho_label)
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
        if self.foto_general_path:
            self.foto_general_label.setText(os.path.basename(self.foto_general_path))

    def take_foto_general(self):
        os.system('start microsoft.windows.camera:')

    def select_foto_frontal(self):
        self.foto_frontal_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto Frontal", "", "Images (*.png *.xpm *.jpg)")
        if self.foto_frontal_path:
            self.foto_frontal_label.setText(os.path.basename(self.foto_frontal_path))

    def take_foto_frontal(self):
        os.system('start microsoft.windows.camera:')

    def select_foto_trasera(self):
        self.foto_trasera_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto Trasera", "", "Images (*.png *.xpm *.jpg)")
        if self.foto_trasera_path:
            self.foto_trasera_label.setText(os.path.basename(self.foto_trasera_path))

    def take_foto_trasera(self):
        os.system('start microsoft.windows.camera:')

    def select_foto_lateral_izquierdo(self):
        self.foto_lateral_izquierdo_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto Lateral Izquierdo", "", "Images (*.png *.xpm *.jpg)")
        if self.foto_lateral_izquierdo_path:
            self.foto_lateral_izquierdo_label.setText(os.path.basename(self.foto_lateral_izquierdo_path))

    def take_foto_lateral_izquierdo(self):
        os.system('start microsoft.windows.camera:')

    def select_foto_lateral_derecho(self):
        self.foto_lateral_derecho_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto Lateral Derecho", "", "Images (*.png *.xpm *.jpg)")
        if self.foto_lateral_derecho_path:
            self.foto_lateral_derecho_label.setText(os.path.basename(self.foto_lateral_derecho_path))

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
