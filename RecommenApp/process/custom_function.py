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



_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Guest-Token': '5wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'vi',
}

_COOKIES = {
    'TKSESSID': '16f55fcbd35a5cdb883de25536242ee4',
    'TOKENS': '{%22access_token%22:%225wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1870359973526%2C%22guest_token%22:%225wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf%22}',
    'delivery_zone': 'Vk4wMzQwMjQwMTM=',
    '_trackity': '7e5dcab4-fa5f-57c7-59c0-7a428c155263'
}

'''
    ------------------- Start - Load reviews from tiki.com -------------------
'''
def get_prod_id(url):
    prod_id_match = re.search(r'-p(\d+)\.html', url)
    spid_match = re.search(r'spid=(\d+)', url)

    if prod_id_match and spid_match:
        prod_id = prod_id_match.group(1)
        spid = spid_match.group(1)
        return prod_id, spid
    else:
        return None

def get_directory(folder):
    directory = os.path.join(os.getcwd(), folder)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


# get reviews from tiki
def get_reviews(prod_id, spid):
    reviews,reviews_count = get_all_reviews(prod_id, spid)
    # save to csv file
    rev_df = pd.DataFrame(reviews,columns=['content'])
    
    file_path = os.path.join(get_directory('data'), f'{prod_id}_origin_reviews.csv')
    
    rev_df.to_csv(file_path, index=False)
    # return number of reviews
    return reviews_count


def get_all_reviews(product_id, spid):
    all_reviews = []

    headers = _HEADERS
    cookies = _COOKIES

    page = 1
    while True:
        TIKI_REVIEWS_API = f'https://tiki.vn/api/v2/reviews?limit=20&include=comments,contribute_info,attribute_vote_summary&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={page}&spid={spid}&product_id={product_id}&seller_id=1'
        print(TIKI_REVIEWS_API)
        response = requests.get(TIKI_REVIEWS_API, headers=headers, cookies=cookies)
        res_body = json.loads(response.content)

        reviews_count = res_body.get('reviews_count', 0)
        
        # break if no reviews
        if reviews_count == 0:
            print('Not has comment!')
            break

        last_page = res_body['paging']['last_page']
        reviews = res_body['data']

        print('loading...')

        # if review content is empty add review content based on rating
        for review in reviews:
            if review['content'].strip():
                all_reviews.append(review['content'])
            else:
                if review['rating'] == 5:
                    all_reviews.append("Cực kì hài lòng")
                elif review['rating'] == 4:
                    all_reviews.append("Hài lòng")
                elif review['rating'] == 3:
                    all_reviews.append("Bình thường")
                elif review['rating'] == 2:
                    all_reviews.append("Không hài lòng")
                elif review['rating'] == 1:
                    all_reviews.append("Rất không hài lòng")

        page += 1
        if page > last_page:
            break

    return all_reviews,reviews_count

'''
    ------------------- End - Load reviews from tiki.com -------------------
'''




