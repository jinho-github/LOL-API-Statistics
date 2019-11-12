from flask import Flask,render_template,request, url_for, session, redirect, flash
import bcrypt
import os
from flask_pymongo import PyMongo
import requests
import urllib.parse
#끌어오기 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
apikey = os.environ['LOL_API_KEY']
#mongokey = os.environ['MONGO_KEY']

app = Flask(__name__)
#DB와 비밀번호는 환경변수에서 가져온다.
app.config['MONGO_URI'] = os.environ['MONGO_KEY']
mongo = PyMongo(app)
#client = pymongo.MongoClient(mongokey)
#db = client.get_database('WGM_DB')



@app.route('/')
def index():
    myurl = "https://www.op.gg/champion/statistics"
    url = urlopen(myurl)
    soup = BeautifulSoup(url,"lxml")
    
    Top_champ_name = []
    Top_champ_pick_per = []
    Jungle_champ_name = []
    Jungle_champ_pick_per = []
    Mid_champ_name = []
    Mid_champ_pick_per = []
    Ad_champ_name = []
    Ad_champ_pick_per = []
    Support_champ_name = []
    Support_champ_pick_per = []
    
    #탑
    Top_champion = soup.find(name='tbody',attrs={'class':'tabItem champion-trend-tier-TOP'})
    for link1 in Top_champion.select('tr'):
        try:
            #챔피언 이름     
            td_tag = link1.select('td')[3]
            a_tag = td_tag.select('a')[0]
            get_name = a_tag.select('div')[0]
            get_name = get_name.text
            get_name = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', get_name) #특수한문자제거
            get_name = re.sub(" ", "", get_name) #공백제거
            Top_champ_name.append(get_name)
            #승률
            td_tag = link1.select('td')[4]
            Top_champ_pick_per.append(td_tag.text)
        except:
            pass
    
    #정글
    Jungle_champion = soup.find(name='tbody',attrs={'class':'tabItem champion-trend-tier-JUNGLE'})
    for link2 in Jungle_champion.select('tr'):
        try:
            #챔피언 이름     
            td_tag = link2.select('td')[3]
            a_tag = td_tag.select('a')[0]
            get_name = a_tag.select('div')[0]
            get_name = get_name.text
            get_name = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', get_name) #특수한문자제거
            get_name = re.sub(" ", "", get_name) #공백제거
            Jungle_champ_name.append(get_name)
            #승률
            td_tag = link2.select('td')[4]
            Jungle_champ_pick_per.append(td_tag.text)
        except:
            pass

    #미드
    Mid_champion = soup.find(name='tbody',attrs={'tabItem champion-trend-tier-MID'})
    for link3 in Mid_champion.select('tr'):
        try:
            #챔피언 이름     
            td_tag = link3.select('td')[3]
            a_tag = td_tag.select('a')[0]
            get_name = a_tag.select('div')[0]
            get_name = get_name.text
            get_name = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', get_name) #특수한문자제거
            get_name = re.sub(" ", "", get_name) #공백제거
            Mid_champ_name.append(get_name)
            #승률
            td_tag = link3.select('td')[4]
            Mid_champ_pick_per.append(td_tag.text)
        except:
            pass

    #바텀
    Ad_champion = soup.find(name='tbody',attrs={'tabItem champion-trend-tier-ADC'})
    for link4 in Ad_champion.select('tr'):
        try:
            #챔피언 이름     
            td_tag = link4.select('td')[3]
            a_tag = td_tag.select('a')[0]
            get_name = a_tag.select('div')[0]
            get_name = get_name.text
            get_name = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', get_name) #특수한문자제거
            get_name = re.sub(" ", "", get_name) #공백제거
            get_name = get_name.replace('KaiSa','Kaisa')#이미지 오류로 인해 이름 변경
            Ad_champ_name.append(get_name)
            #승률
            td_tag = link4.select('td')[4]
            Ad_champ_pick_per.append(td_tag.text)
        except:
            pass

    #서포터
    Support_champion = soup.find(name='tbody',attrs={'class':'tabItem champion-trend-tier-SUPPORT'})
    for link5 in Support_champion.select('tr'):
        try:
            #챔피언 이름     
            td_tag = link5.select('td')[3]
            a_tag = td_tag.select('a')[0]
            get_name = a_tag.select('div')[0]
            get_name = get_name.text
            get_name = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', get_name) #특수한문자제거
            get_name = re.sub(" ", "", get_name) #공백제거
            Support_champ_name.append(get_name)
            
            #승률
            td_tag = link5.select('td')[4]
            Support_champ_pick_per.append(td_tag.text)
        except:
            pass

    return render_template('index.html',Top_champ_name = Top_champ_name, Top_champ_pick_per = Top_champ_pick_per,
                                        Jungle_champ_name = Jungle_champ_name, Jungle_champ_pick_per = Jungle_champ_pick_per,
                                        Mid_champ_name = Mid_champ_name, Mid_champ_pick_per = Mid_champ_pick_per, 
                                        Ad_champ_name = Ad_champ_name, Ad_champ_pick_per = Ad_champ_pick_per, 
                                        Support_champ_name = Support_champ_name, Support_champ_pick_per = Support_champ_pick_per)
@app.route('/application')
def search():
    sum_name = request.args.get('name')
    #sum_name = urllib.parse.quote(sum_name) #URL Encoding
    
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(sum_name)
    
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": apikey,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    res = requests.get(url=url,headers=headers)
    encrypted_id = res.json()['id']
    profileIcon_id = res.json()['profileIconId']
    url_league = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(encrypted_id)
    res_league = requests.get(url=url_league,headers=headers)
    league_dicts = res_league.json()


    def get_league_info(league_dict):
        res = [
        league_dict.get('queueType'),
        league_dict.get('tier'),
        league_dict.get('rank'),
        league_dict.get('wins'),
        league_dict.get('losses'),
        league_dict.get('leagueName'),
        league_dict.get('leaguePoints')
            ]
        return res
        
    results = []
    for league_dict in league_dicts:
        results.append(get_league_info(league_dict))
        #results.append(아이콘넘버)
    length = len(results)
    

    return render_template('application.html',sum_name=sum_name,results=results,length=length, profileIcon=profileIcon_id)

    #에러페이지 404, 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


"""
@app.route('/login_modal', method=['POST', 'GET'])
def login():
    return ''
"""
@app.route('/login_modal', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        myuser = mongo.db.user_Info
        existing_user = myuser.find_one({'email' : request.form['register_email']})
        #오류해결해야함..
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['register_pw2'].encode('utf-8'), bcrypt.gensalt())
            myuser.insert({'email' : request.form['register_email'], 'password' : hashpass})
            #session['register_email'] = request.form['register_email']
            flash("회원가입 완료!")
            return redirect(url_for('index'))
            
        #message = '동일한 이메일이 존재합니다.'
        return redirect(url_for('login'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
