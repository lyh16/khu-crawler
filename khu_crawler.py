#! /usr/bin/python3

from bitly import shorten_url
import bs4 as b
import collections
import datetime
from dbman import DBMan
import requests as r
import telegram.bot
import time
#from telegram.ext import messagequeue as mq

#변수 등

url_base = 'http://khu.ac.kr/kor/notice/'
general = str(url_base + 'list.do?category=GENERAL&page=1')
undergraduate = str(url_base + 'list.do?category=UNDERGRADUATE&page=1')
scholarships = str(url_base + 'list.do?category=SCHOLARSHIP&page=1')
credex = str(url_base + 'list.do?category=CREDIT&page=1')
events = str(url_base + 'list.do?category=EVENT&page=1')

new_pinned = collections.defaultdict(dict)
new_normal = collections.defaultdict(dict)

admins = set(["Admin's Telegram chat_id"])
db = DBMan()
db.setup()

token = 'YOUR TELEGRAM BOT TOKEN'
bot = telegram.Bot(token = token)
#q = mq.MessageQueue()

#함수 및 클래스 정의

def get_notices(soup):
    '''
    This function fetches all notices in the given webpage.
    '''
    global new_pinned
    global new_normal

    table_body = soup.find('tbody')
    table = table_body.find_all('tr')
    for row in table:
        notice_type = row.find('td', {'class':'col01'}).get_text().strip()
        title = row.find('td', {'class':'col02'})
        link = title.find('a')

        if link.has_attr('href'):
            link = link.attrs['href']

        title = title.find('p', {'class':'txt06'}).get_text().strip()

        if title.endswith('...'):
            resp = r.get(url_mod(link))
            subsoup = b.BeautifulSoup(resp.content, from_encoding = 'utf-8', features = 'html.parser')
            title = subsoup.find('div', {'class':'tit'})
            title = title.find('p', {'class':'txt06'}).get_text().strip()

        issuer = row.find('td', {'class':'col03'}).get_text().strip()
        date = row.find('td', {'class':'col04'}).get_text().strip()

        if ((len(date) == 5) or (len(date) < 5)):
            date = datetime.date.today()
            date = date.strftime('%Y-%m-%d')

        try:
            assert notice_type == '공지'
        except:
            new_normal[link]['notice_title'] = title
            new_normal[link]['notice_date'] = date
            new_normal[link]['issuer'] = issuer
        else:
            new_pinned[link]['notice_title'] = title
            new_pinned[link]['notice_date'] = date
            new_pinned[link]['issuer'] = issuer

def url_mod(short_link):
    '''
    This function modifies the given short URL to match/become the full URL.
    '''
    full_url = url_base + short_link
    return full_url

def send_notice(channel, text):
    '''
    This function broadcasts the given text to the specified channel via MQBot.
    '''
    #['return' not functioning as expected!!!] return kic_bot.send_message(chat_id = channel, disable_web_page_preview = True, parse_mode = 'HTML', text = text)
    '''
    The below code may be used in place of the above code. But only one may be used at a time.
    The above delegates the message sending function to MQBot.
    The below executes the message sending function directly.
    '''
    return bot.send_message(chat_id = channel, disable_web_page_preview = True, parse_mode = 'HTML', text = text)

def msg_admin(text):
    '''
    This function sends the given text to the hardcoded 'admin(s)'; usually error messages.
    '''
    global admins
    for admin in admins:
        try:
            bot.send_message(chat_id = admin, text = text)
        except:
            pass

class sieve:
    '''
    This class determines whether elements of 'new_data' are new, old, or obsolete compared to 'check_data'.
    '''
    def __init__(self, new_data, check_data):
        self.new_data = new_data
        self.check_data = check_data

    def new(self):
        answer = [x for x in self.new_data if x not in self.check_data]
        return answer

    def old(self):
        answer = [x for x in self.new_data if x in self.check_data]
        return answer

    def obsolete(self):
        answer = [x for x in self.check_data if x not in self.new_data]
        return answer

"""
class MQBot(telegram.bot.Bot):
    '''
    This class is delegated the message sending function.
    Its job is to automatically pace the sending of messages so that the message sending bot does not exceed Telegram's flood control limits.
    '''
    def __init__(self, *args, is_queued_def = True, mqueue = None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()
    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super(MQBot, self).send_message(*args, **kwargs)
kic_bot = MQBot(token, mqueue = q)
"""

#본 함수