'''
    ------------------- Start - Process data -------------------
'''
# data standardization
def standardize_data(row):
    if isinstance(row, str):
        #Remove all special characters in sentences
        row = row.replace(",", " ").replace(".", " ") \
            .replace(";", " ").replace("“", " ") \
            .replace(":", " ").replace("”", " ") \
            .replace('"', " ").replace("'", " ") \
            .replace("!", " ").replace("?", " ") \
            .replace("-", " ").replace("?", " ") \
            .replace(" 🏻", " ")
        row = re.sub(r'\s+', ' ', row)

        # Reformat long text. EX: đẹpppp -> đẹp
        row = re.sub(r'([A-Z])\1+', lambda m: m.group(1).upper(), row, flags=re.IGNORECASE)

        #Lowercase
        row = row.lower()

        # Normalize vietnamese, emoji
        replace_list = {
            'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé', 'ỏe': 'oẻ',
            'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ', 'ụy': 'uỵ', 'uả': 'ủa',
            'ả': 'ả', 'ố': 'ố', 'u': 'ố', 'ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ',
            'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề', 'ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ',
            'ẻ': 'ẻ', 'àk': u' à ', 'a': 'à', 'i': 'ì', 'ă´': 'ắ', 'ử': 'ử', 'e': 'ẽ', 'y': 'ỹ', 'a': 'á',
            'ak': 'à',
            # Normalize emoji
            "👻": "positive", "💃": "positive", '🤙': ' positive ', '👍': ' positive ', '🦾': 'positive',
            "💄": "neutral", "💎": "neutral", "💩": "positive", "😕": "negative", "😱": "negative", "😸": "positive",
            "😾": "negative", "🚫": "negative", "🤬": "negative", "🧚": "neutral", "🧡": "positive", '🐶': ' neuutral ',
            '👎': ' negative ', '😣': ' negative ', '✨': ' positive ', '❣': ' positive ', '☀': ' positive ',
            '♥': ' positive ', '🤩': ' positive ', 'like': ' positive ', '💌': ' neutral ', '🥰': 'positive',
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
            '🌝': ' positive ', '🌷': ' positive ', '🌸': ' positive ', '🌺': ' positive ',
            '🌼': ' neutral ', '🍓': ' positive ', '🐅': ' positive ', '🐾': ' positive ', '👉': ' positive ',
            '💐': ' positive ', '💞': ' positive ', '💥': ' positive ', '💪': ' positive ', '😘': 'positive',
            '💰': ' positive ', '😇': ' positive ', '😛': ' positive ', '😜': ' positive ', '👍': 'positive',
            '🙃': ' positive ', '🤑': ' positive ', '🤪': ' positive ', '☹': ' negative ', '💀': ' negative ',
            '😔': ' negative ', '😧': ' neutral ', '😩': ' negative ', '😰': ' negative ', '😳': ' neutral ',
            '😵': ' neutral', '😶': ' neutral ', '🙁': ' neutral ', '🥳': 'positive', '😅': 'neutural',

            # Normalize sentiment words/English words
            ':))': '  positive ', ':)': ' positive ', 'ô kêi': ' ok ', 'okie': ' ok ', ' o kê ': ' ok ',
            'yc': 'yêu cầu',
            'okey': ' ok ', 'ôkê': ' ok ', 'oki': ' ok ', ' oke ': ' ok ', ' okay': ' ok ', 'okê': ' ok ',
            ' tks ': u' cám ơn ', 'thks': u' cám ơn ', 'thanks': u' cám ơn ', 'ths': u' cám ơn ', 'thank': u' cám ơn ',
            '⭐': 'star ', '*': 'star ', '🌟': 'star ', '🎉': u' positive ', ' ng ': ' người ',
            'not': u' không ', ' kh ': u' không ', 'kô': u' không ', 'hok': u' không ', ' kp ': u' không phải ',
            u' kô ': u' không ', u' k ': u' không ', '"ko ': u' không ', u' ko ': u' không ', 'khong': u' không ',
            u' hok ': u' không ',
            'he he': ' positive ', 'hehe': ' positive ', 'hihi': ' positive ', 'haha': ' positive ',
            'hjhj': ' positive ',
            ' lol ': ' negative ', ' cc ': ' negative ', 'cute': u' dễ thương ', 'huhu': ' negative ', ' vs ': u' với ',
            'wa': ' quá ', 'wá': u' quá', 'j': u' gì ', '“': ' ',
            ' sz ': u' cỡ ', 'size': u' cỡ ', u' đx ': u' được ', 'dk': u' được ', 'dc': u' được ', 'đk': u' được ',
            'đuoc': u'được', 'mn': u'mọi người',
            'đc': u' được ', 'authentic': u' chuẩn chính hãng ', u' aut ': u' chuẩn chính hãng ',
            u' auth ': u' chuẩn chính hãng ', 'thick': u' positive ', 'store': u' cửa hàng ',
            'shop': u' cửa hàng ', 'sp': u' sản phẩm ', 'gud': u' tốt ', 'god': u' tốt ', 'wel done': ' tốt ',
            'good': u' tốt ', 'gút': u' tốt ',
            'sấu': u' xấu ', 'gut': u' tốt ', u' tot ': u' tốt ', u' nice ': u' tốt ', 'perfect': 'rất tốt',
            'bt': u' bình thường ',
            'time': u' thời gian ', 'qá': u' quá ', u' ship ': u' giao hàng ', u' m ': u' mình ', u' mik ': u' mình ',
            'ể': 'ể', 'product': 'sản phẩm', 'quality': 'chất lượng', 'chat': ' chất ', 'excelent': 'hoàn hảo',
            'bad': 'tệ', 'fresh': ' tươi ', 'sad': ' tệ ',
            'date': u' hạn sử dụng ', 'hsd': u' hạn sử dụng ', 'quickly': u' nhanh ', 'quick': u' nhanh ',
            'fast': u' nhanh ', 'delivery': u' giao hàng ', u' síp ': u' giao hàng ',
            'beautiful': u' đẹp tuyệt vời ', u' tl ': u' trả lời ', u' r ': u' rồi ', u' shopE ': u' cửa hàng ',
            u' order ': u' đặt hàng ',
            'chất lg': u' chất lượng ', u' sd ': u' sử dụng ', u' dt ': u' điện thoại ', u' nt ': u' nhắn tin ',
            u' tl ': u' trả lời ', u' sài ': u' xài ', u'bjo': u' bao giờ ',
            'thik': u' thích ', u' sop ': u' cửa hàng ', ' fb ': ' facebook ', ' face ': ' facebook ',
            ' very ': u' rất ', u'quả ng ': u' quảng  ',
            'dep': u' đẹp ', u' xau ': u' xấu ', 'delicious': u' ngon ', u'hàg': u' hàng ', u'qủa': u' quả ',
            u' dễ mặt ': u' dễ mặc ', u' thấy vọng ': u' thất vọng ', u' vọg ': u' vọng ',
            'iu': u' yêu ', 'fake': u' giả mạo ', 'trl': 'trả lời', '><': u' positive ', 'nice': u' tốt ',
            u' rat ': u' rất ', u' ung ': u' ưng ', u' ung ho ': u' ủng hộ ',
            ' por ': u' tệ ', ' poor ': u' tệ ', 'ib': u' nhắn tin ', 'rep': u' trả lời ', u'fback': ' feedback ',
            'fedback': ' feedback ', u' bill ': u' hóa đơn ', u' chuan ': u' chuẩn ',
            u' chuản ': u' chuẩn ', u' cx ': u' cũng ', u' cg ': u' cũng ', u' cũg ': u' cũng ', u' cugx ': u' cũng ',
            u' thỏa mái ': u' thoải mái ', u' thoai mai ': u' thoải mái ',
            u' ap ': u' ứng dụng ', u' app ': u' ứng dụng ', u' sài ': u' xài ', u' tõ ràng ': u'rõ ràng',
            # normalize rating stars
            '5 sao': ' 5star ', '5 star': ' 5star ', '5sao': ' 5star ', '4 star': ' 4star ', '4 sao': ' 4star ',
            '3sao': ' 3star ', '3 star': ' 3star ', '3 sao': ' 3star ', '3sao': ' 3star ',
            'starstarstarstarstar': ' 5star ', '1 sao': ' 1star ', '1sao': ' 1star ', '2 sao': ' 2star ',
            '2sao': ' 2star ',
            '2 starstar': ' 2star ', '1star': ' 1star ', }

        for k, v in replace_list.items():
            row = row.replace(k, v)

        row = row.strip()
        return row
    else:
        return ''

