
import requests
from lxml import html
import sys
from urllib import parse
import numpy as np
import urllib
import pandas as pd
import re
from bs4 import BeautifulSoup


######
#final_link = "https://www.leboncoin.fr/voitures/1138832934.htm?ca=12_s"
Path = "Desktop/Autre/Scrapping/Car_pictures/"

def extract_nb_img(source_text) :
    try:
        soup = BeautifulSoup(source_text, 'html.parser')
        extNum = int(soup.find('span', class_ = "_2YTBP").get_text().replace(' photos disponibles',''))

        return(extNum)
    except IndexError:
        return(0)

### Fonction permettant de scraper l'élement souhaité dans le code source de la page HTML ####"
def extract(source_text,key_deb,key_end) :
    try:
        return(source_text.split(key_deb)[1].split(key_end)[0])
    except IndexError:
        return(0)

     ### Fonction permettant de scraper l'ensemble des photos d'une UNIQUE page HTML ####"
def scrap_pictures(final_link):
    ### Import du fichier excel contenant l'ensemble des informations des véhicules ou cration si inexistant ####
#    try:
#        Table_desc = pd.read_excel(Path + "Description_veh.xlsx")
#    except IOError:
#         Table_desc = pd.DataFrame(columns=['Lien_URL',	'Id_Photo','Id_Veh',	'Prix',	'Ville',	'Marque',	'Modele',	'Annee_Modele',	'Kilometrage',	'Carburant',	'Boite_de_vitesse',	'Ref',	'Commentaire'])
    global Table_desc_img,Table_com_img ,T_temp_des,T_temp_com,Table_desc,Table_com

    print(final_link)

    response = requests.get(final_link) # Récuperation du code source de la page HTML

    try :
        Nb_Pict = int(extract_nb_img(response.text))
    except AttributeError :
        Nb_Pict = 0

    print("Nombre d'images : {}".format(Nb_Pict))

    if Nb_Pict >= 1 : Nb_Pict = 1
    print('Found {} images'.format(Nb_Pict))

    if Nb_Pict > 0:

        url = []
        Lien_URL = final_link
        Id_Veh   = extract(response.text,'voitures/','.htm')
        Prix   = int(extract(response.text,'prix : "','",'))
        Ville   = extract(response.text,'"address">','\n')
        Marque   = extract(response.text,'marque : "','",')
        Modele   = extract(response.text,'modele : "','",')
        Annee_Modele   = extract(response.text,'annee : "','",')
        Kilometrage   = int(extract(response.text,'\n          km : "','",'))
        Carburant   = extract(response.text,'nrj : "','",')
        Boite_de_vitesse   = extract(response.text,'vitesse : "','",')
        Ref   = extract(response.text,'km : "','",')
        Commentaire   = extract(response.text,'itemprop="description">','id="description_truncated"')

        #Table_desc_avt = Table_desc
        if Nb_Pict == 1: # Si il existe une unique photo, l'élement "images[" n'est pas présent d'ou le choix = ou sup à  1
            url.append(extract(response.text,'img src="','"'))

            #print(response.text)
            #print(url[0])
            resource = urllib.request.urlopen(url[0])
            output = open(Path + url[0].split('/')[-1], 'wb')
            output.write(resource.read())
            output.close()
            Id_Photo = url[0].split('/')[-1].split('.jpg')[0]
            Table_desc_img = pd.DataFrame( np.array([[Id_Photo],[Id_Veh],[Prix],[Ville],[Marque],[Modele],[Annee_Modele],[Kilometrage],[Carburant],[Boite_de_vitesse],[Ref]]).T,
                                                columns=['Id_Photo','Id_Veh',	'Prix',	'Ville',	'Marque',	'Modele',	'Annee_Modele',	'Kilometrage',	'Carburant',	'Boite_de_vitesse',	'Ref'])
            Table_com_img = pd.DataFrame( np.array([[Lien_URL],[Id_Veh],[Commentaire]]).T,
                                                columns=['Lien_URL',	'Id_Veh','Commentaire'])
            T_temp_des = pd.concat([T_temp_des,Table_desc_img])
            T_temp_com = pd.concat([T_temp_com,Table_com_img])
        else:
            for i in range(Nb_Pict):
                url.append("http:" + response.text.split('images[' + str(i) + '] = "')[1].split('"')[0])
                resource = urllib.request.urlopen(url[i])
                output = open(Path + url[i].split('/')[-1], 'wb')
                output.write(resource.read())
                output.close()
                Id_Photo = url[i].split('/')[-1].split('.jpg')[0]
                Table_desc_img = pd.DataFrame( np.array([[Id_Photo],[Id_Veh],[Prix],[Ville],[Marque],[Modele],[Annee_Modele],[Kilometrage],[Carburant],[Boite_de_vitesse],[Ref]]).T,
                                                columns=['Id_Photo','Id_Veh',	'Prix',	'Ville',	'Marque',	'Modele',	'Annee_Modele',	'Kilometrage',	'Carburant',	'Boite_de_vitesse',	'Ref'])
                Table_com_img = pd.DataFrame( np.array([[Lien_URL],[Id_Veh],[Commentaire]]).T,
                                                columns=['Lien_URL',	'Id_Veh','Commentaire'])

                T_temp_des = pd.concat([T_temp_des,Table_desc_img])
                T_temp_com = pd.concat([T_temp_com,Table_com_img])
       # T_temp.to_excel(Path + "T_temp.xlsx", index=False)
        print('All informations scraped')
    if Nb_Pict == 0:
        print('No informations scraped')

     ### Fonction permettant de scraper l'ensemble des liens d'une liste d'annonce de vente de véhicules ####"
