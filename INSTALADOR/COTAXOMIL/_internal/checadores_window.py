from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QInputDialog, QMessageBox
from forms import JornadaEntradaForm, JornadaSalidaForm, InfoForm

class ChecadoresWindow(QWidget):
    def __init__(self, db):
        super(ChecadoresWindow, self).__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Checadores')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        iniciar_jornada_btn = QPushButton('Iniciar Jornada', self)
        iniciar_jornada_btn.clicked.connect(self.iniciar_jornada)
        layout.addWidget(iniciar_jornada_btn)

        terminar_jornada_btn = QPushButton('Terminar Jornada', self)
        terminar_jornada_btn.clicked.connect(self.terminar_jornada)
        layout.addWidget(terminar_jornada_btn)

        ver_info_btn = QPushButton('Ver Información', self)
        ver_info_btn.clicked.connect(self.ver_informacion)
        layout.addWidget(ver_info_btn)

        self.setLayout(layout)

    def iniciar_jornada(self):
        self.jornadaEntradaForm = JornadaEntradaForm(self.db)
        self.jornadaEntradaForm.show()

    def terminar_jornada(self):
        folio, ok = QInputDialog.getInt(self, 'Terminar Jornada', 'Ingrese el folio:')
        if ok:
            self.jornadaSalidaForm = JornadaSalidaForm(self.db, folio)
            self.jornadaSalidaForm.show()

    def ver_informacion(self):
        self.infoForm = InfoForm(self.db)
        self.infoForm.show()