# tokenizer vietnamese
def tokenizer(row):
    if isinstance(row, str):
        return ViTokenizer.tokenize(row)
    else:
        return ''

# process data to predictable format
def predict_process_data(data):
    # Add 'content' column
    data_frame = pd.DataFrame(data, columns=['content'])

    # Drop row contain NaN in 'content' column
    data_frame = data_frame.dropna(subset=['content'])

    # Apply standardization
    data_frame['content'] = data_frame['content'].apply(standardize_data)

    # Apply tokenizer
    data_frame['content'] = data_frame['content'].apply(tokenizer)

    return data_frame

'''
    ------------------- End - Process data -------------------
'''



'''
    ------------------- Start - Predict -------------------
'''
# load TF-IDF model
tf_file_path = os.path.join(os.path.dirname(__file__), 'model\\trained_model', 'tfidf_vectorizer.pk')
#Load TF-IDF weight
tf_idf = pickle.load(open(tf_file_path, 'rb'))

def load_processed_data(prod_id):
    try:
        file_path = os.path.join(get_directory('data'), f'{prod_id}_origin_reviews.csv')
        data = pd.read_csv(file_path)
    except Exception as e:
        print(e)
        return
    
    # process data
    data = predict_process_data(data)

    # # predict
    # load predict model
    sav_file_path = os.path.join(os.path.dirname(__file__), 'model\\trained_model', 'naive_bayes_model.sav')
    pl = pickle.load(open(sav_file_path, "rb"))
    
    # load data to predict
    X_test_tfidf = tf_idf.transform(data['content'])
    y_pred = pl.predict(X_test_tfidf)

    cols = ['content', 'label']
    processed_data = pd.DataFrame(columns=cols)
    processed_data['label'] = y_pred
    processed_data['content'] = data
    
    return processed_data

# 
def get_label_counts(processed_data):
    # Classify labels into corresponding groups(Positive, Negative, Neutral)
    processed_data['label_group'] = processed_data['label'].apply(lambda x: 'Positive' if x == 5.0 else ('Negative' if x in [1.0, 2.0] else 'Neutral'))

    # Count reviews each group
    label_counts = processed_data['label_group'].value_counts()
    print(label_counts)

    pos_count = label_counts.get('Positive', 0)
    neg_count = label_counts.get('Negative', 0)
    neu_count = label_counts.get('Neutral', 0)
    
    # Print Positive, Negative, Neutral count
    print("Positive reviews  😊: ", pos_count)
    print("Negative reviews  😡: ", neg_count)
    print("Neutral reviews   😐: ", neu_count)
    
    return pos_count, neg_count, neu_count


