from PyQt5.QtWidgets import QMainWindow, qApp, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from forms import AddBusForm
from database import Database

from admin_window import AdminWindow
from checadores_window import ChecadoresWindow
from recaudo_window import RecaudoWindow
from electromecanica_window import ElectromecanicaWindow
from diesel_window import DieselWindow
from golpes_window import GolpesWindow

class MainWindow(QMainWindow):
    def __init__(self, db_params, user_roles):
        super(MainWindow, self).__init__()
        self.db = Database(**db_params)
        self.user_roles = user_roles
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('COTAXOMIL')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()

        # Menu Lateral
        menu_layout = QVBoxLayout()

        menu_label = QLabel("MENU")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        menu_label.setFont(font)
        menu_layout.addWidget(menu_label, alignment=Qt.AlignCenter)

        self.adminButton = QPushButton('Administración', self)
        self.adminButton.clicked.connect(self.show_admin_window)
        self.adminButton.setStyleSheet("padding: 10px;")
        menu_layout.addWidget(self.adminButton, alignment=Qt.AlignCenter)

        self.checadorsButton = QPushButton('Checadores', self)
        self.checadorsButton.clicked.connect(self.show_checadores_window)
        self.checadorsButton.setStyleSheet("padding: 10px;")
        menu_layout.addWidget(self.checadorsButton, alignment=Qt.AlignCenter)

        self.recaudoButton = QPushButton('Recaudo', self)
        self.recaudoButton.clicked.connect(self.show_recaudo_window)
        self.recaudoButton.setStyleSheet("padding: 10px;")
        menu_layout.addWidget(self.recaudoButton, alignment=Qt.AlignCenter)

        self.electroMecanicaButton = QPushButton('Electro-Mecánica', self)
        self.electroMecanicaButton.clicked.connect(self.show_electromecanica_window)
        self.electroMecanicaButton.setStyleSheet("padding: 10px;")
        menu_layout.addWidget(self.electroMecanicaButton, alignment=Qt.AlignCenter)

        self.dieselButton = QPushButton('Diesel', self)
        self.dieselButton.clicked.connect(self.show_diesel_window)
        self.dieselButton.setStyleSheet("padding: 10px;")
        menu_layout.addWidget(self.dieselButton, alignment=Qt.AlignCenter)

        self.golpesButton = QPushButton('Golpes', self)
        self.golpesButton.clicked.connect(self.show_golpes_window)
        self.golpesButton.setStyleSheet("padding: 10px;")
        menu_layout.addWidget(self.golpesButton, alignment=Qt.AlignCenter)

        self.exitButton = QPushButton('Salir', self)
        self.exitButton.clicked.connect(qApp.quit)
        self.exitButton.setStyleSheet("padding: 10px;")
        menu_layout.addWidget(self.exitButton, alignment=Qt.AlignCenter)

        menu_layout.addStretch(1)  # Añadir espacio flexible para centrar el menú verticalmente

        # Placeholder para contenido principal
        content_layout = QVBoxLayout()
        logo = QLabel(self)
        pixmap = QPixmap("resources/cotaxomil.jpg")
        logo.setPixmap(pixmap)
        content_layout.addWidget(logo, alignment=Qt.AlignCenter)

        main_layout.addLayout(menu_layout, 1)
        main_layout.addLayout(content_layout, 4)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

    def show_admin_window(self):
        if 'administracion' in self.user_roles or 'system' in self.user_roles:
            self.admin_window = AdminWindow(self.db)
            self.admin_window.show()
        else:
            self.show_error_message()

    def show_checadores_window(self):
        if 'checadores' in self.user_roles or 'system' in self.user_roles:
            self.checadores_window = ChecadoresWindow(self.db)
            self.checadores_window.show()
        else:
            self.show_error_message()

    def show_recaudo_window(self):
        if 'recaudo' in self.user_roles or 'system' in self.user_roles:
            self.recaudo_window = RecaudoWindow(self.db)
            self.recaudo_window.show()
        else:
            self.show_error_message()

    def show_electromecanica_window(self):
        if 'electro_mecanica' in self.user_roles or 'system' in self.user_roles:
            self.electromecanica_window = ElectromecanicaWindow(self.db)
            self.electromecanica_window.show()
        else:
            self.show_error_message()

    def show_diesel_window(self):
        if 'diesel' in self.user_roles or 'system' in self.user_roles:
            self.diesel_window = DieselWindow(self.db)
            self.diesel_window.show()
        else:
            self.show_error_message()

    def show_golpes_window(self):
        if 'golpes' in self.user_roles or 'system' in self.user_roles:
            self.golpes_window = GolpesWindow(self.db)
            self.golpes_window.show()
        else:
            self.show_error_message()

    def show_error_message(self):
        QMessageBox.critical(self, 'Error', 'Usuario no admitido', QMessageBox.Ok)

    def closeEvent(self, event):
        self.db.close()
        event.accept()
