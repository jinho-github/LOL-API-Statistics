
# python code
from flask import Flask,render_template,request
import os
import requests
from pprint import pprint as pp

app = Flask(__name__)

apikey = os.environ['LOL_API_KEY']
print("api_key\n",apikey)

@app.route('/')
def index():
    return render_template('index.html')
    

#그마 유저 데이터 긁어오기
'''
@app.route('/grandmaster')
def grandmaster():
    
    url= "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"
    headers = {
    
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "RGAPI-842c4573-a4c2-4b89-aa33-ea4610a6a7ec",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"

    }    
    res = requests.get(url=url,headers=headers)
    GMLeagueLists = res.json()
    
    def get_grandmaster_data(GMLeagueList):
        res = [        
        GMLeagueList.get('entries')
        ]
        return res
    results = []
    
    #for GMLeagueList in GMLeagueLists: #순회할 리스트가 정해져있을때 for in 반복문 사용  
    results.append(get_grandmaster_data(GMLeagueLists)) #append()는 object를 맨 뒤에 추가
     
    return render_template('search.html',results=results)
'''

#최근 전투 데이터 100개 가져오기
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
    
    spell_1 =[] #스펠1
    spell_2 =[] #스펠2

    for Game_ID in Game_IDs:
        url_GameData = "https://kr.api.riotgames.com/lol/match/v4/matches/{}".format(Game_ID)
        res_GameData = requests.get(url=url_GameData, headers = headers)
        
        #플레이시간
        duration = res_GameData.json()['gameDuration']//60                              
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
        b_baronKills.append(blue['baronKills'])#부순 포탑 갯수
        b_riftHeraldKills.append(blue['riftHeraldKills'])#부순 포탑 갯수
                 
        r_towerKills.append(red['towerKills'])
        r_inhibitorKills.append(red['inhibitorKills'])
        r_baronKills.append(red['baronKills'])
        r_riftHeraldKills.append(red['riftHeraldKills'])
        
        participantId = []
        #최근 20회 데이터 : 블루 5명이 항상 먼저, 그다음 레드 5명
        game_20 = res_GameData.json()['participantIdentities']
        for i in range(0, 10):  
            game_player = game_20[i].get('player') 
            name = game_player.get('summonerName')
            game_summonerName.append(name)    
            
            #내 participantID 찾았다!
            if(name == sum_name):
                participantId.append(i+1)
        
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
        wardsplaced.append(my_stat['wardsPlaced'])
        wardskill.append(my_stat['wardsKilled'])
        rune_1.append(my_stat['perkPrimaryStyle'])
        rune_2.append(my_stat['perkSubStyle'])

        spell_1.append(stats['spell1Id'])
        spell_2.append(stats['spell2Id'])
        champID.append(stats['championId'])

    return render_template('search.html', game_time=game_time , game_summonerName=game_summonerName, 
                            b_baronKills=b_baronKills, b_win=b_win, b_towerKills=b_towerKills, b_riftHeraldKills=b_riftHeraldKills, b_inhibitorKills=b_inhibitorKills,
                            r_baronKills=r_baronKills, r_win=r_win, r_towerKills=r_towerKills, r_riftHeraldKills=r_riftHeraldKills, r_inhibitorKills=r_inhibitorKills,
                            kill=kill, death=death, assist=assist, gold= gold, totalDmg=totalDmg, champDmg=champDmg, takenDmg=takenDmg, minion=minion, heal=heal,
                            largekill=largekill, magicDmg=magicDmg, psyDmg=psyDmg,champlevel=champlevel, visionScore=visionScore, v_wardbuy=v_wardbuy,wardsplaced=wardsplaced, wardskill=wardskill,
                            rune_1=rune_1, rune_2=rune_2,spell_1=spell_1, spell_2=spell_2,champID=champID )
    #return render_template('search.html' , results=Game_ID, length=length)
if __name__ == '__main__':
    app.run(debug=True)
    

