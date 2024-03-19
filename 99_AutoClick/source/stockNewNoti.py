# -*- coding: utf-8 -*-

# seleniumの必要なライブラリをインポート
import mysql.connector
import requests
import slackweb
import time
import datetime
import json
import jpholiday
import schedule

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


#　現在日時
dt_now = datetime.datetime.now()
dt_now_text = dt_now.strftime('%Y年%m月%d日 %H時%M分')


#定数定義
slack_token = "xoxb-6810543998997-6798913149431-XVrloL5YiY9s5lNeOo5I6oHZ"
slack_channel_name = "stock_news" 
slack_post_url = 'https://slack.com/api/chat.postMessage'
stock_news_content = "<!channel>\n" + dt_now_text + " の通知です。 \n 新しいマーケットニュースがありましたので、ご確認ください。 \n <https://www.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_DataStoreID=DSWPLETmgR001Control&_ActionID=DefaultAID&burl=iris_news&cat1=market&cat2=news&dir=tl1-news%7Ctl2-mkt%7Ctl3-jpn%7Ctl4-reuters%7Ctl9-0&file=index.html&getFlg=on | PC版>\n <https://s.sbisec.co.jp/smweb/market/marketNewsList.do? | Mobile版>"
slack_username = 'Notification bot'


# 最初１ページ目の登録用データ作成
def createDataPage1():
    url = 'https://site2.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_DataStoreID=DSWPLETmgR001Control&_ActionID=DefaultAID&burl=iris_news&cat1=market&cat2=news&dir=tl1-news%7Ctl2-mkt%7Ctl3-jpn%7Ctl4-reuters%7Ctl9-0&file=index.html&getFlg=on'
    dt_now = datetime.datetime.now()
    dt_now_text = dt_now.strftime('%Y/%m/%d %H:%M:%S')
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH, "//img[@src='https://sbisec.akamaized.net/sbisec/images/base02/b_koushin.gif']") 
    #マーケット 国内ニュース欄だけが取得対象とする
    targetDiv = driver.find_elements(By.CLASS_NAME, "md-box-list-03")
    for targetListLink in targetDiv:
        targetlink = targetListLink.find_elements(By.TAG_NAME, "a")
    for link in targetlink:
        createData = "'" + link.text +"','"+ link.get_attribute("href")+"','0','0','" + dt_now_text + "'"
        insertDB(createData)
        
# ２ページ目の登録用データ作成
def createDataPage2():
    url = 'https://site2.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_DataStoreID=DSWPLETmgR001Control&_ActionID=DefaultAID&burl=iris_news&cat1=market&cat2=news&file=index.html&getFlg=on&dir=tl1-news%7Ctl2-mkt%7Ctl3-jpn%7Ctl4-reuters%7Ctl9-30'
    dt_now = datetime.datetime.now()
    dt_now_text = dt_now.strftime('%Y/%m/%d %H:%M:%S')
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)
    #マーケット 国内ニュース欄だけが取得対象とする
    targetDiv = driver.find_elements(By.CLASS_NAME, "md-box-list-03")
    for targetListLink in targetDiv:
        targetlink = targetListLink.find_elements(By.TAG_NAME, "a")
    for link in targetlink:
        createData = "'" + link.text +"','"+ link.get_attribute("href")+"','0','0','" + dt_now_text + "'"
        insertDB(createData)
# DBにデータ登録
def insertDB(createData):
    cnx = None
    try:
        # 接続する
        cnx = mysql.connector.connect(
        user='root',  # ユーザー名
        password='password',  # パスワード
        host='localhost',  # ホスト名(IPアドレス）
        database='python-study'  # データベース名
        )
        
        # カーソルを取得する
        cursor = cnx.cursor()
        
        # 登録sql実行
        insertSql = "INSERT INTO news_url_tbl (text,url,user_check_flg,del_flg,create_datetime) VALUES (" + createData + ")"
        #print("実行sql：　" + insertSql)
        cursor.execute(insertSql)
        
        cnx.commit()
        # 接続を閉じる
        cursor.close()
    except Exception as e:
        # エラーが発生する時にエラー内容を出力する
        print(f"エラー発生しました: {e}")
    finally:
        if cnx is not None and cnx.is_connected():
            # 接続を閉じる
            cnx.close()
