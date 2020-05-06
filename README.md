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

## 2) 웹페이지 구현 및 시각화

> Python-Flask를 사용했으며 부트스트랩으로 시각화 했습니다. 

> 코드가 길어 생략합니다. (코드는 [https://github.com/Yeowoolee/LOL-API-Statistics](https://github.com/Yeowoolee/LOL-API-Statistics) 에서 확인 가능합니다.)

-   이번 글에서는 페이지의 구성에 대해서만 간략히 설명합니다.

> 메인화면 header


![로그인 전 상단](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FykrFm%2FbtqBJf05TYY%2Fhxd193ZOhrb9LaYCL9PqvK%2Fimg.png)

![로그인 후 상단](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbHy4LQ%2FbtqBIIoUYCG%2FR9zKxDMMHYfuk4LYeQkjB1%2Fimg.png)

모든 페이지의 상단에 존재해야 하기 때문에 base.html의 <header> 에 코드를 작성 했습니다.

jinja2 문법으로 사용자가 로그인에 성공하면 버튼이 바뀌도록 했습니다.

> 메인화면 body 

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FciirYQ%2FbtqBFwKvuJE%2FdTNEc4cMDu2zcGL3kgK6k0%2Fimg.png)

메인화면에는 위와 같이 소환사 정보 검색창, 라인 별 챔피언 추천, 추천 영상이 노출 되도록 했습니다.

-   소환사 정보 검색창을 통해 리그오브레전드 게임 아이디를 넣고 검색하면 해당 아이디의 게임 정보가 표시된 페이지로 이동합니다.
-   라인 별 챔피언 추천은 각 라이별 승률이 높은 챔피언을 모달을 통해 보여줍니다.
-   추천 영상은 나만의 팁에서 작성한 글에 영상이 포함되어있을 경우 노출됩니다.

> 소환사 정보 확인 페이지

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FoVqCU%2FbtqBGZ58UYo%2FBdn9gNURZQ3UUjh2mXake0%2Fimg.png)
-   소환사 정보 검색 후 위 페이지로 이동하게 됩니다.
-   api를 통해 불러온 정보를 시각적으로 보여주는 페이지 입니다.
-   위와같이 페이지 상단에서는 현재 티어와 리그정보, 랭크 포인트 승패 정보와 모스트 챔피언 최근 경기 K/D/A를 그래프로 확인 할 수 있습니다.
-   페이지 body 부분에는 최근 20 게임의 정보가 표시됩니다.

> 나만의 팁 페이지

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FJdNXs%2FbtqBFvLI0qK%2FDRelY6cSOwarQbYvbmyv80%2Fimg.png)
-   나만의 팁 페이지에서는 각 라인별 팁을 확인 할 수 있습니다.
-   글쓰기 버튼을 클릭하면 글을 작성 할 수 있는 모달이 나타납니다.

> 유저매칭 페이지

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FtF6Py%2FbtqBIHjocJM%2FinJKjkuyNA9iJYeaPyeKM0%2Fimg.png)
-   내 정보를 등록하기 전에는 유저 매칭이 이루어지지 않습니다.
-   유저매칭을 위해 자신의 게임 아이디와 라인, 주로하는 챔피언을 등록합니다.
-   데이터베이스에 등록된 다른 사용자 정보를 이용해 매칭합니다.

---
## 데이터베이스 사용

전적 검색 사이트의 회원가입, 로그인, 게시판, 유저 매칭, 전적 검색 여러 기능들을 구현하기 위해 데이터베이스를 사용했고 mongoDB를 사용했습니다. Flask를 사용했기 때문에 PHP구문 없이 데이터베이스를 활용할 수 있었습니다.

> 회원가입

![]()
페이지 상단의 회원가입 버튼을 누르면

아래와 같이 회원가입 모달이 페이지에 띄워집니다.

![]()
회원가입 모달에 이메일, 비밀번호를 입력하고 회원가입 버튼을 누르면

'POST' 형태로 Flask에 전달됩니다.

```
@app.route('/register_modal', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        myuser = mongo.db.user_Info
        existing_user = myuser.find_one({'email' : request.form['register_email']})
        if existing_user is None:
            hashpass = bcrypt.generate_password_hash(request.form['register_pw2'])
            myuser.insert({'email' : request.form['register_email'], 'password' : hashpass})
            flash('회원가입 성공!!') 
            return redirect(url_for('index'))
        flash('이미 사용중인 이메일입니다.') 
        return redirect(url_for('index'))
    return render_template('index.html')
```

만약 이메일이 mongoDB에 등록되어 있으면 이메일이면 '이미 사용중인 이메일입니다.'라는 플래시 메시지를 출력하고

그렇지 않으면 mongoDB에 이메일과 비밀번호를 등록합니다.

비밀번호는 bcrypt Hash함수를 사용하여 암호화된 상태로 데이터베이스에 저장됩니다.

