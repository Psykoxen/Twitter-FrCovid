import requests
import json
import datetime
import time
import tweepy
import log


############################################################### - LOGIN TWEET - ####################################################################

auth = tweepy.OAuthHandler(log.consumer_key, log.consumer_secret)
auth.set_access_token(log.access_token, log.access_token_secret)
api = tweepy.API(auth)

############################################################### - INITIALISATION - ####################################################################

days_FR = ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi']
mnths_FR = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
certif = True

################################################################## - MAIN - ####################################################################
while certif == True:
	data = requests.get('https://coronavirusapifr.herokuapp.com/data/live/france').json()[0]
	print(data)
	hst = open('date.json')
	hst_date = json.load(hst)
	hst.close()

	if len(hst_date['repertory'])==0 or (data['date'] != hst_date['repertory'][-1]):

		hst = open('date.json','w')
		hst_date['repertory'].append(data['date'])
		json.dump(hst_date, hst)
		hst.close()

		message = '|#COVID19| ~ '+datetime.date(int(data['date'][:4]),int(data['date'][5:7]),int(data['date'][8:])).strftime("{%w} %d {%m} 20%y").format(*days_FR,*mnths_FR)+' :\n\n---- ~ 😷 Contamination 😷 ~ ----\nNouveaux Cas : '+str(int(data['conf_j1']))+'\nCas Totaux : '+str(int(data['conf']))+'\n--------- ~ ⚰️ Décès ⚰️ ~ ---------\nDécès du jour : '+str(int(data['incid_dchosp']))+'\nDécès Totaux : '+str(int(data['dchosp']))+'\n------- ~ 🏥 Hôpitaux 🏥 ~ -------\nHospitalisations : '+str(int(data['hosp']))+'\nSoins Intensif : '+str(int(data['rea']))
		#api.update_status(message)
		print(message)
		print(str(datetime.date.today())+' | TWEET | Covid Data')
	else:
		print(str(datetime.date.today())+' | TWEET | No Covid Data')
	time.sleep(3600)