# 한국어 분석

## KoNLPy 설치

- Java 1.7+ 설치

 * Java를 설치하기 위해  [오라클 홈페이지](https://www.oracle.com/java/technologies/downloads/#jdk17-windows)에 접속하여, 설치파일을 다운로드 한다.

![1](./images/1.png)

- Java 환경변수를 설정한다. 
 * 시스템 변수

![2](./images/2.png)

![3](./images/3.png)

![4](./images/4.png)

- Java 설치 확인
 * Terminal에서 java -version 을 수행해 본다.

```
java -version


java version "17.0.6" 2023-01-17 LTS
Java(TM) SE Runtime Environment (build 17.0.6+9-LTS-190)
Java HotSpot(TM) 64-Bit Server VM (build 17.0.6+9-LTS-190, mixed mode, sharing)
```

```
apt-get install g++ openjdk-8-jdk
```

- KoNLPy 패키지 설치

```
pip install konlpy jpype1
```

- KoNLPy 설치 테스트
 * 혹 오류가 난다면, VScode 를 재시작

 ```
from konlpy.tag import Okt
okt = Okt()
malist = okt.pos("아버지 가방에 들어가신다.", norm=True, stem=True)
print(malist)
 ```


## 형태소 분석을 기반으로 한 단어 출현 빈도 구하기

- 박경리 토지 소설에서 많이 등장한 단어 분석하기

```
import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
# utf-16 인코딩으로 파일을 열고 글자를 출력하기 --- (※1)
fp = codecs.open("https://github.com/CUKykkim/morphological_analysis/blob/master/BEXX0003.txt", "r", encoding="utf-16")
soup = BeautifulSoup(fp, "html.parser")
body = soup.select_one("body > text")
text = body.getText()
# 텍스트를 한 줄씩 처리하기 --- (※2)
twitter = Twitter()
word_dic = {}
lines = text.split("\n")
for line in lines:
    malist = twitter.pos(line)
    for word in malist:
        if word[1] == "Noun": #  명사 확인하기 --- (※3)
            if not (word[0] in word_dic):
                word_dic[word[0]] = 0
            word_dic[word[0]] += 1 # 카운트하기
# 많이 사용된 명사 출력하기 --- (※4)
keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)
for word, count in keys[:50]:
    print("{0}({1}) ".format(word, count), end="")
print()
```




## Gensim의 Word2Vec으로 단어 벡터화 하기

- Gensim 설치

```
pip install gensim
```

- Gensim의 word2vec으로 토지에 나오는 단어 벡터화 하기

```
import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
from gensim.models import word2vec
# utf-16 인코딩으로 파일을 열고 글자를 출력하기 --- (※1)
fp = codecs.open("BEXX0003.txt", "r", encoding="utf-16")
soup = BeautifulSoup(fp, "html.parser")
body = soup.select_one("body > text")
text = body.getText()
# 텍스트를 한 줄씩 처리하기 --- (※2)
twitter = Twitter()
results = []
lines = text.split("\r\n")
for line in lines:
    # 형태소 분석하기 --- (※3)
    # 단어의 기본형 사용
    malist = twitter.pos(line, norm=True, stem=True)
    r = []
    for word in malist:
        # 어미/조사/구두점 등은 대상에서 제외 
        if not word[1] in ["Josa", "Eomi", "Punctuation"]:
            r.append(word[0])
    rl = (" ".join(r)).strip()
    results.append(rl)
    print(rl)
# 파일로 출력하기  --- (※4)
gubun_file = 'toji.gubun'
with open(gubun_file, 'w', encoding='utf-8') as fp:
    fp.write("\n".join(results))
# Word2Vec 모델 만들기 --- (※5)
data = word2vec.LineSentence(gubun_file)
model = word2vec.Word2Vec(data, 
    vector_size=200, window=10, hs=1, min_count=2, sg=1)
model.save("toji.model")
print("ok")
```