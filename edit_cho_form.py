from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QFormLayout, QLineEdit, QDateEdit, QMessageBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QDate
import psycopg2
import sys

class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="tu_db",
            user="tu_usuario",
            password="tu_contraseña",
            host="localhost"
        )
        self.cursor = self.connection.cursor()

class EditChoForm(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Lista de Choferes")
        self.resize(350, 350)

        self.layout = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.layout.addWidget(self.list_widget)

        self.load_data_btn = QPushButton('Cargar Datos', self)
        self.load_data_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_btn)

        self.setLayout(self.layout)

    def load_data(self):
        try:
            query = """
            SELECT e.id_chofer, e.nombre, e.apellido_paterno, e.apellido_materno, a.apodo
            FROM empleado_chofer e
            LEFT JOIN apodos a ON e.id_chofer = a.id_chofer
            """
            self.db.cursor.execute(query)
            rows = self.db.cursor.fetchall()

            self.list_widget.clear()
            for row in rows:
                item_widget = QWidget()
                item_layout = QHBoxLayout()
                item_layout.setContentsMargins(0, 0, 0, 0)
                
                item_text = f"{row[0]} - {row[1]} {row[2]} {row[3]}"
                if row[4]:
                    item_text += f" - \"<span style='color:red;'>{row[4]}</span>\""
                
                item_label = QLabel(item_text)
                item_label.setFixedHeight(25)
                item_label.setTextFormat(Qt.RichText)  # Para que el QLabel interprete el HTML

                edit_btn = QPushButton("Editar")
                edit_btn.setStyleSheet("background-color: rgb(255, 165, 0);")
                edit_btn.setFixedSize(50, 16)
                edit_btn.clicked.connect(lambda ch, row=row: self.edit_item(row[0]))
                
                item_layout.addWidget(item_label)
                item_layout.addWidget(edit_btn)
                
                item_widget.setLayout(item_layout)
                
                list_item = QListWidgetItem(self.list_widget)
                list_item.setSizeHint(item_widget.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)
                
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)

    def edit_item(self, item_id):
        self.edit_window = EditWindow(self.db, item_id)
        self.edit_window.show()

class EditWindow(QWidget):
    def __init__(self, db, item_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.item_id = item_id
        self.setWindowTitle("Editar Chofer")
        
        self.layout = QFormLayout()
        
        self.nombre = QLineEdit(self)
        self.layout.addRow('Nombre:', self.nombre)

        self.apellido_paterno = QLineEdit(self)
        self.layout.addRow('Apellido Paterno:', self.apellido_paterno)

        self.apellido_materno = QLineEdit(self)
        self.layout.addRow('Apellido Materno:', self.apellido_materno)

        self.rfc = QLineEdit(self)
        self.layout.addRow('RFC:', self.rfc)

        self.nss = QLineEdit(self)
        self.layout.addRow('NSS:', self.nss)

        self.curp = QLineEdit(self)
        self.layout.addRow('CURP:', self.curp)

        self.salario_base = QLineEdit(self)
        self.layout.addRow('Salario Base:', self.salario_base)

        self.tipo_jornada = QLineEdit(self)
        self.layout.addRow('Tipo de Jornada:', self.tipo_jornada)

        self.fecha_vencimiento_tarjeton = QDateEdit(self)
        self.fecha_vencimiento_tarjeton.setCalendarPopup(True)
        self.layout.addRow('Fecha de Vencimiento del Tarjeton:', self.fecha_vencimiento_tarjeton)

        self.apodo = QLineEdit(self)
        self.layout.addRow('Apodo:', self.apodo)

        self.update_btn = QPushButton('Actualizar Datos', self)
        self.update_btn.clicked.connect(self.update_data)
        self.layout.addWidget(self.update_btn)

        self.setLayout(self.layout)

        self.load_data()

    def load_data(self):
        try:
            query = """
            SELECT e.nombre, e.apellido_paterno, e.apellido_materno, e.rfc, e.nss, e.curp, e.salario_base, e.tipo_jornada, e.fecha_vencimiento_tarjeton, a.apodo
            FROM empleado_chofer e
            LEFT JOIN apodos a ON e.id_chofer = a.id_chofer
            WHERE e.id_chofer = %s
            """
            self.db.cursor.execute(query, (self.item_id,))
            row = self.db.cursor.fetchone()

            if row:
                self.nombre.setText(row[0])
                self.apellido_paterno.setText(row[1])
                self.apellido_materno.setText(row[2])
                self.rfc.setText(row[3])
                self.nss.setText(row[4])
                self.curp.setText(row[5])
                self.salario_base.setText(str(row[6]))  # Convertir decimal a string
                self.tipo_jornada.setText(row[7])
                self.fecha_vencimiento_tarjeton.setDate(QDate.fromString(str(row[8]), 'yyyy-MM-dd'))
                self.apodo.setText(row[9] if row[9] else "")
            else:
                QMessageBox.warning(self, 'Error', 'No se encontró el chofer con el ID proporcionado', QMessageBox.Ok)
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudieron cargar los datos: {e}', QMessageBox.Ok)

    def update_data(self):
        try:
            nombre = self.nombre.text()
            apellido_paterno = self.apellido_paterno.text()
            apellido_materno = self.apellido_materno.text()
            rfc = self.rfc.text()
            nss = self.nss.text()
            curp = self.curp.text()
            salario_base = self.salario_base.text()
            tipo_jornada = self.tipo_jornada.text()
            fecha_vencimiento_tarjeton = self.fecha_vencimiento_tarjeton.date().toString('yyyy-MM-dd')
            apodo = self.apodo.text()

            if not all([nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton]):
                QMessageBox.critical(self, 'Error', 'Todos los campos deben estar llenos', QMessageBox.Ok)
                return

            query = """
            UPDATE empleado_chofer
            SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, rfc = %s, nss = %s, curp = %s, salario_base = %s, tipo_jornada = %s, fecha_vencimiento_tarjeton = %s
            WHERE id_chofer = %s
            """
            self.db.cursor.execute(query, (nombre, apellido_paterno, apellido_materno, rfc, nss, curp, salario_base, tipo_jornada, fecha_vencimiento_tarjeton, self.item_id))
            
            # Actualizar o insertar apodo en la tabla apodos
            query_apodo = """
            INSERT INTO apodos (id_chofer, apodo)
            VALUES (%s, %s)
            ON CONFLICT (id_chofer)
            DO UPDATE SET apodo = %s
            """
            self.db.cursor.execute(query_apodo, (self.item_id, apodo, apodo))

            self.db.connection.commit()
            QMessageBox.information(self, 'Éxito', 'Datos actualizados correctamente', QMessageBox.Ok)
            self.close()
        except psycopg2.Error as e:
            self.db.connection.rollback()
            print(f"Error durante la actualización del query: {e}")
            QMessageBox.critical(self, 'Error', f'No se pudo actualizar el chofer: {e}', QMessageBox.Ok)
        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.critical(self, 'Error', f'Error inesperado: {e}', QMessageBox.Ok)
