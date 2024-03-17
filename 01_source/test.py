import jpholiday
import datetime
import pytz
import calendar


# 今日の%Y-%m-%d
def fetch_today() -> datetime:
    return datetime.datetime.now(pytz.timezone('Asia/Tokyo')).date()

# 土日、祝日かどうか
def is_holiday(day: datetime) -> bool:
    # day.weekday() => 0=月曜日...5=土曜日、6=日曜日
    return day.weekday() >= 5 or jpholiday.is_holiday(day)

# 月の初日を取得
def first_day(today: datetime) -> datetime:
    return today.replace(day=1)

# 月の末日を取得
def last_day(year, month: datetime) -> datetime:
    day =  calendar.monthrange(year, month)[1]
    return datetime.datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()

# 月の平日の初日を取得
def fetch_first_bizdate(day) -> datetime:
    first_date = first_day(day)
    while is_holiday(first_date):
        first_date = first_date + datetime.timedelta(days=1)

    return first_date

# 月の平日の末日を取得
def fetch_last_bizdate(year, month) -> datetime:
    last_date = last_day(year, month)
    while is_holiday(last_date):
        last_date = last_date - datetime.timedelta(days=1)

    return last_date

if __name__ == '__main__':
  # 今日
  today = fetch_today()
  # 月の平日の初日
  first_bizdate = fetch_first_bizdate(today)
  # 月の平日の末日
  last_bizdate = fetch_last_bizdate(today.year, today.month)

  print(f'today: {today}')
  print(f'last_bizdate: {last_bizdate}')
  print(f'first_bizdate: {first_bizdate}')

  # 今日は月の平日の初日 or 末日かどうか
  today in [first_bizdate, last_bizdate]