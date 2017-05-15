# -*- coding: utf-8 -*-
'''
Edited on 05/14/2017.
@author: Ryububuck
@License: GPL 3.0
'''

import re
import pprint
import schedule
import requests, time, sys, os
from multiprocessing import Process, Queue
from bs4 import BeautifulSoup as bs


global replace_string
global prev_date, pre_pre_date
t = time.localtime(time.time() - 86400 * 2)
t2 = time.localtime(time.time() - 86400 * 3)
prev_date = "17.%02d.%02d" % (t.tm_mon, t.tm_mday)  # 2일 전 발견하면 q.put
pre_pre_date = "17.%02d.%02d" % (t2.tm_mon, t2.tm_mday)  # 3일 전 발견하면 q.put
replace_string = "%04d.%02d" % (t.tm_year, t.tm_mon)

def replace_kdol(category):
    if category == '55140133':
        return '<font style=\"color:#c9c5c5\">방탄소년단</font>'
    elif category == '38608002':
        return '<font style=\"color:#79e5cb\">샤이니</font>'
    elif category == '85437064':
        return '<font style=\"color:#00bf5f\">GOT7</font>'
    elif category == '26699':
        return '<font style=\"color:#ff0000\">동방신기</font>'
    elif category == '160145694':
        return '<font style=\"color:#aaaaff\">세븐틴</font>'
    elif category == '38659297':
        return '<font style=\"color:#000000\">2PM</font>'
    elif category == '38659328':
        return '<font style=\"color:#0a3875\">빅스</font>'
    elif category == '186883457':
        return '<font style=\"color:#ff7f00\">신화</font>'
    elif category == '98188368':
        return '<font style=\"color:#e57f8c\">소녀시대</font>'
    elif category == '161629987':
        return '<font style=\"color:#a3a39c\">하이라이트</font>'
    elif category == '136446617':
        return '<font style=\"color:#f9ee16\">빅뱅</font>'
    elif category == '244170032':
        return '<font style=\"color:#e8e84e\">NCT</font>'
    elif category == '250137634':
        return '<font style=\"color:#ffe500\">젝스키스</font>'
    elif category == '353880268':
        return '<font style=\"color:#aa56ff\">틴탑</font>'
    elif category == '244170055':
        return '<font style=\"color:#ffaad4\">러블리즈</font>'
    elif category == '244170129':
        return '<font style=\"color:#ffaaaa\">레드벨벳</font>'
    elif category == '161636969':
        return '<font style=\"color:#0002f2\">위너</font>'
    elif category == '244186435':
        return '<font style=\"color:#005fbf\">비투비</font>'
    elif category == '388541893':
        return '<font style=\"color:#d4aaff\">여자친구</font>'
    elif category == '244186465':
        return '<font style=\"color:#ff1493\">트와이스</font>'
    elif category == '369461587':
        return '펜타곤'
    elif category == '347959614':
        return '<font style=\"color:#5f00bf\">아스트로</font>'
    return category

#샤이니 ~ 소시
def get_kdol2(q):
    s = requests.session()
    kdol_cate = ['38608002', '85437064', '26699', '160145694', '38659297', '38659328', '186883457', '98188368'] #샤이니 ~ 소녀시대 #

    for category in kdol_cate:
        url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&page=1&category=' + str(category)
        html = s.get(url).text.replace(replace_string, '')
        if html.find(prev_date) != -1:  # 2일전 찾음: 0 출력(1페이지 미만)
            print('0', replace_kdol(category))
            q.put([0, '<b>' + replace_kdol(category) + '</b>'])
            continue

        i = 2
        while (1):
            url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=' + str(category) + '&page=' + str(i)
            tempHtml = s.get(url).text.replace(replace_string, '')
            if tempHtml.find(prev_date) !=-1 or tempHtml.find(pre_pre_date) != -1:
                url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=' + str(category) + '&page=' + str(i - 1)
                tempHtml = requests.get(url).text.replace(replace_string, '')
                if tempHtml.find(prev_date) != -1:
                    i -= 1
                    break
                else: break
            i += 2
        print(i-1, '<b>' + replace_kdol(category) + '</b>')
        q.put([i-1, '<b>' + replace_kdol(category) + '</b>'])

