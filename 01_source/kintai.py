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
dt_now_text = dt_now.strftime('%Y年%m月%d日')


#定数定義
slack_token = "xoxb-6810543998997-6798913149431-XVrloL5YiY9s5lNeOo5I6oHZ"
slack_channel_name = "kintai-noti" 
slack_channel_id = "C06PUG1BMDK"
slack_post_url = 'https://slack.com/api/chat.postMessage'
kintai_content = "<!channel>\n" + dt_now_text + " の通知です。 \n Mykintaiアプリから勤務時間を入力してください。"
timesheet_content = "<!channel>\n 今月のタイムシートを作成してから提出してください。"
slack_username = 'Notification bot'

# 通知内容作成
def createKintaiNoti():
    try:
        # Slackで通知する際に必要なデータを設定する
        data = {
            'token': slack_token,
            'channel': slack_channel_name,
            'text': kintai_content,
            'username': slack_username
        }
        
        # POSTメソッドで送信する
        response = requests.post(slack_post_url, data=data)
    except Exception as e:
        print(e)
        
# 平日のみSlack通知する
def sendSlack():
        weekday = datetime.date.today().weekday()
        if weekday >= 7 or jpholiday.is_holiday(datetime.date.today()):
            exit()
        else:
            createKintaiNoti()

# メインメソッド
def main():
    sendSlack()

# メイン処理
if __name__ == '__main__':
    main()
