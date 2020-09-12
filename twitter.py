# coding: utf-8
import json
import csv
import sys
import MeCab
import re
import configparser
from requests_oauthlib import OAuth1Session
from datetime import datetime
from pytz import timezone

# TwitterAPI URL
API_URL = "https://api.twitter.com/1.1/search/tweets.json"

# Confファイルパス
CONF_PATH = "./conf/config.ini"

# 認証情報
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""

# 入出力ファイル設定
INPUT_FILE_PATH = "./data/input/keywords_list/"
INPUT_FILE_EXTENSION = ".txt"
OUTPUT_FILE_PATH = "./data/output/"
OUTPUT_FILE_EXTENSION = ".txt"

# メイン処理
def main():
    load_config()
    check_args()
    keywords = load_keyword_from_text()
    for keyword in keywords:
        tweets = keyword_search(keyword)
        pickup_from_data(tweets,keyword)

# 設定をロード
def load_config():
    conf = configparser.ConfigParser()
    conf.read(CONF_PATH)

    # 認証鍵パラメータを設定
    global CONSUMER_KEY
    global CONSUMER_SECRET
    global ACCESS_TOKEN
    global ACCESS_SECRET
    CONSUMER_KEY = conf["TwitterAuthKey"]["consumer_key"]
    CONSUMER_SECRET = conf["TwitterAuthKey"]["consumer_secret"]
    ACCESS_TOKEN = conf["TwitterAuthKey"]["access_token"]
    ACCESS_SECRET = conf["TwitterAuthKey"]["access_secret"]

# 引数チェック
def check_args():
    if len(sys.argv) == 2:
        return
    else:
        print("[ERROR] Not enough arguments. Please pass the target keyword as an argument.")
        sys.exit(-1)

# キーワード一覧をファイルから読み込む
def load_keyword_from_text():
    f = open(INPUT_FILE_PATH + sys.argv[1] + INPUT_FILE_EXTENSION)
    keywords = f.read().split()
    f.close()
    return keywords

# データ出力
def data_output(data):
    with open(OUTPUT_FILE_PATH + sys.argv[1] + OUTPUT_FILE_EXTENSION, "a") as f:
                print(json.dumps(data, ensure_ascii=True), file=f)

# キーワード検索
def keyword_search(keyword):
    
    # 検索条件設定
    params = {
        "q": keyword,
        "exclude": "retweets",
        "lang": "ja",
        "result_type": "recent",
        "locate": "ja",
        "lang": "ja",
        "count": "1",
        "include_entitles": False
    }

    # 検索実行
    oauth1 = create_oauth1_session()
    res = oauth1.get(API_URL, params = params)
    if res.status_code != 200:
        print("[Error] Twitter API HTTP Response error : " + str(res.status_code))
    tweets = json.loads(res.text)
    return tweets 

# OAuth1認証
def create_oauth1_session():
    return OAuth1Session(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET)

# 検索結果から必要な情報のみ抽出
def pickup_from_data(tweets,keyword):

    if tweets["statuses"] != None:
        for tweet in tweets["statuses"]:
            tweet_data = {} 
            tweet_data["tweet_id"] = tweet["id_str"] # ツイートID
            tweet_data["tweet_date"] = convert_date_format(tweet["created_at"]) # ツイート日時
            tweet_data["tweet_text"] = tweet["text"] # ツイートテキスト
            tweet_data["tweet_words"] = mecab_analyze(tweet["text"]) # ツイートテキスト要素（名詞）
            tweet_data["user_id"] = tweet["user"]["id_str"] # ユーザID
            tweet_data["user_name"] = tweet["user"]["screen_name"] # ユーザ名
            tweet_data["search_word"] = keyword # 検索ワード
            data_output(tweet_data)
    return

def convert_date_format(date):
    utc = datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y")
    jst = utc.astimezone(timezone("Asia/Tokyo"))
    jst_str = datetime.strftime(jst, "%Y-%m-%d %H:%M:%S")
    return jst_str

# mecabによるワード解析の実行
def mecab_analyze(sentences):

    words = []

    # 事前に、除外対象ワードを文章から取り除く
    sentences = re.sub(r"(http|https)://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?", "",sentences)
    sentences = re.sub(r"[!-~]", "",sentences)
    sentences = re.sub(r"[︰-＠]", "",sentences)
    sentences = re.sub("さん", "",sentences)
    sentences = re.sub("ちゃん", "",sentences)
    sentences = re.sub("様", "",sentences)
    
    # mecabの解析を実行する
    mecab = MeCab.Tagger("-Ochasen")
    node = mecab.parseToNode(sentences)
    
    while node:
        if node.feature.split(",")[0] == "名詞":
            words.append(str(node.surface))
        node = node.next

    return words

if __name__ == '__main__':
    main()

