from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from add_chofer_form import AddChoferForm

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

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def show_add_chofer_form(self):
        self.add_chofer_form = AddChoferForm(self.db)
        self.add_chofer_form.show()
