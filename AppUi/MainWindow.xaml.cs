using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Win32;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.Formats.Asn1;
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
using System.Collections.Generic;
using System.Globalization;
using System;


namespace AppUi
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        //public ListView csvList;
        //public DataGrid csvDF;
        //public string csvDirectory = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "data");
        public string csvDirectory = @"C:\Users\ADMIN\Documents\EDISK\nam5\datn\UI\RecommenApp\data";
        private Cursor defaultCursor;

        public MainWindow()
        {
            InitializeComponent();
            defaultCursor = Cursors.Arrow;
            LoadCsvFiles();

            // Find the ListView element in XAML
            //csvList = (ListView)FindName("csvList");
            //csvDF = (DataGrid)FindName("csvDF");
            //prodUrl = (TextBox)FindName("prodUrl");
        }

        private async void GetReviewsButton_Click(object sender, RoutedEventArgs e)
        {
            await GetReviewsAsync();
            LoadCsvFiles(); // Gọi lại phương thức load danh sách file CSV
        }


        private void PredictButton_Click(object sender, RoutedEventArgs e)
        {
            // Lấy prod_id từ một nguồn dữ liệu nào đó, ví dụ từ URL
            string prod_id = GetProdId(prodUrl.ToString());

            // Đóng form PredictF hiện tại nếu có
            CloseCurrentPredictForm();

            // Khởi tạo và hiển thị form PredictF mới
            PredictF predictFormInstance = new PredictF(prod_id);
            predictFormInstance.Show();
        }
        // Phương thức để đóng form PredictF hiện tại
        private void CloseCurrentPredictForm()
        {
            // Duyệt qua tất cả các Window hiện tại của ứng dụng
            foreach (Window window in Application.Current.Windows)
            {
                // Kiểm tra nếu là PredictF và không phải là cửa sổ này đang được xem
                if (window is PredictF predictForm && window != this)
                {
                    predictForm.Close(); // Đóng form PredictF hiện tại
                    break; // Sau khi đóng form, thoát vòng lặp
                }
            }
        }

        // tách prod_id từ url
        private string GetProdId(string url)
        {
            // Tách chuỗi để lấy prod_id
            string[] parts = url.Split(new string[] { "-p", ".html" }, StringSplitOptions.None);

            // Lấy phần tử cuối cùng trong mảng parts
            string prodId = parts[parts.Length - 2]; // parts.Length - 1 sẽ là chuỗi rỗng

            return prodId;
        }

        public static string ExtractSpid(string url)
        {
            var query = new Uri(url).Query;
            var queryParams = System.Web.HttpUtility.ParseQueryString(query);
            return queryParams["spid"];
        }

        private async Task GetReviewsAsync()
        {
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    // Thiết lập thời gian timeout cho HttpClient
                    client.Timeout = TimeSpan.FromMinutes(5);

                    string apiUrl = "http://localhost:5000/api/get-reviews"; 
                    
                    main.Cursor = Cursors.Wait;

                    string prod_id = GetProdId(prodUrl.ToString());
                    string spid = ExtractSpid(prodUrl.ToString());
                    // Tạo đối tượng để chứa dữ liệu cần gửi
                    var data = new { prod_id = prod_id, spid = spid };

                    // Chuyển đổi đối tượng thành JSON string
                    string json = JsonConvert.SerializeObject(data);

                    // Tạo nội dung request là JSON
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    // Gửi request POST đến API và nhận response
                    HttpResponseMessage response = await client.PostAsync(apiUrl, content);

                    // Xử lý response từ API
                    if (response.IsSuccessStatusCode)
                    {
                        // Đọc dữ liệu từ response
                        string responseData = await response.Content.ReadAsStringAsync();

                        // Chuyển đổi dữ liệu từ JSON về đối tượng trong C#
                        var result = JObject.Parse(responseData);

                        Console.WriteLine("a");

                        Cursor = defaultCursor;

                        // Thông báo lấy reviews thành công
                        MessageBox.Show($"{result["message"]}");
                    }
  
                    else
                    {
                        Cursor = defaultCursor;
                        MessageBox.Show($"App: Failed to get data. Status code: {response.StatusCode}");
                    }
                }
            }
            catch (Exception ex)
            {
                Cursor = defaultCursor;
                MessageBox.Show($"APP: An error occurred: {ex.Message}");
            }

        }

        private void DeleteMenuItem_Click(object sender, RoutedEventArgs e)
        {
            if (csvList.SelectedItem != null)
            {
                string selectedCsvFile = csvList.SelectedItem.ToString();
                string csvFilePath = System.IO.Path.Combine(csvDirectory, selectedCsvFile);

                if (File.Exists(csvFilePath))
                {
                    File.Delete(csvFilePath);
                    csvList.Items.Remove(selectedCsvFile);
                    csvDF.ItemsSource = null;
                }
                else
                {
                    MessageBox.Show($"File not found: {selectedCsvFile}");
                }
            }
        }

        private void ClearCsvDF_Click(object sender, RoutedEventArgs e)
        {
            csvDF.ItemsSource = null;
        }
        private void ReloadMenuItem_Click(object sender, RoutedEventArgs e)
        {
            LoadCsvFiles(); // Gọi lại phương thức load danh sách file CSV
        }

        private void LoadCsvFiles()
        {

            csvList.Items.Clear(); // Xóa các phần tử cũ trong danh sách trước khi tải lại
            try
            {
                if (Directory.Exists(csvDirectory))
                {
                    var csvFiles = Directory.GetFiles(csvDirectory, "*.csv");
                    foreach (var csvFile in csvFiles)
                    {
                        csvList.Items.Add(System.IO.Path.GetFileName(csvFile));
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Lỗi khi load dữ liệu từ file CSV: {ex.Message}", "Lỗi", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void CsvList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (csvList.SelectedItem != null)
            {
                string selectedCsvFile = csvList.SelectedItem.ToString();
                string csvFilePath = System.IO.Path.Combine(csvDirectory, selectedCsvFile);
                LoadCsvData(csvFilePath);
            }
        }

        private void LoadCsvData(string filePath)
        {
            try
            {
                var lines = File.ReadAllLines(filePath);
                if (lines.Length > 0)
                {
                    var headers = lines[0].Split(','); // Lấy tiêu đề các cột

                    var dataTable = new System.Data.DataTable();

                    // Thêm cột vào DataTable dựa trên tiêu đề
                    foreach (var header in headers)
                    {
                        dataTable.Columns.Add(header);
                    }

                    // Thêm dữ liệu vào các cột tương ứng
                    for (int i = 1; i < lines.Length; i++) // Bỏ qua hàng tiêu đề
                    {
                        var values = lines[i].Split(',');
                        var row = dataTable.NewRow();

                        for (int j = 0; j < values.Length; j++)
                        {
                            if (j < dataTable.Columns.Count)
                            {
                                row[j] = values[j]; // Gán giá trị vào các cột tương ứng
                            }
                        }

                        dataTable.Rows.Add(row);
                    }

                    // Gán ItemsSource của DataGrid
                    csvDF.ItemsSource = dataTable.DefaultView;

                    // Thiết lập độ rộng cột
                    foreach (var column in csvDF.Columns)
                    {
                        column.Width = new DataGridLength(1, DataGridLengthUnitType.Star);
                        column.MaxWidth = 100;

                        // Kiểm tra nếu là cột hàng đầu tiên và điều chỉnh độ rộng
                        if (column.DisplayIndex == 0)
                        {
                            column.MaxWidth = 600;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Lỗi khi load dữ liệu từ file CSV: {ex.Message}", "Lỗi", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }


        private void main_Closed(object sender, EventArgs e)
        {
            Application.Current.Shutdown();
        }


        private async void crawlBtn_Click(object sender, RoutedEventArgs e)
        {
            await CrawlReviewsAsync();
        }
        private async Task CrawlReviewsAsync() {
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    string apiUrl = "http://localhost:5000/api/crawl";

                    main.Cursor = Cursors.Wait;

                    string cate_name = string.Empty;

                    if (cateCbb.SelectedItem != null)
                    {
                        cate_name = ((ComboBoxItem)cateCbb.SelectedItem).Content.ToString();
                    }
                    
                    // Tạo đối tượng để chứa dữ liệu cần gửi
                    var data = new { cate_name = cate_name };

                    // Chuyển đổi đối tượng thành JSON string
                    string json = JsonConvert.SerializeObject(data);

                    // Tạo nội dung request là JSON
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    // Gửi request POST đến API và nhận response
                    HttpResponseMessage response = await client.PostAsync(apiUrl, content);

                    // Xử lý response từ API
                    if (response.IsSuccessStatusCode)
                    {
                        // Đọc dữ liệu từ response
                        string responseData = await response.Content.ReadAsStringAsync();

                        // Chuyển đổi dữ liệu từ JSON về đối tượng trong C#
                        var result = JObject.Parse(responseData);

                        Cursor = defaultCursor;

                        // Thông báo lấy reviews thành công
                        MessageBox.Show($"{result["message"]}");
                    }

                    else
                    {
                        Cursor = defaultCursor;
                        MessageBox.Show($"App: Failed to get data. Status code: {response.StatusCode}");
                    }
                }
            }
            catch (Exception ex)
            {
                Cursor = defaultCursor;
                MessageBox.Show($"APP: An error occurred: {ex.Message}");
            }
        }

        private void TrainMenuItem_Click(object sender, RoutedEventArgs e)
        {

        }
    }
}