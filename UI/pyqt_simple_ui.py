import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QLinearGradient
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class BotUI(QWidget):
    def __init__(self):
        super().__init__()

        # Задаём размеры и заголовок окна
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Мой бот')

        # Задаём фоновое изображение
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap('background.jpg')
        self.background_label.setPixmap(self.background_pixmap)

        # Задаём кнопку "Запустить бота"
        self.start_button = QPushButton('Запустить бота', self)
        self.start_button.setGeometry(150, 125, 200, 100)
        self.start_button.clicked.connect(self.run_bot)

        # Добавляем стиль для кнопки
        self.start_button.setStyleSheet('''
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #FFFFFF, stop: 1 #CCCCCC);
                border-style: solid;
                border-radius: 10px;
                border-width: 2px;
                border-color: #888888;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #EEEEEE, stop: 1 #CCCCCC);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #CCCCCC, stop: 1 #EEEEEE);
            }
        ''')

        # Устанавливаем фиксированный размер для окна и лейбла с фоновым изображением
        self.setFixedSize(400, 300)
        self.background_label.setFixedSize(400, 300)

        # Задаём политику масштабирования для фонового изображения и лейбла с фоном
        self.background_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Создаём вертикальный лэйаут и добавляем в него виджеты
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.background_label)
        self.layout.addWidget(self.start_button)

        # Задаём лэйаут для виджета
        self.setLayout(self.layout)

    def run_bot(self):
        # Функция, которая будет вызываться при нажатии на кнопку "Запустить бота"
        print('Бот запущен!')

if __name__ == '__main__':
    class MultiButtons(QWidget):

        def __init__(self):
            # Call parent constructor
            super().__init__()

            # Define label at the top of the button
            self.topLabel = QLabel('<h2>Do you like python?</h2>', self)
            # Set the geometry of the label
            self.topLabel.setGeometry(100, 20, 290, 50)

            # Create the first button
            self.btn1 = QPushButton('Yes', self)
            # Set the geometry of the button
            self.btn1.setGeometry(130, 70, 60, 40)
            # Call function when the button is clicked
            self.btn1.clicked.connect(self.btn1_onClicked)

            # Create the second button
            self.btn2 = QPushButton('No', self)
            # Set the geometry of the button
            self.btn2.setGeometry(200, 70, 60, 40)
            # Call function when the button is clicked
            self.btn2.clicked.connect(self.btn2_onClicked)

            # Define label at the bottom of the button
            self.msgLabel = QLabel('', self)
            # Set the geometry of the label
            self.msgLabel.setGeometry(130, 120, 300, 80)

            # Set the title of the window
            self.setWindowTitle('Use of multiple PushButtons')
            # Set the geometry of the main window
            self.setGeometry(10, 10, 400, 200)

            # Set the position of the main window in the screen
            self.move(850, 300)
            # Display the window
            self.show()

        def btn1_onClicked(self):
            # Set text for the bottom label
            self.msgLabel.setText('<h3>You clicked Yes.</h3>')



    # Create app object and execute the app
    app = QApplication(sys.argv)
    button = MultiButtons()
    app.exec()
