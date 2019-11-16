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

    url_GameID = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(account_Id) #{encryptedAccountId} = account_ID
    res_GameID = requests.get(url=url_GameID, headers=headers)
    Matches = res_GameID.json()['matches'] #gameID가 들어있는 Mathes를 가져옴
    
    def get_matches_info(Match):
        res=[
            Match.get('gameId')
        ]
        return res

    Game_ID = []    

    for Match in Matches:
        Game_ID.append(get_matches_info(Match))

    Game_ID = sum(Game_ID, [])
    #게임 ID 출력 확인(100개)
    '''
    for i in Game_ID:
        print(i)
    '''
    
    #게임 데이터 가져오려고 노력 중(20개씩)
    ##단일 데이터 : MatchDuration(게임 플레이 시간)
    ##리스트 안 딕셔너리 : participantIdentities
    i = 0
    game_Duration = []
    while True:
        url_GameData = "https://kr.api.riotgames.com/lol/match/v4/matches/{}".format(Game_ID[i])
        res_GameData = requests.get(url=url_GameData, headers = headers)
        
        #단일 데이터
        duration = res_GameData.json()['gameDuration']
        game_Duration.append(duration)

        #다중 데이터
        part = res_GameData.json()['participantIdentities']        
        
        i += 1
        if i == 20 :
            break

    #duration 출력 확인(20개)
    '''
    for j in game_Duration:
        print(j)
    '''    
    #participantIdentities 출력 확인(20개)
    '''
    for j in part :
            print(j)
    '''

    return render_template('search.html', results=duration)
    #return render_template('search.html' , results=Game_ID, length=length)
if __name__ == '__main__':
    app.run(debug=True)
    