#하이라이트 ~ 아스트로
def get_kdol3(q):
    s = requests.session()
    kdol_cate = [
        '161629987', #하이라이트
        '136446617', #빅뱅
        '244170032', #엔씨티
        '250137634', #젝키
        '353880268', #틴탑
        '244170055', #러블
        '244170129', #레벨
        '161636969', #위너
        '244186435', #비투비
        '388541893', #여친
        '244186465', #트와
        '369461587', #펜타곤
        '347959614' #아스트로
    ]


    for category in kdol_cate:
        url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&page=1&category=' + str(category)
        html = s.get(url).text.replace(replace_string, '')
        if html.find(prev_date) != -1:  # 2일전 찾음: 0 출력(1페이지 미만)
            print('0', replace_kdol(category))
            q.put([0, '<b>' + replace_kdol(category) + '</b>'])
            continue


        i = 2
        while (1):
            url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=' + str(category) + '&page=' + str(i)
            tempHtml = s.get(url).text.replace(replace_string, '')
            if tempHtml.find(prev_date) !=-1 or tempHtml.find(pre_pre_date) != -1:
                url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=' + str(category) + '&page=' + str(i - 1)
                tempHtml = requests.get(url).text.replace(replace_string, '')
                if tempHtml.find(prev_date) != -1:
                    i -= 1
                    break
                else: break
            i += 2
        print(i - 1, '<b>' + replace_kdol(category) + '</b>')
        q.put([i-1, '<b>' + replace_kdol(category) + '</b>'])

#인피니트
def get_simple_ifnt(q):
    s = requests.session()
    i = 1
    while (1):
        url = 'http://theqoo.net/index.php?mid=infinite&filter_mode=normal&page=' + str(i)
        tempHtml = s.get(url).text.replace(replace_string, '')
        if tempHtml.find(prev_date) != -1:  break
        i += 5

    while(1):
        i -= 1
        url = 'http://theqoo.net/index.php?mid=infinite&filter_mode=normal&page=' + str(i)
        tempHtml = requests.get(url).text.replace(replace_string, '')
        if tempHtml.find(prev_date) == -1: break
    print(i, '<b><font style=\"color:#E6CC54\">인피니트</font></b>')
    q.put([i, '<b><font style=\"color:#E6CC54\">인피니트</font></b>'])

#엑소
def get_simple_exo(q):
    s = requests.session()
    i = 1
    while (1):
        url = 'http://theqoo.net/index.php?mid=exo&filter_mode=normal&page=' + str(i)
        tempHtml = s.get(url).text.replace(replace_string, '')
        if tempHtml.find(prev_date) != -1:  break
        i += 5

    while (1):
        i -= 1
        url = 'http://theqoo.net/index.php?mid=exo&filter_mode=normal&page=' + str(i)
        tempHtml = requests.get(url).text.replace(replace_string, '')
        if tempHtml.find(prev_date) == -1: break

    print(i, '<b><font style=\"color:#778899\">엑소</font></b>')
    q.put([i, '<b><font style=\"color:#778899\">엑소</font></b>'])

#방탄
def get_simple_bts(q):
    s = requests.session()
    i = 1
    while (1):
        url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=55140133&page=' + str(i)
        tempHtml = s.get(url).text.replace(replace_string, '')
        if tempHtml.find(prev_date) != -1:  break
        i += 5

    while (1):
        i -= 1
        url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=55140133&page=' + str(i)
        tempHtml = requests.get(url).text.replace(replace_string, '')
        if tempHtml.find(prev_date) == -1: break

    print(i, '<b>방탄소년단</b>')
    q.put([i, '<b>방탄소년단</b>'])

def GetItemList(q):
    ret=[]
    n=q.qsize()
    while n > 0:
        ret.append(q.get())
        n -= 1
    ret.sort()
    ret.reverse()
    return ret

