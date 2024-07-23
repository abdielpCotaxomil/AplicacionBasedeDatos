from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QDateTimeEdit, QMessageBox, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QDateTime
import psycopg2

class AddEstTanForm(QMainWindow):
    def __init__(self, db):
        super(AddEstTanForm, self).__init__()
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

        self.cuenta_litros_inicial_label = QLabel('Litros inicial:')
        self.cuenta_litros_inicial_edit = QLineEdit(self)
        layout.addWidget(self.cuenta_litros_inicial_label)
        layout.addWidget(self.cuenta_litros_inicial_edit)

        self.add_recaudo_button = QPushButton('Mostrar Datos Recaudo', self)
        self.add_recaudo_button.clicked.connect(self.show_saved_form)
        layout.addWidget(self.add_recaudo_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def show_saved_form(self):
        fecha_hora = self.fecha_hora_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        cuenta_litros_inicial = self.cuenta_litros_inicial_edit.text()

        # No hay campo para "Litros Final" ahora, así que no lo manejamos aquí

        self.saved_form = RecSavedForm(self, self.db, fecha_hora, cuenta_litros_inicial)
        self.saved_form.show()
        self.close()


class RecSavedForm(QMainWindow):
    def __init__(self, parent, db, fecha_hora, cuenta_litros_inicial):
        super(RecSavedForm, self).__init__(parent)
        self.parent = parent
        self.db = db
        self.fecha_hora = fecha_hora
        self.cuenta_litros_inicial = cuenta_litros_inicial
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Recaudo Guardado')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.folio_label = QLabel('Folio: Será generado al guardar')
        layout.addWidget(self.folio_label)

        self.fecha_hora_label = QLabel(f'Fecha y Hora: {self.fecha_hora}')
        layout.addWidget(self.fecha_hora_label)

        self.litros_inicial_label = QLabel(f'Litros inicial: {self.cuenta_litros_inicial}')
        layout.addWidget(self.litros_inicial_label)

        # Ya no se necesita "Litros Final", así que lo eliminamos

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
            query_folio = "SELECT nextval('folio_seq_dos')"
            self.db.cursor.execute(query_folio)
            folio = self.db.cursor.fetchone()[0]

            # Extraer la hora sin microsegundos
            hora_sin_microsegundos = self.fecha_hora.split(' ')[1]
            hora_formateada = QDateTime.fromString(self.fecha_hora, 'yyyy-MM-dd HH:mm:ss').toString('HH:mm:ss')

            query_insert = """
            INSERT INTO cuenta_litros (folio, fecha, hora, cuenta_litros_inicial)
            VALUES (%s, current_date, %s, %s)
            """
            self.db.cursor.execute(query_insert, (folio, hora_formateada, self.cuenta_litros_inicial))
            self.db.connection.commit()

            QMessageBox.information(self, 'Éxito', 'Recaudo agregado correctamente.', QMessageBox.Ok)
            self.open_historial_diesel_window()  # Abrir la ventana de historial de diesel
            self.close()

        except psycopg2.Error as e:
            self.db.connection.rollback()
            QMessageBox.critical(self, 'Error', f'Error al agregar recaudo: {e}', QMessageBox.Ok)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)

    def edit(self):
        self.close()
        self.parent.show()

    def open_historial_diesel_window(self):
        self.historial_diesel_window = HistorialDieselWindow(self, self.db)
        self.historial_diesel_window.show()
