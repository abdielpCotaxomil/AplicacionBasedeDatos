from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QDateTimeEdit, QMessageBox, QHBoxLayout, QComboBox
from PyQt5.QtCore import QDateTime
import psycopg2

class AddRecForm(QMainWindow):
    def __init__(self, db):
        super(AddRecForm, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Agregar Recaudo')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.folio_label = QLabel('Folio: Generado automáticamente')
        layout.addWidget(self.folio_label)

        self.fecha_hora_label = QLabel('Fecha y Hora:')
        self.fecha_hora_edit = QDateTimeEdit(self)
        self.fecha_hora_edit.setDateTime(QDateTime.currentDateTime())
        self.fecha_hora_edit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.fecha_hora_edit.setReadOnly(True)
        layout.addWidget(self.fecha_hora_label)
        layout.addWidget(self.fecha_hora_edit)

        self.eco_label = QLabel('Eco:')
        self.eco_combo = QComboBox(self)
        self.load_autobus_data()  # Load data into combo box
        layout.addWidget(self.eco_label)
        layout.addWidget(self.eco_combo)

        self.id_chofer1_label = QLabel('ID Chofer 1:')
        self.id_chofer1_combo = QComboBox(self)
        self.load_chofer_data(self.id_chofer1_combo)  # Load data into combo box
        layout.addWidget(self.id_chofer1_label)
        layout.addWidget(self.id_chofer1_combo)

        self.id_chofer2_label = QLabel('ID Chofer 2 (opcional):')
        self.id_chofer2_combo = QComboBox(self)
        self.load_chofer_data(self.id_chofer2_combo)  # Load data into combo box
        layout.addWidget(self.id_chofer2_label)
        layout.addWidget(self.id_chofer2_combo)

        self.monedas_label = QLabel('Monedas:')
        self.monedas_edit = QLineEdit(self)
        layout.addWidget(self.monedas_label)
        layout.addWidget(self.monedas_edit)

        self.billetes_label = QLabel('Billetes:')
        self.billetes_edit = QLineEdit(self)
        layout.addWidget(self.billetes_label)
        layout.addWidget(self.billetes_edit)

        self.add_recaudo_button = QPushButton('GUARDAR', self)
        self.add_recaudo_button.clicked.connect(self.show_saved_form)
        layout.addWidget(self.add_recaudo_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def load_autobus_data(self):
        try:
            query = "SELECT eco, tipo FROM autobus"
            self.db.cursor.execute(query)
            autobuses = self.db.cursor.fetchall()

            for eco, tipo in autobuses:
                self.eco_combo.addItem(f"{eco} - {tipo}", eco)

        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar datos de autobuses: {e}', QMessageBox.Ok)

    def load_chofer_data(self, combo_box):
        try:
            query = """
            SELECT c.id_chofer, c.nombre, c.apellido_paterno, c.apellido_materno, a.apodo
            FROM empleado_chofer c
            LEFT JOIN apodos a ON c.id_chofer = a.id_chofer
            """
            self.db.cursor.execute(query)
            choferes = self.db.cursor.fetchall()

            for id_chofer, nombre, apellido_paterno, apellido_materno, apodo in choferes:
                display_text = f"{id_chofer} - {nombre} {apellido_paterno} {apellido_materno} - {apodo}"
                combo_box.addItem(display_text, id_chofer)

        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar datos de choferes: {e}', QMessageBox.Ok)

    def show_saved_form(self):
        fecha_hora = self.fecha_hora_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        eco = self.eco_combo.currentData()  # Get the eco value
        id_chofer1 = self.id_chofer1_combo.currentData()  # Get the id_chofer1 value
        id_chofer2 = self.id_chofer2_combo.currentData() or None  # Get the id_chofer2 value
        monedas = self.monedas_edit.text()
        billetes = self.billetes_edit.text()

        self.saved_form = RecSavedForm(self, self.db, fecha_hora, eco, id_chofer1, id_chofer2, monedas, billetes)
        self.saved_form.show()
        self.close()

class RecSavedForm(QMainWindow):
    def __init__(self, parent, db, fecha_hora, eco, id_chofer1, id_chofer2, monedas, billetes):
        super(RecSavedForm, self).__init__(parent)
        self.parent = parent
        self.db = db
        self.fecha_hora = fecha_hora
        self.eco = eco
        self.id_chofer1 = id_chofer1
        self.id_chofer2 = id_chofer2
        self.monedas = monedas
        self.billetes = billetes
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Recaudo Guardado')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.folio_label = QLabel('Folio: Será generado al guardar')
        layout.addWidget(self.folio_label)

        self.fecha_hora_label = QLabel(f'Fecha y Hora: {self.fecha_hora}')
        layout.addWidget(self.fecha_hora_label)

        self.eco_label = QLabel(f'Eco: {self.eco}')
        layout.addWidget(self.eco_label)

        self.id_chofer1_label = QLabel(f'ID Chofer 1: {self.id_chofer1}')
        layout.addWidget(self.id_chofer1_label)

        self.id_chofer2_label = QLabel(f'ID Chofer 2: {self.id_chofer2}')
        layout.addWidget(self.id_chofer2_label)

        self.monedas_label = QLabel(f'Monedas: {self.monedas}')
        layout.addWidget(self.monedas_label)

        self.billetes_label = QLabel(f'Billetes: {self.billetes}')
        layout.addWidget(self.billetes_label)

        buttons_layout = QHBoxLayout()

        self.accept_button = QPushButton('Aceptar', self)
        self.accept_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.accept_button)

        self.edit_button = QPushButton('Editar', self)
        self.edit_button.clicked.connect(self.edit)
        buttons_layout.addWidget(self.edit_button)

        layout.addLayout(buttons_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def accept(self):
        try:
            # Generar folio automáticamente (entero)
            query_folio = "SELECT nextval('folio_seq')"
            self.db.cursor.execute(query_folio)
            folio = self.db.cursor.fetchone()[0]

            query_insert = """
            INSERT INTO historial_recaudo (folio, fecha, hora, eco, id_chofer1, id_chofer2, monedas, billetes)
            VALUES (%s, current_date, %s, %s, %s, %s, %s, %s)
            """

            self.db.cursor.execute(query_insert, (folio, self.fecha_hora, self.eco, self.id_chofer1, self.id_chofer2, self.monedas, self.billetes))
            self.db.connection.commit()

            QMessageBox.information(self, 'Éxito', 'Recaudo agregado correctamente.', QMessageBox.Ok)
            self.close()

        except psycopg2.Error as e:
            self.db.connection.rollback()
            QMessageBox.critical(self, 'Error', f'Error al agregar recaudo: {e}', QMessageBox.Ok)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)

    def edit(self):
        self.close()
        self.parent.show()
