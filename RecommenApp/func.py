import os
import csv
from PyQt5 import QtWidgets


class FuncHandler:
    def __init__(self, ui):
        self.ui = ui
        self.csv_data = {}
        self.page_size = 100
        self.current_file = None
        self.page_data = []

    def _assign_reviews(self, reviews):
        # Xử lý dữ liệu reviews ở đây
        print('cào')
        print("Dữ liệu reviews:", reviews)
        # Ví dụ gán reviews vào một biến instance để sử dụng ở các phần khác của UI
        # self.ui.reviews = reviews
        # Lưu dữ liệu vào file CSV
        self.save_to_csv(reviews, 'tiki.csv')
        print('2 đã lwu')

    def save_to_csv(self, data, filename):
        # Lưu dữ liệu vào file CSV
        file_path = os.path.join("data", filename)
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for review in data:
                    writer.writerow([review])  # Ghi mỗi review vào một dòng trong file CSV
            print(f"Lưu dữ liệu vào file {file_path} thành công.")
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vào file {file_path}: {e}")


    def _load_csv_data(self, filename):
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

    def update_csvdf(self):
        if self.current_file is not None:
            # Lấy kích thước trang từ combobox
            if self.ui.comboBox.currentIndex() == 0:
                self.page_size = 100
            elif self.ui.comboBox.currentIndex() == 1:
                self.page_size = 200
            elif self.ui.comboBox.currentIndex() == 2:
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
                self.ui.csvDF.setRowCount(len(self.page_data))
                self.ui.csvDF.setColumnCount(len(self.page_data[0]))
                for row, line in enumerate(self.page_data):
                    for col, value in enumerate(line):
                        item = QtWidgets.QTableWidgetItem(value)
                        self.ui.csvDF.setItem(row, col, item)
            else:
                # Xử lý trường hợp không có dữ liệu
                self.ui.csvDF.setRowCount(0)
                self.ui.csvDF.setColumnCount(0)
                print("Không có dữ liệu cho trang hiện tại.")

    def list_item_clicked(self, index):
        item = self.ui.csvList.model().itemFromIndex(index)
        self.current_file = item.text()
        print(f"File được chọn: {self.current_file}")  # In ra để debug
        self._load_csv_data(self.current_file)

        # Thiết lập lại combobox về giá trị mặc định (100 hàng) khi thay đổi file
        self.ui.comboBox.setCurrentIndex(0)