from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ChoferInfoWindow(QDialog):
    def __init__(self, chofer_data, parent=None):
        super(ChoferInfoWindow, self).__init__(parent)
        self.chofer_data = chofer_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Información del Chofer')
        self.resize(300, 400)

        layout = QVBoxLayout()

        for key, value in self.chofer_data.items():
            label = QLabel(f"{key}: {value}", self)
            layout.addWidget(label)

        close_button = QPushButton('Cerrar', self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
