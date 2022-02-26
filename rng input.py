import random

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dice app")
        self.setFixedSize(QSize(210, 300))

        self.num_label_start = "Number generated: "
        self.number_label = QLabel()

        self.button = QPushButton("Generate a number!")
        self.button.clicked.connect(self.generate_number)

        self.default_min, self.default_max = self.min, self.max = 1, 10
        self.min_head = QLabel("Set minimum:")
        self.min_input = QLineEdit()
        self.min_start = "Minimum: "
        self.min_confirm = QPushButton("Set minimum")
        self.min_confirm.setEnabled(False)
        self.min_confirm.clicked.connect(lambda: self.set_minimum(self.min_input.text()))
        self.min_label = QLabel(f"{self.min_start}{self.min}")

        self.max_head = QLabel("Set maximum:")
        self.max_input = QLineEdit()
        self.max_start = "Maximum: "
        self.max_confirm = QPushButton("Set maximum")
        self.max_confirm.setEnabled(False)
        self.max_confirm.clicked.connect(lambda: self.set_maximum(self.max_input.text()))
        self.max_label = QLabel(f"{self.max_start}{self.max}")

        self.min_input.textChanged.connect(lambda: self.valid_input(self.min_input.text(), self.min_confirm))
        self.max_input.textChanged.connect(lambda: self.valid_input(self.max_input.text(), self.max_confirm))

        self.reset_button = QPushButton("Reset values")
        self.reset_button.clicked.connect(self.reset_values)

        objects = [
            self.number_label,
            self.button,
            self.min_head,
            self.min_input,
            self.min_label,
            self.min_confirm,
            self.max_head,
            self.max_input,
            self.max_label,
            self.max_confirm,
            self.reset_button
        ]

        layout = QVBoxLayout()
        for item in objects:
            layout.addWidget(item)
        
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def generate_number(self):
        self.number = random.randint(self.min, self.max)
        self.number_label.setText(f"{self.num_label_start}{self.number:,d}")

    def set_minimum(self, num):
        self.min = int(num)
        self.min_label.setText(f"{self.min_start}{self.min:,d}")
        self.min_input.clear()
        self.verify_min_max_values()
    
    def set_maximum(self, num):
        self.max = int(num)
        self.max_label.setText(f"{self.max_start}{self.max:,d}")
        self.max_input.clear()
        self.verify_min_max_values()

    def verify_min_max_values(self):
        if self.min < self.max:
            self.button.setText("Generate a number!")
            self.button.setEnabled(True)
            return
        self.button.setText("Minimum is larger than maximum.")
        self.button.setEnabled(False)

    def valid_input(self, text, button):
        try:
            int(text)
            button.setEnabled(True)
        except Exception as e:
            button.setEnabled(False)

    def reset_values(self):
        self.set_minimum(self.default_min)
        self.set_maximum(self.default_max)
        


app = QApplication([])
window = MainWindow()
window.show()
app.exec()