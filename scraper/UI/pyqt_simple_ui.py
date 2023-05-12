import asyncio
import sys
import os
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget

from ..bot.bot import dp


class BotUI(QWidget):
    class BotPolling(QThread):
        def __init__(self):
            super().__init__()

        @staticmethod
        async def bot_poll():
            # Здесь выполняется долгая операция, которая может блокировать основной поток
            # Например, скачивание большого файла или обработка большого объема данных
            await dp.start_polling()  # имитация долгой операции

        @classmethod
        def run(cls):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(cls.bot_poll())
            loop.close()

    def __init__(self):
        # Call parent constructor
        super().__init__()

        # Set background image
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap(f"jpg/background.jpg")
        # self.background_pixmap = QPixmap(f"{os.path.dirname(os.path.abspath(__file__))}/jpg/background.jpg")
        self.background_label.setPixmap(self.background_pixmap)

        # Define label at the top of the button
        self.topLabel = QLabel('<h2 style="color: white;">Coinmarketcap parser</h2>', self)
        # Set the geometry of the label
        self.topLabel.setGeometry(52, 10, 290, 50)
        self.topLabel.setAlignment(Qt.AlignCenter)

        # Set fixed size of the window and background
        self.setFixedSize(400, 200)
        # self.background_label.setFixedSize(400, 200)

        # Create the first button
        self.bot_start_button = QPushButton('Запустить бота', self)
        # Set the geometry of the button
        self.bot_start_button.setGeometry(100, 70, 200, 40)
        # Call function when the button is clicked
        self.bot_start_button.clicked.connect(self.bot_start_button_on_click)

        self.bot_start_button.setStyleSheet('''
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #FFFFFF, stop: 1 #CCCCCC);
                border-style: solid;
                border-radius: 10px;
                border-width: 2px;
                border-color: #888888;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #EEEEEE, stop: 1 #CCCCCC);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #CCCCCC, stop: 1 #EEEEEE);
            }
        ''')

        # # Field for the token
        # self.input_field = QLineEdit(self)
        # # self.input_field.setFixedSize(200, 30)
        # self.input_field.setStyleSheet("""
        #             QLineEdit {
        #                 border-radius: 5px;
        #                 background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        #                                                   stop:0 #FFFFFF, stop:1 #ECECEC);
        #                 color: #333333;
        #                 font-size: 14px;
        #                 font-family: Arial;
        #                 padding: 5px;
        #             }
        #         """)
        # # self.input_field.setGeometry(50, 120, 200, 30)
        # self.input_field.editingFinished.connect(self.on_input_finished)

        # Define label at the bottom of the button
        self.msgLabel = QLabel('', self)
        # Set the geometry of the label
        self.msgLabel.setGeometry(50, 120, 300, 80)
        self.msgLabel.setAlignment(Qt.AlignCenter)

        # Set the title of the window
        self.setWindowTitle('Parser')
        # Set the geometry of the main window
        self.setGeometry(10, 10, 400, 200)

        # Set the position of the main window in the screen
        self.move(800, 350)

        # Create second thread object to poll messages from bot
        self.msgThread = BotUI.BotPolling()

    def bot_start_button_on_click(self):
        # Set text for the bottom label
        self.msgLabel.setText('<h4 style="color: white;">Бот успешно запущен<p>'
                              'Для его остановки закройте это окно</h4>')
        # self.msgThread.finished.connect(self.show_debug_console)
        self.bot_start_button.setEnabled(False)
        self.msgThread.start()

    # def on_input_finished(self):
    #     # Получаем текст, введенный пользователем в поле ввода
    #     input_text = self.input_field.text()
    #
    #     # Обработка введенного текста
    #     print(f"Введенный текст: {input_text}")


def activate_gui():
    if sys.platform == 'linux':
        os.environ["QT_QPA_PLATFORM"] = "wayland"
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(f"jpg/icon.jpg"))
    # app.setWindowIcon(QtGui.QIcon(f"{os.path.dirname(os.path.abspath(__file__))}/jpg/icon.jpg"))
    bot_ui = BotUI()
    bot_ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    activate_gui()
