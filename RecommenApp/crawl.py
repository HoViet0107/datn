# import os
# import csv
# import pandas as pd
# import requests
# import json
# import apiFunc
#
#
# _HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#     'X-Guest-Token': '5wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf',
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Accept-Language': 'vi',
# }
#
# # _PARAMS = {
# #           'limit': '{limit}',
# #           'include': 'comments,contribute_info,attribute_vote_summary',
# #           'sort': f'stars|{star}',
# #           'page': {page},
# #           'product_id': {product_id},
# # }
#
# _COOKIES = {
#     # 'TIKI_RECOMMENDATION':'c2b76cc59f1d63ef5aaa9e9883de3fdc',
#     'TKSESSID': '16f55fcbd35a5cdb883de25536242ee4',
#     'TOKENS': '{%22access_token%22:%225wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1870359973526%2C%22guest_token%22:%225wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf%22}',
#     'delivery_zone': 'Vk4wMzQwMjQwMTM=',
#     '_trackity': '7e5dcab4-fa5f-57c7-59c0-7a428c155263'
# }
#
#
# # lấy product id trong url
# def get_prod_id(url):
#     prod_id = url.split('-p')[-1].split('.html')[0]
#     return prod_id
#
# # --------- start -------------
# # lấy prod_ids và spid của từng danh mục
# def get_spid(url_path):
#   return url_path.split('spid=')[1].split('.html?')[0]
#
#
# def get_prod_ids(cate_id, cate_name, stop):
#     prod_ids = []
#     spid = []
#     limit = 40
#     page = 1
#     # TIKI_PRODUCT_API = f'https://tiki.vn/api/personalish/v1/blocks/listings?category={cate_id}&page={page}&urlKey={cate_name}&limit={limit}'
#     headers = _HEADERS
#     cookies = _COOKIES
#     cur_page = stop
#     while True:
#         TIKI_PRODUCT_API = f'https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&version=home-persionalized&trackity_id=7e5dcab4-fa5f-57c7-59c0-7a428c155263&category={cate_id}&page={page}&urlKey={cate_name}'
#         print(page, ' - ', cur_page)
#         print(TIKI_PRODUCT_API)
#         if page > cur_page:
#             break
#
#         response = requests.get(TIKI_PRODUCT_API.format(cate_id, page, cate_name), headers=headers, cookies=cookies)
#         res_body = json.loads(response.content)
#
#         if 'data' not in res_body or not res_body['data']:
#             break  # Dừng vòng lặp nếu không còn sản phẩm
#
#         products = res_body['data']
#         for product in products:
#             prod_ids.append(product['id'])
#             spid.append(get_spid(product['url_path']))
#
#         page += 1
#
#     return prod_ids, spid
#
# # ------------end------------
#
#
# # ----------------------------------------- #
# # ----- start - crawl data ------#
# def crawl_all_reviews(product_id, spid):
#     all_reviews = []
#     all_labels = []
#
#     limit = 20  # Giới hạn số lượng đánh giá mỗi lần gọi
#     headers = _HEADERS
#     cookies = _COOKIES
#     page = 1
#     print(product_id, ' - ', spid)
#     print(f'https://tiki.vn/api/v2/reviews?limit=20&include=comments,contribute_info,attribute_vote_summary&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={page}&spid={spid}&product_id={product_id}&seller_id=1')
#     while True:
#         TIKI_REVIEWS_API = f'https://tiki.vn/api/v2/reviews?limit=20&include=comments,contribute_info,attribute_vote_summary&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={page}&spid={spid}&product_id={product_id}&seller_id=1'
#
#         response = requests.get(TIKI_REVIEWS_API, headers=headers, cookies=cookies)
#         res_body = json.loads(response.content)
#
#         reviews_count = res_body['reviews_count']
#         if reviews_count == 0:
#             print(f'Not has comment!')
#             break
#         last_page = res_body['paging']['last_page']
#         print('reviews_count: ', reviews_count, 'củ_page: ', page, 'last_page: ', last_page, '   -/-   ', end='')
#
#         reviews = res_body['data']
#         for review in reviews:
#             if review['content'] != "" or review['content'].strip():
#                 all_reviews.append(review['content'])
#                 all_labels.append(review['rating'])
#             elif review['content'] == "" and review['rating'] == 5:
#                 all_reviews.append("Cực kì hài lòng")
#                 all_labels.append(5)
#             elif review['content'] == "" and review['rating'] == 4:
#                 all_reviews.append("Hài lòng")
#                 all_labels.append(4)
#             elif review['content'] == "" and review['rating'] == 3:
#                 all_reviews.append("Bình thường")
#                 all_labels.append(3)
#             elif review['content'] == "" and review['rating'] == 2:
#                 all_reviews.append("Không hài lòng")
#                 all_labels.append(2)
#             elif review['content'] == "" and review['rating'] == 1:
#                 all_reviews.append("Rất không hài lòng")
#                 all_labels.append(1)
#
#         page += 1
#
#         if page > last_page:
#             break
#
#     return all_reviews, all_labels
# # ----- end - crawl data ------#
# # ----------------------------------------- #
#
#
# # ------------------ start ---------------------
# # lấy các reviews của các sản phẩm từ danh mục do-choi-me-be
# mbprods, mbspid = get_prod_ids(2549,'do-choi-me-be',1)
# # Tạo DataFrame từ danh sách
# _1p = pd.DataFrame(mbprods, columns=['prod_id'])
# _2p = pd.DataFrame(mbspid, columns=['spid'])
#
# # Gộp hai DataFrame lại thành một
# _p = pd.concat([_1p, _2p], axis=1)
#
# # Loại bỏ các hàng trùng lặp dựa trên cột 'prod_id'
# _p_unique = _p.drop_duplicates(subset=['prod_id'])
#
# # In ra DataFrame mới
# # print(_p_unique)
# all_reviews = []
# all_labels = []
# for index, row in _p_unique.iterrows():
#     reviews, labels = crawl_all_reviews(row['prod_id'], row['spid'])
#     all_reviews.extend(reviews)
#     all_labels.extend(labels)
#
# reviews_df = pd.DataFrame(all_reviews, columns=['content'])
# labels_df = pd.DataFrame(all_labels, columns=['label'])
# ori_data = pd.concat([reviews_df, labels_df], axis=1)
# _unique_data = ori_data.drop_duplicates(subset=['content'])
#
# # Lưu vào file CSV
# csv_file = '/data/MB_sub_origin_reviews_data.csv'
# _unique_data.to_csv(csv_file, index=False, encoding='utf-8')
# # ----------------- end -----------------
#
#
# # ------------ start ---------------
# # lấy các reviews của các sản phẩm từ danh mục dien-tu-dien-lanh
# dtprods, dtspid = get_prod_ids(4221,'dien-tu-dien-lanh',10)
# # Tạo DataFrame từ danh sách
# _dt1p = pd.DataFrame(dtprods, columns=['prod_id'])
# _dt2p = pd.DataFrame(dtspid, columns=['spid'])
#
# # Gộp hai DataFrame lại thành một
# _dtp = pd.concat([_dt1p, _dt2p], axis=1)
#
# # Loại bỏ các hàng trùng lặp dựa trên cột 'prod_id'
# __dt_unique = _dtp.drop_duplicates(subset=['prod_id'])
#
# # In ra DataFrame mới
# print(__dt_unique)
#
# dt_all_reviews = []
# dt_all_labels = []
# for index, row in __dt_unique.iterrows():
#     reviews, labels = crawl_all_reviews(row['prod_id'], row['spid'])
#     dt_all_reviews.extend(reviews)
#     dt_all_labels.extend(labels)
#
# # lưu vào csv
# dt_reviews_df = pd.DataFrame(dt_all_reviews, columns=['content'])
# dt_labels_df = pd.DataFrame(dt_all_labels, columns=['label'])
# dt_ori_data = pd.concat([dt_reviews_df, dt_labels_df], axis=1)
# _dt_unique_data = dt_ori_data.drop_duplicates(subset=['content'])
#
# # Lưu vào file CSV
# csv_file = '/content/gdrive/MyDrive/ColabNotebooks/content/DT_sub_origin_reviews_data.csv'
# _dt_unique_data.to_csv(csv_file, index=False, encoding='utf-8')