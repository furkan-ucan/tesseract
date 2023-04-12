import sys
import pyperclip
import pytesseract
import keyboard
import nltk

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QPlainTextEdit
from PyQt5 import QtWidgets



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ekran Görüntüsü Okuyucu")
        self.setGeometry(200, 200, 500, 400)

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
        # Etiketleri oluştur
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap("default_image.png"))
        self.text_edit = QPlainTextEdit(self)

        # Dikey düzenleyici oluştur
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(screenshot_button)
        vbox.addWidget(read_button)
        vbox.addWidget(self.text_edit)
        vbox.setSpacing(20)
        vbox.setContentsMargins(30, 30, 30, 30)

        # Merkezdeki widget'ı ayarla
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def take_screenshot(self):
        # Win+Shift+S tuş kombinasyonunu kullanarak ekran görüntüsü al
        keyboard.press_and_release('win+shift+s')

    def copy_text(self):
        try:
            # Ekran görüntüsü al ve metni oku
            image = QGuiApplication.clipboard().pixmap()
            if not image.isNull():
                # Resmi işle
                image.save("temp.png", "png")
                text = pytesseract.image_to_string("temp.png", lang="tur+eng")
                # Metni düzenleyicide göster
                self.text_edit.setPlainText(text)
                # Metni kopyala
                pyperclip.copy(text)

                # Metni işleme
                self.process_text(text)
        except Exception as e:
            self.statusBar().showMessage(f"Hata oluştu: {e}")

    def process_text(self, text):
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        nouns = [word for (word, pos) in tagged if pos.startswith('N')]
        verbs = [word for (word, pos) in tagged if pos.startswith('V')]

        # Nouns ve verbs listelerini statusBar() üzerinde göster
        nouns_str = ", ".join(nouns)
        verbs_str = ", ".join(verbs)
        self.statusBar().showMessage(f"İsimler: {nouns_str}. Fiiller: {verbs_str}.")

        # Nouns ve verbs listelerini göster
        print("Nouns: ", nouns)
        print("Verbs: ", verbs)
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
