from flask import Flask,render_template,request, url_for, session, redirect, flash
from flask_bcrypt import Bcrypt
import os
from flask_pymongo import PyMongo
import requests
import urllib.parse
from flask_ngrok import run_with_ngrok
from collections import Counter #모스트 원 구하기
#끌어오기 
import opgg_crawling
from time import sleep #받아오기 속도조절


apikey = os.environ['LOL_API_KEY']

app = Flask(__name__)
run_with_ngrok(app)
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
    #Matches = Matches.json()['matches']
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

    r_win = []
    r_towerKills = []
    r_inhibitorKills = []
    r_baronKills = []
    r_riftHeraldKills = []

    kill=[] #킬
    death=[] #데스
    assist=[] #어시
    gold=[] #획득한 골드
    totalDmg=[] #몬스터+게이머에게 가한 총 데미지
    champDmg=[] #게이머에게만 가한 총 데미지
    takenDmg=[] #받은 총 피해        
    minion=[] #미니언 수
    heal=[] #총 힐량
    largekill=[] #최대 킬수(최대트리플킬 까지 했당! 최대 쿼드라했다! 이런거)
    magicDmg=[] #마법공격력
    psyDmg=[] #신체 공격력?
    champlevel=[] #챔프 레벨
        
    visionScore=[] #시야점수
    v_wardbuy=[] #산 제어와드 갯수
    wardsplaced=[] #설치한 와드
    wardskill=[] #파괴한 와드

    rune_1 =[] #룬1
    rune_2=[] #룬2

    champID=[] #챔프
    champname=[] #챔프 이름
    spell_1 =[] #스펠1
    spell_2 =[] #스펠2
   
    champname_e = [] #영문 이름

    for Game_ID in Game_IDs:
        url_GameData = "https://kr.api.riotgames.com/lol/match/v4/matches/{}".format(Game_ID)
        res_GameData = requests.get(url=url_GameData, headers = headers)
        #플레이시간
        duration = res_GameData.json()['gameDuration']
        game_time.append(duration)

        #팀정보
        teams = res_GameData.json()['teams']
        
        blue = teams[0] 
        red = teams[-1]
          
        #딕셔너리로 넘기는것 보다 그냥 변수하나하나쪼개서 주는게 편하낭..? 
        if (blue['win']=='Win') :
            b_win.append('승리')
            r_win.append('패배')
        else :
            b_win.append('패배')
            r_win.append('승리')
                
        b_towerKills.append(blue['towerKills'])#부순 포탑 갯수
        b_inhibitorKills.append(blue['inhibitorKills'])#부순 억제기 갯수
        b_baronKills.append(blue['baronKills'])#바론 처치 수
        b_riftHeraldKills.append(blue['riftHeraldKills'])#전령 처치 수
                 
        r_towerKills.append(red['towerKills'])
        r_inhibitorKills.append(red['inhibitorKills'])
        r_baronKills.append(red['baronKills'])
        r_riftHeraldKills.append(red['riftHeraldKills'])

        #최근 20회 데이터
        participantId = []
        game_20 = res_GameData.json()['participantIdentities']
        temp = []
        for i in range(0, 10):
            game_player = game_20[i].get('player') 
            temp.append(game_player.get('summonerName'))
        
            #내 participantID 
            name = game_player.get('summonerName')
            if(name == sum_name):
                participantId.append(i+1)

        game_summonerName.append(temp)

        #개인 통계
        stats=[]
        participants = res_GameData.json()['participants']
        for i in participantId:
            stats.append(participants[i-1])
        stats=stats[0]

        my_stat=stats['stats']
                
        kill.append(my_stat['kills'])
        death.append(my_stat['deaths'])
        assist.append(my_stat['assists'])
        gold.append(my_stat['goldEarned'])
        totalDmg.append(my_stat['totalDamageDealt'])
        champDmg.append(my_stat['totalDamageDealtToChampions'])
        takenDmg.append(my_stat['totalDamageTaken'])
        minion.append(my_stat['totalMinionsKilled'])
        heal.append(my_stat['totalHeal'])
        largekill.append(my_stat['largestMultiKill'])
        magicDmg.append(my_stat['magicDamageDealtToChampions'])
        psyDmg.append(my_stat['physicalDamageDealtToChampions'])
        champlevel.append(my_stat['champLevel'])        
        visionScore.append(my_stat['visionScore'])
        v_wardbuy.append(my_stat['visionWardsBoughtInGame'])
        #wardsplaced.append(my_stat['wardsPlaced'])
        #wardskill.append(my_stat['wardsKilled'])
        rune_1.append(my_stat['perkPrimaryStyle'])
        rune_2.append(my_stat['perkSubStyle'])

        spell_1.append(stats['spell1Id'])
        spell_2.append(stats['spell2Id'])
        champID.append(stats['championId'])


    static_data_url = 'http://ddragon.leagueoflegends.com/cdn/9.24.2/data/ko_KR/champion.json'
    data = requests.get(static_data_url).json()
    data = data['data']    
    data=list(data.values())

    

    for i in range(0,20):
        id=int(champID[i])
        for j in range(0,147):
            d = data[j]  
            key = int(d['key'])
            if (id == key):
                n = d['name']
                champname.append(n)

    #영문
    static_data_url_e = 'http://ddragon.leagueoflegends.com/cdn/9.24.2/data/en_US/champion.json'
    data_e = requests.get(static_data_url_e).json()
    data_e = data_e['data']    
    data_e=list(data_e.values())

    for i in range(0,20):
        id=int(champID[i])
        for j in range(0,147):
            d_e = data[j]  
            key_e = int(d_e['key'])
            if (id == key_e):
                n_e = d_e['name']
                champname_e.append(n_e)
   
    #모스트
    most_champ = sorted(champname)
    most_champ = Counter(most_champ)
    most_one = most_champ.most_common(1)

    #모스트 영문
    most_champ_e = sorted(champname_e)
    most_champ_e = Counter(most_champ_e)
    most_one_e = most_champ_e.most_common(1)
    """
    temp_index = []
    for i in (0, 20):
        if champname[i] is most_one[0][0]:
            temp_index.append(i)
    for j in temp_index:
        k = kill[j]
        d = death[j]
        a = assist[j]
    """
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
    game_time=game_time , game_summonerName=game_summonerName, 
                            b_baronKills=b_baronKills, b_win=b_win, b_towerKills=b_towerKills, b_riftHeraldKills=b_riftHeraldKills, b_inhibitorKills=b_inhibitorKills,
                            r_baronKills=r_baronKills, r_win=r_win, r_towerKills=r_towerKills, r_riftHeraldKills=r_riftHeraldKills, r_inhibitorKills=r_inhibitorKills,
                            kill=kill, death=death, assist=assist, gold= gold, totalDmg=totalDmg, champDmg=champDmg, takenDmg=takenDmg, minion=minion, heal=heal,
                            largekill=largekill, magicDmg=magicDmg, psyDmg=psyDmg,champlevel=champlevel, visionScore=visionScore, v_wardbuy=v_wardbuy,wardsplaced=wardsplaced, wardskill=wardskill,
                            rune_1=rune_1, rune_2=rune_2,spell_1=spell_1, spell_2=spell_2,champname=champname, most_one=most_one, champname_e=champname_e, most_one_e=most_one_e)


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

        return render_template('matching.html', my_info_list=my_info_list)
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
    #app.run(debug=True, host='127.0.0.1')
    app.run()
