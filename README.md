# LOL-API-Statistics
배포된 페이지 : http://3.133.102.24:5000/

## Python-Flask 설치

-   파이썬에서는 웹 페이지 제작을 위해 디장고, 플라스크를 많이 사용하는데 소규모 프로젝트이기 때문에 플라스크를 사용했습니다.
    
-   Flask위에서 웹 페이지가 동작하기 때문에 번거롭게 XAMPP를 사용하거나 PHP문을 사용할 필요가 없다는 장점이 있습니다.
    

pip install Flask를 명령 프롬프트 창에 입력해서 Flask를 설치 할 수 있습니다.

## 웹 페이지 만들기

-   부트스트랩을 사용했습니다.
-   Python-Flask에서 지원하는 jinja2문을 사용해 html문을 작성했습니다.

디자인과 반응형 웹 페이지를 생각해 부트스트랩을 사용해서 만들었습니다.

nav부분과 footer 부분은 다른 페이지로 넘어가더라도 바뀌지 않는 부분이라서 base.html로 만들어 줬습니다.

(jinja2문법을 이용해서 base.html을 기초로 하는 html파일들을 만들 수 있습니다.)

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2F00ag8%2FbtqAQM8bVPK%2FW8UKXZ3C528z12r9NlpQTK%2Fimg.png)

헤더와 footer 사이에 block content 라고 선언합니다.

block content를 사용하기 위해서는 불러올 html 파일의 첫 부분에 아래와 같이 선언해야 합니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FnQkG2%2FbtqAQkRCwvt%2F0gqXu9M7adBYTNJo8LzOn0%2Fimg.png)
index.html 파일의 첫 부분입니다. 

extends로 base.html을 상속받는다고 선언합니다.

이제 base.html에서 채워주지 않았던 body부분을 채워줍니다.

```
{% extends "base.html" %}

{% block content %}

html문 채워 넣기

{% endblock %}
```

위와 같이 block content와 endblock 사이에 원하는 html문으로 내용을 채워 넣습니다.

## Flask로 웹 페이지 띄우기

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
```

@app. route('/') 역 슬레쉬는 Flask에서 가장 처음 실행될 부분이라는 뜻입니다.

위 코드처럼 입력하고 코드를 실행, 로컬 호스트(127.0.0.1)에 접속하면 index.html 창이 열리게 됩니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FcEqe5Q%2FbtqATgteTyk%2FmEA7xPJSSXT7jluRFNQuOk%2Fimg.png)

단 아래와 같이 같은 파일의 templates 파일 안에 index.html 파일이 존재해야 합니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FIBtUq%2FbtqAQ3ICsHA%2FycQGkZTbKLFisXZGwp7wi1%2Fimg.png)

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FMFrry%2FbtqARieu5xi%2FjK93YR2KzJ1LEkHkScgk81%2Fimg.png)


## 목표

이미 많은 유저들이 OP.GG와 같은 전적 검색 사이트를 이용하지만 상위 티어의 통계만을 이용해 분석된 데이터만 보여줍니다. 따라서 하위 티어에 있는 유저에게는 큰 도움이 되지 않습니다.

또 유저 매칭 시 보이는 정보가 부족하고  라이너 별 팁 정보를 확인하기 어렵습니다.

때문에 이러한 문제점을 해결해서 전적 검색 사이트를 만드는 것을 목표로 했습니다.

---

## 수행 내용 및 방법

1) 정적 정보 불러오기

-   리그오브레전드에서 제공하는 API 파싱을 통해, 최근 경기 20개의 데이터를 JSON 형태로 가져옵니다.

2) 웹페이지 구현 및 시각화

-   Python-Flask를 기반으로 웹 개발 (HTML, CSS, JavaScript를 사용하여 웹 페이지를 구현)
-   부트스트랩 사용

3) 데이터베이스 사용

-   웹 페이지 사용자의 정보를 이용해 다양한 기능 제공을 위해 데이터베이스(MongoDB)를 사용
-   회원가입, 로그인 기능을 구현
-   게시물 등록, 노출 기능을 구현
-   수집된 사용자 정보를 이용해 유저매칭

---

## 1) 정적 정보 불러오기

https://developer.riotgames.com/

위 사이트에 로그인을 하고 API 키를 발급받아야 API 사용이 가능합니다.

(발급받지 않고 임시로 발급되는 키를 사용하면 일정 시간 동안만 사용이 가능합니다.)

https://velog.io/@marcus/TOY-1-라이엇-API를-사용해서-롤-전적-사이트를-만들어보자-gojpscoym4

API 키 발급에 대한 내용은 위 블로그에 자세히 나와 있습니다.

발급받은 키는 윈도우 시스템 환경변수에 등록해서 사용했습니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2F5L0Oi%2FbtqATgzUjb7%2FXiS0BI4IFqlJAuBUtYali0%2Fimg.png)

```
import os
apikey = os.environ['LOL_API_KEY']

```

시스템 환경 변수를 사용하기 위해 파이썬 os라이브러리를 import 했습니다.

API를 사용해 여러 가지 게임 정보를 불러올 수 있는데 라이엇 디벨로퍼 페이지에서 확인 가능합니다.

저는 검색한 유저의 정보와 최근 게임 기록을 가져왔습니다.

```
@app.route('/data')

def data():
    sum_name = request.args.get('name') 

    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": apikey,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }

    url_SummonerName = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(sum_name) 
    res_SummonerName = requests.get(url=url_SummonerName, headers=headers)
    account_Id = res_SummonerName.json()['accountId'] #account id 가져오기
```

유저 정보와 게임 기록을 가져오기 위해서는 유저 아이디가 아닌 코드로 이루어진 계정 아이디를 사용해야 하기 때문에 

**우선 계정 아이디를 알아내야 합니다.**

위 코드와 같이 url과 헤더를 붙여서 json형태로 요청했습니다.

가져온 json코드에서 'accountId'만 떼어 **account\_Id를** 사용할 수 있게 되었습니다.

이제 **account\_Id를** 사용해서 유저 정보와 게임 정보를 가져옵니다.

```
url_GameID = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420".format(account_Id) #{encryptedAccountId} = account_ID, 솔랭은 queuetype = 420
    res_GameID = requests.get(url=url_GameID, headers=headers)
    Matches = res_GameID.json()['matches'] #gameID가 들어있는 Mathes를 가져옴
    
    Game_IDs = []  
    for m in range(0, 20):
        Game_IDs.append(Matches[m].get('gameId'))

    game_time = []
    game_summonerName = []
    b_win= []
    b_towerKills = []
    b_inhibitorKills = []
    b_baronKills = []
    b_riftHeraldKills = []
    .
    .
    .
    .
```

수집된 데이터 확인을 위해 웹 페이지에 수집된 정보를 뿌려봤습니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2Fee4ARr%2FbtqAQmohr8a%2FaMnobYGeZbPktw7i97TH9k%2Fimg.png)

---

## 한계점

라이엇 측에서 한 번에 가져올 수 있는 데이터에 제한을 걸어둬서 통계, 분석이 어렵다는 한계점이 있었고 데이터를 매번 가져오기 때문에 속도가 느려서 많은 데이터를 가져올 수 없었습니다.

문제 해결을 위해 데이터베이스를 사용을 고려해봤지만 방대한 양의 데이터를 저장하기엔 자금이 부족했기 때문에 검색한 유저의 최근 게임 기록 20개만 가져오도록 했습니다.

---


