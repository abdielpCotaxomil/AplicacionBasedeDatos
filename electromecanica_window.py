from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton

class ElectromecanicaWindow(QMainWindow):
    def __init__(self, db):
        super(ElectromecanicaWindow, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Electro-Mecánica')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Agregar botones y funcionalidades específicos para el rol de Electro-Mecánica
        # self.some_button = QPushButton('Some Action', self)
        # layout.addWidget(self.some_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
