using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System;
using System.ComponentModel;
using System.Net.Http;
using System.Text;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media.Imaging;
using System.Windows.Media;

namespace AppUi
{
    public partial class PredictF : Window
    {
        BitmapImage defaultImg = new BitmapImage(new Uri("C:\\Users\\ADMIN\\Documents\\EDISK\\nam5\\datn\\UI\\RecommenApp\\img\\default.png"));
        private string prod_id;

        public PredictF(string prod_id)
        {
            InitializeComponent();
            this.prod_id = prod_id;
            imgPie.Source = defaultImg;

            // Đăng ký sự kiện Unloaded để giải phóng tài nguyên
            this.Unloaded += PredictF_Unloaded;
        }
        private void PredictF_Unloaded(object sender, RoutedEventArgs e)
        {
            // Giải phóng tài nguyên hình ảnh khi form được giải phóng
            imgPie.Source = null;
        }
        private void Window_Closed(object sender, EventArgs e)
        {
            imgPie.Source = null; // Giải phóng tài nguyên hình ảnh hiện tại
            imgPie.Source = defaultImg; // Cập nhật lại với hình ảnh mặc định
            Application.Current.Shutdown();
            MessageBox.Show("closed");
        }

        private void Window_Closing(object sender, CancelEventArgs e)
        {
            imgPie.Source = null; // Giải phóng tài nguyên hình ảnh hiện tại
            imgPie.Source = defaultImg; // Cập nhật lại với hình ảnh mặc định
            Application.Current.Shutdown();
        }

        private async Task PredictAsync()
        {
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    preForm.Cursor = Cursors.Wait; // Sử dụng Cursor của MainWindow
                    // Kiểm tra nếu predictFormInstance đã được khởi tạo
                    
                    string apiUrl = "http://localhost:5000/api/draw_pie_chart";

                    // Tạo đối tượng để chứa dữ liệu cần gửi
                    var data = new { prod_id = prod_id };

                    // Chuyển đổi đối tượng thành JSON string
                    string json = JsonConvert.SerializeObject(data);

                    // Tạo nội dung request là JSON
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    // Gửi request POST đến API và nhận response
                    HttpResponseMessage response = await client.PostAsync(apiUrl, content);

                    // Xử lý response từ API
                    if (response.IsSuccessStatusCode)
                    {
                        string responseData = await response.Content.ReadAsStringAsync();
                        try
                        {
                            var result = JObject.Parse(responseData);
                            string posCount = result["pos_count"].ToString();
                            string neuCount = result["neu_count"].ToString();
                            string negCount = result["neg_count"].ToString();
                            string piePath = "C:\\Users\\ADMIN\\Documents\\EDISK\\nam5\\datn\\UI\\RecommenApp\\" + result["pie_path"].ToString();
                            float rating = ((float)result["rating"]);

                            lblPosCount.Content = posCount;
                            lblNeuCount.Content = neuCount;
                            lblNegCount.Content = negCount;
                            imgPie.Source = new BitmapImage(new Uri(piePath));
                            ratinglbl.Content = rating;
                            if(rating > 4)
                            {
                                lblsuggest.Content = "Good! You can buy it! 👌👌👌";
                            } else if(rating > 2 && rating <= 4){
                                lblsuggest.Content = "Please check it carefully! ❗❗❗";
                            }
                            else
                            {
                                lblsuggest.Content = "Bad! 👎👎👎";
                            }
                        }
                        catch (Exception ex)
                        {
                        }
                    }
                    else
                    {
                        MessageBox.Show($"App: Failed to get data. Status code: {response.StatusCode}");
                    }
                    
                    preForm.Cursor = Cursors.Arrow;
                }
            }
            catch (Exception ex)
            {
                preForm.Cursor = Cursors.Arrow;
                // Hiển thị thông báo lỗi
                MessageBox.Show($"Đã xảy ra lỗi khi mở form predictForm: {ex.Message}", "Lỗi", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void preForm_Closed(object sender, EventArgs e)
        {
            lblPosCount.Content = "0";
            lblNeuCount.Content = "0";
            lblNegCount.Content = "0";
            imgPie.Source = defaultImg;
            ratinglbl.Content = "0.0";
            lblsuggest.Content = "";
            MessageBox.Show("Closed");
            this.Close();
        }

        private async void PredictMenuItem_Click(object sender, RoutedEventArgs e)
        {
            await PredictAsync();
        }

        private void ReloadMenuItem_Click(object sender, RoutedEventArgs e)
        {
            lblPosCount.Content = "0";
            lblNeuCount.Content = "0";
            lblNegCount.Content = "0";
            imgPie.Source = defaultImg;
            ratinglbl.Content = "0.0";
            lblsuggest.Content = "";
        }

        private void ShowWordCloudMenuItem_Click(object sender, RoutedEventArgs e)
        {
            CloseCurrentWcForm();

            // Khởi tạo và hiển thị form PredictF mới
            WordCloud wcForm = new WordCloud();
            wcForm.Show();
        }
        // Phương thức để đóng form PredictF hiện tại
        private void CloseCurrentWcForm()
        {
            // Duyệt qua tất cả các Window hiện tại của ứng dụng
            foreach (Window window in Application.Current.Windows)
            {
                // Kiểm tra nếu là PredictF và không phải là cửa sổ này đang được xem
                if (window is WordCloud wcForm && window != this)
                {
                    wcForm.Close(); // Đóng form PredictF hiện tại
                    break; // Sau khi đóng form, thoát vòng lặp
                }
            }
        }
    }
}
