using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace AppUi
{
    /// <summary>
    /// Interaction logic for WordCloud.xaml
    /// </summary>
    public partial class WordCloud : Window
    {
        private string txtDir = @"C:\Users\ADMIN\Documents\EDISK\nam5\datn\UI\RecommenApp\analyze";
        public WordCloud()
        {
            InitializeComponent();
            LoadTxtFiles();
        }

        private void Window_Closed(object sender, EventArgs e)
        {

        }

        private void LoadTxtFiles()
        {

            txtList.Items.Clear(); // Xóa các phần tử cũ trong danh sách trước khi tải lại
            try
            {
                if (Directory.Exists(txtDir))
                {
                    var csvFiles = Directory.GetFiles(txtDir, "*.txt");
                    foreach (var csvFile in csvFiles)
                    {
                        txtList.Items.Add(System.IO.Path.GetFileName(csvFile));
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Lỗi khi load dữ liệu từ file TXT: {ex.Message}", "Lỗi", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void txtList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // Lấy tên file được chọn từ ListBox
            if (txtList.SelectedItem != null)
            {
                string selectedFile = txtList.SelectedItem.ToString();
                string filePath = System.IO.Path.Combine(txtDir, selectedFile);

                // Kiểm tra nếu file tồn tại
                if (File.Exists(filePath))
                {
                    try
                    {
                        // Đọc nội dung file
                        string fileContent = File.ReadAllText(filePath, Encoding.UTF8);

                        // Tạo một FlowDocument từ nội dung file
                        FlowDocument flowDoc = new FlowDocument();
                        Paragraph paragraph = new Paragraph();
                        paragraph.Inlines.Add(new Run(fileContent));
                        flowDoc.Blocks.Add(paragraph);

                        // Hiển thị nội dung trong RichTextBox
                        txtData.Document = flowDoc;
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Lỗi khi đọc dữ liệu từ file TXT: {ex.Message}", "Lỗi", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
                else
                {
                    MessageBox.Show("File không tồn tại.", "Lỗi", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }
    }
}
