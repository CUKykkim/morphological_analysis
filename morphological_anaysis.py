import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
import requests
# utf-16 인코딩으로 파일을 열고 글자를 출력하기 --- (※1)

URL = "https://cukykkim.github.io/toji/"  # 웹상에서 토지 소설의 일부를 불러오기

toji = requests.get(URL)
toji.encoding= "utf-16"     # utf-16으로 인코딩
html = toji.text

# print(html)

soup = BeautifulSoup(html, 'html.parser')

body = soup.select_one("body > text")

text = body.get_text()

# 텍스트를 한 줄씩 처리하기 --- (※2)
twitter = Twitter()   #  트위터 객체를 생성
word_dic = {}      # 추출한 명사와 그 출현 빈도를 저장하기 위한 딕셔너리를 생성
lines = text.split("\n")
for line in lines:
    # print(line)
    malist = twitter.pos(line)  # 주어진 텍스트를 형태소 단위로 분석하고, 각 형태소의 품사 태그와 함께 튜플 형태로 반환
    # print(malist)
    for word in malist:
        if word[1] == "Noun": #  명사 확인하기 --- (※3)
            if not (word[0] in word_dic):
                word_dic[word[0]] = 0
            word_dic[word[0]] += 1 # 카운트하기
    # print(word_dic) 
# 많이 사용된 명사 출력하기 --- (※4)
keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True) # 딕셔너리의 값을 기준으로 내림차순으로 정렬
for word, count in keys[:50]:
    print("{0}({1}) ".format(word, count), end="")
print()