# 古いデータを論理削除フラグ更新
def updateDelFlg():
    cnx = None
    try:
        # 接続する
        cnx = mysql.connector.connect(
        user='root',  # ユーザー名
        password='password',  # パスワード
        host='localhost',  # ホスト名(IPアドレス）
        database='python-study'  # データベース名
        )
        
        # カーソルを取得する
        cursor = cnx.cursor()

        # 登録sql実行
        maxId = 0
        getMaxIdSql = "select max(id) as maxId from news_url_tbl;"
        cursor.execute(getMaxIdSql)
        for row in cursor.fetchall():
            maxId = row[0]
        maxIdInt = 0
        if int(maxId) > 120:
            maxIdInt = int(maxId) - 120
        updateDelFlgSql = "UPDATE news_url_tbl SET del_flg = 1 WHERE del_flg != 1 and  id <= " + str(maxIdInt)
        print(updateDelFlgSql)
        cursor.execute(updateDelFlgSql)
        cnx.commit()
        # 接続を閉じる
        cursor.close()
    except Exception as e:
        # エラーが発生する時にエラー内容を出力する
        print(f"エラー発生しました: {e}")
    finally:
        # 接続を閉じる
        cnx.close()
# 通知内容作成
def createStockNewsNoti():
    try:
        # Slackで通知する際に必要なデータを設定する
        data = {
            'token': slack_token,
            'channel': slack_channel_name,
            'text': stock_news_content,
            'username': slack_username
        }
        
        # POSTメソッドで送信する
        response = requests.post(slack_post_url, data=data)
    except Exception as e:
        print(e)

# 通知判断
def isNoti():
    cnx = None
    try:
        # 接続する
        cnx = mysql.connector.connect(
        user='root',  # ユーザー名
        password='password',  # パスワード
        host='localhost',  # ホスト名(IPアドレス）
        database='python-study'  # データベース名
        )
        
        # カーソルを取得する
        cursor = cnx.cursor()

        # データ削除sql実行
        delData = "DELETE FROM news_url_tbl WHERE del_flg = 1"
        cursor.execute(delData)
        cnx.commit()
        
        getNewCount = "SELECT text,count(text) FROM news_url_tbl where del_flg != 1 GROUP BY text HAVING count(text) = 1;"
        cursor.execute(getNewCount)
        if len(cursor.fetchall()) >= 1:
            createStockNewsNoti()
        # 接続を閉じる
        cursor.close()
    except Exception as e:
        # エラーが発生する時にエラー内容を出力する
        print(f"エラー発生しました: {e}")
    finally:
        # 接続を閉じる
        cnx.close()

# マーケットニューステーブルのデータをTRUNCATE
def truncateData():
    cnx = None
    try:
        # 接続する
        cnx = mysql.connector.connect(
        user='root',  # ユーザー名
        password='password',  # パスワード
        host='localhost',  # ホスト名(IPアドレス）
        database='python-study'  # データベース名
        )
        
        # カーソルを取得する
        cursor = cnx.cursor()

        # 登録sql実行
        truncateSql = "truncate table news_url_tbl;"
        cursor.execute(truncateSql)
        cnx.commit()
        # 接続を閉じる
        cursor.close()
    except Exception as e:
        # エラーが発生する時にエラー内容を出力する
        print(f"エラー発生しました: {e}")
    finally:
        # 接続を閉じる
        cnx.close()

# データTRUNCATEのスケジュール
def truncateDataSche():
    schedule.every().day.at("00:00").do(truncateData)

# メインメソッド
def main():
    # 毎日 0:00 にテーブルをTRUNCATE
    truncateDataSche()
    # 論理削除フラグの値更新
    updateDelFlg()
    # １ページ目のデータを登録
    createDataPage1()
    # ２ページ目のデータを登録
    createDataPage2()
    # 最新ニュースが出た場合はSlackで通知
    isNoti()


# メイン処理
if __name__ == '__main__':
    main()

# Webドライバー の セッションを終了
#driver.quit()