for category in [general, undergraduate, scholarships, credex, events]:
    if category == general:
        cat = 'Gen'
        channel = '@khu_notices_general'
    elif category == undergraduate:
        cat = 'Und'
        channel = '@khu_notices_undergraduate'
    elif category == scholarships:
        cat = 'Sch'
        channel = '@khu_notices_scholarships'
    elif category == credex:
        cat = 'Cdx'
        channel = '@khu_notices_credex'
    elif category == events:
        cat = 'Evt'
        channel = '@khu_notices_events'

    response = r.get(category)

    if response.status_code == 200:
        soup = b.BeautifulSoup(response.content, from_encoding = 'utf-8', features = 'html.parser')

        get_notices(soup)

        check_pinned = db.get_notices(str(cat + '_Pinned'))
        s_p = sieve(new_data = list(new_pinned.keys()), check_data = check_pinned)

        if s_p.new():
            notice_category = str(cat + '_Pinned')
            for short_link in s_p.new()[::-1]:
                notice_date = new_pinned[short_link]['notice_date']
                crawl_dt = datetime.datetime.now()
                issuer = new_pinned[short_link]['issuer']
                title = new_pinned[short_link]['notice_title']

                full_url = shorten_url(url_mod(short_link))
                final_notice = '#중요_공지\n' + f'<code>{notice_date}</code>' + '\n' + f'<b>{title}</b>' + '\n' + f'<code>작성자: {issuer}</code>' + '\n' + full_url
                msg = send_notice(channel, final_notice)
                msg_id = msg['message_id']
                db.add_notice(notice_category, notice_date, crawl_dt, issuer, title, short_link, msg_id)
                time.sleep(2)

        if s_p.obsolete():
            notice_category = str(cat + '_Pinned')
            for stuff in s_p.obsolete():
                stuff_notice_date = datetime.datetime.strptime(db.get_notice_date(notice_category, stuff), '%Y-%m-%d')
                tdelta = datetime.datetime.today() - stuff_notice_date
                if tdelta.days > 180:
                    #등록 뒤 180일을 초과한 시간이 지난 공지만 삭제 또는 열람 불가 처리
                    #코드 작성 시점에서는 Telegram 메신저 자체의 정책으로 봇 계정은 작성 뒤 48시간 이내의 메시지만 삭제할 수 있음
                    message_id = str(db.get_msg_id(notice_category, stuff))
                    try:
                        bot.delete_message(chat_id = channel, message_id = message_id)
                    except:
                        bot.edit_message_text(text = '#obsolete\n오래된 공지입니다.\n다시 보려면 학교 누리집을 방문해주십시오.' , chat_id = channel, message_id = message_id)
                    db.del_notice(notice_category, stuff)

        new_pinned.clear()
        check_pinned.clear()

        check_normal = db.get_notices(str(cat + '_Normal'))
        s_n = sieve(new_data = list(new_normal.keys()), check_data = check_normal)

        if s_n.new():
            notice_category = str(cat + '_Normal')
            for short_link in s_n.new()[::-1]:
                notice_date = new_normal[short_link]['notice_date']
                crawl_dt = datetime.datetime.now()
                issuer = new_normal[short_link]['issuer']
                title = new_normal[short_link]['notice_title']

                full_url = shorten_url(url_mod(short_link))
                final_notice = f'<code>{notice_date}</code>' + '\n' + f'<b>{title}</b>' + '\n' + f'<code>작성자: {issuer}</code>' + '\n' + full_url
                msg = send_notice(channel, final_notice)
                msg_id = msg['message_id']
                db.add_notice(notice_category, notice_date, crawl_dt, issuer, title, short_link, msg_id)
                time.sleep(2)

        if s_n.obsolete():
            notice_category = str(cat + '_Normal')
            for stuff in s_n.obsolete():
                stuff_notice_date = datetime.datetime.strptime(db.get_notice_date(notice_category, stuff), '%Y-%m-%d')
                tdelta = datetime.datetime.today() - stuff_notice_date
                if tdelta.days > 180:
                    #등록 뒤 180일을 초과한 시간이 지난 공지만 삭제 또는 열람 불가 처리
                    #코드 작성 시점에서는 Telegram 메신저 자체의 정책으로 봇 계정은 작성 뒤 48시간 이내의 메시지만 삭제할 수 있음
                    message_id = str(db.get_msg_id(notice_category, stuff))
                    try:
                        bot.delete_message(chat_id = channel, message_id = message_id)
                    except:
                        bot.edit_message_text(text = '#obsolete\n오래된 공지입니다.\n다시 보려면 학교 누리집을 방문해주십시오.' , chat_id = channel, message_id = message_id)
                    db.del_notice(notice_category, stuff)

        new_normal.clear()
        check_normal.clear()

    else:
        try:
            response.raise_for_status()
        except r.exceptions.HTTPError as e:
            if response.status_code == 502:
                pass
            else:
                #관리자는 봇 계정 개설 이후 최초 1회는 봇에게 '/start' 등의 말을 걸어줘야 향후 봇이 단독으로 관리자에게 메시지 발송 가능함
                #봇에게 최초 1회 말을 걸어준 다음 대화 내용을 삭제하든 채팅방을 삭제하든 무관계함
                #단, '대화방을 삭제하고 차단'하면 '차단' 때문에 당연히 봇이 관리자에게 연락할 수 없음
                msg_admin(f'CRAWLING FAILED!\n{e}')
            time.sleep(900)