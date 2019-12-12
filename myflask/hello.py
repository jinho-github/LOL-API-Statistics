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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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
<<<<<<< HEAD
<<<<<<< HEAD

    tip_List = mongo.db.tip_List
    get_tips = tip_List.find().sort([['_id', -1]]).limit(10)
    tip_lists = []
    
    for get_tip in get_tips:
        temp = []
        temp.append(get_tip['tip_select'])
        temp.append(get_tip['tip_url'])
        temp.append(get_tip['tip_text'])
        temp.append(get_tip['name'])
        tip_lists.append(temp)

=======
=======
>>>>>>> 8c8bc26ea6e88d76dd79e36a8b9063ee96620a1e
    '''
    #디비에서 video_id 가져오기
    myvideo = mongo.db.video_List 
    get_video_ids = myvideo.find().sort([['_id', -1]]).limit(10)
    video_id_list = []
    for get_video_id in get_video_ids:
        video_id_list.append(get_video_id['video_id'])
    '''
<<<<<<< HEAD
>>>>>>> 8c8bc26ea6e88d76dd79e36a8b9063ee96620a1e
=======
>>>>>>> 8c8bc26ea6e88d76dd79e36a8b9063ee96620a1e
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
<<<<<<< HEAD
<<<<<<< HEAD
                                        Support_champ_name = Support_champ_name, Support_champ_pick_per = Support_champ_pick_per,
                                        tip_lists = tip_lists)
=======
                                        Support_champ_name = Support_champ_name, Support_champ_pick_per = Support_champ_pick_per)
                                      
>>>>>>> 8c8bc26ea6e88d76dd79e36a8b9063ee96620a1e
=======
                                        Support_champ_name = Support_champ_name, Support_champ_pick_per = Support_champ_pick_per)
                                      
>>>>>>> 8c8bc26ea6e88d76dd79e36a8b9063ee96620a1e
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
        url_GameData = "https://kr.api.riotgames.com/lol/match/v4/matches/{}".format(Game_ID)
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


@app.route('/Tip_list')
def Tip_list():
    #데이터베이스에 저장된 팁을 리스트로 전달
    tip_List = mongo.db.tip_List
    get_tips = tip_List.find().sort([['_id', -1]])
    tip_lists = []
    
    for get_tip in get_tips:
        temp = []
        temp.append(get_tip['tip_select'])
        temp.append(get_tip['tip_url'])
        temp.append(get_tip['tip_title'])
        temp.append(get_tip['tip_text'])
        temp.append(get_tip['name'])
        tip_lists.append(temp)
    tip_list_size =len(tip_lists)
    return render_template('Tip_list.html', tip_lists = tip_lists, tip_list_size = tip_list_size)

@app.route('/Tip_add', methods=['POST', 'GET'])
def Tip_add():
    #받아온 팁 정보를 데이터 베이스에 저장

    if int(request.form['tip_select']) is 1:
        select = '탑'
    elif int(request.form['tip_select']) is 2:
        select = '정글'
    elif int(request.form['tip_select']) is 3:
        select = '미드'
    elif int(request.form['tip_select']) is 4:
        select = '원딜'
    else:
        select = '서포터'

    add_tip = mongo.db.tip_List
    name = str(session['email'])
    name = name.split('@')[0]
 
    add_tip.insert({'tip_select' : select, 'tip_url' : request.form['tip_url'], 'tip_title' : request.form['tip_title'], 'tip_text' : request.form['tip_text'], 'name' : name })
    flash('나만의 팁 등록!!') 
    return redirect(url_for('Tip_list'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


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

@app.route('/matching')
def matching():

    return render_template('matching.html')
if __name__ == '__main__':
    app.run(debug=True)
