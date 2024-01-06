import time,os,sys

#import config parser
import configparser
config = configparser.ConfigParser()
config.read('classrum.ini')

# init connect to mogodb
import pymongo
dbclient = pymongo.MongoClient(config['MONGODB']['ServerAddress']) # get db address from config
dbdatabase = dbclient["traindata"]
TrainColumn = dbdatabase["train"]


TrainColumn.delete_many({})



def checkinline(TheDict, TheLine): # if this string is in the dict, return true
    for i in range(len(TheDict)):
        if TheDict[i] in TheLine:
            return True
    return False

def DoCheckInLine(TheDict,line,SubjectNum,TrainColumn): # if the string is in the dict, add to db
   if checkinline(TheDict,line):
       data = {"name": line.replace('\n','') , "subject" : SubjectNum}
       TrainColumn.insert_one(data)
       return True
   else:
       return False

def DoAllCheckInL(line,AllDicts,TrainColumn,AllSubjectNum): # testing all subject dicts
    theround = 0
    for littleDict in AllDicts:
        if DoCheckInLine(littleDict,line,AllSubjectNum[theround],TrainColumn):
            return True
        else:
            theround += 1
    return False

helpful_info = '''1英文
2國文
3地理
4家政
5公民
6體育
7歷史
8資訊
9音樂
10物理
11化學
12數學
13健康
14地科
15視覺藝術
16班級事物
17生物
18作文
19童軍
20輔導
'''
EnglishDict = ['英課','英文學習單','英翰','英習','英將','英講','英文','海洋之美','英文翰將','英卷','3688英文','英復講','橘子','英複講','2000單','單字','表藝']
ChineseDict = ['國課','國翰','國文學習單','國習','國文習作','國文','國講','國文講義','國卷','3688國文','國復講','國複講','自學','古文','默書','日日讀','解釋','國','字音字形','成語','文學海洋','情歌心得','仿寫','訪寫','最美的一句話學習單','世說新語','世說','國翰自學']
GeographyDict = ['地課','地學習單','地翰','地習','地理','地紙講']
HouseThingDict = ['家政','盤子','食材','圍裙','針線','食譜','烹飪']
CivisDict = ['公課','公民學習單','公獎','公習','公講','公民','公民講義','公填','公民填充']
SportDict = ['體育']
HistoryDict = ['歷史','歷講','歷史講義','歷卷','歷習']
ComputerDict = []
MusicDict = ['音樂','直笛']
PhysicsDict = ['物理','物講',"物卷"]
ChemistryDict = ['化學','化講','理化復講','化翰','理化','化卷','離子','海洋科學','自翰','元素表','周期表']
MathDict = ['數講','數學題本','百分百','段考王','數卷','3688數學','數復講','數學3688','數學','數複講','數學複講','尺','數練','練功坊','數習']
HealthDict = ['健康']
GeoscienceDict = ['地科','地講','地卷']
ArtDict = ["美術",'速寫','設計單']
ClassThingDict = ['班級事物','札記','回條','通知單','健保卡','學生證','校車','餐費','繳費單','制服','保險單','手冊','共讀書','通知書','服儀','回報','閱讀護照','調查表','意願書','單子','回饋單','同意書','班費','成績單','團膳費用']
BioDict = ['生物','生講','小白講','生卷','ko','KO']
WritingDict = ['作文']
KidArmyDict = ['童軍'] # wt happened to this translation
TakecareDict = ['輔導']
AllDicts = [EnglishDict,ChineseDict,GeographyDict,HouseThingDict,CivisDict,SportDict,HistoryDict,ComputerDict,MusicDict,PhysicsDict,ChemistryDict,MathDict,HealthDict,GeoscienceDict,ArtDict,ClassThingDict,BioDict,WritingDict,KidArmyDict,TakecareDict]
AllSubjectNum = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]

with open('train.txt', 'r',encoding="utf-8") as file:
    for line in file:
        if DoAllCheckInL(line,AllDicts,TrainColumn,AllSubjectNum):
            continue

        # check if the tag 'build' is there
        try:
             if sys.argv[1] == 'build':
                 print(line.replace('\n','')+ ' is passed because we wre running in build env.')
                 continue
        except IndexError:
                 pass

        print(helpful_info)
        response = input(line)
        data = { "name" : line.replace('\n','') , "subject" : response }
        TrainColumn.insert_one(data)
        print(data)
