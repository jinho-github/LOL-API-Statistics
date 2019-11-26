from flask import Flask,render_template,request, url_for, session, redirect, flash
from flask_bcrypt import Bcrypt
import os
from flask_pymongo import PyMongo
import requests
import urllib.parse
#끌어오기 
import opgg_crawling

from time import sleep #받아오기 속도조절


apikey = os.environ['LOL_API_KEY']

app = Flask(__name__)
#DB와 비밀번호는 환경변수에서 가져온다.
app.config['MONGO_URI'] = os.environ['MONGO_KEY']
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


"""
Rate Limits
20 requests every 1 seconds
100 requests every 2 minutes
"""

@app.route('/')
def index():
    #디비에서 video_id 가져오기
    myvideo = mongo.db.video_List 
    get_video_ids = myvideo.find().sort([['_id', -1]]).limit(10)
    video_id_list = []
    for get_video_id in get_video_ids:
        video_id_list.append(get_video_id['video_id'])

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

    opgg_crawling.opgg(Top_champ_name,
    Top_champ_pick_per,
    Jungle_champ_name,
    Jungle_champ_pick_per,
    Mid_champ_name,
    Mid_champ_pick_per,
    Ad_champ_name,
    Ad_champ_pick_per,
    Support_champ_name,
    Support_champ_pick_per)
    
    return render_template('index.html',Top_champ_name = Top_champ_name, Top_champ_pick_per = Top_champ_pick_per,
                                        Jungle_champ_name = Jungle_champ_name, Jungle_champ_pick_per = Jungle_champ_pick_per,
                                        Mid_champ_name = Mid_champ_name, Mid_champ_pick_per = Mid_champ_pick_per, 
                                        Ad_champ_name = Ad_champ_name, Ad_champ_pick_per = Ad_champ_pick_per, 
                                        Support_champ_name = Support_champ_name, Support_champ_pick_per = Support_champ_pick_per,
                                        video_id_list = video_id_list)
@app.route('/application')
def search():
    sum_name = request.args.get('name')

    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": apikey,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }

    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(sum_name)
    res = requests.get(url=url,headers=headers)
    encrypted_id = res.json()['id'] #id 가져오기
    accountId = res.json()['accountId']
    profileIcon_id = res.json()['profileIconId'] #소환사 프로필ID 가져오기
    
    #id로 소환사 정보 불러오기
    url_league = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(encrypted_id)
    res_league = requests.get(url=url_league,headers=headers)
    league_dicts = res_league.json()

    #매치정보 불러오기
    url_GameID = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(accountId) #{encryptedAccountId} = account_ID
    res_GameID = requests.get(url=url_GameID, headers=headers)
    Matches = res_GameID.json()['matches'] #gameID가 들어있는 Mathes를 가져옴
    #Matches = Matches.json()['matches']
    Game_IDs = []  
    for m in range(0, 20):
        Game_IDs.append(Matches[m].get('gameId'))

    game_time = []
    game_summonerName = []
    sleep(2) #20개 불러오기전에 쉬기
    #테스트하다 가끔씩 api락 걸림
    for Game_ID in Game_IDs:
        url_GameData = "https://ㄴkr.api.riotgames.com/lol/match/v4/matches/{}".format(Game_ID)
        res_GameData = requests.get(url=url_GameData, headers = headers)
        #플레이시간
        duration = res_GameData.json()['gameDuration']
        game_time.append(duration)
        #최근 20회 데이터
        game_20 = res_GameData.json()['participantIdentities']
        temp = []
        for i in range(0, 10):
            game_player = game_20[i].get('player') 
            temp.append(game_player.get('summonerName'))
        game_summonerName.append(temp)

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
    length = len(results)
    

    return render_template('application.html',sum_name=sum_name,results=results,
    length=length, profileIcon=profileIcon_id,
    game_time=game_time , game_summonerName=game_summonerName)


    #에러페이지 404, 500
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



@app.route('/login_modal', methods=['POST'])
def login():
    if request.method == 'POST':
        myuser = mongo.db.user_Info
        login_user = myuser.find_one({'email' : request.form['login_email']})
        if login_user:
            pw_check = bcrypt.check_password_hash(login_user['password'], request.form['login_pw'])
            if pw_check is True:
                #session['username'] == request.form['login_email']
                return redirect(url_for('index'))
            return '유저이름, 패스워드 오류'

@app.route('/register_modal', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        myuser = mongo.db.user_Info
        existing_user = myuser.find_one({'email' : request.form['register_email']})
        if existing_user is None:
            hashpass = bcrypt.generate_password_hash(request.form['register_pw2'])
            myuser.insert({'email' : request.form['register_email'], 'password' : hashpass})
            return redirect(url_for('index')) 
        return '동일한 이메일이 존재합니다.'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
