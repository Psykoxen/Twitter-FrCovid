import requests
import json
import time
import tweepy
import log
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from rich import print

############################################################### - LOGIN TWEET - ####################################################################

auth = tweepy.OAuthHandler(log.consumer_key, log.consumer_secret)
auth.set_access_token(log.access_token, log.access_token_secret)
api = tweepy.API(auth)

############################################################### - INITIALISATION - ####################################################################

days_FR = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
mnths_FR = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
certif = True
filenames = ['positif.png', 'death.png', 'care.png','intensif.png']
filename_ids = []
messages = {'Auvergne et Rhône-Alpes':'','Bourgogne et Franche-Comté':'','Bretagne':'','Centre-Val de Loire':'','Corse':'','Grand Est':'','Hauts-de-France':'','Île-de-France':'','Normandie':'','Nouvelle Aquitaine':'','Occitanie':'','Pays de la Loire':'',"Provence-Alpes-Côte d'Azur":''}
last_id = 0

################################################################## - MAIN - ####################################################################
while certif == True:
	try:
		data = requests.get('https://coronavirusapifr.herokuapp.com/data/live/france').json()[0]
		hst = open('date.json')
		hst_date = json.load(hst)
		hst.close()
		if len(hst_date['date'])==0 or (data['date'] != hst_date['date'][-1]):
			hst = open('date.json','w')
			hst_date['date'].append(data['date'])
			hst_date['data'][data['date']] = {
												"pos":data['conf_j1'],
												"allPos":"/",
												"death":data['incid_dchosp'],
												"allDeath":data['dchosp'],
												"care":data['hosp'],
												"intCare":data['rea']
											}
			json.dump(hst_date, hst)
			hst.close()
			x = []
			y = []
			for j in hst_date['date']:
				x.append(datetime.datetime.strptime(j, '%Y-%m-%d'))
			for i in hst_date['data']:
				y.append(hst_date['data'][i]['pos'])

			plt.grid(True)
			plt.title("Cas Positifs")
			plt.yticks(y)
			plt.yticks(np.arange(0, 600000, 30000))
			plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
			plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
			plt.xticks(rotation=30)
			plt.plot(x, y, c = 'r')
			plt.savefig("positif.png")
			plt.clf() 


			y = []
			for i in hst_date['data']:
				y.append(hst_date['data'][i]['death'])

			plt.grid(True)
			plt.title("Décès")
			plt.yticks(y)
			plt.yticks(np.arange(0, 500, 30))
			plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
			plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
			plt.xticks(rotation=30)
			plt.plot(x, y, c = 'black')
			plt.savefig("death.png") 
			plt.clf()

			y = []
			for i in hst_date['data']:
				y.append(hst_date['data'][i]['care'])

			plt.grid(True)
			plt.title("Hospitalisations")
			plt.yticks(y)
			plt.yticks(np.arange(0, 60000, 1000))
			plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
			plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
			plt.xticks(rotation=30)
			plt.plot(x, y, c = 'orange')
			plt.savefig("care.png") 
			plt.clf()

			y = []
			for i in hst_date['data']:
				y.append(hst_date['data'][i]['intCare'])

			plt.grid(True)
			plt.title("Soins Intensif")
			plt.yticks(y)
			plt.yticks(np.arange(0, 5000, 300))
			plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
			plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
			plt.xticks(rotation=30)
			plt.plot(x, y, c = 'y')
			plt.savefig("intensif.png") 

			for filename in filenames:
				res = api.media_upload(filename)
				filename_ids.append(res.media_id)

			for i in data:
				if data[i] == None:
					data[i] = '/'
			data['date'] = datetime.date(int(data['date'][:4]),int(data['date'][5:7]),int(data['date'][8:]))
			message = '|#COVID19| ~ '+days_FR[data['date'].weekday()]+' '+str(data['date'].day)+' '+mnths_FR[data['date'].month-1]+' '+str(data['date'].year)+' :\n\n---- ~ 😷 Contamination 😷 ~ ----\nNouveaux Cas : '+str(data['conf_j1'])+'\nCas Totaux : '+str(data['conf'])+'\n--------- ~ ⚰️ Décès ⚰️ ~ ---------\nDécès du jour : '+str(data['incid_dchosp'])+'\nDécès Totaux : '+str(data['dchosp'])+'\n------- ~ 🏥 Hôpitaux 🏥 ~ -------\nHospitalisations : '+str(data['hosp'])+'\nSoins Intensif : '+str(data['rea'])
			api.update_status(status=message, media_ids=filename_ids)
			time.sleep(900)

			chiffre = {'TO':[],'avg_TO':0,'hosp':0,'rea':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0}
			regions = {'Auvergne et Rhône-Alpes':{'ID':'@auvergnerhalpes','TAG':'#auvergnerhonealpes','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Bourgogne et Franche-Comté':{'ID':'@bfc_region','TAG':'#BourgogneFrancheCompté','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Bretagne':{'ID':'@regionbretagne','TAG':'#Bretagne','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Centre-Val de Loire':{'ID':'@RCValdeLoire','TAG':'#CentreValdeLoire','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Corse':{'ID':'@IsulaCorsica','TAG':'#Corse','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Grand Est':{'ID':'@regiongrandest','TAG':'#GrandEst','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Hauts-de-France':{'ID':'@hautsdefrance','TAG':'#hautsdefrance','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Île-de-France':{'ID':'@iledefrance','TAG':'#RégionIDF','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Normandie':{'ID':'@RegionNormandie','TAG':'#Normandie','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Nouvelle Aquitaine':{'ID':'@NvelleAquitaine','TAG':'#NouvelleAquitaine','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Occitanie':{'ID':'@Occitanie','TAG':'#Occitanie','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   'Pays de la Loire':{'ID':'@paysdelaloire','TAG':'#Paysdelaloire','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0},
					   "Provence-Alpes-Côte d'Azur":{'ID':'@MaRegionSud','TAG':'#RégionSud','TO':0,'hosp':0,'rea':0,'incid_hosp':0,'incid_rad':0,'incid_rea':0,'incid_dchosp':0,'bil_hosp':0}
					   }

			for i in regions:
				data = requests.get('https://coronavirusapifr.herokuapp.com/data/live/region/'+i).json()
				for j in data:
					regions[i]['TO'] = j['TO']
					regions[i]['hosp']+= j['hosp']
					regions[i]['rea']+= j['rea']
					regions[i]['incid_hosp']+= j['incid_hosp']
					regions[i]['incid_rad']+= j['incid_rad']
					regions[i]['incid_rea']+= j['incid_rea']
					regions[i]['incid_dchosp']+= j['incid_dchosp']
					regions[i]['bil_hosp'] = regions[i]['incid_hosp']-regions[i]['incid_rad']-regions[i]['incid_dchosp']		

				message = 'En '+regions[i]['TAG']+' || '+regions[i]['ID']+' :\n  Occupation : '+str(int(regions[i]['TO']*100))+'%\n  Hospitalisation : '+str(regions[i]['hosp'])+' ('
				if regions[i]['bil_hosp'] >= 0:
					message+='+'
				message+=str(regions[i]['bil_hosp'])+')\n  Réanimation : '+str(regions[i]['rea'])+' (+'+str(regions[i]['incid_rea'])+')\n  Décès : '+str(regions[i]['incid_dchosp'])
				messages[i] = message
				
				chiffre['TO'].append(regions[i]['TO'])
				chiffre['hosp'] += regions[i]['hosp']
				chiffre['rea'] += regions[i]['rea']
				chiffre['incid_rea'] += regions[i]['incid_rea']
				chiffre['incid_dchosp'] += regions[i]['incid_dchosp']
				chiffre['bil_hosp'] += regions[i]['bil_hosp']

			message = "|#COVID19| ~ Les chiffres des hopitaux en #France:\n  Taux d'occupation moyen : "+str(int(sum(chiffre['TO'])/len(chiffre['TO'])*100))+"%\n  Hopitaux : "+str(chiffre['hosp'])+" ("
			if chiffre['bil_hosp'] >= 0:
				message+='+'
			message += str(chiffre['bil_hosp'])+")\n  Réanimation : "+str(chiffre['rea'])+" (+"+str(chiffre['incid_rea'])+")\n  Décès : "+str(chiffre['incid_dchosp'])
			last_id = api.update_status(status=message,auto_populate_reply_metadata=True)
			time.sleep(900)
			for message in messages:
				last_id = api.update_status(status=messages[message],in_reply_to_status_id=last_id.id,auto_populate_reply_metadata=True)
				time.sleep(900)
			print('[bold green4]'+str(datetime.date.today())+' | TWEET | Covid Data [/bold green4]')

		else:
			print('[bold dodger_blue2]'+str(datetime.date.today())+' | TWEET | No Covid Data [/bold dodger_blue2]')
			time.sleep(3600)
	except:
		print('[bold bright_red]'+str(datetime.date.today())+' | ERROR | Covid API [/bold bright_red]')
		time.sleep(1800)