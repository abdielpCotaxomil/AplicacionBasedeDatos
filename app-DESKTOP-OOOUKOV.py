import sys
import json
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QFile, QTextStream, Qt
from main_window import MainWindow
from database import Database

class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.resize(600, 300)

        self.config_file = 'config.json'
        self.load_config()

        main_layout = QHBoxLayout()

        form_layout = QVBoxLayout()

        self.ip = QLineEdit(self)
        self.ip.setPlaceholderText('IP de la base de datos')
        self.ip.setText(self.config.get('host', ''))
        form_layout.addWidget(self.ip)

        self.port = QLineEdit(self)
        self.port.setPlaceholderText('Puerto')
        self.port.setText(self.config.get('port', ''))
        form_layout.addWidget(self.port)

        self.user = QLineEdit(self)
        self.user.setPlaceholderText('Usuario')
        self.user.setText(self.config.get('user', ''))
        form_layout.addWidget(self.user)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Contraseña')
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setText(self.config.get('password', ''))
        form_layout.addWidget(self.password)

        self.dbname = QLineEdit(self)
        self.dbname.setPlaceholderText('Nombre de la base de datos')
        self.dbname.setText(self.config.get('dbname', ''))
        form_layout.addWidget(self.dbname)

        self.login_btn = QPushButton('Login', self)
        self.login_btn.clicked.connect(self.check_login)
        form_layout.addWidget(self.login_btn)

        main_layout.addLayout(form_layout)

        image_label = QLabel(self)
        pixmap = QPixmap("resources/cotaxomil.jpg")
        scaled_pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2, Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        main_layout.addWidget(image_label)

        self.setLayout(main_layout)

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {}
        except json.JSONDecodeError:
            self.config = {}

    def save_config(self):
        self.config['host'] = self.ip.text()
        self.config['port'] = self.port.text()
        self.config['user'] = self.user.text()
        self.config['password'] = self.password.text()
        self.config['dbname'] = self.dbname.text()
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file)

    def check_login(self):
        ip = self.ip.text()
        port = self.port.text()
        user = self.user.text()
        password = self.password.text()
        dbname = self.dbname.text()

        db_params = {
            'host': ip,
            'port': port,
            'user': user,
            'password': password,
            'dbname': dbname
        }

        try:
            db = Database(**db_params)
            roles = db.get_user_roles(user)
            if roles:
                self.main_window = MainWindow(db_params, roles)
                self.main_window.show()
                self.save_config()
                self.close()
            else:
                QMessageBox.critical(self, 'Error', 'Usuario o contraseña incorrectos', QMessageBox.Ok)
        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, 'Error', 'No se pudo conectar a la base de datos', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Cargar el archivo de estilos QSS
    file = QFile("resources/styles.qss")
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

    login = LoginForm()
    login.show()
    sys.exit(app.exec_())
