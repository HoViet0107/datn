import os
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

import apiFunc


def train_model(train_data, test_data):
    # X_train = train_data['content']
    # y_train = train_data['labels']
    # X_test = test_data['content']
    # y_test = test_data['labels']

    # Chia dữ liệu thành tập huấn luyện và tập kiểm thử
    train_data, test_data = train_test_split(train_data, test_size=0.2, random_state=42)

    X_train = train_data['content']
    y_train = train_data['labels']
    X_test = test_data['content']
    y_test = test_data['labels']

    # Loại bỏ các giá trị NaN nếu còn tồn tại
    mask_train = X_train.notna() & y_train.notna()
    X_train = X_train[mask_train]
    y_train = y_train[mask_train]

    mask_test = X_test.notna() & y_test.notna()
    X_test = X_test[mask_test]
    y_test = y_test[mask_test]

    # Khởi tạo TF-IDF Vectorizer và biến đổi dữ liệu
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    # Lưu TfidfVectorizer để sử dụng sau này
    tfidt_path = os.path.join('model', 'tfidf_vectorizer.pk')
    with open(tfidt_path, 'wb') as f:
        pickle.dump(tfidf_vectorizer, f)

    # Huấn luyện mô hình Naive Bayes
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)

    # Dự đoán trên tập kiểm thử
    y_pred = model.predict(X_test_tfidf)

    # Tính toán độ chính xác và in ra
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

    # Lưu mô hình đã huấn luyện
    model_path = os.path.join('model', 'naive_bayes_model.sav')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)


train_file_path = os.path.join('model', 'train_data.csv')
train_data = pd.read_csv(train_file_path)

test_file_path = os.path.join('model', 'test_data.csv')
test_data = pd.read_csv(test_file_path)

# huấn luyện mô hình
train_model(train_data, test_data)


# xử lý dữ liệu trước khi huấn luyện
# ori_file_path = os.path.join('model', 'ori_train_data.csv')
# data = pd.read_csv(ori_file_path)
# processed_data = apiFunc.predict_process_data(data)

train_file_path = os.path.join('model', 'train_data.csv')
# # Kiểm tra sự tồn tại của tệp và xử lý dữ liệu
# if os.path.exists(train_file_path):
#     data = pd.read_csv(train_file_path)

# data = pd.read_csv(train_file_path)
# processed_data.to_csv(train_file_path, index=False, encoding='utf-8')
