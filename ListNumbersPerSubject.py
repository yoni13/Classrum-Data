#import config parser
import configparser
config = configparser.ConfigParser()
config.read('classrum.ini')

# init connect to mogodb
import pymongo
dbclient = pymongo.MongoClient(config['MONGODB']['ServerAddress']) # get db address from co>
dbdatabase = dbclient["traindata"]
TrainColumn = dbdatabase["train"]

startnum = 0


AllSubjectNum = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
SubjectNames = ["英文","國文","地理","家政","公民","體育","歷史","資訊","音樂","物理","化學","數學","健康","地科","視覺藝術","班級事物","生物","作文","童軍",'輔導']
round = 0
for CurrentRoundNum in AllSubjectNum:
	for x in TrainColumn.find({ "subject": CurrentRoundNum}):
		startnum += 1
	print(SubjectNames[round] + " : " + str(startnum))
	startnum = 0
	round += 1
