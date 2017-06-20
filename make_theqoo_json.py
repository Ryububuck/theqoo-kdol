# -*- coding: utf-8 -*-
'''
Edited on 06/20/2017.
@author: Ryububuck
@License: GPL 3.0
'''
import json, random, requests


def json_loading():
    json_load = requests.get('http://lovelyz.gtz.kr/theqoo.json').text
    b = json.loads(json_load)
    i = random.randrange(0, len(b))
    j = random.randrange(0, len(b[i]['img']))
    print(b[i]['memo'] + '<br><img src="' + b[i]['img'][j] + '" />')


def make_json():
    jsonObj = []
    jsonObj.append(
        {
            'memo': '1일 1영업! 러블리즈 리다 <b>베이비소울</b>! <span style=\"color: rgb(194, 194, 194);\">(aka 벱)</span>',
            'img': ['https://i.imgur.com/WkeUI8V.gif', 'https://i.imgur.com/PwUUB9l.gif', 'https://i.imgur.com/ovVDVRd.jpg']
        }
    )
    jsonObj.append(
        {
            'memo': '1일 1영업! 러블리즈 무미니 <b>유지애</b>! <span style=\"color: rgb(194, 194, 194);\">(aka 쟤)</span>',
            'img': ['https://i.imgur.com/isBkvtu.gif', 'https://i.imgur.com/ESUX9Ln.jpg', 'https://i.imgur.com/MvySuyI.gif',
                    'https://pbs.twimg.com/media/DAR-sY6VwAAm1lS.jpg', 'https://i.imgur.com/ZQwXHuK.gif']
        }
    )
    jsonObj.append(
        {
            'memo': '1일 1영업! 러블리즈 비쥬얼 <b>서지수</b>! <span style=\"color: rgb(194, 194, 194);\">(aka 짓뚜)</span>',
            'img': ['https://i.imgur.com/GYBwlxg.gif', 'https://i.imgur.com/NSS60MB.jpg', 'https://i.imgur.com/4ku3ESo.jpg']
        }
    )
    jsonObj.append(
        {
            'memo': "1일 1영업! 러블리즈 도도미 'ㅅ' <b>이미주</b>! <span style=\"color: rgb(194, 194, 194);\">(aka 뚀)</span>",
            'img': ['https://i.imgur.com/eMgQoJr.gif', 'https://i.imgur.com/EdEVUcy.jpg', 'https://i.imgur.com/OkjHdY8.gif',
                    'http://cfile26.uf.tistory.com/image/21789D5059203A62250274']
        }
    )
    jsonObj.append(
        {
            'memo': '1일 1영업! 러블리즈 천상아이도루 <b>Kei</b>! <span style=\"color: rgb(194, 194, 194);\">(aka 켕)</span>',
            'img': ['https://i.imgur.com/AI5q5Rt.gif', 'https://i.imgur.com/MNuu2CG.jpg', 'https://i.imgur.com/SK7EVWn.gif','https://i.imgur.com/rBXtSiV.gif'
                    ,'https://i.imgur.com/osROIuc.jpg']
        }
    )
    jsonObj.append(
        {
            'memo': '1일 1영업! 러블리즈 감성보컬 <b>JIN</b> <span style=\"color: rgb(194, 194, 194);\">(aka 띵)</span>',
            'img': ['https://i.imgur.com/XqSpcYn.gif', 'https://i.imgur.com/gLToywg.jpg', 'https://i.imgur.com/ptgHBLy.jpg']
        }
    )
    jsonObj.append(
        {
            'memo': '1일 1영업! 러블리즈 <b>류수정</b>! <span style=\"color: rgb(194, 194, 194);\">(aka 빵)</span>',
            'img': ['https://i.imgur.com/uX4cL98.gif', 'https://i.imgur.com/eBXfUyo.gif', 'https://i.imgur.com/LKOzRVY.gif',
                    'http://cfile9.uf.tistory.com/image/273EA84759203BAE2B88A7']
        }
    )
    jsonObj.append(
        {
            'memo': '1일 1영업! 러블리즈 <b>정예인</b>! <span style=\"color: rgb(194, 194, 194);\">(aka 옝)</span>',
            'img': ['https://i.imgur.com/B8WwWqk.gif', 'https://i.imgur.com/GYReXdJ.jpg', 'https://i.imgur.com/7RGssmH.jpg']
        }
    )
    jsonObj.append(
        {
            'memo': '1일 1영업! <b>러블리즈</b>!',
            'img': ['https://i.imgur.com/pBCATpD.gif', 'https://i.imgur.com/a3R2OdJ.gif', 'http://cfile10.uf.tistory.com/image/223A1D4759202BC11D3130']
        }
    )
    dat = json.dumps(jsonObj, ensure_ascii=False, sort_keys=True, indent=4)
    print(dat)
    with open("theqoo.json", 'w') as f:
        f.write(dat)

#make_json()
for _ in range(0, 24):  json_loading()