class HistorialDieselWindow(QMainWindow):
    def __init__(self, parent, db):
        super(HistorialDieselWindow, self).__init__(parent)
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Historial de Diesel')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.historial_table = QTableWidget(self)
        self.historial_table.setColumnCount(6)  # Cambiado a 6 para incluir "Litros Final"
        self.historial_table.setHorizontalHeaderLabels(['Folio', 'Fecha', 'Hora', 'Eco', 'Kilometraje', 'Litros Diesel'])
        layout.addWidget(self.historial_table)

        self.eco_label = QLabel('Eco:')
        self.eco_combo = QComboBox(self)
        self.load_eco_options()  # Cargar opciones de eco
        layout.addWidget(self.eco_label)
        layout.addWidget(self.eco_combo)

        self.kilometraje_label = QLabel('Kilometraje:')
        self.kilometraje_edit = QLineEdit(self)
        layout.addWidget(self.kilometraje_label)
        layout.addWidget(self.kilometraje_edit)

        self.litros_diesel_label = QLabel('Litros Diesel:')
        self.litros_diesel_edit = QLineEdit(self)
        layout.addWidget(self.litros_diesel_label)
        layout.addWidget(self.litros_diesel_edit)

        # Agregar el campo de Litros Final
        self.litros_final_label = QLabel('Litros Final:')
        self.litros_final_edit = QLineEdit(self)
        layout.addWidget(self.litros_final_label)
        layout.addWidget(self.litros_final_edit)

        self.add_button = QPushButton('Agregar', self)
        self.add_button.clicked.connect(self.add_historial_entry)
        layout.addWidget(self.add_button)

        self.finalize_button = QPushButton('Finalizar', self)
        self.finalize_button.clicked.connect(self.finalize_entries)
        layout.addWidget(self.finalize_button)

        self.load_historial_data()  # Cargar datos del historial

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def load_eco_options(self):
        try:
            query = """
            SELECT eco
            FROM autobus
            """
            self.db.cursor.execute(query)
            rows = self.db.cursor.fetchall()

            self.eco_combo.addItem("Seleccionar Eco")  # Añadir un item inicial que indique al usuario que seleccione
            for row in rows:
                eco_text = str(row[0])  # Convertir el valor a cadena de texto
                self.eco_combo.addItem(eco_text)

        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar opciones de eco: {e}', QMessageBox.Ok)

    def load_historial_data(self):
        try:
            fecha_actual = QDateTime.currentDateTime().toString('yyyy-MM-dd')
            query = """
            SELECT folio, fecha, hora, eco, kilometraje, litros_diesel
            FROM historial_diesel
            WHERE fecha = %s
            """
            self.db.cursor.execute(query, (fecha_actual,))
            rows = self.db.cursor.fetchall()

            self.historial_table.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                for col_idx, item in enumerate(row):
                    if col_idx == 2:  # La columna de la hora
                        item = item.strftime('%H:%M:%S')  # Formatear hora
                    self.historial_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar historial: {e}', QMessageBox.Ok)

    def add_historial_entry(self):
        try:
            eco = self.eco_combo.currentText()
            kilometraje = self.kilometraje_edit.text()
            litros_diesel = self.litros_diesel_edit.text()

            if not eco or not kilometraje or not litros_diesel:
                QMessageBox.warning(self, 'Advertencia', 'Por favor, complete todos los campos.', QMessageBox.Ok)
                return

            query_insert = """
            INSERT INTO historial_diesel (fecha, eco, kilometraje, litros_diesel)
            VALUES (current_date, %s, %s, %s)
            """
            self.db.cursor.execute(query_insert, (eco, kilometraje, litros_diesel))
            self.db.connection.commit()

            QMessageBox.information(self, 'Éxito', 'Entrada agregada al historial.', QMessageBox.Ok)
            self.load_historial_data()

        except psycopg2.Error as e:
            self.db.connection.rollback()
            QMessageBox.critical(self, 'Error', f'Error al agregar entrada: {e}', QMessageBox.Ok)

    def finalize_entries(self):
        litros_final = self.litros_final_edit.text()
        if not litros_final:
            QMessageBox.warning(self, 'Advertencia', 'El campo Litros Final es obligatorio.', QMessageBox.Ok)
            return

        try:
            fecha_actual = QDateTime.currentDateTime().toString('yyyy-MM-dd')
            query_update = """
            UPDATE cuenta_litros
            SET cuenta_litros_final = %s
            WHERE fecha = %s
            """
            self.db.cursor.execute(query_update, (litros_final, fecha_actual))
            self.db.connection.commit()

            QMessageBox.information(self, 'Éxito', 'Historial de diesel finalizado correctamente.', QMessageBox.Ok)
            self.close()

        except psycopg2.Error as e:
            self.db.connection.rollback()
            QMessageBox.critical(self, 'Error', f'Error al finalizar historial: {e}', QMessageBox.Ok)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
