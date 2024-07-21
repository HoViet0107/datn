from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import os
from func import list_item_clicked


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(771, 591)
        MainWindow.setMinimumSize(QtCore.QSize(771, 591))
        MainWindow.setMaximumSize(QtCore.QSize(771, 591))
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainWindow.setAcceptDrops(True)

        # Thiết lập central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Thiết lập tab widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 771, 571))
        self.tabWidget.setObjectName("tabWidget")

        # Tab "Recomnend"
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        # Nút "GetReview"
        self.getBtn = QtWidgets.QPushButton(self.tab)
        self.getBtn.setGeometry(QtCore.QRect(10, 10, 71, 31))
        self.getBtn.setObjectName("getBtn")

        # TextEdit để nhập từ khóa tìm kiếm
        self.searchTxt = QtWidgets.QTextEdit(self.tab)
        self.searchTxt.setGeometry(QtCore.QRect(180, 10, 481, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe Fluent Icons")
        font.setPointSize(13)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.searchTxt.setFont(font)
        self.searchTxt.setObjectName("searchTxt")

        # Nút "Search"
        self.searchBtn = QtWidgets.QPushButton(self.tab)
        self.searchBtn.setGeometry(QtCore.QRect(680, 10, 71, 31))
        self.searchBtn.setObjectName("searchBtn")

        # Nhãn "Column:"
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(190, 60, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # ComboBox để chọn số lượng cột
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setGeometry(QtCore.QRect(250, 50, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        # ListView để hiển thị danh sách CSV
        self.csvList = QtWidgets.QListView(self.tab)
        self.csvList.setGeometry(QtCore.QRect(10, 100, 161, 421))
        self.csvList.setObjectName("csvList")

        # TableWidget để hiển thị dữ liệu CSV
        self.csvDF = QtWidgets.QTableWidget(self.tab)
        self.csvDF.setGeometry(QtCore.QRect(180, 100, 571, 421))
        self.csvDF.setObjectName("csvDF")
        self.csvDF.setColumnCount(0)
        self.csvDF.setRowCount(0)

        # Nút "Export"
        self.exportBtn = QtWidgets.QPushButton(self.tab)
        self.exportBtn.setGeometry(QtCore.QRect(680, 50, 71, 31))
        self.exportBtn.setObjectName("exportBtn")

        # Nút "Predict"
        self.predictBtn = QtWidgets.QPushButton(self.tab)
        self.predictBtn.setGeometry(QtCore.QRect(90, 10, 71, 31))
        self.predictBtn.setObjectName("predictBtn")

        # Nút "Analyze"
        self.analBtn = QtWidgets.QPushButton(self.tab)
        self.analBtn.setGeometry(QtCore.QRect(50, 50, 71, 31))
        self.analBtn.setObjectName("analBtn")

        # Thêm tab "Recomnend" vào tab widget
        self.tabWidget.addTab(self.tab, "")

        # Tab "CrawData"
        self.crawData = QtWidgets.QWidget()
        self.crawData.setObjectName("crawData")

        # Nút "GetReview"
        self.crawlBtn = QtWidgets.QPushButton(self.crawData)
        self.crawlBtn.setGeometry(QtCore.QRect(670, 10, 71, 31))
        self.crawlBtn.setObjectName("crawlBtn")

        # Nhãn "Category:"
        self.label_2 = QtWidgets.QLabel(self.crawData)
        self.label_2.setGeometry(QtCore.QRect(10, 9, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # TableWidget để hiển thị dữ liệu preview
        self.previewDF = QtWidgets.QTableWidget(self.crawData)
        self.previewDF.setGeometry(QtCore.QRect(180, 90, 571, 431))
        self.previewDF.setObjectName("previewDF")
        self.previewDF.setColumnCount(0)
        self.previewDF.setRowCount(0)

        # Nút "Export"
        self.exportCsvBtn = QtWidgets.QPushButton(self.crawData)
        self.exportCsvBtn.setGeometry(QtCore.QRect(620, 50, 71, 31))
        self.exportCsvBtn.setObjectName("exportCsvBtn")

        # SpinBox để chọn giá trị
        self.spinBoxVal = QtWidgets.QSpinBox(self.crawData)
        self.spinBoxVal.setGeometry(QtCore.QRect(500, 10, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxVal.setFont(font)
        self.spinBoxVal.setMinimum(1)
        self.spinBoxVal.setMaximum(5)
        self.spinBoxVal.setProperty("value", 5)
        self.spinBoxVal.setObjectName("spinBoxVal")

        # SpinBox khác để chọn giá trị
        self.spinBValP = QtWidgets.QSpinBox(self.crawData)
        self.spinBValP.setGeometry(QtCore.QRect(430, 10, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBValP.setFont(font)
        self.spinBValP.setMinimum(1)
        self.spinBValP.setMaximum(20)
        self.spinBValP.setProperty("value", 5)
        self.spinBValP.setObjectName("spinBValP")

        # Nhãn "Page:"
        self.label_5 = QtWidgets.QLabel(self.crawData)
        self.label_5.setGeometry(QtCore.QRect(390, 9, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        # ComboBox để chọn danh mục
        self.cateCbb_2 = QtWidgets.QComboBox(self.crawData)
        self.cateCbb_2.setGeometry(QtCore.QRect(70, 10, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cateCbb_2.setFont(font)
        self.cateCbb_2.setObjectName("cateCbb_2")
        self.cateCbb_2.addItem("")
        self.cateCbb_2.addItem("")

        # ListView để hiển thị danh sách dữ liệu gốc
        self.oriDataList = QtWidgets.QListView(self.crawData)
        self.oriDataList.setGeometry(QtCore.QRect(10, 90, 161, 431))
        self.oriDataList.setObjectName("oriDataList")

        # Nhãn "⭐"
        self.label_6 = QtWidgets.QLabel(self.crawData)
        self.label_6.setGeometry(QtCore.QRect(480, 10, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        # Thêm tab "CrawData" vào tab widget
        self.tabWidget.addTab(self.crawData, "")

        # Tab "TrainModel"
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        # Nhãn "Original reviews:"
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(20, 19, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        # Nút "Import"
        self.loadOriBtn = QtWidgets.QPushButton(self.tab_2)
        self.loadOriBtn.setGeometry(QtCore.QRect(630, 20, 71, 31))
        self.loadOriBtn.setObjectName("loadOriBtn")

        # TextEdit để nhập dữ liệu gốc
        self.oriData = QtWidgets.QTextEdit(self.tab_2)
        self.oriData.setGeometry(QtCore.QRect(130, 20, 481, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe Fluent Icons")
        font.setPointSize(13)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.oriData.setFont(font)
        self.oriData.setObjectName("oriData")

        # Nút "Process"
        self.processBtn = QtWidgets.QPushButton(self.tab_2)
        self.processBtn.setGeometry(QtCore.QRect(450, 60, 71, 31))
        self.processBtn.setObjectName("processBtn")

        # TableWidget để hiển thị dữ liệu preview
        self.previewDF_2 = QtWidgets.QTableWidget(self.tab_2)
        self.previewDF_2.setGeometry(QtCore.QRect(10, 100, 741, 421))
        self.previewDF_2.setObjectName("previewDF_2")
        self.previewDF_2.setColumnCount(0)
        self.previewDF_2.setRowCount(0)

        # Nút "Train"
        self.trainBtn = QtWidgets.QPushButton(self.tab_2)
        self.trainBtn.setGeometry(QtCore.QRect(540, 60, 71, 31))
        self.trainBtn.setObjectName("trainBtn")

        # Nút "Test"
        self.testBtn = QtWidgets.QPushButton(self.tab_2)
        self.testBtn.setGeometry(QtCore.QRect(630, 60, 71, 31))
        self.testBtn.setObjectName("testBtn")

        # Nhãn "Accuracy:"
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(60, 70, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        # Nhãn để hiển thị giá trị độ chính xác
        self.accuracyVal = QtWidgets.QLabel(self.tab_2)
        self.accuracyVal.setGeometry(QtCore.QRect(120, 70, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accuracyVal.setFont(font)
        self.accuracyVal.setObjectName("accuracyVal")

        # Thêm tab "TrainModel" vào tab widget
        self.tabWidget.addTab(self.tab_2, "")

        # Thiết lập central widget
        MainWindow.setCentralWidget(self.centralwidget)

        # Thiết lập menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Thiết lập statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Thiết lập lại các đối tượng UI
        self.retranslateUi(MainWindow)

        # Đặt tab hiện tại là tab "CrawData"
        self.tabWidget.setCurrentIndex(0)



        #--------------- func -------------------#
            # ----  ---- #
        # Khởi tạo lưu trữ dữ liệu CSV và file hiện tại
        self.csv_data = {}
        self.current_file = None
        self.page_size = 100  # Kích thước trang mặc định, đặt là tùy chọn đầu tiên (100)
        # Hàm để tải dữ liệu CSV vào self.csv_data
        self.load_csv_data = lambda filename: self._load_csv_data(filename)
            # ---- end ---- #

        # Kết nối tín hiệu khi người dùng click vào mục trong danh sách CSV
        self.csvList.clicked.connect(self.list_item_clicked)

        # Kết nối tín hiệu khi combobox thay đổi(thay đổi số lượng hiển thị trên df)
        self.comboBox.currentIndexChanged.connect(self.update_csvdf)

            # ---- hiển thị file csv trên csvList -----
        # Lấy danh sách các file CSV trong thư mục "data"
        self.csv_files = [f for f in os.listdir("data") if f.endswith(".csv")]
        # Thêm các file CSV vào danh sách csvList
        model = QtGui.QStandardItemModel(self.csvList)
        for file in self.csv_files:
            item = QtGui.QStandardItem(file)
            model.appendRow(item)
        self.csvList.setModel(model)
            # ---- end ---- #



        # --------------- end func -------------------#
        # Dịch các chuỗi sang ngôn ngữ được lựa chọn
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.getBtn.setText(_translate("MainWindow", "GetReview"))
        self.searchBtn.setText(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "Column:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "50"))
        self.comboBox.setItemText(1, _translate("MainWindow", "100"))
        self.comboBox.setItemText(2, _translate("MainWindow", "200"))
        self.comboBox.setItemText(3, _translate("MainWindow", "all"))
        self.exportBtn.setText(_translate("MainWindow", "Export"))
        self.predictBtn.setText(_translate("MainWindow", "Predict"))
        self.analBtn.setText(_translate("MainWindow", "Analyze"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Recomnend"))
        self.crawlBtn.setText(_translate("MainWindow", "GetReview"))
        self.label_2.setText(_translate("MainWindow", "Category:"))
        self.exportCsvBtn.setText(_translate("MainWindow", "Export"))
        self.label_5.setText(_translate("MainWindow", "Page:"))
        self.cateCbb_2.setItemText(0, _translate("MainWindow", "thoi-trang-nam"))
        self.cateCbb_2.setItemText(1, _translate("MainWindow", "thoi-trang-nu"))
        self.label_6.setText(_translate("MainWindow", "⭐"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.crawData), _translate("MainWindow", "CrawData"))
        self.label_3.setText(_translate("MainWindow", "Original reviews:"))
        self.loadOriBtn.setText(_translate("MainWindow", "Import"))
        self.processBtn.setText(_translate("MainWindow", "Process"))
        self.trainBtn.setText(_translate("MainWindow", "Train"))
        self.testBtn.setText(_translate("MainWindow", "Test"))
        self.label_4.setText(_translate("MainWindow", "Accuracy: "))
        self.accuracyVal.setText(_translate("MainWindow", "0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "TrainModel"))

    # Hàm để tải dữ liệu từ file CSV
    def load_csv_data(self, filename):
        print(f"Loading CSV file: {filename}")
        try:
            with open(os.path.join("data", filename), "r", newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                self.csv_data[filename] = list(reader)  # Lưu tất cả dữ liệu
                self.update_csvdf()  # Cập nhật bảng sau khi tải dữ liệu
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file: {filename}. Chi tiết: {e}")
        except csv.Error as e:
            print(f"Lỗi: Lỗi khi phân tích file CSV: {filename}. Chi tiết: {e}")
        except Exception as e:
            print(f"Lỗi: Đã xảy ra lỗi không mong muốn khi tải file CSV: {filename}. Chi tiết: {e}")

    # Hàm để cập nhật dữ liệu trong bảng từ file CSV
    def update_csvdf(self):
        if self.current_file is not None:
            # Lấy kích thước trang từ combobox
            if self.comboBox.currentIndex() == 0:
                self.page_size = 100
            elif self.comboBox.currentIndex() == 1:
                self.page_size = 200
            elif self.comboBox.currentIndex() == 2:
                self.page_size = 500
            else:
                # Tùy chọn "all", đặt kích thước trang là tổng số hàng
                self.page_size = len(self.csv_data[self.current_file])

            # Tính toán số trang hiện tại
            page_number = 1  # Mặc định là trang 1

            # Tính toán chỉ số bắt đầu và kết thúc cho trang hiện tại
            start_index = (page_number - 1) * self.page_size
            end_index = start_index + self.page_size

            # Cập nhật page_data với dữ liệu của trang hiện tại
            self.page_data = self.csv_data[self.current_file][start_index:end_index]

            # Cập nhật bảng dữ liệu
            if self.page_data:
                self.csvDF.setRowCount(len(self.page_data))
                self.csvDF.setColumnCount(len(self.page_data[0]))
                for row, line in enumerate(self.page_data):
                    for col, value in enumerate(line):
                        item = QtWidgets.QTableWidgetItem(value)
                        self.csvDF.setItem(row, col, item)
            else:
                # Xử lý trường hợp không có dữ liệu
                self.csvDF.setRowCount(0)
                self.csvDF.setColumnCount(0)
                print("Không có dữ liệu cho trang hiện tại.")

    # Hàm xử lý sự kiện khi người dùng chọn một file trong danh sách CSV
    def list_item_clicked(self, index):
        item = self.csvList.model().itemFromIndex(index)
        self.current_file = item.text()
        print(f"File được chọn: {self.current_file}")  # In ra để debug
        self.load_csv_data(self.current_file)

        # Thiết lập lại combobox về giá trị mặc định (100 hàng) khi thay đổi file
        self.comboBox.setCurrentIndex(0)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
