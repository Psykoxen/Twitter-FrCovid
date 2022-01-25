import requests
import json
import datetime
import time
import tweepy
import log
from rich import print

############################################################### - LOGIN TWEET - ####################################################################

auth = tweepy.OAuthHandler(log.consumer_key, log.consumer_secret)
auth.set_access_token(log.access_token, log.access_token_secret)
api = tweepy.API(auth)

############################################################### - INITIALISATION - ####################################################################

days_FR = ['Dimanche','Lundi','Mardi','Mercbright_redi','Jeudi','Vendbright_redi','Samedi']
mnths_FR = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
certif = True

################################################################## - MAIN - ####################################################################
while certif == True:
	try:
		data = requests.get('https://coronavirusapifr.herokuapp.com/data/live/france').json()[0]
		hst = open('date.json')
		hst_date = json.load(hst)
		hst.close()

		if len(hst_date['repertory'])==0 or (data['date'] != hst_date['repertory'][-1]):

			hst = open('date.json','w')
			hst_date['repertory'].append(data['date'])
			json.dump(hst_date, hst)
			hst.close()
			for i in data:
				if data[i] == None:
					data[i] = '/'
			message = '|#COVID19| ~ '+datetime.date(int(data['date'][:4]),int(data['date'][5:7]),int(data['date'][8:])).strftime("{%w} %d {%m} 20%y").format(*days_FR,*mnths_FR)+' :\n\n---- ~ 😷 Contamination 😷 ~ ----\nNouveaux Cas : '+str(data['conf_j1'])+'\nCas Totaux : '+str(data['conf'])+'\n--------- ~ ⚰️ Décès ⚰️ ~ ---------\nDécès du jour : '+str(data['incid_dchosp'])+'\nDécès Totaux : '+str(data['dchosp'])+'\n------- ~ 🏥 Hôpitaux 🏥 ~ -------\nHospitalisations : '+str(data['hosp'])+'\nSoins Intensif : '+str(data['rea'])
			api.update_status(message)
			print('[bold green4]'+str(datetime.date.today())+' | TWEET | No Covid Data [/bold green4]')
		else:
			print('[bold dodger_blue2]'+str(datetime.date.today())+' | TWEET | Covid Data [/bold dodger_blue2]')
			time.sleep(3600)
	except:
		print('[bold bright_red]'+str(datetime.date.today())+' | ERROR | Covid API [/bold bright_red]')
		time.sleep(1800)
