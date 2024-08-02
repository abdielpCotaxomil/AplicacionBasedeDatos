from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import QDateTime
import psycopg2

class AddElecMecForm(QMainWindow):
    def __init__(self, db):
        super(AddElecMecForm, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Agregar Historial Electro-Mecánica')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.folio_label = QLabel('Folio: Generado automáticamente')
        layout.addWidget(self.folio_label)

        self.eco_label = QLabel('Eco:')
        self.eco_combo = QComboBox(self)
        layout.addWidget(self.eco_label)
        layout.addWidget(self.eco_combo)
        self.load_eco()

        self.tipo_label = QLabel('Tipo:')
        self.tipo_combo = QComboBox(self)
        self.tipo_combo.addItems(['Electro', 'Mecanica'])
        layout.addWidget(self.tipo_label)
        layout.addWidget(self.tipo_combo)

        self.descripcion_label = QLabel('Descripción:')
        self.descripcion_edit = QTextEdit(self)
        layout.addWidget(self.descripcion_label)
        layout.addWidget(self.descripcion_edit)

        self.add_button = QPushButton('GUARDAR', self)
        self.add_button.clicked.connect(self.save_electro_mecanic_history)
        layout.addWidget(self.add_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def load_eco(self):
        try:
            query = "SELECT eco FROM autobus WHERE estatus = 'ACTIVO'"
            self.db.cursor.execute(query)
            ecos = self.db.cursor.fetchall()
            for eco in ecos:
                self.eco_combo.addItem(str(eco[0]))
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar ecos: {e}', QMessageBox.Ok)

    def save_electro_mecanic_history(self):
        eco = self.eco_combo.currentText()
        tipo = self.tipo_combo.currentText()
        descripcion = self.descripcion_edit.toPlainText()
        fecha_hora = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        # Convertir tipo a número
        tipo_num = 1 if tipo == 'Electro' else 2

        try:
            query_folio = "SELECT nextval('folio_seq_seis')"
            self.db.cursor.execute(query_folio)
            folio = self.db.cursor.fetchone()[0]

            query_insert = """
            INSERT INTO historial_electro_mecanica (folio, fecha, hora, eco, tipo_electro_mecanica, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            fecha, hora = fecha_hora.split(' ')
            self.db.cursor.execute(query_insert, (folio, fecha, hora, eco, tipo_num, descripcion))
            self.db.connection.commit()

            QMessageBox.information(self, 'Éxito', 'Historial electro-mecánica agregado correctamente.', QMessageBox.Ok)
            self.close()

        except psycopg2.Error as e:
            self.db.connection.rollback()
            QMessageBox.critical(self, 'Error', f'Error al agregar historial electro-mecánica: {e}', QMessageBox.Ok)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
