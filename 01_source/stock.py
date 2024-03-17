# -*- coding: utf-8 -*-

# インポート
import requests
import mysql.connector
import slackweb
import time
import datetime
import json
#　現在日時
dt_now = datetime.datetime.now()
dt_now_text = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')

#定数定義
#slack_token = "xoxp-6810543998997-6813352205075-6798913141463-a22b27316c21f21ab35f1b636242490e"  # slackのtoken admin
slack_token = "xoxb-6810543998997-6798913149431-XVrloL5YiY9s5lNeOo5I6oHZ"  # slackのtoken bot
slack_channel_name = "stock_news"  # Slackのチャンネル名
slack_channel_id = "C06PUG1BMDK"
slack_post_url = 'https://slack.com/api/chat.postMessage'  # Slackでメッセージを送信するためのurl
slack_del_url = 'https://slack.com/api/chat.delete'
slack_username = 'Notification bot'
slack_content = "<!channel>\n" + dt_now_text + "の株価です。" + (
    "\n"
    "こちらはテスト投稿です。"
)
# DBにデータ登録
def insertDB():
    cnx = None
    try:
        # 接続する
        cnx = mysql.connector.connect(
        user='root',  # ユーザー名
        password='password',  # パスワード
        host='localhost',  # ホスト名(IPアドレス）
        database='python_test'  # データベース名
        )
        
        # カーソルを取得する
        cursor = cnx.cursor()
        # 実行sql
        sql = ('''
               INSERT INTO test (content,note,del_flg)
               VALUES (%s,%s,%s)
               ''')
        data = [
                ('content test 1','note 1','1'),
                ('content test 2','note 2','0'),
                ('content test 3','note 3','1')
                ]
        cursor.executemany(sql, data)
        cnx.commit()
        print(f"{cursor.rowcount} records inserted.")
        # 接続を閉じる
        cursor.close()
    except Exception as e:
        # エラーが発生する時にエラー内容を出力する
        print(f"Error Occurred: {e}")
    finally:
        if cnx is not None and cnx.is_connected():
            # 接続を閉じる
            cnx.close()


# Slackに通知するメソッド
def sendSlack():
    try:
        # Slackで通知する際に必要なデータを設定する
        data = {
            'token': slack_token,
            'channel': slack_channel_name,
            'text': slack_content,
            'username': slack_username
        }
        
        # POSTメソッドで送信する
        response = requests.post(slack_post_url, data=data)
    except Exception as e:
        print(e)
        


# メインメソッド
def main():
#    insertDB()
    sendSlack()
    

# メイン処理
if __name__ == '__main__':
    main()
