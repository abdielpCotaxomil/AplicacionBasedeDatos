from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from add_sum_tan_form import AddSumTanForm
from info_tan import InfoTan

from add_elec_mec_form import AddElecMecForm
from info_reg_elec_mec import InfoElecMec
from arr_elecmec_form import ArrElecMec
from info_arr_elec_mec import InfoArrElecMec


class ElectromecanicaWindow(QMainWindow):
    def __init__(self, db):
        super(ElectromecanicaWindow, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Recaudo')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Espacio flexible para centrar los botones
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.check_add_elec_mec_form_button = QPushButton('Agregar Arreglo', self)
        self.check_add_elec_mec_form_button.clicked.connect(self.show_add_elec_mec_form)
        self.check_add_elec_mec_form_button.setStyleSheet('background-color: rgb(38, 77, 43); color: white;')
        self.check_add_elec_mec_form_button.setMinimumWidth(200)  # Asegura un ancho mínimo
        self.check_add_elec_mec_form_button.setMaximumWidth(300)  # Limita el ancho máximo
        layout.addWidget(self.check_add_elec_mec_form_button, alignment=Qt.AlignCenter)

        self.check_info_reg_elec_mec_button = QPushButton('Registros', self)
        self.check_info_reg_elec_mec_button.clicked.connect(self.show_info_reg_elec_mec_form)
        self.check_info_reg_elec_mec_button.setStyleSheet('background-color: rgb(38, 77, 43); color: white;')
        self.check_info_reg_elec_mec_button.setMinimumWidth(200)  # Asegura un ancho mínimo
        self.check_info_reg_elec_mec_button.setMaximumWidth(300)  # Limita el ancho máximo
        layout.addWidget(self.check_info_reg_elec_mec_button, alignment=Qt.AlignCenter)

        self.check_info_tan_button = QPushButton('Arreglar', self)
        self.check_info_tan_button.clicked.connect(self.show_arr_electromec_form)
        self.check_info_tan_button.setStyleSheet('background-color: rgb(38, 77, 43); color: white;')
        self.check_info_tan_button.setMinimumWidth(200)  # Asegura un ancho mínimo
        self.check_info_tan_button.setMaximumWidth(300)  # Limita el ancho máximo
        layout.addWidget(self.check_info_tan_button, alignment=Qt.AlignCenter)

        self.check_info_tan_button = QPushButton('Resueltos', self)
        self.check_info_tan_button.clicked.connect(self.show_info_arr_elec_mec_form)
        self.check_info_tan_button.setStyleSheet('background-color: rgb(38, 77, 43); color: white;')
        self.check_info_tan_button.setMinimumWidth(200)  # Asegura un ancho mínimo
        self.check_info_tan_button.setMaximumWidth(300)  # Limita el ancho máximo
        layout.addWidget(self.check_info_tan_button, alignment=Qt.AlignCenter)

        # Espacio flexible después de los botones
        layout.addItem(spacer)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def show_add_elec_mec_form(self):
        self.add_elec_mec_form = AddElecMecForm(self.db)
        self.add_elec_mec_form.show()
    
    def show_info_reg_elec_mec_form(self):
        self.info_reg_elec_mec = InfoElecMec(self.db)
        self.info_reg_elec_mec.show()

    def show_arr_electromec_form(self):
        self.arr_elecmec_form = ArrElecMec(self.db)
        self.arr_elecmec_form.show()

    def show_info_arr_elec_mec_form(self):
        self.info_arr_elec_mec = InfoArrElecMec(self.db)
        self.info_arr_elec_mec.show()
