from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def opgg(Top_champ_name,
    Top_champ_pick_per,
    Jungle_champ_name,
    Jungle_champ_pick_per,
    Mid_champ_name,
    Mid_champ_pick_per,
    Ad_champ_name,
    Ad_champ_pick_per,
    Support_champ_name,
    Support_champ_pick_per):
    
    myurl = "https://www.op.gg/champion/statistics"
    url = urlopen(myurl)
    soup = BeautifulSoup(url,"lxml")
    
    
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
    
    return Top_champ_name,
    Top_champ_pick_per,
    Jungle_champ_name,
    Jungle_champ_pick_per,
    Mid_champ_name,
    Mid_champ_pick_per,
    Ad_champ_name,
    Ad_champ_pick_per,
    Support_champ_name,
    Support_champ_pick_per