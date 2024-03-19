# -*- coding: utf-8 -*-

# インポート
import requests
import mysql.connector
import slackweb
import time
import datetime
import json
import jpholiday
import schedule

#　現在日時
dt_now = datetime.datetime.now()
dt_now_text = dt_now.strftime('%Y年%m月%d日 %H時%M分')


#定数定義
slack_token = "xoxb-6810543998997-6798913149431-XVrloL5YiY9s5lNeOo5I6oHZ"
slack_channel_name = "stock_news" 
slack_post_url = 'https://slack.com/api/chat.postMessage'
stock_news_content = "<!channel>\n" + dt_now_text + " の通知です。 \n 新しいマーケットニュースがありましたので、ご確認ください。 \n <https://www.sbisec.co.jp/ETGate/?_ControlID=WPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_DataStoreID=DSWPLETmgR001Control&_ActionID=DefaultAID&burl=iris_news&cat1=market&cat2=news&dir=tl1-news%7Ctl2-mkt%7Ctl3-jpn%7Ctl4-reuters%7Ctl9-0&file=index.html&getFlg=on | PC版>\n <https://s.sbisec.co.jp/smweb/market/marketNewsList.do? | Mobile版>"
slack_username = 'Notification bot'

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

# メインメソッド
def main():
    isNoti()

# メイン処理
if __name__ == '__main__':
    main()
