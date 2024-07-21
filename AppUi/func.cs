using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AppUi
{
    internal class func
    {
        private string GetProdId(string url)
        {
            // Tách chuỗi để lấy prod_id
            string[] parts = url.Split(new string[] { "-p", ".html" }, StringSplitOptions.None);

            // Lấy phần tử cuối cùng trong mảng parts
            string prodId = parts[parts.Length - 2]; // parts.Length - 1 sẽ là chuỗi rỗng

            return prodId;
        }
    }
}
