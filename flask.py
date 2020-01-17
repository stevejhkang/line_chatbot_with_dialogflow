from flask import Flask, request, make_response, jsonify
from urllib.request import urlopen, Request
import urllib
import bs4
import requests, json
app = Flask(__name__)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from sklearn.decomposition import PCA

from gensim.test.utils import datapath, get_tmpfile
# from gensim.models import KeyedVectors
# print("start")
# model_ko = KeyedVectors.load_word2vec_format('./wiki.ko.vec')
#
#
# model_ko.init_sims(replace=True)
# model_ko.save('bio_word')
#
# KeyedVectors.load('bio_word',mmap='r')
#
# print("end")
#
# print(model_ko.most_similar('요리'))



def get_weather():
    location = '서울'
    enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html5lib')
    print('현재 ' + location + ' 기온은 ' +
          soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text
          + '도 입니다.')

    temp = soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text
    weather = soup.find('p', class_='cast_txt').text.split(',')[0]
    dust = soup.find('dd', class_='lv2').text.split('㎥')[1]
    print("기온 : " + soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text)
    print("날씨 : " + soup.find('p', class_='cast_txt').text.split(',')[0])
    print("미세먼지 : " + soup.find('dd', class_='lv2').text.split('㎥')[1])
    return [weather, dust, temp]


@app.route('/')
def index():
    return "Hello Post!!"


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))


def results():
    req = request.get_json(force=True)
    print(req)
    print('-----------------------------')
    # queryText = req.get('queryResult').get('queryText')
    # address = req.get('queryResult').get('parameters').get('address')
    # color = req.get('queryResult').get('parameters').get('color')
    # size = req.get('queryResult').get('parameters').get('size')

    # print("address : "+address+"\ncolor : "+color+"\nsize : "+size)
    intent = req.get('queryResult').get('intent').get('displayName')
    print(intent)
    act = "test"
    if intent == "weather_data":
        chk = 0
        weather_data = get_weather()
        print('오늘 날씨는 ' + weather_data[0] + ", 미세먼지는 " + weather_data[1])
        if weather_data[0] in "맑음" or weather_data[0] in "구름" or weather_data[0] in "흐림":
            chk += 1
        if weather_data[1] == "좋음" or weather_data[1] == "보통":
            chk += 1
        if int(weather_data[2]) >= 0:
            chk += 1
        flag = 0

        if chk >= 2:
            flag = True
            act="야외활동"
        else:
            flag = False
            act="실내활동"

        return {'fulfillmentText': '오늘 날씨는 ' + weather_data[0] + ", 미세먼지는 " + weather_data[1] + ", 기온은 " + weather_data[
            2] + "도입니다. "+ "오늘 같은 날씨에는 "+act+"을 추천드려요. "+act+"을 추천드릴까요?" }
    if intent == "weather_data_yes":
        weather_data = get_weather()
        chk = 0
        print('오늘 날씨는 ' + weather_data[0] + ", 미세먼지는 " + weather_data[1])
        if weather_data[0] in "맑음" or weather_data[0] in "구름" or weather_data[0] in "흐림":
            chk += 1
        if weather_data[1] == "좋음" or weather_data[1] == "보통":
            chk += 1
        if int(weather_data[2]) >= 0:
            chk += 1
        flag = 0

        if chk >= 2:
            flag = True
            act = "야외활동"
        else:
            flag = False
            act = "실내활동"
        print(act)
        if act=="야외활동":
            return {"fulfillmentText": "네. " + act + "을 추천해드릴게요. 추천하는 " + act + "리스트입니다. ", "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "선택해주세요."
                        ]
                    },
                    "platform": "LINE"
                },
                {
                    "quickReplies": {
                        "title": "하고 싶은 활동은..",
                        "quickReplies": [
                            "자전거",
                            "한강",
                            "등산",
                            "놀이공원",
                            "낚시",
                            "축구","테니스","야구관람","스키장","눈썰매","해수욕장","캠핑"
                        ]
                    },
                    "platform": "LINE"
                },

            ]
                    }
        else:
            return {"fulfillmentText": "네. " + act + "을 추천해드릴게요. 추천하는 " + act + "리스트입니다. ", "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "선택해주세요."
                        ]
                    },
                    "platform": "LINE"
                },
                {
                    "quickReplies": {
                        "title": "하고 싶은 활동은..",
                        "quickReplies": [
                            "박물관",
                            "도서관",
                            "영화관",
                            "카페","PC방","술","스케이트장","삼겹살","미술관"
                        ]
                    },
                    "platform": "LINE"
                },

            ]
                    }
    if intent=="active_detail":
        activity=req.get('queryResult').get('parameters').get('act')
        print(activity)
       


        client_id = "PhDm_JK08OUyY0dAPd0I"
        client_secret = "XlH0QepBb2"

        url = "https://openapi.naver.com/v1/search/blog.json"

        params = {'query': activity, 'display': 1}

        response = requests.get(url=url,
                                params=params,
                                headers={"X-Naver-Client-Id": client_id,
                                         "X-Naver-client-Secret": client_secret,
                                         "Content-Type": "application/json; charset=utf-8"})

        rescode = response.status_code

        if rescode == 200:
            response_body = response.content
            y = json.loads(response_body)
            print(y.get('items')[0].get('link'))
            return {'fulfillmentText': y.get('items')[0].get('link') }

        else:
            print("Error Code", rescode)



# {
  #       "text": {
  #         "text": [
  #           "선택해주세요"
  #         ]
  #       }
  #     }

if __name__ == '__main__':
    app.run(debug=True)

