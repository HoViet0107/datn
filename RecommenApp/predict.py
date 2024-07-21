import os
import pickle
import re
import requests
import json
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import wordcloud

from pyvi import ViTokenizer

class PredictHand:
    def __init__(self, ui):
        self.ui = ui
    def get_all_reviews(self, product_id):
        all_reviews = []

        limit = 10  # Giới hạn số lượng đánh giá mỗi lần gọi
        stars = 5

        while stars <= 5:
          page = 1
          reviews = []
          TIKI_REVIEWS_API = f'https://tiki.vn/api/v2/reviews?include=comments,contribute_info,attribute_vote_summary&sort=stars%7C{stars}&page={page}&product_id={product_id}&limit={limit}'

          headers = {
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
              'X-Guest-Token':'5wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf',
              'Accept':'application/json, text/plain, */*',
              'Accept-Encoding':'gzip, deflate, br, zstd',
              'Accept-Language':'vi',
          }

          params ={
              'limit': limit,
              'include': 'comments,contribute_info,attribute_vote_summary',
              'sort': f'stars|{stars}',
              'page': page,
              'product_id': {product_id},
          }

          cookies = {
              # 'TIKI_RECOMMENDATION':'c2b76cc59f1d63ef5aaa9e9883de3fdc',
              'TKSESSID': '16f55fcbd35a5cdb883de25536242ee4',
              'TOKENS' : '{%22access_token%22:%225wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1870359973526%2C%22guest_token%22:%225wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf%22}',
              'delivery_zone' : 'Vk4wMzQwMjQwMTM=',
              '_trackity' : '7e5dcab4-fa5f-57c7-59c0-7a428c155263'
          }

          response = requests.get(TIKI_REVIEWS_API.format(stars,page,product_id,limit),headers = headers, params = params, cookies = cookies)
          res_body = json.loads(response.content)

          reviews_count = res_body['reviews_count']
          # dừng nếu không có reviews
          if reviews_count == 0:
              print('Not has comment!')
              break

          last_page = res_body['paging']['last_page']
          reviews = reviews + res_body['data']

          while True:
            # thêm các đánh giá vào all_reviews
            for review in reviews:
              if (review['content'] != "" or review['content'].strip()):
                all_reviews += [review['content']]
              elif (review['content'] == "" and review['rating'] == 5 ):
                all_reviews += ["Cực kì hài lòng"]
              elif (review['content'] == "" and review['rating'] == 4 ):
                all_reviews += ["Hài lòng"]
              elif (review['content'] == "" and review['rating'] == 3 ):
                all_reviews += ["Bình thường"]
              elif (review['content'] == "" and review['rating'] == 2 ):
                all_reviews += ["Không hài lòng"]
              elif (review['content'] == "" and review['rating'] == 1 ):
                all_reviews += ["Rất không hài lòng"]

            page+=1

            if(page>last_page):
                break

          stars-=1
          if(stars == 0):
            break

        return all_reviews

    # ------------- chuẩn hóa dữ liệu --------------
    from pyvi import ViTokenizer
    import re
    # chuẩn hóa dữ liệu
    def standardize_data(self, row):
      if isinstance(row, str):
        #Remove all . , " ... in sentences
        row = row.replace(",", " ").replace(".", " ") \
              .replace(";", " ").replace("“", " ") \
              .replace(":", " ").replace("”", " ") \
              .replace('"', " ").replace("'", " ") \
              .replace("!", " ").replace("?", " ") \
              .replace("-", " ").replace("?", " ")\
              .replace(" 🏻"," ")
        row = re.sub(r'\s+', ' ', row)

        #Loại bỏ các từ kéo dài như đẹppppp -> đẹp
        row = re.sub(r'([A-Z])\1+', lambda m: m.group(1).upper(), row, flags=re.IGNORECASE)

        #Lowercase
        row = row.lower()

        #Chuẩn hóa tiếng Việt, xử lý emoj, chuẩn hóa tiếng Anh, thuật ngữ
        replace_list = {
            'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé','ỏe': 'oẻ',
            'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ','ụy': 'uỵ', 'uả': 'ủa',
            'ả': 'ả', 'ố': 'ố', 'u´': 'ố','ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ',
            'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề','ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ',
            'ẻ': 'ẻ', 'àk': u' à ','aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ','ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á',
            'ak': 'à',
            #Quy các icon về 3 loại emoj: Tích cực tiêu cực và trung lâp
            "👻": "positive", "💃": "positive",'🤙': ' positive ', '👍': ' positive ','🦾':'positive',
            "💄": "neutral", "💎": "neutral", "💩": "positive","😕": "negative", "😱": "negative", "😸": "positive",
            "😾": "negative", "🚫": "negative",  "🤬": "negative","🧚": "neutral", "🧡": "positive",'🐶':' neuutral ',
            '👎': ' negative ', '😣': ' negative ','✨': ' positive ', '❣': ' positive ','☀': ' positive ',
            '♥': ' positive ', '🤩': ' positive ', 'like': ' positive ', '💌': ' neutral ','🥰':'positive',
            '🤣': ' positive ', '🖤': ' positive ', '🤤': ' positive ', ':(': ' negative ', '😢': ' negative ',
            '❤': ' positive ', '😍': ' positive ', '😘': ' positive ', '😪': ' negative ', '😊': ' positive ',
            '?': ' ? ', '😁': ' positive ', '💖': ' positive ', '😟': ' negative ', '😭': ' negative ',
            '💯': ' positive ', '💗': ' positive ', '♡': ' positive ', '💜': ' positive ', '🤗': ' positive ',
            '^^': ' positive ', '😨': ' negative ', '☺': ' positive ', '💋': ' positive ', '👌': ' positive ',
            '😖': ' negative ', '😀': ' positive ', ':((': ' negative ', '😡': ' negative ', '😠': ' negative ',
            '😒': ' negative ', '🙂': ' posiive ', '😏': ' negative ', '😝': ' positive ', '😄': ' positive ',
            '😙': ' positive ', '😤': ' negative ', '😎': ' positive ', '😆': ' positive ', '💚': ' positive ',
            '✌': ' positive ', '💕': ' positive ', '😞': ' negative ', '😓': ' negative ', '️🆗️': ' positive ',
            '😉': ' positive ', '😂': ' positive ', ':v': '  positive ', '=))': '  positive ', '😋': ' positive ',
            '💓': ' positive ', '😐': ' neutral ', ':3': ' positive ', '😫': ' negative ', '😥': ' negative ',
            '😃': ' positive ', '😬': ' 😬 ', '😌': ' 😌 ', '💛': ' positive ', '🤝': ' positive ', '🎈': ' positive ',
            '😗': ' positive ', '🤔': ' negative ', '😑': ' negative ', '🔥': ' negative ', '🙏': ' negative ',
            '🆗': ' positive ', '😻': ' positive ', '💙': ' positive ', '💟': ' positive ',
            '😚': ' positive ', '❌': ' negative ', '👏': ' positive ', ';)': ' positive ', '<3': ' positive ',
            '🌝': ' positive ',  '🌷': ' positive ', '🌸': ' positive ', '🌺': ' positive ',
            '🌼': ' neutral ', '🍓': ' positive ', '🐅': ' positive ', '🐾': ' positive ', '👉': ' positive ',
            '💐': ' positive ', '💞': ' positive ', '💥': ' positive ', '💪': ' positive ', '😘':'positive',
            '💰': ' positive ',  '😇': ' positive ', '😛': ' positive ', '😜': ' positive ','👍':'positive',
            '🙃': ' positive ', '🤑': ' positive ', '🤪': ' positive ','☹': ' negative ',  '💀': ' negative ',
            '😔': ' negative ', '😧': ' neutral ', '😩': ' negative ', '😰': ' negative ', '😳': ' neutral ',
            '😵': ' neutral', '😶': ' neutral ', '🙁': ' neutral ', '🥳':'positive','😅': 'neutural',

            #Chuẩn hóa 1 số sentiment words/English words
            ':))': '  positive ', ':)': ' positive ', 'ô kêi': ' ok ', 'okie': ' ok ', ' o kê ': ' ok ','yc':'yêu cầu',
            'okey': ' ok ', 'ôkê': ' ok ', 'oki': ' ok ', ' oke ':  ' ok ',' okay':' ok ','okê':' ok ',
            ' tks ': u' cám ơn ', 'thks': u' cám ơn ', 'thanks': u' cám ơn ', 'ths': u' cám ơn ', 'thank': u' cám ơn ',
            '⭐': 'star ', '*': 'star ', '🌟': 'star ', '🎉': u' positive ', ' ng ' :' người ',
            'not': u' không ',' kh ':u' không ','kô':u' không ','hok':u' không ',' kp ': u' không phải ',u' kô ': u' không ', u' k ': u' không ', '"ko ': u' không ', u' ko ': u' không ','khong': u' không ', u' hok ': u' không ',
            'he he': ' positive ','hehe': ' positive ','hihi': ' positive ', 'haha': ' positive ', 'hjhj': ' positive ',
            ' lol ': ' negative ',' cc ': ' negative ','cute': u' dễ thương ','huhu': ' negative ', ' vs ': u' với ', 'wa': ' quá ', 'wá': u' quá', 'j': u' gì ', '“': ' ',
            ' sz ': u' cỡ ', 'size': u' cỡ ', u' đx ': u' được ', 'dk': u' được ', 'dc': u' được ', 'đk': u' được ', 'đuoc': u'được', 'mn': u'mọi người',
            'đc': u' được ','authentic': u' chuẩn chính hãng ',u' aut ': u' chuẩn chính hãng ', u' auth ': u' chuẩn chính hãng ', 'thick': u' positive ', 'store': u' cửa hàng ',
            'shop': u' cửa hàng ', 'sp': u' sản phẩm ', 'gud': u' tốt ','god': u' tốt ','wel done':' tốt ', 'good': u' tốt ', 'gút': u' tốt ',
            'sấu': u' xấu ','gut': u' tốt ', u' tot ': u' tốt ', u' nice ': u' tốt ', 'perfect': 'rất tốt', 'bt': u' bình thường ',
            'time': u' thời gian ', 'qá': u' quá ', u' ship ': u' giao hàng ', u' m ': u' mình ', u' mik ': u' mình ',
            'ể': 'ể', 'product': 'sản phẩm', 'quality': 'chất lượng','chat':' chất ', 'excelent': 'hoàn hảo', 'bad': 'tệ','fresh': ' tươi ','sad': ' tệ ',
            'date': u' hạn sử dụng ', 'hsd': u' hạn sử dụng ','quickly': u' nhanh ', 'quick': u' nhanh ','fast': u' nhanh ','delivery': u' giao hàng ',u' síp ': u' giao hàng ',
            'beautiful': u' đẹp tuyệt vời ', u' tl ': u' trả lời ', u' r ': u' rồi ', u' shopE ': u' cửa hàng ',u' order ': u' đặt hàng ',
            'chất lg': u' chất lượng ',u' sd ': u' sử dụng ',u' dt ': u' điện thoại ',u' nt ': u' nhắn tin ',u' tl ': u' trả lời ',u' sài ': u' xài ',u'bjo':u' bao giờ ',
            'thik': u' thích ',u' sop ': u' cửa hàng ', ' fb ': ' facebook ', ' face ': ' facebook ', ' very ': u' rất ',u'quả ng ':u' quảng  ',
            'dep': u' đẹp ',u' xau ': u' xấu ','delicious': u' ngon ', u'hàg': u' hàng ', u'qủa': u' quả ', u' dễ mặt ': u' dễ mặc ',u' thấy vọng ': u' thất vọng ',u' vọg ': u' vọng ',
            'iu': u' yêu ','fake': u' giả mạo ', 'trl': 'trả lời', '><': u' positive ','nice' : u' tốt ',u' rat ': u' rất ', u' ung ': u' ưng ', u' ung ho ': u' ủng hộ ',
            ' por ': u' tệ ',' poor ': u' tệ ', 'ib':u' nhắn tin ', 'rep':u' trả lời ',u'fback':' feedback ','fedback':' feedback ',u' bill ': u' hóa đơn ', u' chuan ': u' chuẩn ',
            u' chuản ': u' chuẩn ',u' cx ': u' cũng ',u' cg ': u' cũng ', u' cũg ': u' cũng ', u' cugx ': u' cũng ', u' thỏa mái ': u' thoải mái ', u' thoai mai ': u' thoải mái ',
            u' ap ': u' ứng dụng ', u' app ': u' ứng dụng ', u' sài ': u' xài ', u' tõ ràng ': u'rõ ràng',
            #quy chuan sao thanh star
            '5 sao': ' 5star ','5 star': ' 5star ','5sao': ' 5star ', '4 star': ' 4star ','4 sao': ' 4star ','3sao': ' 3star ','3 star': ' 3star ','3 sao': ' 3star ','3sao': ' 3star ',
            'starstarstarstarstar': ' 5star ', '1 sao': ' 1star ', '1sao': ' 1star ','2 sao':' 2star ','2sao':' 2star ',
            '2 starstar':' 2star ','1star': ' 1star ',}

        for k, v in replace_list.items():
            row = row.replace(k, v)

        row = row.strip()
        return row
      else:
          return ''

    # tách câu thành các từ riêng lẻ
    def tokenizer(self, row):
        if isinstance(row, str):
            return ViTokenizer.tokenize(row)
        else:
            return ''

    def processing_data(self, data):
        #Standardize data
        data_frame = pd.DataFrame(data)
        #print('dataframe':, data_frame)
        data_frame[0] = data_frame[0].apply(self.standardize_data)

        #Tokenizer
        data_frame[0] = data_frame[0].apply(self.tokenizer)
        return data_frame[0]

    #  dự đoán
    def predict(self, prod_id):
        #Load URL and print comments
        data = self.get_all_reviews(prod_id)
        data = self.processing_data(data)

        #predict
        sav_file_path = os.path.join(os.path.dirname(__file__), 'model','naive_bayes_model.sav')
        pl = pickle.load(open(sav_file_path, "rb"))
        X_test_tfidf = tf_idf.transform(data)
        print(X_test_tfidf.shape)
        y_pred = pl.predict(X_test_tfidf)

        cols = ['content', 'label']
        test_data = pd.DataFrame(columns=cols)
        test_data['label'] = y_pred
        test_data['content'] = data
        return test_data

    # phân tích
    def analyze(self,test_data):
        label_counts = self.get_label_counts(test_data)
        pos_count, neg_count, neu_count = label_counts
        self.print_label_counts(pos_count, neg_count, neu_count)

        self.draw_pie_chart(pos_count, neg_count, neu_count)

        rating = self.predict_rating(pos_count, neg_count, neu_count)
        self.print_rating_suggestion(rating)

        self.create_word_clouds(test_data)

    def get_label_counts(self, test_data):
        label_counts = test_data['label'].value_counts()
        pos_count = label_counts.get(1, 0)
        neg_count = label_counts.get(2, 0)
        neu_count = label_counts.get(3, 0)
        return pos_count, neg_count, neu_count

    def print_label_counts(self,pos_count, neg_count, neu_count):
        print("Positive reviews  😊: ", pos_count)
        print("Negative reviews  😡: ", neg_count)
        print("Neutral reviews   😐: ", neu_count)

    def draw_pie_chart(self,pos_count, neg_count, neu_count):
        pie_chart = np.array([pos_count, neg_count, neu_count])
        mylabels = ["Positive", "Negative", "Neutral"]

        if np.sum(pie_chart) == 0:
            print("No data to create pie chart.")
        else:
            plt.pie(pie_chart, labels=mylabels, shadow=True, startangle=90, autopct='%1.1f%%')
            plt.show()
        print("--------------------------------------")

    def predict_rating(self,pos_count, neg_count, neu_count):
        rating = float((pos_count * 5 + neg_count * 1.5 + neu_count * 3.5) / (pos_count + neg_count + neu_count))
        return round(rating, 1)

    def print_rating_suggestion(self,rating):
        print("Rating Predict: ", rating, "⭐")
        if rating > 4:
            print("Good! You can buy it! 👌👌👌")
        elif rating > 2 and rating <= 4:
            print("Please check it carefully! ❗❗❗")
        elif rating <= 2:
            print("Bad! 👎👎👎")
        print("--------------------------------------")

    def create_word_clouds(self,test_data):
        stop_ws = [u'rằng', u'thì', u'là', u'mà', u'mình', u'bé', u'cho', u'chỉ', u'em', u'và', u'gì', u'này', u'các',
                   u'cái', u'cần', u'càng', u'cho', u'chiếc', u'chứ', u'ng', u'cùng', u'cũng',
                   u'gì', u'của', u'còn', u'có', u'cũng', u'khi', u'sẽ', u'về', u'với', u'để', u'nên', u'thêm', u'con',
                   u'nữa', u'sau', u'so', u'tôi', u'vì', u'vẫn', u'đã', u'lần', u'lại', u'bằng', u'biết',
                   u'do', u'người', u'ra', u'tiki', u'vậy', u'trên', u'trong', u'giống', u'cả', u'bên', u'giờ', u'nào',
                   u'rồi', u'đầu', u'bộ', u'một', u'như', u'đi', u'đơn', u'đây',
                   u'vừa', u'đó', u'dc', u'dùng', u'ghi', u'hơi', u'hơn', u'hộp', u'loại', u'luôn', u'làm', u'lên',
                   u'lúc', u'lắm', u'máy', u'mẫu', u'mở', u'ngoài', u'ngày', u'nhiều', u'nhà', u'nhìn', u'nói',
                   u'nước', u'phải', u'qua', u'sao', u'thấy', u'trước', u'tới', u'từ', u'vào', u'vừa', u'xem', u'xong',
                   u'bạn', u'chính', u'chơi', u'hang', u'mọi', u'mới', u'nhé', u'quá',
                   u'tầm', u'ai', u'bạn', u'báo', u'dán', u'kg', u'miếng', u'mấy', u'mặc', u'nó', u'phần', u'tháng',
                   u'tiếng', u'đến', u'xe', u'bh', u'cáo']

        neg_word = test_data['content'].loc[test_data['label'] == 2]
        pos_word = test_data['content'].loc[test_data['label'] == 1]
        neu_word = test_data['content'].loc[test_data['label'] == 3]

        tfidf_pos = TfidfVectorizer(ngram_range=(1, 5), min_df=4, max_df=0.9, stop_words=stop_ws, max_features=100,
                                    sublinear_tf=True, smooth_idf=True)
        tfidf_neg = TfidfVectorizer(ngram_range=(1, 5), min_df=2, max_df=0.9, stop_words=stop_ws, max_features=100,
                                    sublinear_tf=True, smooth_idf=True)
        tfidf_neu = TfidfVectorizer(ngram_range=(1, 5), min_df=3, max_df=0.9, stop_words=stop_ws, max_features=100,
                                    sublinear_tf=True, smooth_idf=True)

        tfidf_matrix_pos = self.create_tfidf_matrix(tfidf_pos, pos_word)
        tfidf_matrix_neg = self.create_tfidf_matrix(tfidf_neg, neg_word)
        tfidf_matrix_neu = self.create_tfidf_matrix(tfidf_neu, neu_word)

        feature_names_pos = tfidf_pos.get_feature_names_out() if tfidf_matrix_pos is not None else []
        feature_names_neg = tfidf_neg.get_feature_names_out() if tfidf_matrix_neg is not None else []
        feature_names_neu = tfidf_neu.get_feature_names_out() if tfidf_matrix_neu is not None else []

        self.create_word_cloud(feature_names_pos, "Positive")
        self.create_word_cloud(feature_names_neg, "Negative")
        self.create_word_cloud(feature_names_neu, "Neutral")

    def create_tfidf_matrix(self,vectorizer, word_list):
        if word_list.empty:
            return None
        else:
            return vectorizer.fit_transform(word_list)

    def create_word_cloud(self,feature_names, sentiment):
        print(f"{sentiment} Review :")
        print(feature_names)
        if feature_names:
            cloud = np.array(feature_names)
            plt.figure(figsize=(12, 6))
            plt.title(f"WordCloud for {sentiment} Reviews")
            word_cloud = wordcloud.WordCloud(max_words=30, background_color="black",
                                             width=1200, height=600, mode="RGB").generate(str(cloud))
            plt.axis("off")
            plt.imshow(word_cloud)
        print("--------------------------------------")

# load mô hình TF-IDF
# đã được huấn luyện trước đó, giúp biến đổi các văn bản thành dạng đặc trưng
# số để có thể áp dụng các thuật toán học máy cho các tác vụ như phân loại, hồi quy, v.v.
# Đường dẫn tương đối tới file tfidf_vectorizer.pk
tf_file_path = os.path.join(os.path.dirname(__file__), 'model', 'tfidf_vectorizer.pk')
#Load TF-IDF weight
tf_idf = pickle.load(open(tf_file_path, 'rb'))