import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QComboBox, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QTransform
from PyQt5.QtCore import QTimer, Qt
import serial.tools.list_ports
from PyQt5.QtGui import QIcon

class RotatableLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._pixmap = pixmap
        self.setAlignment(Qt.AlignCenter)
        self.updatePixmap()

    def updatePixmap(self):
        transform = QTransform().rotate(self._angle)
        self._rotated_pixmap = self._pixmap.transformed(transform)
        self.setPixmap(self._rotated_pixmap)

    def rotation(self):
        return self._angle

    def setRotation(self, angle):
        self._angle = angle % 360  # Mantém o ângulo entre 0 e 359 graus
        self.updatePixmap()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Giroscópio Serial')
        self.setFixedSize(500, 500)  # Define um tamanho fixo para a janela

        # Widget principal para o layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Layout principal
        main_layout = QVBoxLayout(main_widget)

        # Layout horizontal para combobox e botão
        hbox_layout = QHBoxLayout()

        # Combobox para escolher a porta serial
        self.port_combobox = QComboBox()
        self.populate_ports()
        hbox_layout.addWidget(self.port_combobox)

        # Botão para iniciar a conexão
        self.connect_button = QPushButton('Conectar')
        self.connect_button.clicked.connect(self.connect_serial)
        hbox_layout.addWidget(self.connect_button)

        # Adicionar o layout horizontal ao layout principal
        main_layout.addLayout(hbox_layout)

        # Carrega a imagem PNG da seta
        self.original_pixmap = QPixmap('image1.png')
        if self.original_pixmap.isNull():
            print("Erro ao carregar o pixmap.")
            return
        self.setWindowIcon(QIcon('icone.ico'))

        self.arrow_image = RotatableLabel(self.original_pixmap, self)
        main_layout.addWidget(self.arrow_image)  # Adicionando a imagem ao layout

        self.serial_port = None  # Inicialmente, nenhuma porta está aberta

        self.text_label = QLabel(self)
        self.text_label.setGeometry(50, 460, 400, 30)  # Posição ajustada para o texto
        main_layout.addWidget(self.text_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_angle)
        self.timer.start(2)

    def populate_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combobox.addItems(ports)

    def connect_serial(self):
        port_name = self.port_combobox.currentText()
        if self.serial_port is None or not self.serial_port.is_open:
            self.serial_port = serial.Serial(port_name, 115200)
            print(f"Conectado à porta {port_name}")

    def update_angle(self):
        if self.serial_port and self.serial_port.in_waiting:
            line = self.serial_port.readline().decode('latin1', errors='ignore').strip()
            self.text_label.setText(f'{line}')

            if 'Direita' in line:
                self.rotate_image(20)
            elif 'Esquerda' in line:
                self.rotate_image(-20)
            else:
                self.rotate_image(0)

    def rotate_image(self, angle):
        current_angle = self.arrow_image.rotation()
        self.arrow_image.setRotation(angle)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
