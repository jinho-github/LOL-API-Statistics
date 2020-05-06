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

https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2F00ag8%2FbtqAQM8bVPK%2FW8UKXZ3C528z12r9NlpQTK%2Fimg.png

헤더와 footer 사이에 block content 라고 선언합니다.

block content를 사용하기 위해서는 불러올 html 파일의 첫 부분에 아래와 같이 선언해야 합니다.

[##_Image|kage@nQkG2/btqAQkRCwvt/0gqXu9M7adBYTNJo8LzOn0/img.png|alignLeft|data-origin-width="0" data-origin-height="0"|||_##]

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

[##_Image|kage@cEqe5Q/btqATgteTyk/mEA7xPJSSXT7jluRFNQuOk/img.png|alignLeft|data-origin-width="0" data-origin-height="0" width="614" height="312"|||_##]

단 아래와 같이 같은 파일의 templates 파일 안에 index.html 파일이 존재해야 합니다.

[##_Image|kage@IBtUq/btqAQ3ICsHA/ycQGkZTbKLFisXZGwp7wi1/img.png|alignLeft|data-origin-width="0" data-origin-height="0" width="616" height="56"|||_##]

[##_Image|kage@MFrry/btqARieu5xi/jK93YR2KzJ1LEkHkScgk81/img.png|alignLeft|data-origin-width="0" data-origin-height="0"|||_##]

