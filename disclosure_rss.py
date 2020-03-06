import feedparser
import time
import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(filename='message.log', level=logging.DEBUG)

url = 'http://dart.fss.or.kr/api/todayRSS.xml'
BOT_TOKEN = '1130486519:AAE1_bf0sA5_QwyX2cPl4dJX5C6KvUishqo'
BOT_CHAT_ID = '879729250'
BOT_URL = \
    f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={BOT_CHAT_ID}'
EXCEPT_WORDS = ['참고서류', '주주총회', '투자설명서', '현금', '파생', '일괄', '증권발행', '채무보증', '기타', '대규모기업집단현황공시']

stored_data = []


def send_msg(text=''):
    """
        텔레그램 메신저로 메시지를 송신한다.

    Args:
        text: 송신할 메시지 내용. string

    """
    data = {'text': text}
    res = requests.post(BOT_URL, data=data)

    if res.status_code == 200:
        logging.info("텔레그렘 메시지 전송 완료")
    else:
        logging.info("텔레그램 메시지 전송 실패")


# request infinitely
while True:
    feed = feedparser.parse(url)
    fetched_entries = feed.entries
    
    now = datetime.now()
    if now.hour >= 23: break

    # if received data is equal to the previous one,
    # skip.
    if len(stored_data) == len(fetched_entries):
        time.sleep(1)
        print('Polling . . .')
        continue

    # if there is sth now,
    # send the new ones.
    new_entries = reversed(
        fetched_entries[:len(fetched_entries)-len(stored_data)])

    for disclosure_info in new_entries:
        title = disclosure_info.title
        link = disclosure_info.link
        datetime = datetime.fromisoformat(
            disclosure_info.updated[:-1]) + timedelta(hours=9)
        # company = disclosure_info.author

        # check if a title contains at least the one of EXCEPT_WORDS,
        # not send message
        is_excluded = False
        for word in EXCEPT_WORDS:
            if word in title:
                is_excluded = True

        if is_excluded:
            continue
        else:
            msg = title + '\n' + f'[{datetime}]' + '\n' + link
            send_msg(msg)
            time.sleep(1)

    # store data for future comparison
    stored_data = fetched_entries
