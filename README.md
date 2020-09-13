# README

## 動作確認済み環境

```bash
$ cat /etc/redhat-release 
CentOS Linux release 8.1.1911 (Core) 
$ python3 --version
Python 3.6.8
```

その他、python内で使用する各種ライブラリは適宜pipコマンド等でインストールしてください。

## ディレクトリ構成

```bash
$ tree
.
├── README.md
├── conf
│   └── config.ini
├── data
│   ├── input
│   │   └── keywords_list
│   │       └── hinatazaka46.txt
│   └── output
│       └── hinatazaka46.txt

└── twitter.py
```

## 環境構築手順

以下、コマンドを実行する

```bash
$ git clone https://github.com/k-kusaka/python-twitter-keyword-search.git
$ mkdir ./python-twitter-keyword-search/data/output
$ mkdir ./python-twitter-keyword-search/conf
$ vi ./python-twitter-keyword-search/conf/config.ini
```

```ini:config.ini
[TwitterAuthKey]
consumer_key = XXXXXXXXXXXXXXXXXX
consumer_secret = XXXXXXXXXXXXXXXXXX
access_token = XXXXXXXXXXXXXXXXXX
access_secret = XXXXXXXXXXXXXXXXXX
```

※ 各種keyの値は、適宜変更してください

## 実行方法

```bash
$ python3 twitter.py hinatazaka46
```

なお、keywords_listディレクトリ配下に、"hinatazaka46.txt"以外の検索キーワードが含まれたキーワードテキストを配置し、twitter.py実行時の引数とする文字列をファイル名（拡張子無し）で実行することで、他のキーワードで検索してくることができます。