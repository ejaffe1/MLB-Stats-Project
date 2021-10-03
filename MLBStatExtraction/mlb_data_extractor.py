#Ezra Jaffe
#08/18/2021

import os
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

def main():
    #ESPN()
    proceed=True
    while(proceed==True):
        BaseballReference()
        user=input("If you are done, enter 'stop', otherwise hit enter to continue\n")
        if user=='stop' or user=='Stop':
            proceed=False
                
def ESPN(): #WebScraping Practice
    URL='http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2018/start/1'
    page=requests.get(URL)
    soup=BeautifulSoup(page.text,'html.parser')
        
    header=soup.find('tr', attrs={'class':'colhead'})
    print(header)
    columns=[col.get_text() for col in header.find_all('td')]
    final_df=pd.DataFrame(columns=columns)
        
    for i in range(1,331,50):
        URL='http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2021/start/{}'.format(i)
        page=requests.get(URL)
        soup=BeautifulSoup(page.text,'html.parser')

        ##row=soup.find('tr', attrs = {'class': 'oddrow player-10-33039'})
        #row=soup.find('tr', attrs = {'class': 'evenrow player-10-30112'})
        ##for data in row.find_all('td'):
            ##print(data.get_text())
        
        players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
        for player in players:
            
            stats=[stat.get_text() for stat in player.find_all('td')]
            
            temp_df=pd.DataFrame(stats).transpose()
            temp_df.columns=columns

            final_df=pd.concat([final_df,temp_df], ignore_index=True)
            
        final_df
            
    final_df.to_csv(r'MLB_Stats_Test_2021.csv',index=False,sep=',',encoding='utf-8')

def BaseballReference():
    #player=' '
    #https://www.baseball-reference.com/register/player.fcgi?id=bishop000hun
    playerName=input('Enter player name\n')
    mOmi=input('Has this player played in the majors? Please enter yes or no\n')

    if mOmi=='yes' or mOmi=='Yes':
        MLB_Player(playerName)

    if mOmi=='no' or mOmi=='No':
        MiLB_Player(playerName, '000',0)
        

def MLB_Player(playerName):
    baseURL='https://www.baseball-reference.com/players/{}.shtml'
    player=playerName.lower()
    nameList=player.split()
    firstName=nameList[0]
    lastName=nameList[1]
    
    if len(lastName)>5:
        size=len(lastName)
        remove=size-5
        lastName=lastName[:size-remove]
        
    playerCode=lastName[0]+'/'+lastName+firstName[:2]+'01'

    if len(nameList)>2:
        if nameList[2]=='jr' or nameList[2]=='jr.':
            yn=input("Did this player's father play in the MLB? Please enter yes or no\n")

            if yn=='yes' or yn=='Yes':
                playerCode=playerCode.replace('1','2')
    
    #w/wadela01
    #URL='https://www.baseball-reference.com/players/w/wadela01.shtml'
                
    URL=baseURL.format(playerCode)
    print(URL)
    
    #URL CHECK
    if (requests.head(URL).status_code)==404:
        print('This player does not exist')
        return
    
    df=pd.read_html(URL,header=0)
    df_mm=df[0]
    eIndex=int(df_mm[df_mm['Year']=='162 Game Avg.'].index.values)
    df_mm=df_mm.drop(range(eIndex-1,len(df_mm)))
    player=player.replace(' ','')
          
    df_mm.to_csv('%s.csv' % player,index=False,sep=',',encoding='utf-8')
    
    print('CSV file for', playerName, 'has been created')
    
def MiLB_Player(playerName, numbers, count):
    baseURL='https://www.baseball-reference.com/register/player.fcgi?{}'
    #id=bishop000hun
    player=playerName.lower()
    nameList=player.split()
    firstName=nameList[0]
    lastName=nameList[1]
    
    if len(lastName)>6:
        size=len(lastName)
        remove=size-6
        lastName=lastName[:size-remove]
    if len(lastName)<6:
        size=6-len(lastName)
        for i in range(size):
            lastName=lastName+'-'
    
    playerCode='id='+lastName+numbers+firstName[:3]

##        if len(nameList)>2:
##            if nameList[2]=='jr' or nameList[2]=='jr.':
##                yn=input("Did this player's father play in the MLB? Please enter yes or no\n")
##
##                if yn=='yes' or yn=='Yes':
##                    playerCode=playerCode.replace('1','2')
    
                
    URL=baseURL.format(playerCode)
    print(URL)
    
    #URL CHECK
    if (requests.head(URL).status_code)==302:
        count=count+1
        strCount=str(count)
        numbers=numbers[:2]+strCount
        MiLB_Player(playerName, numbers, count)
        return
    
    if (requests.head(URL).status_code)==404:
        print('This player does not exist/n')
        return
    
    df=pd.read_html(URL,header=0)
    print(df)
    df_mm=df[0]
##    eIndex=int(df_mm[df_mm['Year']=='Year'].index.values)
##    df_mm=df_mm.drop(range(eIndex,len(df_mm)))
    player=player.replace(' ','')
    
    df_mm.to_csv('%s.csv' % player,index=False,sep=',',encoding='utf-8')
    
    print('CSV file for', playerName, 'has been created')

    correctPlayer=input('Is this the correct player? Please type yes or no\n')

    if correctPlayer=='yes' or correctPlayer=='Yes':
        return

    if correctPlayer=='no' or correctPlayer=='No':
        count=count+1
        strCount=str(count)
        numbers=numbers[:2]+strCount
        MiLB_Player(playerName, numbers, count)
        return

######################################################################################################
    
#ESPN()
#BaseballReference()
main()
print('ALL DONE')
