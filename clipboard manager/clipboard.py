import pyperclip
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QLabel, QVBoxLayout, QWidget,
    QComboBox, QSlider
) 


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # set window title
        self.setWindowTitle("Clipboard Manager")
        # set window size
        self.resize(QSize(400, 200))

        # initialise memory to store clipboard
        self.clip_memory = list()
        self.max_memory_length = 0

        # create a combo box
        self.clip_combo = QComboBox()

        # create a button
        self.copy_to_clip_button = QPushButton("Copy to clipboard")
        self.copy_to_clip_button.clicked.connect(self.copy_to_clipboard)

        # create a label that shows the recently copied text (from button click)
        self.copied_label = QLabel()

        # create a label which shows the max clipboard memory
        self.memory_start = "Max clipboard memory:"
        self.memory_label = QLabel(f"{self.memory_start} {self.max_memory_length}")

        # create a slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(32)
        # set the ticks to appear above the slider
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        # when the slider's value changes, update the memory label
        self.slider.valueChanged.connect(self.update_memory_label)
        self.update_memory_label()

        # put the items to be added to the layout in a list to be iterated through
        qItems = [
            self.clip_combo,
            self.copy_to_clip_button,
            self.copied_label,
            self.memory_label,
            self.slider
        ]

        # create a vertical box layout
        layout = QVBoxLayout()
        # add each item to the layout
        for qItem in qItems:
            layout.addWidget(qItem)

        # create a QWidget and set its layout to layout
        container = QWidget()
        container.setLayout(layout)

        # set the central widget to the container
        self.setCentralWidget(container)

    def new_copy(self, clipboard):
        text = clipboard.text()
        self.enqueue(text)
        # while loop used just in case the memory limit was decreased
        while len(self.clip_memory) > self.max_memory_length and self.max_memory_length != 0:
            self.dequeue()

    def enqueue(self, text):
        # insert text at the start of memory
        self.clip_memory.insert(0,text)
        # clear the combo table
        self.clip_combo.clear()
        # replace with the clip memory
        self.clip_combo.addItems(self.clip_memory)
    
    def dequeue(self):
        tmp = self.clip_memory[-1]
        del self.clip_memory[-1]
        self.clip_combo.clear()
        self.clip_combo.addItems(self.clip_memory)
        return tmp

    def copy_to_clipboard(self):

        tmp = self.clip_memory
        pyperclip.copy(self.clip_combo.currentText())
        # this copy is detected and is added to the list
        # next lines restore the previous clip_memory
        self.clip_combo.clear()
        self.clip_memory = tmp
        self.clip_combo.addItems(self.clip_memory)
        # show message that text was successfully copied
        self.copied_label.setText(f"Successfully copied text: {self.clip_combo.currentText()}")

    def update_memory_label(self):
        self.max_memory_length = self.slider.value()
        if self.max_memory_length == 0:
            val = "No limit"
        else:
            val = self.max_memory_length
        self.memory_label.setText(f"{self.memory_start} {val}")


def main():
    app = QApplication([])
    window = MainWindow()
    clipboard = app.clipboard()
    clipboard.dataChanged.connect(lambda: window.new_copy(clipboard))
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
