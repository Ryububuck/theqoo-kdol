# -*- coding: utf-8 -*-
'''
@Edited on 05/06/2018.
@author: Ryububuck
@License: GPL 3.0
'''
from bs4 import BeautifulSoup as bs
from multiprocessing import Process, Queue
import requests, time, random, json, re
THEQOO_ID = 'YOUR THEQOO ID'
THEQOO_PW = 'YOUR THEQOO PW'

INIT_URL = 'http://theqoo.net/index.php'


class Theqoo:
    def __init__(self):
        self.s = requests.session()
        self.s.heaedrs = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Host': 'theqoo.net'
        }

        url = '{}?mid=cate_index&act=dispMemberLoginForm'.format(INIT_URL)
        data = {
            'error_return_url': '/index.php?mid=cate_index&act=dispMemberLoginForm',
            'mid': 'index',
            'vid': '',
            'ruleset': '@login',
            'success_return_url': '{}'.format(INIT_URL),
            'act': 'procMemberLogin',
            'xe_validator_id': 'modules/member/skins/sketchbook5_member_skin/1',
            'user_id': THEQOO_ID,
            'password': THEQOO_PW
        }

        tmp = self.s.post(url, data=data).text
        if tmp.find('로그아웃') != -1:
            print('Login Success!')
        else:
            print('Login Fail!')

    def write(self, draft):
        xml, mid = make_xml(draft['subject'], draft['memo'], draft['category_srl'])
        url = '{}'.format(INIT_URL)
        self.s.headers = {
            'Content-Type': 'application/xml',
            'Referer': '{}?mid=test&act=dispBoardWrite'.format(INIT_URL)
        }
        tmp = self.s.post(url, data=xml.encode('utf-8')).text
        return get_document_srl(tmp)

    def writeComment(self, s, xml, document_srl):
        url = '{}'.format(INIT_URL)
        s.headers['Referer'] = '{}?mid=test&act=procBoardInsertComment'.format(INIT_URL)
        res = s.post(url, data=xml.encode('utf-8'))
        print('http://theqoo.net/' + str(document_srl))
        return res.status_code


def get_document_srl(txt):
    p = re.compile('<document_srl>[0-9]*')
    m = p.search(txt)
    document_srl = m.group().split('<document_srl>')[1]
    return document_srl


# Write Document XML
def make_xml(subject, memo, category_srl):
    if category_srl == '1':
        mid = 'ktalk'
        category_srl = 1947874
    elif category_srl == '2':
        mid = 'ktalk'
        category_srl = 21832056
    else:
        mid = 'test'

    xml = """<?xml version="1.0" encoding="UTF-8"?><methodCall><params><_filter><![CDATA[insert]]></_filter><category_srl><![CDATA[{}]]></category_srl><error_return_url><![CDATA[/index.php?mid=test&act=dispBoardWrite]]></error_return_url><act><![CDATA[procBoardInsertDocument]]></act><mid><![CDATA[{}]]></mid><content><![CDATA[{}]]></content><title><![CDATA[{}]]></title><_saved_doc_message><![CDATA[자동 저장된 글이 있습니다. 복구하시겠습니까? 글을 다 쓰신 후 저장하면 자동 저장 본은 사라집니다.]]></_saved_doc_message><comment_status><![CDATA[ALLOW]]></comment_status><status><![CDATA[PUBLIC]]></status><module><![CDATA[board]]></module></params></methodCall>"""\
          .format(category_srl, mid, memo, subject)
    return xml, mid


# Write Comment XML
def make_xml2(mid, memo, document_srl):
    xml = """<?xml version="1.0" encoding="utf-8" ?><methodCall><params><_filter><![CDATA[insert_comment]]></_filter><error_return_url><![CDATA[/index.php?mid={}&filter_mode=normal&document_srl={}]]></error_return_url><mid><![CDATA[{}]]></mid><document_srl><![CDATA[{}]]></document_srl><content><![CDATA[{}]]></content><module><![CDATA[board]]></module><act><![CDATA[procBoardInsertComment]]></act></params></methodCall>"""\
        .format(mid, document_srl, mid, document_srl, memo)
    return xml


def main():
    theqoo = Theqoo()

    draft = {
        'mid': 'ktalk',
        'subject': '테스트중',
        'memo': '테스트중입니다.',
        'comment': '댓글 내용',
        'category_srl': '3'
    }

    document_srl = theqoo.write(draft)
    print('http://theqoo.net/' + str(document_srl))


if __name__ == "__main__":
    main()
