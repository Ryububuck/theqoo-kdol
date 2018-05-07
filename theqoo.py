# -*- coding: utf-8 -*-
'''
Created on 07/22/2017.
Edited on 05/07/2018.
@author: Ryububuck
@License: GPL 3.0
'''
from bs4 import BeautifulSoup as bs
from multiprocessing import Process, Queue
import requests, time, random, json, re
import sqlite3
from TheqooAPI import theqoo

now = time.time()
yday_time = time.localtime(now - 86400) #어제
yyday_time = time.localtime(now - 86400 * 2) #2일전
yyyday_time = time.localtime(now - 86400 * 3) #3일전
findtxt = '%02d-%02d' % (yyday_time.tm_mon, yyday_time.tm_mday)
findtxt2 = '%02d-%02d' % (yday_time.tm_mon, yday_time.tm_mday)
ifntxt = '%02d-%02d' % (yyyday_time.tm_mon, yyyday_time.tm_mday)

def replace_kdol(category):
    if category == '38608002':
        return '<font style=\"color:#79e5cb\">샤이니</font>'
    elif category == '85437064':
        return '<font style=\"color:#c0db3a\">GOT7</font>'
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
    elif category == '347959614':
        return '<font style=\"color:#5f00bf\">아스트로</font>'
    elif category == '518965544':
        return '<font style=\"color:#1ec91e\">마마무</font>'
    elif category == '518960998':
        return '<font style=\"color:#ffd700\">골든차일드</font>'
    elif category == '490141128':
        return '<font style=\"color:#14bcbc\">데이식스</font>'
    elif category == '490139957':
        return '<font style=\"color:#333333\">몬스타엑스</font>'
    elif category == '347959614':
        return '<font style=\"color:#5f00bf\">아스트로</font>'
    elif category == '244186465':
        return '<font style=\"color:#ff1493\">트와이스</font>'
    elif category == '369461587':
        return '펜타곤'
    elif category == '525073759':
        return '<font style=\"color:black\">더보이즈</font>'
    elif category == '552661373':
        return '<font style=\"color:black\">정세운</font>'
    elif category == '560064972':
        return '<font style=\"color:#3F0099\">이호원</font>'
    elif category == '610094282':
        return '<font style=\"color:#ff007f\">JBJ</font>'
    elif category == '610095075':
        return '<font style=\"color:#ff007f\">MXM</font>'
    elif category == '610096101':
        return '<font style=\"color:#ff007f\">구구단</font>'
    elif category == '631798964':
        return '<font style=\"color:#778899\">엑소</font>'
    elif category == '686532564':
        return '<font style=\"color:#000000\">H.O.T</font>'
    return category

# 세븐틴, 잉피, 방탄, 워너원, 늉
def get_kdol1(q, kdol):
    if kdol == 'ifnt':
        const_url = 'http://theqoo.net/index.php?mid=infinite&filter_mode=normal&page='
        name = '<b><font style=\"color:#E6CC54\">인피니트</font></b>'
    elif kdol == 'svt':
        const_url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=160145694&page='
        name = '<b><font style=\"color:#aaaaff\">세븐틴</font></b>'
    elif kdol == 'nuest':
        const_url = 'http://theqoo.net/index.php?mid=nuest&filter_mode=normal&page='
        name = '<b><font style=\"color:#e81ee8\">뉴이스트</font></b>'
    elif kdol == 'wannaone':
        const_url = 'http://theqoo.net/index.php?mid=wannaone&filter_mode=normal&page='
        name = '<b><font style=\"color:black\">워너원</font></b>'
    else:
        const_url = 'http://theqoo.net/index.php?mid=bts&filter_mode=normal&page='
        name = '<b><font style=\"color:#c9c5c5\">방탄소년단</font></b>'

    s = requests.session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Linux; U; Android 1.5; de-de; Galaxy Build/CUPCAKE) Mobile Safari/525.20.1'
    i = 1

    while (1):
        res = s.get(const_url + str(i))
        html = bs(res.text, 'lxml')
        lis = html.find_all('li', 'date el')
        if str(lis).find(findtxt) != -1: break
        if str(lis).find(ifntxt) != -1: break
        i += 5

    while (1):
        i -= 1
        res = s.get(const_url + str(i))
        html = bs(res.text, 'lxml')
        lis = html.find_all('li', 'date el')
        if str(lis).find(findtxt) == -1:
            print(i-1, name)
            q.put([i-1, name])
            return 0

# 엑소 ~ 소녀시대
def get_kdol2(q):
    kdol_cate = ['631798964', '38608002', '85437064', '26699', '38659297', '38659328', '186883457', '98188368']

    s = requests.session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Linux; U; Android 1.5; de-de; Galaxy Build/CUPCAKE) Mobile Safari/525.20.1'

    for category in kdol_cate:
        const_url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=' + str(category) + '&page='
        i = 1
        while (1):
            res = s.get(const_url + str(i))
            html = bs(res.text, 'lxml')
            lis = html.find_all('li', 'date el')
            if str(lis).find(findtxt) != -1:
                print(i - 1, '<b>' + replace_kdol(category) + '</b>')
                q.put([i - 1, '<b>' + replace_kdol(category) + '</b>'])
                break
            i += 1

