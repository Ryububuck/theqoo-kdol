# -*- coding: utf-8 -*-
"""
Created on 07/22/2017.
Edited on 05/07/2018.
@author: Ryububuck
@License: GPL 3.0
"""
from bs4 import BeautifulSoup as bs
from multiprocessing import Process, Queue
import requests, time, re
import sqlite3
from TheqooAPI import Theqoo

now = time.time()
yday_time = time.localtime(now - 86400)         # 어제
yyday_time = time.localtime(now - 86400 * 2)    # 2일전
yyyday_time = time.localtime(now - 86400 * 3)   # 3일전
findtxt = '%02d-%02d' % (yyday_time.tm_mon, yyday_time.tm_mday)
findtxt2 = '%02d-%02d' % (yday_time.tm_mon, yday_time.tm_mday)
ifntxt = '%02d-%02d' % (yyyday_time.tm_mon, yyyday_time.tm_mday)


def get_cate():
    init_url = 'http://theqoo.net/index.php'
    cate = []
    res = requests.get('{}?mid=kdol'.format(init_url)).text
    soup = bs(res, 'lxml')
    catd = soup.find('ul', {'id': 'catd'})
    data = catd.find_all('li')

    for n in data[1:-1]:
        srl = re.findall(r'\d+', n.a['href'])[0]
        name = re.sub(r"\(\d+\)", '', n.get_text().rstrip('\n'))
        cate.append({
            'const_url': '{}?mid=kdol&category={}&page='.format(init_url, srl),
            'name': "<font style='{}'>{}</font>".format(n.a.get('style'), name)
        })

    return cate


def get_kdol1(q):
    init_url = 'http://theqoo.net/index.php'
    cate = [
        {'const_url': '{}?mid=infinite&page='.format(init_url),
         'name': '<font style=\"color:#E6CC54\">인피니트</font>'},
        {'const_url': '{}?mid=nuest&page='.format(init_url),
         'name': '<font style=\"color:#e81ee8\">뉴이스트</font>'},
        {'const_url': '{}?mid=wannaone&page='.format(init_url),
         'name': '<font style=\"color:black\">워너원</font>'},
        {'const_url': '{}?mid=bts&page='.format(init_url),
         'name': '<font style=\"color:#c9c5c5\">방탄소년단</font>'}
    ]
    s = requests.session()
    s.headers['User-Agent'] = 'Mozilla/5.0 Galaxy Mobile'

    for a in cate:
        i = 1
        while 1:
            res = s.get(a['const_url'] + str(i))
            html = bs(res.text, 'lxml')
            lis = html.find_all('li', 'date el')
            if str(lis).find(findtxt) != -1: break
            if str(lis).find(ifntxt) != -1: break
            i += 5

        while 1:
            i -= 1
            res = s.get(a['const_url'] + str(i))
            html = bs(res.text, 'lxml')
            lis = html.find_all('li', 'date el')
            if str(lis).find(findtxt) == -1:
                print(i - 1, '<b>{}</b>'.format(a['name']))
                q.put([i - 1, '<b>{}</b>'.format(a['name'])])
                break


def get_page(q, cateq):
    s = requests.session()
    s.headers['User-Agent'] = 'Mozilla/5.0 Galaxy Mobile'

    while cateq.qsize() > 0:
        catedata = cateq.get()
        i = 1
        while 1:
            res = s.get(catedata['const_url'] + str(i))
            html = bs(res.text, 'lxml')
            lis = html.find_all('li', 'date el')
            if str(lis).find(findtxt) != -1:
                print(i - 1, '<b>' + catedata['name'] + '</b>')
                q.put([i - 1, '<b>' + catedata['name'] + '</b>'])
                break
            elif str(lis).find(ifntxt) != -1:
                if str(lis).find(findtxt) == -1:
                    print(0, '<b>' + catedata['name'] + '</b>')
                    q.put([0, '<b>' + catedata['name'] + '</b>'])
                    break
            i += 1


def sort_list(q):
    avg_page = 0
    memo = []
    tmp_arr, db_data = sort_queue(q)
    insert_db(db_data)

    for item in tmp_arr:
        page = item[0]
        avg_page += page
        memo.append('{} {}'.format(item[1], str(page)) if page else '{} 1페이지 미만'.format(item[1]))

    memo.append('<br>')
    yesterday = '18%02d%02d' % (yday_time.tm_mon, yday_time.tm_mday)
    today = time.localtime()
    ss = '18%02d%02d %02d:%02d:%02d' % (today.tm_mon, today.tm_mday, today.tm_hour, today.tm_min, today.tm_sec)
    memo.append('* 집계 기간: %s 00:00:00 ~ %s' % (yesterday, ss))
    memo.append('* 평균 페이지 수: %.2f' % (avg_page / len(tmp_arr)))
    memo.append('* 카테별 페이지수는 케이돌 화력이 절대절대 아님!!!!!!! 떡밥 잘 달렸는지 확인하라고 보는 재미용임!!!!!')
    memo.append('* 카테별 페이지수 Q&A: http://theqoo.net/ktalk/720752754')
    return "<br />".join(memo)


def sort_queue(q):
    date = '18%02d%02d' % (yday_time.tm_mon, yday_time.tm_mday)
    p = re.compile(r'<font style=(.+)>(.+)</font>')
    ret = []
    db_data = []
    n = q.qsize()
    while n > 0:
        ret.append(q.get())
        n -= 1

    c = {}
    for item in ret:
        # 페이지수
        i = item[0]
        # 카테명 ex) <b><font style="color:#ffaad4">러블리즈</font></b>
        name = item[1]

        try:
            c[i] = c[i] + ', ' + name
        except KeyError:
            c[i] = name

        m = p.search(name)
        db_data.append((m.group(2), i, date))

    tmp_arr = sorted(c.items())
    tmp_arr.reverse()
    return tmp_arr, db_data


def insert_db(db_data):
    conn = sqlite3.connect("theqoo.db")
    cur = conn.cursor()
    sql = "insert into theqoo(name,page,date) values (?, ?, ?)"
    cur.executemany(sql, db_data)
    conn.commit()
    conn.close()


def main():
    ss = time.strftime("%y%m%d %H:%M:%S", time.localtime())
    print('프로그램 실행 시각: ' + str(ss))
    print('찾을 텍스트: ', findtxt)

    q = Queue()
    cate = Queue()
    for item in get_cate():
        cate.put(item)
    procs = [
        Process(target=get_page, args=(q, cate)),
        Process(target=get_page, args=(q, cate)),
        Process(target=get_page, args=(q, cate)),
        Process(target=get_kdol1, args=(q,)),
    ]

    # 프로세스 시작 후, 완료까지 대기
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    yesterday = '18%02d%02d' % (yday_time.tm_mon, yday_time.tm_mday)

    theqoo = Theqoo()

    draft = {
        'mid': 'ktalk',
        'subject': '%s 카테별 페이지수' % yesterday,
        'memo': sort_list(q),
        'comment': '댓글 내용',
        'category_srl': '2'
    }

    document_srl = theqoo.write(draft)
    print('http://theqoo.net/' + str(document_srl))
    print("--- %s seconds ---" % (time.time() - now))


if __name__ == "__main__":
    main()
