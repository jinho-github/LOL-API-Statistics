from flask import Flask,render_template,request, url_for, session, redirect, flash
from flask_bcrypt import Bcrypt
import os
from flask_pymongo import PyMongo
import requests
import urllib.parse
#끌어오기 
import opgg_crawling
from time import sleep #받아오기 속도조절



app = Flask(__name__)
#DB와 비밀번호는 환경변수에서 가져온다.
app.config['SECRET_KEY'] = ""
app.config['MONGO_URI'] = ""
apikey = ""
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


"""
Rate Limits
20 requests every 1 seconds
100 requests every 2 minutes
"""

@app.route('/')
def index(name=None):

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
                                        tip_lists = tip_lists)

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
    if not encrypted_id:
        return "아이디를 찾을 수 없습니다."
    accountId = res.json()['accountId']
    profileIcon_id = res.json()['profileIconId'] #소환사 프로필ID 가져오기
    
    #id로 소환사 정보 불러오기
    url_league = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(encrypted_id)
    res_league = requests.get(url=url_league,headers=headers)
    league_dicts = res_league.json()

    #매치정보 불러오기
    url_GameID = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420".format(accountId)  #{encryptedAccountId} = account_ID
    res_GameID = requests.get(url=url_GameID, headers=headers)
    
    Matches = res_GameID.json()['matches'] #gameID가 들어있는 Mathes를 가져옴
    #매치 20개로 자르기
    Matches = Matches[:20]

    #매치를 못찾을 경우
    if not Matches:
        return "이번 시즌 랭크 매치 정보를 찾을 수 없습니다."
    Game_IDs = []
    for Matche in Matches:
        Game_IDs.append(Matche['gameId'])
           
    champID=[] #챔프
    Game_DATAs = []
    for Game_ID in Game_IDs:

        Game_DATA = {'game_time':'','b_win':'', 'b_towerKills':'', 'b_inhibitorKills':'', 'b_baronKills':'', 'b_riftHeraldKills':'',
        'r_win':'', 'r_towerKills':'', 'r_inhibitorKills':'', 'r_baronKills':'', 'r_riftHeraldKills':'',
        'b_player':[], 'r_player':[], 'stats':''}

        url_GameData = "https://kr.api.riotgames.com/lol/match/v4/matches/{}".format(Game_ID)
        res_GameData = requests.get(url=url_GameData, headers = headers)
        #플레이시간
        Game_DATA['game_time'] = res_GameData.json()['gameDuration']

        #팀정보
        teams = res_GameData.json()['teams']
        
        blue = teams[0] 
        red = teams[-1]
        if (blue['win']=='Win') :
            Game_DATA['b_win'] = '승리'
            Game_DATA['r_win'] = '패배'
        else :
            Game_DATA['b_win'] = '패배'
            Game_DATA['r_win'] = '승리'
                
        Game_DATA['b_towerKills'] = blue['towerKills'] #포탑
        Game_DATA['b_inhibitorKills'] = blue['inhibitorKills'] #억제기
        Game_DATA['b_baronKills'] = blue['baronKills'] #바론
        Game_DATA['b_riftHeraldKills'] = blue['riftHeraldKills'] #전령

        Game_DATA['r_towerKills'] = red['towerKills'] #포탑
        Game_DATA['r_inhibitorKills'] = red['inhibitorKills'] #억제기
        Game_DATA['r_baronKills'] = red['baronKills'] #바론
        Game_DATA['r_riftHeraldKills'] = red['riftHeraldKills'] #전령

        #최근 20회 데이터
        game_20 = res_GameData.json()['participantIdentities']
        myid_num = 0
        #blue, red 플레이어 이름 
        for i in range(0, 10):
            if accountId == game_20[i].get('player').get('accountId'):
                myid_num = i
            if i < 5:
                Game_DATA['b_player'] += [game_20[i].get('player').get('summonerName')]
            else:
                Game_DATA['r_player'] += [game_20[i].get('player').get('summonerName')]
        
        #개인 통계
        participants = res_GameData.json()['participants'][myid_num]
        champID.append(participants['championId'])
        stats = participants['stats']
        Game_DATA['stats'] = stats
        Game_DATAs.append(Game_DATA)

    static_data_url = 'http://ddragon.leagueoflegends.com/cdn/9.24.2/data/ko_KR/champion.json'
    data = requests.get(static_data_url).json()
    data = data['data']
    my_most_one = []
    my_most = dict()
    for mychamp in champID:
        for key, value in data.items():
            if int(mychamp) == int(value['key']):
                n = value['name']
                en_n = value['id']
                my_most_one.append([en_n, n])
                if (en_n, n) not in my_most:
                    my_most[(en_n, n)] = 1
                else:
                    my_most[(en_n, n)] += 1

    most_num = 0
    most_one = ()
    for key, value in my_most.items():
        if int(value) > most_num:
            most_num = value
            most_one = key
    
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
    length=length, profileIcon=profileIcon_id, my_most_one=my_most_one, most_one=most_one, most_num=most_num,Game_DATAs=Game_DATAs, zip=zip)


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

@app.route('/matching')
def matching():
    try:
        my_info = mongo.db.matching_user_info
        name = str(session['email'])
        name = name.split('@')[0]
        get_my_info = my_info.find_one({'name' : name})
        my_info_list = []
        my_info_list.append(get_my_info['matching_select'])
        my_info_list.append(get_my_info['user_id'])
        my_info_list.append(get_my_info['matching_champ'])

        user_info_list = []
        get_user_infos = my_info.find( { 'name': { '$ne': name } } )
        
        for get_user_info in get_user_infos:
            temp_info = []
            temp_info.append(get_user_info['matching_select'])
            temp_info.append(get_user_info['user_id'])
            temp_info.append(get_user_info['matching_champ'])
            user_info_list.append(temp_info)

        return render_template('matching.html', my_info_list=my_info_list, user_info_list=user_info_list)
    except:
        return render_template('matching.html')

@app.route('/matching_user_add', methods=['POST', 'GET'])
def matching_user_add():
    if int(request.form['matching_line_select']) is 1:
        select = '탑'
    elif int(request.form['matching_line_select']) is 2:
        select = '정글'
    elif int(request.form['matching_line_select']) is 3:
        select = '미드'
    elif int(request.form['matching_line_select']) is 4:
        select = '원딜'
    elif int(request.form['matching_line_select']) is 5:
        select = '서포터'
    else:
        select = '올라이너'

    matching_user = mongo.db.matching_user_info
    name = str(session['email'])
    name = name.split('@')[0]

    existing_user = matching_user.find_one({'name' : name})
    if existing_user is None:
        matching_user.insert({'matching_select' : select, 'user_id' : request.form['matching_user_id'], 'matching_champ' : request.form['matching_champ'],  'name' : name })
        flash('내 매칭 정보 등록!!')
    else:
        matching_user.update({'name': name}, {'matching_select' : select, 'user_id' : request.form['matching_user_id'], 'matching_champ' : request.form['matching_champ'], 'name' : name})
        flash('내 매칭 정보 수정!!') 
    return redirect(url_for('matching'))

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



if __name__ == '__main__':
    app.run(host='127.0.0.1')
