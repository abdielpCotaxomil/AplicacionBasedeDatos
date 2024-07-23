from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
import psycopg2

class InfoRec(QMainWindow):
    def __init__(self, db):
        super(InfoRec, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Información de Recaudos')
        self.setGeometry(200, 200, 800, 600)

        # Tabla para mostrar la información detallada de recaudos
        self.recaudo_table = QTableWidget()
        self.recaudo_table.setColumnCount(8)
        self.recaudo_table.setHorizontalHeaderLabels(
            ['Folio', 'Fecha', 'Hora', 'Eco', 'ID Chofer 1', 'ID Chofer 2', 'Monedas', 'Billetes'])
        header = self.recaudo_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.recaudo_table)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.load_data()

    def load_data(self):
        try:
            query = "SELECT folio, fecha, hora, eco, id_chofer1, id_chofer2, monedas, billetes FROM historial_recaudo"
            self.db.cursor.execute(query)
            recaudos = self.db.cursor.fetchall()

            self.recaudo_table.setRowCount(len(recaudos))

            for i, recaudo in enumerate(recaudos):
                for j, item in enumerate(recaudo):
                    self.recaudo_table.setItem(i, j, QTableWidgetItem(str(item)))

        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar recaudos: {e}', QMessageBox.Ok)
