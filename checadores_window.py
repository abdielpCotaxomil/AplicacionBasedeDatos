from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton

class ChecadoresWindow(QMainWindow):
    def __init__(self, db):
        super(ChecadoresWindow, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Checadores')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Agregar botones y funcionalidades específicos para el rol de Checadores
        # self.some_button = QPushButton('Some Action', self)
        # layout.addWidget(self.some_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