\-회원가입 실패

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbP4e3B%2FbtqBZrOONFx%2F7tj7kK1yFukGZ9YoLgSf3k%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbeXuow%2FbtqBZg7PrxU%2FgopEfwUb4hPWLawCX8eTVk%2Fimg.png)

\-회원가입 성공

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbkkbkA%2FbtqBZNKSBMa%2FHhu0rpiIXEZtx0dfSuggXK%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FowUGr%2FbtqB1HbRrcU%2FFneg7yRHOmUcLII3ORmPLk%2Fimg.png)
\-mongoDB에 등록된 이메일과 비밀번호

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FAPh1G%2FbtqBZrOPqNe%2FrZKxVJxcsRcu6T6tB4wxwk%2Fimg.png)

> 로그인

회원가입과 마찬가지로 로그인 버튼을 누르면 로그인 모달이 띄워지고

mongoDB의 데이터와 비교해 이메일과 비밀번호가 일치하면 '로그인 성공' 플래시 메시지를 출력하고

그렇지 않으면 '로그인 실패' 플레쉬를 출력합니다.

bcrypt Hash함수를 사용하여 암호화해줬기 때문에 마찬가지로 bcrypt Hash함수를 이용해 복호화 후 비밀번호를 비교합니다.

```
@app.route('/login_modal', methods=['POST'])
def login():
    #if request.method == 'POST':
    myuser = mongo.db.user_Info
    login_user = myuser.find_one({'email' : request.form['login_email']})
    if login_user:
        pw_check = bcrypt.check_password_hash(login_user['password'], request.form['login_pw'])
        if pw_check is True:
            session['email'] = request.form['login_email']
            flash('로그인 성공!')
            return redirect(url_for('index'))
        
        flash('이메일, 패스워드를 다시 확인해주세요.')
        return redirect(url_for('index'))
    flash('이메일, 패스워드를 다시 확인해주세요.')
    return redirect(url_for('index'))
```

\-로그인 성공

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FV3yyP%2FbtqB0e2wbiS%2F5E5aKMYdUAtPbSKIkOj421%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FqzPN8%2FbtqBZgzZp6o%2F36hOu9p6mCh9HoeUUEdsw1%2Fimg.png)

\-로그인 실패

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FTDOhl%2FbtqB1HCWuyf%2FxNhinp3ooOGawzDQyUxJIK%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbT5iSQ%2FbtqBZr2kjRb%2FJsVS4Z5P1Nb27YebiIc5Vk%2Fimg.png)

> 게시판

로그인에 성공하면 '나만의 팁', '유저 매칭' 버튼이 생기게 됩니다.

'나만의 팁' 버튼을 클릭하면 게시판으로 이동 할 수 있고 '글쓰기' 버튼을 눌러 정보를 입력할 수 있습니다.

입력된 내용은 mongoDB에 저장되며 게시판 글을 클릭해 확인 할 수 있고

유튜브 영상이 첨부된 경우 메인 페이지에서 확인이 가능합니다.

\-게시판 글 등록

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbtijUB%2FbtqBZg06p6Y%2Fn7WyYJjMGGcnAydFe5bNCk%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FrpBFW%2FbtqB1cpUQp8%2FlU0zGzDoU7Oq7qJjbDi060%2Fimg.png)

\-게시글 확인

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2F5TyIA%2FbtqBYf9xSeS%2FqMnIqcul37LK0R8lNXF8h1%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FlnaK0%2FbtqB1cjbJKK%2FH2RB1DRXMWxwGU9831gvl0%2Fimg.png)

> 유저매칭

유저 매칭 게시판으로 이동하면 사용자가 등록한 유저 정보에 맞춰 유저를 매칭 합니다.

등록된 상태가 아니면 매칭 정보를 등록해달라는 메시지를 출력하고

등록이 되어있으면 등록한 사용자들의 정보를 보여줍니다.

변경사항이 있으면 다시 등록해 내 정보를 변경할 수 있습니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FZhzVh%2FbtqBXVDqQr1%2FzXiLewNCIDYhFuyI7w49Ak%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2Fxvk5F%2FbtqB0eBxFJx%2FKyh4v0EvM74JQ8hT19MFNK%2Fimg.png)

\-변경 전

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FdqeJ3F%2FbtqB1doPEAj%2F3br7rZhqrfc0pTtj7kiNnk%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FRc3Oj%2FbtqB1ccoE9I%2FyID0P2LSufEHtTpRyFCuA1%2Fimg.png)

\-변경 후

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbGKFva%2FbtqBZfHT89v%2FAUZBhWFC6V6NfLsXHbv1w0%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FdlI7tl%2FbtqBYtGqQJD%2FnBOrpe6rwruj4eeAW0KQP1%2Fimg.png)

> 전적 검색