#  Draw pie_chart
def draw_pie_chart(pos_count, neg_count, neu_count):
    pie_chart = np.array([pos_count, neg_count, neu_count])
    mylabels = ["Positive", "Negative", "Neutral"]

    if np.sum(pie_chart) == 0:
        print("No data to create pie chart.")
    else:
        
        plt.pie(pie_chart, labels=mylabels, shadow=True, startangle=90, autopct='%1.1f%%')
        plt.tight_layout()  # Automatically adjust layout to reduce excess white space

        img_path = os.path.join('img', 'pie_chart.png')  
        plt.savefig(img_path)
        plt.close()
        
    print(f'Pie chart created at: {img_path}')

# ⭐
def predict_rating(pos_count, neg_count, neu_count):
    total_reviews = pos_count + neg_count + neu_count
    rating = float((pos_count * 5 + neg_count * 1.5 + neu_count * 3.5) / (total_reviews))
    print_rating_suggestion(round(rating, 1))

def print_rating_suggestion(rating):
    print("Rating Predict: ", rating, "⭐")
    if rating > 4:
        print("Good! You can buy it! 👌👌👌")
    elif rating > 2 and rating <= 4:
        print("Please check it carefully! ❗❗❗")
    elif rating <= 2:
        print("Bad! 👎👎👎")
    

'''
    ------------------- End - Suggest -------------------
'''




'''
    ------------------- Start - Analysis -------------------
'''
wc_stop_ws = [u'rằng', u'thì', u'là', u'mà', u'mình', u'bé', u'cho', u'chỉ', u'em', u'và', u'gì', u'này', u'các',
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
def create_word_clouds(test_data):

    pos_word = test_data['content'].loc[(test_data['label'] >= 4) & (test_data['label'] <= 5)]
    neg_word = test_data['content'].loc[(test_data['label'] >= 1) & (test_data['label'] <= 2)]
    neu_word = test_data['content'].loc[test_data['label'] == 3]

    print("Positive words:")
    print(pos_word)
    print("Negative words:")
    print(neg_word)
    print("Neutral words:")
    print(neu_word)

    tfidf_pos = TfidfVectorizer(ngram_range=(1, 5), min_df=0.01, max_df=0.99, stop_words=wc_stop_ws, max_features=100,
                                sublinear_tf=True, smooth_idf=True)
    tfidf_neg = TfidfVectorizer(ngram_range=(1, 5), min_df=0.01, max_df=0.99, stop_words=wc_stop_ws, max_features=100,
                                sublinear_tf=True, smooth_idf=True)
    tfidf_neu = TfidfVectorizer(ngram_range=(1, 5), min_df=0.01, max_df=0.99, stop_words=wc_stop_ws, max_features=100,
                                sublinear_tf=True, smooth_idf=True)

    tfidf_matrix_pos = create_tfidf_matrix(tfidf_pos, pos_word)
    tfidf_matrix_neg = create_tfidf_matrix(tfidf_neg, neg_word)
    tfidf_matrix_neu = create_tfidf_matrix(tfidf_neu, neu_word)

    feature_names_pos = tfidf_pos.get_feature_names_out() if tfidf_matrix_pos is not None else []
    feature_names_neg = tfidf_neg.get_feature_names_out() if tfidf_matrix_neg is not None else []
    feature_names_neu = tfidf_neu.get_feature_names_out() if tfidf_matrix_neu is not None else []

    create_word_cloud(feature_names_pos, "Positive")
    create_word_cloud(feature_names_neg, "Negative")
    create_word_cloud(feature_names_neu, "Neutral")


def create_tfidf_matrix(vectorizer, word_list):
    if word_list.empty:
        return None
    else:
        return vectorizer.fit_transform(word_list)

# common word in reviews data about specify product
def save_feature_names_to_txt(feature_names, file_name):
    file_path = os.path.join('analyze', file_name+'.txt')
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for feature in feature_names:
                file.write(f"{feature}\n")
        print(f"Feature names saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving feature names: {e}")

def create_word_cloud(feature_names, sentiment):
    print(f"{sentiment} Review :")
    # print('cwc feature_names: ',feature_names)
    save_feature_names_to_txt(feature_names, f'{sentiment} Reviews')
    if len(feature_names) > 0:
        try: 
            cloud = " ".join(feature_names)
            plt.figure(figsize=(12, 6))
            plt.title(f"WordCloud for {sentiment} Reviews")
            word_cloud = (wordcloud.WordCloud(max_words=30, background_color="black",
                                            width=1200, height=600, mode="RGB").generate(str(cloud)))
            plt.axis("off")
            plt.imshow(word_cloud)

            img_path = os.path.join('img',f'{sentiment}_word_cloud.png')
            plt.savefig(img_path)  
            print(f"{sentiment} WordCloud saved at {img_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    print("--------------------------------------")

'''
    ------------------- Start - Analysis -------------------
'''





