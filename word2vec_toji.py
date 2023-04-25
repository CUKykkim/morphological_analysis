import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
from gensim.models import word2vec
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
twitter = Twitter()
results = []
lines = text.split("\r\n")
for line in lines:
    # 형태소 분석하기 --- (※3)
    # 단어의 기본형 사용
    malist = twitter.pos(line, norm=True, stem=True)   #norm=True 각 단어의 정규화(normalization)를 수행하도록 지정하는 인자, stem=True, 각 단어를 어간(stem)으로 추출하도록 지정하는 인자
    r = []
    for word in malist:
        # 어미/조사/구두점 등은 대상에서 제외 
        if not word[1] in ["Josa", "Eomi", "Punctuation"]:
            r.append(word[0])
    rl = (" ".join(r)).strip()
    results.append(rl)
    # print(rl)
# 파일로 출력하기  --- (※4)
gubun_file = 'toji.gubun'
with open(gubun_file, 'w', encoding='utf-8') as fp:
    fp.write("\n".join(results))
# Word2Vec 모델 만들기 --- (※5)
data = word2vec.LineSentence(gubun_file) # 주어진 파일에 한 줄씩 접근하여 각 줄에 포함된 단어들을 띄어쓰기로 구분하여 LineSentence 객체로 적재

 # window는 한 단어 주변에 고려할 단어의 수, min_count는 최소 단어 빈도수, sg는 Word2Vec의 학습 알고리즘을 선택 sg=1로 설정하면 Skip-Gram 알고리즘을 사용하고, sg=0으로 설정하면 CBOW(Continuous Bag-of-Words) 알고리즘을 사용
 # hs=1로 설정하면 hierarchical softmax를 사용, hs=0으로 설정하면 negative sampling을 사용
model = word2vec.Word2Vec(data, 
    vector_size=200, window=10, hs=1, min_count=2, sg=1) 
model.save("toji.model")  
print("ok")