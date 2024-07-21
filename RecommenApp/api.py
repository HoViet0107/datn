import os

from flask import Flask, request, jsonify
import csv
import pandas as pd

import apiFunc
import crawl

app = Flask(__name__)

FIXED_FILE_PATH = r"C:\Users\ADMIN\Documents\EDISK\nam5\datn\SERVER_DATA"

reviews_count = 0
# Route để nhận request POST từ phía C#
@app.route('/api/get-reviews', methods=['POST'])
def get_data():
    # Lấy dữ liệu từ request JSON
    data = request.json
    prod_id = data['prod_id']  # Đây là key cần trích xuất từ JSON
    spid = data['spid']

    # Lấy và lưu dữ liệu
    global reviews_count
    reviews_count = apiFunc.get_reviews(prod_id, spid)

    # Trả về một response cho phía C#
    return jsonify({'message': 'Get reviews Success!'})


# predict
@app.route('/api/draw_pie_chart', methods=['POST'])
def predict():
    data = request.json
    prod_id = data['prod_id']

    processed_data = apiFunc.predict(prod_id)
    df_processed_data = pd.DataFrame(processed_data)

    file_path = os.path.join(apiFunc.get_directory('data'), f'{prod_id}_processed_reviews.csv')
    df_processed_data.to_csv(file_path, index=False)
    # apiFunc.save_to_csv(processed_data,f'${prod_id}_processed_reviews.csv','data')

    pos_count, neg_count, neu_count = apiFunc.get_label_counts(processed_data)
    apiFunc.print_label_counts(pos_count, neg_count, neu_count)
    pie_path = 'C:\\Users\\ADMIN\\Documents\\EDISK\\nam5\\datn\\UI\\RecommenApp\\img\\default.png'
    try:
        pie_path = apiFunc.draw_pie_chart(pos_count, neg_count, neu_count)  # Đường dẫn đầy đủ của thư mục img
    except Exception as e:
        print(e)
    # print(pie_path)
    # phan tich
    rating = apiFunc.predict_rating(pos_count, neg_count, neu_count)

    try:
        apiFunc.create_word_clouds(processed_data)
    except Exception as e:
        print(e)
    # Chuyển đổi các giá trị thành kiểu dữ liệu Python gốc trước khi jsonify
    return jsonify(
        pie_path=pie_path,
        pos_count=int(pos_count),
        neu_count=int(neu_count),
        neg_count=int(neg_count),
        rating=float(rating)
    )


# @app.route('/api/crawl', methods=['POST'])
# def crawl_data():
#     cl_request = request.json
#
#     cate_name = cl_request['cate_name']
#     prod_ids = []
#     if cate_name == 'dien-tu-dien-lanh':
#         prod_ids = crawl.get_prod_ids(4221,'dien-tu-dien-lanh')
#
#     if cate_name == 'do-choi-me-be':
#         prod_ids = crawl.get_prod_ids(2549,'do-choi-me-be')
#     print(prod_ids)
#     all_reviews = []
#     all_labels = []
#     for prod_id in prod_ids:
#         all_reviews, all_labels = crawl.crawl_all_reviews(prod_id)
#
#     # lưu data lấy được vào csv
#     data_csv = crawl.save_crawled_reviews(all_reviews, all_labels, cate_name)
#     # xử lý data
#     processed_dt_csv_df = crawl.process_crawl_data(data_csv)
#
#     # lưu dữ liệu đã xử lý thành file csv
#     file_path = os.path.join(apiFunc.get_directory('data'), f'{cate_name}_processed_data.csv')
#     processed_dt_csv_df.to_csv(file_path, index=False)
#     print(processed_dt_csv_df)
#
#     return jsonify({'message': 'Crawl success!'})


if __name__ == '__main__':
    app.run(debug=True)