def scrap_link(lien_LB):
     global Table_desc_img,Table_com_img ,T_temp_des,T_temp_com,Table_desc,Table_com
     try:
        Table_desc = pd.read_excel(Path + "Descriptions_veh.xlsx")
     except IOError:
        Table_desc = pd.DataFrame(columns=['Id_Photo','Id_Veh',	'Prix',	'Ville',	'Marque',	'Modele',	'Annee_Modele',	'Kilometrage',	'Carburant',	'Boite_de_vitesse',	'Ref'])
     try:
        Table_com = pd.read_excel(Path + "Descriptions_com.xlsx")
     except IOError:
        Table_com = pd.DataFrame(columns=['Lien_URL',	'Id_Veh',	'Commentaire'])



     #for i in [j +2700 for j in range(1000)]:
     for i in [j +2700 for j in range(1)]:

         T_temp_des = pd.DataFrame(columns=['Id_Photo','Id_Veh',	'Prix',	'Ville',	'Marque',	'Modele',	'Annee_Modele',	'Kilometrage',	'Carburant',	'Boite_de_vitesse',	'Ref'])
         T_temp_com = pd.DataFrame(columns=['Lien_URL',	'Id_Veh','Commentaire'])
         lien_LB =  "https://www.leboncoin.fr/voitures/offres/ile_de_france/occasions/?o="  + str(i)
         response = requests.get(lien_LB)
         links = ["https:" + i for i in re.findall('"(//www.leboncoin.fr/voitures/.*ca=12_s)"', response.text)]

         print('Found {} links'.format(len(links)))
         Links_Idphotos = [int(extract(l,'voitures/','.htm?ca=12_s')) for l in links]
         links_int =  set(Links_Idphotos).intersection(set(Table_desc.Id_Veh))
         links_scr =  [x for x in Links_Idphotos if x not in links_int]
         links_scr = ['http://www.leboncoin.fr/voitures/' + str(l) + '.htm?ca=12_s' for l in links_scr]
         if len(links_int) != 0:
             print('{} links already scraped '.format((len(links_int))))
             print('So {} links to scraped  '.format((len(links_scr))))
         for k in range(len(links_scr)):
             print('Link : {} / {} de la {} eme page : {}'.format(k+1,len(links_scr),(lien_LB.split("?o=")[1]),links_scr[k]))
             scrap_pictures(links_scr[k])
         Table_desc = pd.concat([Table_desc,T_temp_des])
         Table_com = pd.concat([Table_com,T_temp_com])

     Table_desc.to_excel(Path + "Descriptions_veh.xlsx", index=False)
     Table_com.to_excel(Path + "Descriptions_com.xlsx", index=False)


lien_LB =  "https://www.leboncoin.fr/voitures/offres/ile_de_france/occasions/?o=1"
scrap_link(lien_LB)

#scrap_link()
