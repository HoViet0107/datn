import json

import requests



_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Guest-Token': '5wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'vi',
}

_COOKIES = {
    # 'TIKI_RECOMMENDATION':'c2b76cc59f1d63ef5aaa9e9883de3fdc',
    'TKSESSID': '16f55fcbd35a5cdb883de25536242ee4',
    'TOKENS': '{%22access_token%22:%225wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1870359973526%2C%22guest_token%22:%225wy6mHsTRpjA0Z89PaCcVSDLOxNegEtf%22}',
    'delivery_zone': 'Vk4wMzQwMjQwMTM=',
    '_trackity': '7e5dcab4-fa5f-57c7-59c0-7a428c155263'
}


def crawl_all_reviews(product_id):
    all_reviews = []
    all_labels = []

    limit = 20  # Giới hạn số lượng đánh giá mỗi lần gọi
    headers = _HEADERS
    cookies = _COOKIES

    page = 1
    while True:
        TIKI_REVIEWS_API = f'https://tiki.vn/api/v2/reviews?limit=20&include=comments,contribute_info,attribute_vote_summary&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={page}&product_id={product_id}&seller_id=1'
        print(TIKI_REVIEWS_API)
        response = requests.get(TIKI_REVIEWS_API, headers=headers, cookies=cookies)
        res_body = json.loads(response.content)

        reviews_count = res_body['reviews_count']
        if reviews_count == 0:
            print(f'Not has comment!')
            break
        print('reviews_count: ', reviews_count)
        last_page = res_body['paging']['last_page']
        print('last_page: ', last_page)

        reviews = res_body['data']
        for review in reviews:
            if review['content'] != "" or review['content'].strip():
                all_reviews.append(review['content'])
                all_labels.append(review['rating'])
            elif review['content'] == "" and review['rating'] == 5:
                all_reviews.append("Cực kì hài lòng")
                all_labels.append(5)
            elif review['content'] == "" and review['rating'] == 4:
                all_reviews.append("Hài lòng")
                all_labels.append(4)
            elif review['content'] == "" and review['rating'] == 3:
                all_reviews.append("Bình thường")
                all_labels.append(3)
            elif review['content'] == "" and review['rating'] == 2:
                all_reviews.append("Không hài lòng")
                all_labels.append(2)
            elif review['content'] == "" and review['rating'] == 1:
                all_reviews.append("Rất không hài lòng")
                all_labels.append(1)

        page += 1

        if page > last_page:
            break

    return all_reviews, all_labels


all_reviews0, all_labels0 = crawl_all_reviews(97551646)
print(all_reviews0)
print(all_labels0)

#  xem lại link api. gọi ra không giống nhau