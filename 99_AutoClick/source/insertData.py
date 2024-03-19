# seleniumの必要なライブラリをインポート
import time
import csv
import datetime
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

# 最初１ページ目の登録用データ作成
def createDataPage1():
    url = 'https://site2.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_DataStoreID=DSWPLETmgR001Control&_ActionID=DefaultAID&burl=iris_news&cat1=market&cat2=news&dir=tl1-news%7Ctl2-mkt%7Ctl3-jpn%7Ctl4-reuters%7Ctl9-0&file=index.html&getFlg=on'
    dt_now = datetime.datetime.now()
    dt_now_text = dt_now.strftime('%Y/%m/%d %H:%M:%S')
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)
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
    time.sleep(5)
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
        
        # 登録する前にTRUNCATE
        #sql1 = "TRUNCATE TABLE news_url_tbl"
        #cursor.execute(sql1)
        # 登録sql実行
        insertSql = "INSERT INTO news_url_tbl (text,url,user_check_flg,del_flg,create_datetime) VALUES (" + createData + ")"
        print("実行sql：　" + insertSql)
        cursor.execute(insertSql)
        
        cnx.commit()
        print(f"{cursor.rowcount} レコード登録しました。")
        # 接続を閉じる
        cursor.close()
    except Exception as e:
        # エラーが発生する時にエラー内容を出力する
        print(f"エラー発生しました: {e}")
    finally:
        if cnx is not None and cnx.is_connected():
            # 接続を閉じる
            cnx.close()


# メインメソッド
def main():
    # １ページ目のデータを登録
    createDataPage1()
    # ２ページ目のデータを登録
    createDataPage2()
    

# メイン処理
if __name__ == '__main__':
    main()

# Webドライバー の セッションを終了
#driver.quit()