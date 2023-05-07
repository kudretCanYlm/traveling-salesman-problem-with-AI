import sys
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyqtgraph import *
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from aco import ACO, Graph
import math
import operator

class mainWidget(QWidget):
    def __init__(self, parent=None):
        super(mainWidget, self).__init__(parent)

        # setting title
        self.setWindowTitle(
            "Ant Colony Optimization for the Traveling Salesman Problem")

        # font family
        font = QFont()
        font.setFamily("Arial")
        self.setFont(font)

        # layouts
        left_label_layout = QVBoxLayout()

        right_input_layout = QVBoxLayout()
        label_input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        main_input_layout = QVBoxLayout()

        chart_layout = QVBoxLayout()

        main_layout = QGridLayout()

        # labels

        path_x_inputs_label = QLabel()
        path_x_inputs_label.setText("Paths x (use ',' for the per x value): ")
        path_x_inputs_label.setStyleSheet("font-size:18px")
        path_x_inputs_label.setAlignment(QtCore.Qt.AlignRight)
        left_label_layout.addWidget(path_x_inputs_label)

        path_y_inputs_label = QLabel()
        path_y_inputs_label.setText("Paths y (use ',' for the per y value): ")
        path_y_inputs_label.setStyleSheet("font-size:18px")
        path_y_inputs_label.setAlignment(QtCore.Qt.AlignRight)
        left_label_layout.addWidget(path_y_inputs_label)

        path_result_label = QLabel()
        path_result_label.setStyleSheet("font-size:18px")
        path_result_label.setScaledContents(True)
        path_result_label.setAlignment(QtCore.Qt.AlignCenter)
        path_result_label.setObjectName("path_result_label")

        # Text Boxes

        path_x_inputs_textbox = QLineEdit()
        path_x_inputs_textbox.setObjectName("path_x_inputs_textbox")
        path_x_inputs_textbox.setStyleSheet(
            "padding:5px 5px;border:none;border-radius:10px;font-size:16px")
        right_input_layout.addWidget(path_x_inputs_textbox)

        path_y_inputs_textbox = QLineEdit()
        path_y_inputs_textbox.setObjectName("path_y_inputs_textbox")
        path_y_inputs_textbox.setStyleSheet(
            "padding:5px 5px;border:none;border-radius:10px;font-size:16px")
        right_input_layout.addWidget(path_y_inputs_textbox)

        # Buttons

        draw_points_button = QPushButton("Draw Points")
        draw_points_button.setObjectName("draw_points_button")
        draw_points_button.setStyleSheet(
            "outline:none;background-color:green;padding:5px 5px;border:none;border-radius:10px;font-size:16px;color:white")
        draw_points_button.clicked.connect(self.on_click_draw_points)
        draw_points_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_layout.addWidget(draw_points_button)

        draw_ways_button = QPushButton("Draw Ways")
        draw_ways_button.setObjectName("draw_ways_button")
        draw_ways_button.setStyleSheet(
            "outline:none;background-color:green;padding:5px 5px;border:none;border-radius:10px;font-size:16px;color:white")
        draw_ways_button.clicked.connect(self.on_click_draw_ways_button)
        draw_ways_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_layout.addWidget(draw_ways_button)

        # Charts

        self.points_figure = plt.figure()
        points_chart = FigureCanvas(self.points_figure)
        points_toolbar = NavigationToolbar(points_chart, self)
        points_chart.setObjectName("points_chart")
        chart_layout.addWidget(points_toolbar)
        chart_layout.addWidget(points_chart)

        # message box
        self.msg_error = QMessageBox()
        self.msg_error.setObjectName("msg_error")
        self.msg_error.setIcon(QMessageBox.Warning)

        self.msg_error.setWindowTitle("Warning")

        # Options

        label_input_layout.addLayout(left_label_layout)
        label_input_layout.addLayout(right_input_layout)
        main_input_layout.addLayout(label_input_layout)
        main_input_layout.addLayout(button_layout)

        main_layout.addLayout(main_input_layout, 0, 0, 1, 2)
        main_layout.addWidget(path_result_label, 1, 0, 1, 2)
        main_layout.addLayout(chart_layout, 2, 0, 1, 2)

        main_layout.setRowStretch(0, 5)
        main_layout.setRowStretch(1, 2)
        main_layout.setRowStretch(2, 13)
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)

        # Self options
        self.setLayout(main_layout)

    @pyqtSlot()
    def on_click_draw_ways_button(self):

        path_x_inputs = list(map(int, self.findChild(
            QLineEdit, "path_x_inputs_textbox").text().split(",")))
        path_y_inputs = list(map(int, self.findChild(
            QLineEdit, "path_y_inputs_textbox").text().split(",")))

        self.findChild(QPushButton, "draw_ways_button").setStyleSheet(
                "outline:none;background-color:red;padding:5px 5px;border:none;border-radius:10px;font-size:16px;color:white")

        if(path_x_inputs.__len__() != path_y_inputs.__len__()):
            self.msg_error.setText(
                "Paths x array and paths y array must be equal")
            self.msg_error.show()

        def draw_ways():

                cities = []
                points = []
                point_len = path_x_inputs.__len__()

                def distance(city1: dict, city2: dict):
                    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)

                for i in range(point_len):
                    cities.append(dict(index=int(i), x=int(
                        path_x_inputs[i]), y=int(path_y_inputs[i])))
                    points.append(
                        (int(path_x_inputs[i]), int(path_y_inputs[i])))

                cost_matrix = []
                rank = len(cities)
                for i in range(rank):
                    row = []
                    for j in range(rank):
                        row.append(distance(cities[i], cities[j]))
                    cost_matrix.append(row)
                aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
                graph = Graph(cost_matrix, rank)
                path, cost = aco.solve(graph)

                # set path text
                print('cost: {}, path: {}'.format(cost, path))

                def plot(points, path: list):
                    x = []
                    y = []

                    for point in points:
                        x.append(point[0])
                        y.append(point[1])

                    # clearing old figure
                    self.points_figure.clear()

                    # create an axis
                    ax = self.points_figure.add_subplot(111)

                    # noinspection PyUnusedLocal
                    y = list(map(operator.sub, [max(y)
                             for i in range(len(points))], y))
                    ax.plot(x, y, 'co')

                    for _ in range(1, len(path)):

                        i = path[_ - 1]
                        j = path[_]
                        # noinspection PyUnresolvedReferences
                        ax.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i],
                                 color='r', length_includes_head=True)

                    for i in range(x.__len__()):
                        ax.text(x[i], y[i], str(i), fontsize=16,
                                bbox=dict(facecolor='red', alpha=1))

                    # set text path
                    self.findChild(QLabel,"path_result_label").setText( str([ str(test)+" > " for test in path]))

                    # noinspection PyTypeChecker
                    ax.set_xlim(0, max(x) * 1.1)

                    # noinspection PyTypeChecker
                    ax.set_ylim(0, max(y) * 1.1)

                    # refresh canvas
                    self.findChild(FigureCanvas, "points_chart").draw()

                # distance
                plot(points, path)

                self.findChild(QPushButton, "draw_ways_button").setStyleSheet(
                    "outline:none;background-color:green;padding:5px 5px;border:none;border-radius:10px;font-size:16px;color:white")

        threading.Thread(target=draw_ways).start()

    @pyqtSlot()
    def on_click_draw_points(self):



        path_x_inputs = list(map(int, self.findChild(
            QLineEdit, "path_x_inputs_textbox").text().split(",")))
        path_y_inputs = list(map(int, self.findChild(
            QLineEdit, "path_y_inputs_textbox").text().split(",")))

        if(path_x_inputs.__len__() != path_y_inputs.__len__()):
            self.msg_error.setText(
                "Paths x array and paths y array must be equal")
            self.msg_error.show()
        
        self.findChild(QPushButton, "draw_points_button").setStyleSheet(
                "outline:none;background-color:red;padding:5px 5px;border:none;border-radius:10px;font-size:16px;color:white")

        def draw_points():

            # clearing old figure
            self.points_figure.clear()
            # create an axis
            ax = self.points_figure.add_subplot(111)

            # plot data
            for i in range(path_x_inputs.__len__()):
                ax.text(path_x_inputs[i], path_y_inputs[i], str(
                    i), fontsize=16, bbox=dict(facecolor='red', alpha=1))

            # noinspection PyTypeChecker
            ax.set_xlim(0, max(path_x_inputs) * 1.1)

            # noinspection PyTypeChecker
            ax.set_ylim(0, max(path_y_inputs) * 1.1)

            # refresh canvas
            self.findChild(
                FigureCanvas, "points_chart").draw()
            
            self.findChild(QPushButton, "draw_points_button").setStyleSheet(
                    "outline:none;background-color:green;padding:5px 5px;border:none;border-radius:10px;font-size:16px;color:white")

        threading.Thread(target=draw_points).start()


def main():
    app = QApplication(sys.argv)
    ex = mainWidget()
    # opening window in maximized size
    ex.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
