from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from add_est_tan_form import AddEstTanForm
from add_llen_aut_form import AddLlenAutForm

class DieselWindow(QMainWindow):
    def __init__(self, db):
        super(DieselWindow, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Recaudo')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Espacio flexible para centrar los botones
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Botón Agregar Recaudo
        self.check_AddEstTanForm_button = QPushButton('Agregar Estado del tanque', self)
        self.check_AddEstTanForm_button.clicked.connect(self.show_add_est_tan_form)
        self.check_AddEstTanForm_button.setStyleSheet('background-color: rgb(38, 77, 43); color: white;')
        self.check_AddEstTanForm_button.setMinimumWidth(200)  # Asegura un ancho mínimo
        self.check_AddEstTanForm_button.setMaximumWidth(300)  # Limita el ancho máximo
        layout.addWidget(self.check_AddEstTanForm_button, alignment=Qt.AlignCenter)

        # Botón Información de Recaudos
        self.info_AddLlenAutForm_button = QPushButton('Información de Recaudos', self)
        self.info_AddLlenAutForm_button.clicked.connect(self.show_add_llen_aut_form)
        self.info_AddLlenAutForm_button.setStyleSheet('background-color: rgb(38, 77, 43); color: white;')
        self.info_AddLlenAutForm_button.setMinimumWidth(200)  # Asegura un ancho mínimo
        self.info_AddLlenAutForm_button.setMaximumWidth(300)  # Limita el ancho máximo
        layout.addWidget(self.info_AddLlenAutForm_button, alignment=Qt.AlignCenter)

        # Espacio flexible después de los botones
        layout.addItem(spacer)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def show_add_est_tan_form(self):
        self.add_est_tan_form = AddEstTanForm(self.db)
        self.add_est_tan_form.show()

    def show_add_llen_aut_form(self):
        self.add_llen_aut_form = AddLlenAutForm(self.db)
        self.add_llen_aut_form.show()