#하이라이트 ~ 맘무
def get_kdol3(q):
    s = requests.session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Linux; U; Android 1.5; de-de; Galaxy Build/CUPCAKE) Mobile Safari/525.20.1'

    kdol_cate = [
        '161629987', #하라
        '136446617', #빅뱅
        '244170032', #엔씨티
        '250137634', #젝키
        '353880268', #틴탑
        '244170055', #러블
        '244170129', #레벨
        '161636969', #위너
        '244186435', #비투비
        '388541893', #여친
        '490141128',  # 데이식스
        '490139957',  # 몬스타엑스
        '518960998', #골든차일드
        '518965544', #마마무
        '525073759', #더보이즈
        '552661373', #정세운
        '560064972', #이호원
        '610094282', #jbj
        '610095075', #mxm
        '686532564', #HOT
    ]


    for category in kdol_cate:
        const_url = 'http://theqoo.net/index.php?mid=kdol&filter_mode=normal&category=' + str(category) + '&page='
        i = 1
        while (1):
            res = s.get(const_url + str(i))
            html = bs(res.text, 'lxml')
            lis = html.find_all('li', 'date el')
            if str(lis).find(findtxt) != -1:
                print(i - 1, '<b>' + replace_kdol(category) + '</b>')
                q.put([i - 1, '<b>' + replace_kdol(category) + '</b>'])
                break
            elif str(lis).find(ifntxt) != -1:
                if str(lis).find(findtxt) == -1:
                    print(0, '<b>' + replace_kdol(category) + '</b>')
                    q.put([0, '<b>' + replace_kdol(category) + '</b>'])
                    break
            i += 1

def SortList(q):
    conn = sqlite3.connect("theqoo.db")
    cur = conn.cursor()
    avg_page = 0
    all_lists = []
    ret = []
    db_data = []
    date = '18%02d%02d' % (yday_time.tm_mon, yday_time.tm_mday)
    p = re.compile(r'<font style="color:(.+)>(.+)</font>')

    n = q.qsize()
    while n > 0:
        ret.append(q.get())
        n -= 1
    ret.sort()
    ret.reverse()

    c = {}
    for item in ret:
        # 페이지수
        i = item[0]
        # 카테명 ex) <b><font style="color:#ffaad4">러블리즈</font></b>
        name = item[1]

        try:    c[i] = c[i] + ', ' + name
        except: c[i] = name

        #db 넣기
        m = p.search(name)
        db_data.append((m.group(2), i, date))

    #db data 넣기
    sql = "insert into theqoo(name,page,date) values (?, ?, ?)"
    cur.executemany(sql, db_data)
    conn.commit()
    conn.close()


    tmpArr = sorted(c.items())
    tmpArr.reverse()

    for item in tmpArr:
        avg_page += item[0]
        if str(item[0]) == '0':
            tmpStr = item[1] + ' 1페이지 미만'
        else:
            tmpStr = item[1] + ' ' + str(item[0])
        all_lists.append(tmpStr)

    all_lists.append('<br>')
    yesterday = '18%02d%02d' % (yday_time.tm_mon, yday_time.tm_mday)
    now = time.localtime()
    ss = '18%02d%02d %02d:%02d:%02d' % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    all_lists.append('* 집계 기간: %s 00:00:00 ~ %s' % (yesterday, ss))
    all_lists.append('* 평균 페이지 수: %.2f' % (avg_page / 33))
    return all_lists

def json_loading():
    json_load = requests.get('http://lovelyz.gtz.kr/theqoo.json').text
    b = json.loads(json_load)
    i = random.randrange(0, len(b))
    j = random.randrange(0, len(b[i]['img']))
    tmpStr = b[i]['memo'] + '<br><img src="' + b[i]['img'][j] + '" />'
    return tmpStr

def main():
    ss = time.strftime("%y%m%d %H:%M:%S", time.localtime())
    print('프로그램 실행 시각: ' + str(ss))
    print('찾을 텍스트: ', findtxt)

    q = Queue()
    procs = []
    procs.append(Process(target=get_kdol1, args=(q, 'svt')))
    procs.append(Process(target=get_kdol1, args=(q,'bts')))
    procs.append(Process(target=get_kdol1, args=(q,'ifnt')))
    procs.append(Process(target=get_kdol1, args=(q, 'nuest')))
    procs.append(Process(target=get_kdol1, args=(q, 'wannaone')))
    procs.append(Process(target=get_kdol2, args=(q,)))
    procs.append(Process(target=get_kdol3, args=(q,)))

    # 프로세스 시작 후, 완료까지 대기
    for p in procs: p.start()
    for p in procs: p.join()

    all_lists = SortList(q)
    b = "<br />".join(all_lists)
    print(b)

    yesterday = '18%02d%02d' % (yday_time.tm_mon, yday_time.tm_mday)

    Theqoo = theqoo()

    draft = {
        'mid': 'ktalk',
        'subject': '%s 카테별 페이지수' % yesterday,
        'memo': b,
        'comment': '댓글 내용',
        'category_srl': '2'
    }

    document_srl = Theqoo.write(draft)
    print('http://theqoo.net/' + str(document_srl))

    # Write Comment
    '''
    memo = json_loading()
    xml2 = make_xml2(mid, memo, document_srl)
    write2(session, xml2, document_srl)
    '''
if __name__ == "__main__":  main()