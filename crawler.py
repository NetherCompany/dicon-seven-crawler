from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import os
import csv
import boto3

# Chromeのオプションを設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ヘッドレスモードで起動（GUIを使用しない）
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 対象のURL群
product_urls = {
    "onigiri": "https://www.sej.co.jp/products/a/onigiri/",
    "sushi": "https://www.sej.co.jp/products/a/sushi/",
    "bento": "https://www.sej.co.jp/products/a/bento/",
    "sandwich": "https://www.sej.co.jp/products/a/sandwich/",
    "bread": "https://www.sej.co.jp/products/a/bread/",
    "donut": "https://www.sej.co.jp/products/a/donut/",
    "men": "https://www.sej.co.jp/products/a/men/",
    "pasta": "https://www.sej.co.jp/products/a/pasta/",
    "gratin": "https://www.sej.co.jp/products/a/gratin/",
    "dailydish": "https://www.sej.co.jp/products/a/dailydish/",
    "salad": "https://www.sej.co.jp/products/a/salad/",
    "sweets": "https://www.sej.co.jp/products/a/sweets/",
    # アイス、ホットスナック、おでん、中華まんはページ構造が違うので別で対応する
}

# ChromeのWebDriverを作成
driver = webdriver.Chrome(options=chrome_options)

for type, url in product_urls.items():
    # Webページにアクセス
    driver.get(url)

    # 要素を取得してデータを作成
    items = driver.find_elements("xpath", "//div[contains(@class, 'item_ttl')]")
    result = [['type', 'name', 'url']]
    for item in items:
        # href属性の値を取得
        a_element = item.find_element("xpath", ".//a")
        href = a_element.get_attribute("href")
        result.append([type, item.text, href])

    # CSVファイルを作成
    filename = type + '.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(result)

    # s3にアップロード
    s3 = boto3.resource('s3', endpoint_url=os.environ.get('LOCALSTACK_ENDPOINT_URL'))
    bucket = s3.Bucket('dicon-seven-crawler-url-bucket')
    timestamp = datetime.now() + timedelta(hours=9)
    timestamp_str = timestamp.strftime("%Y-%m-%d_%H:%M:%S")
    bucket.upload_file(filename, timestamp_str + '/' + filename)

# WebDriverを終了
driver.quit()