def login():
    user_id = input('더쿠 아이디: ')
    user_pw = input('더쿠 비밀번호: ')
    s = requests.session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    s.headers['Host'] = 'theqoo.net'

    url = 'http://theqoo.net/index.php?mid=main&act=dispMemberLoginForm'
    data = {
        'error_return_url': '%2Findex.php%3Fmid%3Dmain%26act%3DdispMemberLoginForm',
        'mid': 'main',
        'vid': '',
        'ruleset': '@login',
        'success_return_url': 'http://theqoo.net/main',
        'act': 'procMemberLogin',
        'xe_validator_id': 'modules%2Fmember%2Fskins%2Fsketchbook5_member_skin%2F1',
        'user_id': user_id,
        'password': user_pw
    }
    tmp = s.post(url, data=data).text
    if tmp.find('로그아웃') != -1:
        print('Login Success!')
        return s
    else:
        print('Login Fail!')
        sys.exit(input('엔터를 누르면 종료됩니다..'))

def write(s, xml):
    url = 'http://theqoo.net/index.php?mid=test&act=dispBoardWrite'
    s.get(url)
    url = 'http://theqoo.net/index.php'
    s.headers['Content-Type'] = 'application/xml'
    s.headers['Referer'] = 'http://theqoo.net/index.php?mid=test&act=dispBoardWrite'
    tmp = s.post(url, data=xml.encode('utf-8')).text
    p = re.compile('<document_srl>[0-9]*')
    m = p.search(tmp)
    document_srl = m.group().split('<document_srl>')[1]
    os.system('explorer http://theqoo.net/' + str(document_srl))
    print('http://theqoo.net/' + str(document_srl))

def make_xml(subject, memo, category_srl):
    if category_srl == '1':
        mid = 'ktalk'
        category_srl = 1947874
    elif category_srl == '2':
        mid = 'ktalk'
        category_srl = 21832056
    else:
        mid = 'test'
    xml = """﻿<?xml version="1.0" encoding="UTF-8"?><methodCall><params><_filter><![CDATA[insert]]></_filter><category_srl><![CDATA[""" + str(category_srl) + """]]></category_srl><error_return_url><![CDATA[/index.php?mid=test&act=dispBoardWrite]]></error_return_url><act><![CDATA[procBoardInsertDocument]]></act><mid><![CDATA[""" + mid + """]]></mid><content><![CDATA[""" + memo + """]]></content><title><![CDATA[""" + subject + """]]></title><_saved_doc_message><![CDATA[자동 저장된 글이 있습니다. 복구하시겠습니까? 글을 다 쓰신 후 저장하면 자동 저장 본은 사라집니다.]]></_saved_doc_message><comment_status><![CDATA[ALLOW]]></comment_status><status><![CDATA[PUBLIC]]></status><module><![CDATA[board]]></module></params></methodCall>"""
    return xml

def main():
    s = login()
    ss = time.strftime("%y%m%d %H:%M:%S", time.localtime())
    print('프로그램 실행 시각: ' + str(ss))

    q = Queue()
    procs = []
    procs.append(Process(target=get_simple_exo, args=(q,)))
    procs.append(Process(target=get_simple_bts, args=(q,)))
    procs.append(Process(target=get_simple_ifnt, args=(q,)))
    procs.append(Process(target=get_kdol2, args=(q,)))
    procs.append(Process(target=get_kdol3, args=(q,)))

    # 프로세스 시작
    for p in procs: p.start()
    for p in procs: p.join()

    avg_page = 0
    all_lists = []
    q = GetItemList(q)

    c = {}
    for item in q:
        i = item[0]
        name = item[1]
        try:
            c[i] = c[i] + ', ' + name
        except:
            c[i] = name

    for item in c.items():
        avg_page += item[0]
        tmpStr = item[1] + ' ' + str(item[0]).replace('0', '1페이지 미만')
        all_lists.append(tmpStr)

    all_lists.append('<br>')
    all_lists.append('* 프로그램 실행 시각 %s' % (ss))
    all_lists.append('* 평균 페이지 수: %.2f' % (avg_page/24))
    b = "<br>".join(all_lists)

    t = time.localtime(time.time()-86400)
    ss = time.strftime("%y%m%d", t)

    print('---------------------------------')
    print('1. 케톡 잡담 카테고리')
    print('2. 케톡 스퀘어 카테고리')
    print('3. 테스트방 (본인만 볼 수 있음)')
    print('---------------------------------')
    tmpInt = input('숫자만 입력: ')

    xml = make_xml('%s 카테별 페이지수' % ss, b, tmpInt)
    write(s, xml)
    sys.exit(input('엔터를 누르면 프로그램이 종료됩니다..'))


if __name__ == "__main__": main()