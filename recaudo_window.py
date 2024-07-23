from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy
from add_rec_form import AddRecForm  # Asegúrate de que también se importe correctamente el archivo add_rec_form si es necesario
from info_rec import InfoRec  # Importa la clase InfoRec
from PyQt5.QtCore import Qt

class RecaudoWindow(QMainWindow):
    def __init__(self, db):
        super(RecaudoWindow, self).__init__()
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
        self.check_addRec_button = QPushButton('Agregar Recaudo', self)
        self.check_addRec_button.clicked.connect(self.show_add_rec_form)
        self.check_addRec_button.setStyleSheet('background-color: rgb(127, 98, 184); color: white;')
        self.check_addRec_button.setMinimumWidth(200)  # Asegura un ancho mínimo
        self.check_addRec_button.setMaximumWidth(300)  # Limita el ancho máximo
        layout.addWidget(self.check_addRec_button, alignment=Qt.AlignCenter)

        # Botón Información de Recaudos
        self.info_rec_button = QPushButton('Información de Recaudos', self)
        self.info_rec_button.clicked.connect(self.show_info_rec_form)
        self.info_rec_button.setStyleSheet('background-color: rgb(127, 98, 184); color: white;')
        self.info_rec_button.setMinimumWidth(200)  # Asegura un ancho mínimo
        self.info_rec_button.setMaximumWidth(300)  # Limita el ancho máximo
        layout.addWidget(self.info_rec_button, alignment=Qt.AlignCenter)

        # Espacio flexible después de los botones
        layout.addItem(spacer)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def show_add_rec_form(self):
        self.add_rec_form = AddRecForm(self.db)
        self.add_rec_form.show()

    def show_info_rec_form(self):
        self.info_rec_form = InfoRec(self.db)
        self.info_rec_form.show()