메인 페이지의 검색창에 리그 오브 레전드 닉네임을 입력하면 api를 이용해 최근 전적 20게임을 불러옵니다.

불러온 데이터를 기반으로 최근 경기 킬/데스/어시스트를 그래프로 표시하고

모스트 챔피언, 현재 리그 정보를 표시합니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FHGZ6w%2FbtqBYe3QxIM%2F73UVbJVODKh5HKLpPRUnF1%2Fimg.png)

> 라인 별 챔피언 추천

초기 계획은 티어 별 추천 챔피언을 제공할 계획이었지만 상당히 많은 양의 데이터를 필요로 해서 다른 사이트의 정보를 파싱 해오는 것으로 대체했습니다.

BeautifulSoup를 이용해 파싱 하고 수집한 데이터는 모달에 출력합니다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FyktOU%2FbtqB1c4Bi4C%2F2Jv5wJmL0L7U4pZQ82nR1K%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FAg0hT%2FbtqB1mFVT6g%2F6ZuZZS8gpnQXwjQFWK7NU1%2Fimg.png)

---

## 배포

## **ngrok**

완성된 웹 페이지를 배포하는 방법은 여러 가지가 있습니다.

가장 빠른 배포 방법은 ngrok를 사용하는 방법입니다.

ngrok는 Flask에서 라이브러리로 지원하며 테스트 환경에서. py 코드를 실행시키면 배포가 완료됩니다.

ngrok로 실행시 터미널에 띄워지는 주소로 접속할 수 있습니다.

하지만 24시간 서버를 열어놓기 위해서는 터미널을 계속 열어두어야 하고 주소가 매번 바뀐다는 단점이 있습니다.

## **Heroku**

heroku는 배포를 하기 위해 몇가지 조건이 필요합니다. 설치된 라이브러리가 들어있는 **requirements.txt **파일이 필요하고 **Procfile**에서 서버의 구동 방식과 시작할 파이썬 파일을 지정해줘야 합니다. 처음 배포할 때 자잘한 오류로 인해 배포하는데 오래 걸렸지만 익숙해지면 배포하기 정말 편한 서비스인 것 같습니다.

장점으로는 배포시 인증서 발급, 주소 고정, 클라우드 서비스이므로 배포가 완료된 후에는 언제든 접속 가능합니다.

**헤로쿠 배포에 대한 자세한 내용은 아래 게시글에서 확인할 수 있습니다.**

https://yeowool0217.tistory.com/616?category=854081

## **AWS**

서버관리부터 데이터베이스 도메인 등 모든 걸 한 번에 해결할 수 있는 서비스입니다.

원하는 운영체제로 서버를 구동시킬 수 있다는 장점이 있고 heroku처럼 배포하기 위한 파일이 필요하지 않습니다.

원하는 운영체제로 인스턴스를 생성하고 프로젝트 파일을 가져오고

배포에 필요한 조건**(debug mode = off, host = '0.0.0.0')**을 맞춰주면 배포하는데 필요한 준비가 끝납니다.

단점은 위 2개의 서비스와는 다르게 **기간제(12개월) 무료**라는 점입니다.

**AWS배포에 대한 자세한 내용은 아래 게시글에서 확인할 수 있습니다.**

https://yeowool0217.tistory.com/620?category=854081

---

LOL전적 검색 App은 AWS로 배포했습니다.

배포과정은 위에 첨부된 'Flask를 AWS에 Deploy 하기'라는 글에서 확인할 수 있습니다.

#### 배포 과정에서 생긴 오류 

> OSError: \[Errno 98\] Address already in use

인스턴스에 연결 후 터미널에서 파이썬 파일을 열어 Flask를 작동시키려고 할 때 생기는 오류입니다.

이 오류가 방생한다는 것은 이미 같은 포트를 사용하는 프로세스가 작동중이기 때문입니다.

따라서 강제로 프로세스를 종료시켜야 하는데

터미널에 다음과 같은 명령어를 입력하면 됩니다.

\>> fuser -k 포트번호/ tcp 

오류가 생긴이유 Flask실행 후 종료 시 Ctrl + z를 눌러서 종료했기 때문인 것 같습니다.

Ctrl + c 를 눌러서 종료했을 때는 위와 같은 문제가 발생하지 않았습니다.

> 부트스트랩 모달 오류

부트스트랩 모달마다 html파일을 따로 만들어두고 jinja의 macro를 이용해 불러오기를 할 때 경로를 찾지 못하는 문제가 발생합니다. 테스트 환경인 Windows10 + Python3.6에서는 문제없이 작동하지만 리눅스 환경에서는 제대로 작동하지 않았습니다. 

macro를 사용하지 않고 모든 모달 태그를 모달을 요청하는 html에 넣어주었습니다.

코드가 많이 길어졌지만 오류는 해결되었습니다.

---

