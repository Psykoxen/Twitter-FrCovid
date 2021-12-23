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
	try:
		r = requests.get('https://covid.ourworldindata.org/data/owid-covid-data.json').json()
		data = r['FRA']['data'][-1]

		hst = open('date.json')
		hst_date = json.load(hst)
		hst.close()

		if len(hst_date['repertory'])==0 or (data['date'] != hst_date['repertory'][-1]):

			hst = open('date.json','w')
			hst_date['repertory'].append(data['date'])
			json.dump(hst_date, hst)
			hst.close()

			message = '|#COVID19| ~ '+datetime.datetime.now().strftime("{%w} %d {%m} 20%y").format(*days_FR,*mnths_FR)+' :\n\n---- ~ 😷 Contamination 😷 ~ ----\nNouveaux Cas : '+str(int(data['new_cases']))+'\nCas Totaux : '+str(int(data['total_cases']))+'\n--------- ~ ⚰️ Décès ⚰️ ~ ---------\nDécès du jour : '+str(int(data['new_deaths']))+'\nDécès Totaux : '+str(int(data['total_deaths']))+'\n------- ~ 🏥 Hôpitaux 🏥 ~ -------\nHospitalisations : '+str(int(data['hosp_patients']))+'\nSoins Intensif : '+str(int(data['icu_patients']))
			api.update_status(message)
			print(str(datetime.date.today())+' | TWEET | Covid Data')

		else:
			print(str(datetime.date.today())+' | TWEET | No Covid Data')

		time.sleep(3600)

	except:
		print(str(datetime.date.today())+' | ERROR | Covid Data')