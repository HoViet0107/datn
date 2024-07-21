from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(505, 540)
        self.csvDF_3 = QtWidgets.QTableWidget(Form)
        self.csvDF_3.setGeometry(QtCore.QRect(10, 10, 481, 151))
        self.csvDF_3.setObjectName("csvDF_3")
        self.csvDF_3.setColumnCount(0)
        self.csvDF_3.setRowCount(0)
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(20, 230, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(20, 170, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(20, 200, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.exportBtn = QtWidgets.QPushButton(Form)
        self.exportBtn.setGeometry(QtCore.QRect(420, 170, 71, 31))
        self.exportBtn.setObjectName("exportBtn")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(170, 170, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(170, 200, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(170, 230, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.matPltChart = QtWidgets.QWidget(Form)
        self.matPltChart.setGeometry(QtCore.QRect(10, 260, 481, 261))
        self.matPltChart.setObjectName("matPltChart")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_10.setText(_translate("Form", "Negative reviews  😡:"))
        self.label_8.setText(_translate("Form", "Positive reviews  😊 :"))
        self.label_9.setText(_translate("Form", "Neutral reviews   😐 :"))
        self.exportBtn.setText(_translate("Form", "Export"))
        self.label_11.setText(_translate("Form", "0"))
        self.label_12.setText(_translate("Form", "0"))
        self.label_13.setText(_translate("Form", "0"))

class PredictWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_connections()

    def setup_connections(self):
        self.ui.exportBtn.clicked.connect(self.export_data)

    def export_data(self):
        print("Exporting data...")

    def draw_pie_chart(self, sizes):
        labels = ['Positive', 'Negative', 'Neutral']  # Nhãn cho biểu đồ

        # Kiểm tra tổng số để xem có dữ liệu để tạo biểu đồ không
        if sum(sizes) == 0:
            print("No data to create pie chart.")
        else:
            try:
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
                ax.axis('equal')  # Đảm bảo hình tròn
                chart = FigureCanvas(fig)
                layout = QtWidgets.QVBoxLayout()
                layout.addWidget(chart)
                self.ui.matPltChart.setLayout(layout)
            except Exception as e:
                print(e)

# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = PredictWindow()
#     window.show()
#     sys.exit(app.exec_())
