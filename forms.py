from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDateEdit, QPushButton
from PyQt5.QtCore import QDate

class AddBusForm(QWidget):
    def __init__(self, parent=None):
        super(AddBusForm, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Agregar Autobus')
        self.resize(400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.eco = QLineEdit(self)
        form_layout.addRow('ECO:', self.eco)

        self.placa = QLineEdit(self)
        form_layout.addRow('Placa:', self.placa)

        self.numero_serie = QLineEdit(self)
        form_layout.addRow('Número de Serie:', self.numero_serie)

        self.numero_motor = QLineEdit(self)
        form_layout.addRow('Número de Motor:', self.numero_motor)

        self.fecha_vigencia_seguro = QDateEdit(self)
        self.fecha_vigencia_seguro.setCalendarPopup(True)
        self.fecha_vigencia_seguro.setDate(QDate.currentDate())
        form_layout.addRow('Fecha Vigencia Seguro:', self.fecha_vigencia_seguro)

        self.nombre_aseguradora = QLineEdit(self)
        form_layout.addRow('Nombre de la Aseguradora:', self.nombre_aseguradora)

        self.tipo = QComboBox(self)
        self.tipo.addItems(['TORETO', 'ZAFIRO'])
        form_layout.addRow('Tipo:', self.tipo)

        self.submit_btn = QPushButton('Agregar', self)
        form_layout.addRow(self.submit_btn)

        layout.addLayout(form_layout)
        self.setLayout(layout)
