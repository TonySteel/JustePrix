# -*- coding: utf-8 -*-
# Juste prix
# API CDiscount : https://dev.cdiscount.com/apiReference/v1

import webbrowser
from flask import Flask , jsonify, render_template, request
from random import randint
import requests, json
import time

class InterfaceWeb():
    def __init__(self):
        self.justePrix = []
        self.idArticle = 0
        self.nbRandom = 10
        self.NomtypeArticle = ['tv', 'cycle', 'cinema', 'sport', 'maison', 'animaux', 'divertissement', 'musique', 'jouet', 'cuisine']
        self.description = []
        self.imageUrl = []
        self.prixSaisie = 0
        self.prixMini = 0
        self.prixMaxi = 1000
        self.nbEssai = 0
        self.NbEssaiMax = 50
        self.start_time = time

        # IHM Web
        #webbrowser.open("http://localhost:5000/", 1)
        self.createApp()
        # ---"""

    # ------------------------------------------------------------------------
    # Requete API , clé API : 54fb15bb-eba6-4bac-af23-39f54cd258c5
    def reqApi(self):
        url = "https://api.cdiscount.com/OpenApi/json/Search"
        params = {
            "ApiKey": "54fb15bb-eba6-4bac-af23-39f54cd258c5",
            "SearchRequest": {
                "Keyword": self.NomtypeArticle[self.typeArticle],
                "Pagination": {
                    "ItemsPerPage": self.nbRandom,
                    "PageNumber": 0
                },
                "Filters": {
                    "Price": {
                        "Min": 0,
                        "Max": 1000
                    },
                    "Navigation": "tv",
                    "IncludeMarketPlace": "false"
                }
            }
        }
        reponse = requests.post(url, data=json.dumps(params)).content
        self.justePrix = self.find_values('SalePrice', reponse)
        self.description = self.find_values('Description', reponse)
        self.imageUrl = self.find_values('MainImageUrl', reponse)

        """print(self.description)
        print(self.justePrix, "€")
        print("img :", self.imageUrl)
    # ---"""

    def find_values(self, cle, reponse):
        results = []
        def _decode_dict(a_dict):
            try:
                if cle == 'SalePrice':
                    results.append(float(a_dict[cle]))
                else:
                    results.append(a_dict[cle])
            except KeyError:
                pass
            return a_dict
        json.loads(reponse, object_hook=_decode_dict)  # Return value ignored.
        return results

    # ------------------------------------------------------------------------
    # IHM app Web
    def createApp(self):
        app = Flask(__name__)

        # Initialisation
        @app.route("/")
        def pageIHM():
            return render_template("justePrix.html")

        # Démarrer une partie
        @app.route("/initJustePrix/")
        def initJustePrix():
            self.NbEssaiMax = request.args.get('NbEssaiMax')
            self.idArticle = randint(0, self.nbRandom-1)
            self.typeArticle = randint(0, self.nbRandom-1)
            self.reqApi()

            self.start_time = time.time()  # start temps de la partie
            #---"""
            return jsonify({'justePrix': self.justePrix[self.idArticle],
                            'description': self.description[self.idArticle],
                            'imageUrl': self.imageUrl[self.idArticle],
                            'nbEssai' : self.nbEssai})

        # Tester le prix saisie
        @app.route("/testPrixSaisie/")
        def testPrixSaisie():
            tpsPartie = time.time() - self.start_time  # Temps de la partie

            self.prixSaisie = float(request.args.get('prixSaisie'))
            resultat = 0

            if self.prixSaisie < self.justePrix[self.idArticle]:
                resultat = "jp+"
            elif self.prixSaisie > self.justePrix[self.idArticle]:
                resultat = "jp-"
            else:
                resultat = "jp"

            return jsonify({'resultat': resultat, 'tpsPartie': round(tpsPartie, 2)})

    # Lancement de l'appli serveur
        app.run(host="0.0.0.0", debug=True)
# ------------------------------------------------------------------------
if __name__ == "__main__":
    InterfaceWeb()