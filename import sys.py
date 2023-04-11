import sys
import pyperclip
import pytesseract
import keyboard
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
         # Fusion stilini ayarla
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))

        self.setWindowTitle("Ekran Görüntüsü Okuyucu")
        self.setGeometry(200, 200, 300, 200)
        
        # Menü bar oluşturma
        menubar = self.menuBar()
        filemenu = menubar.addMenu("Dosya")
        exit_action = QtWidgets.QAction("Çıkış", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        filemenu.addAction(exit_action)
        
        # Düğmeleri oluştur
        screenshot_button = QPushButton(
            "Ekran Görüntüsü Al (Win+Shift+S)", self, clicked=self.take_screenshot
        )
        read_button = QPushButton(
            "Metni Oku ve Kopyala", self, clicked=self.copy_text
        )
        read_button.setObjectName("read_button")
        # Etiketleri oluştur
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap("default_image.png"))
        self.text_label = QLabel(self)
        self.text_label.setWordWrap(True)

        # Dikey düzenleyici oluştur
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(screenshot_button)
        vbox.addWidget(read_button)
        vbox.addWidget(self.text_label)
        vbox.setSpacing(20)
        vbox.setContentsMargins(30, 30, 30, 30)
        
        # Merkezdeki widget'ı ayarla
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
        # Stil yapısını oluşturma
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f2f2f2;
            }
            QPushButton#screenshot_button {
                color: white;
                background-color: #009999;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton#screenshot_button:hover {
                background-color: #33cccc;
            }
            QPushButton#read_button {
                color: white;
                background-color: #ff9933;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton#read_button:hover {
                background-color: #ffad33;
            }
            QLabel {
                font-size: 16px;
            }
        """)
    def take_screenshot(self):
        # Win+Shift+S tuş kombinasyonunu kullanarak ekran görüntüsü al
        keyboard.press_and_release('win+shift+s')
        
    def copy_text(self):
        # Ekran görüntüsü al ve metni oku
        image = QGuiApplication.clipboard().pixmap()
        if not image.isNull():
            # Resmi işle
            image.save("temp.png", "png")
            text = pytesseract.image_to_string("temp.png", lang="tur+eng")
            # Metni düzelt
            text = self.correct_text(text)
            # Metni etikete yaz
            self.text_label.setText(text)
            # Metni panoya kopyala
            pyperclip.copy(text)
    
    def correct_text(self, text):
        # Türkçe karakterlerin düzeltilmesi
        text = text.replace("ı", "i")
        text = text.replace("İ", "I")
        text = text.replace("ö", "o")
        text = text.replace("Ö", "O")
        text = text.replace("ü", "u")
        text = text.replace("Ü", "U")
        text = text.replace("ş", "s")
        text = text.replace("Ş", "S")
        text = text.replace("ç", "c")
        text = text.replace("Ç", "C")
        return text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
