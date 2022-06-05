import json, sys, inspect

from PyQt5.QtCore import QRegExp

import manage_files, main_window
from collections import Counter
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication, QLineEdit, QLabel, QTextEdit, QMainWindow, QFileDialog,
                             QCheckBox, QComboBox, QMessageBox)


class ManageDefaults:
    def __init__(self, file, defaults_dict):
        self.file = file
        self.defaults_dict = defaults_dict

    def create_file(self):
        mw = main_window.MainWidget()
        mw.textarea_txt = self.read_file()
        self.save_file()

    def save_file(self):
        with open(self.file, "w") as wf:
            wf.write(json.dumps(self.defaults_dict))


class EditVars(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 200)

        mf = manage_files.DefaultLocations()
        self.defaults_dict = mf.check_defaults_file()

        self.widgets = []
        for key in self.defaults_dict:
            self.widgets.append(QLabel(key))
            line_object = QLineEdit(self.defaults_dict[key])
            self.widgets.append(line_object)
            line_object.setObjectName(key + "_text")

    def save(self):
        # get values
        for i in self.defaults_dict:
            child = self.findChild(QLineEdit, f"{i}_text")
            self.defaults_dict[i] = child.text()

        mf = manage_files.DefaultLocations()
        md = ManageDefaults(file=mf.file, defaults_dict=self.defaults_dict)
        md.save_file()

    def create_ui(self):
        # get form items

        buttons = [QPushButton("close"), QPushButton("save")]
        buttons[0].clicked.connect(QApplication.instance().quit)
        buttons[1].clicked.connect(lambda: self.save())

        grid = QGridLayout()
        self.setLayout(grid)

        count = 0
        x_axis = 0
        max_col_size = 2
        max_rows = int(len(self.widgets) + len(buttons) / max_col_size)

        positions = [(i, j) for i in range(max_rows) for j in range(max_col_size)]
        for position, name in zip(positions, self.widgets):
            if name == '':
                continue
            grid.addWidget(name, *position, 1, max_col_size)
            x_axis = position[0] + 1

        positions2 = [(h, k) for h in range(x_axis, x_axis + (max_rows - x_axis)) for k in range(max_col_size)]
        for position2, name2 in zip(positions2, buttons[count:]):
            if name2 == '':
                continue
            grid.addWidget(name2, *position2)
            x_axis = x_axis + 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EditVars()
    ex.create_ui()
    ex.show()
    sys.exit(app.exec_())
