#!/usr/bin/env python
'''
Calcule la balance analytique a partir des brouillards de banque

USAGE :
$python brouillards2balance.py
CONFIG:
les 3 variables globales au debut de ce fichier
OUTPUT:
banlance_new.xlsx

Copyright: Croix-Rouge Francaise 2016 (French Red Cross)
Author   : Julien Borghetti June 24th 2016
'''

import openpyxl
import subprocess
import re
import calendar
import datetime
from brouillards2balance_config import set_configuration
# import ipdb
# import sys


class configuration:
    def __init__(self):
        self.file_balance_in = None
        self.file_brouillard_CE = None
        self.file_brouillard_BP = None
        self.brouillard_CE_resulat = None
        self.brouillard_BP_resulat = None
        self.brouillards_resultat = None
        self.solde_comptable_CE = None  # selon le brouillard d'Anne Lise
        self.solde_comptable_BP = None  # selon le brouillard d'Anne Lise
        self.solde_bancaire_CE = None  # selon le pdf du releves bancaires
        self.solde_bancaire_BP = None  # selon le rapprochement d'Anne-Lise


class transaction:
    def __init__(self, ligne=None, RouD=None, ws_banque=None):
        self.ligne = ligne
        if (ligne, RouD, ws_banque) != (None, None, None):
            if RouD == "D":
                self.montant = ws_banque.cell(row=ligne, column=16).value
            elif RouD == "R":
                self.montant = ws_banque.cell(row=ligne, column=15).value
            else:
                print "ERREUR dans le constructeur de l'objet transaction"
                exit()
            self.RouE = ws_banque.cell(row=ligne, column=4).value
            self.code = str(ws_banque.cell(row=ligne, column=5).value) \
                + str(ws_banque.cell(row=ligne, column=6).value)
            self.antenne = ws_banque.cell(row=ligne, column=14).value
        else:
            self.ligne = 0
            self.RouD = "?"  # Recette ou Depense
            self.code = 0
            self.antenne = 0
            self.montant = 0

    def imprime(self):
        print "    self.ligne   = " + str(self.ligne)
        print "    self.RouE    = " + str(self.RouE)
        print "    self.code    = " + str(self.code)
        print "    self.antenne = " + str(self.antenne)
        print "    self.montant = " + str(self.montant)
        print " "

    def imprime_light(self):
        print "    self.code = " + str(self.code)
        print "    self.montant = " + str(self.montant)


class Balance:
    def __init__(self, file_name, (liste_depense, liste_recette)=(None, None)):
        self.file_balance_output = \
            re.search('(\w+).xlsx', file_name).group(1) + "_new.xlsx"
        command = "cp " + file_name + " " + self.file_balance_output
        print command+"\n"
        subprocess.call(command, shell=True)
        self.wb_out = openpyxl.load_workbook(self.file_balance_output,
                                             data_only=True)
        self.ws = self.wb_out.get_sheet_by_name('Balance')
        self.solde_initial = self.ws.cell(row=56, column=15).value
        self.solde_final = None
        self.resultat = None
        self.resultat_cumul = None
        self.date_initiale = self.ws.cell(row=1, column=18).value
        self.date_Format = self.ws.cell(row=1, column=18).number_format
        self.date_initiale_annee = int(re.search("^(20\d\d)-\d\d-.+",
                                       str(self.date_initiale)).group(1))
        self.date_initiale_mois = int(re.search("^20\d\d-([01]\d)-.+",
                                      str(self.date_initiale)).group(1))
        self.date_finale_mois = self.date_initiale_mois + 1
        _, date_dinale_LastDay = calendar.monthrange(self.date_initiale_annee,
                                                     self.date_finale_mois)
        self.date_finale = datetime.datetime(self.date_initiale_annee,
                                             self.date_finale_mois,
                                             date_dinale_LastDay)
        if True:
            ''' Depenses '''
            (self.A4012, self.A3180, self.A3170) = ([], [], [])
            (self.A3082, self.A3084, self.A3011) = ([], [], [])
            (self.A3012, self.A3160, self.A3161) = ([], [], [])
            (self.A3162, self.A3131, self.A3132) = ([], [], [])
            (self.A2041, self.A2042, self.A2042) = ([], [], [])
            (self.A2011, self.A2012, self.A9010) = ([], [], [])
            (self.A9011, self.A9012, self.A9013) = ([], [], [])
            (self.A9014, self.A9015, self.A9016) = ([], [], [])
            (self.A9032, self.A3030, self.A21810) = ([], [], [])

        if (liste_depense, liste_recette) != (None, None):
            self.ws.cell(row=1, column=18).value = self.date_finale
            self.ws.cell(row=1, column=18).number_format = self.date_Format
            self.ws.cell(row=55, column=13).value = self.date_finale
            self.ws.cell(row=55, column=13).number_format = self.date_Format
            self.ws.cell(row=56, column=13).value = self.date_finale
            self.ws.cell(row=56, column=13).number_format = self.date_Format
            print "NETTOYAGE DE LA BALANCE"
            self.nettoyage_balance()

            print "PEUPLEMENT DE LA BALANCE"
            print "....DEPENSES"
            debug_antenne = None
            self.peuple_balance_depenses(liste_depense, debug_antenne)
            self.show_depenses_peuplement(debug_antenne)
            print "....RECETTES"
            self.peuple_balance_recettes(liste_recette)
            print "....SOUS TOTAUX DEPENSES"
            self.totaux_balance_depense()
            print "....SOUS TOTAUX RECETTES"
            self.totaux_balance_recettes()
            print "....TOTAUX"
            self.resultat = self.totaux_balance()

    def show_depenses_peuplement(self, debug_antenne):
        if not debug_antenne:
            return
        print "....debug antenne : " + str(debug_antenne)
        tmp = 0
        for elements in self.A3170:
            elements.imprime()
            tmp += elements.montant
        print "........total A3170 = " + str(tmp) + "\n"

        tmp = 0
        for elements in self.A3082:
            elements.imprime()
            tmp += elements.montant
        print "........total A3082 = " + str(tmp) + "\n"

        tmp = 0
        for elements in self.A3160:
            elements.imprime()
            tmp += elements.montant
        print "........total A3160 = " + str(tmp) + "\n"

        tmp = 0
        for elements in self.A3162:
            elements.imprime()
            tmp += elements.montant
        print "........total A3162 = " + str(tmp) + "\n"

        tmp = 0
        for elements in self.A2041:
            elements.imprime()
            tmp += elements.montant
        print "........total A2041 = " + str(tmp) + "\n"

        tmp = 0
        for elements in self.A2042:
            elements.imprime()
            tmp += elements.montant
        print "........total A2042 = " + str(tmp) + "\n"

        tmp = 0
        for elements in self.A2011:
            elements.imprime()
            tmp += elements.montant
        print "........total A2011 = " + str(tmp) + "\n"

        tmp = 0
        for elements in self.A9012:
            elements.imprime()
            tmp += elements.montant
        print "........total A9012 = " + str(tmp) + "\n"

    def nettoyage_balance(self):
        l_recettes = range(7, 13)+[16, 22, 24, 25, 26, 28, 31, 34, 36, 37, 38,
                                   43, 45, 47, 48, 49, 51, 52, 53]
        for ligne in l_recettes:
            for col in range(3, 11):
                self.ws.cell(row=ligne, column=col).value = 0
        l_depenses = [8, 9, 11, 12, 13, 14, 16, 17, 18, 20, 21, 22, 23, 25, 26,
                      27, 29, 30, 31, 33, 34, 35] + \
            range(37, 44)+[45]+range(47, 55)
        for ligne in l_depenses:
            for col in range(13, 21):
                self.ws.cell(row=ligne, column=col).value = 0

    def peuple_balance_depenses(self, liste, debug_antenne=None):
        '''
        - Peuple les depenses
        '''
        for i in range(0, len(liste)):
            if liste[i].antenne == 4012:
                column_antenne = 16
            elif liste[i].antenne == 4011:
                column_antenne = 15
            elif liste[i].antenne == 4010:
                column_antenne = 14
            elif liste[i].antenne == 3969:
                column_antenne = 13
            elif liste[i].antenne == 4013:
                column_antenne = 17
            elif liste[i].antenne == 4015:
                column_antenne = 18
            elif liste[i].antenne == 4016:
                column_antenne = 19
            else:
                print "\n ERREUR : Antenne INCONNUE"
                print "Antenne = " + str(liste[i].antenne)
                print "ligne du brouillard = " + str(liste[i].ligne)
                exit()
            self.peuple_balance_depenses_antenne(liste, i, column_antenne,
                                                 debug_antenne=debug_antenne)

    def peuple_balance_depenses_antenne(self, liste, i, antenne,
                                        debug_antenne=None):
        if liste[i].code == "A4012":
            if liste[i].antenne == debug_antenne:
                self.A4012.append(liste[i])
                pass
            self.ws.cell(row=8, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=8, column=antenne).value)
        elif liste[i].code == "A3180":
            if liste[i].antenne == debug_antenne:
                self.A3180.append(liste[i])
                pass
            self.ws.cell(row=11, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=11, column=antenne).value)
        elif liste[i].code == "A3170":
            if liste[i].antenne == debug_antenne:
                self.A3170.append(liste[i])
                pass
            self.ws.cell(row=12, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=12, column=antenne).value)
        elif liste[i].code == "A3082":
            if liste[i].antenne == debug_antenne:
                self.A3082.append(liste[i])
                pass
            self.ws.cell(row=13, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=13, column=antenne).value)
        elif liste[i].code == "A3084":
            if liste[i].antenne == debug_antenne:
                self.A3084.append(liste[i])
                pass
            self.ws.cell(row=14, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=14, column=antenne).value)
        elif liste[i].code == "A3011":
            if liste[i].antenne == debug_antenne:
                self.A3011.append(liste[i])
                pass
            self.ws.cell(row=16, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=16, column=antenne).value)
        elif liste[i].code == "A3012":
            if liste[i].antenne == debug_antenne:
                self.A3012.append(liste[i])
                pass
            self.ws.cell(row=17, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=17, column=antenne).value)
        elif liste[i].code == "A3160":
            if liste[i].antenne == debug_antenne:
                self.A3160.append(liste[i])
                pass
            self.ws.cell(row=20, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=20, column=antenne).value)
        elif liste[i].code == "A3161":
            if liste[i].antenne == debug_antenne:
                self.A3161.append(liste[i])
                pass
            self.ws.cell(row=21, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=21, column=antenne).value)
        elif liste[i].code == "A3162":
            if liste[i].antenne == debug_antenne:
                self.A3162.append(liste[i])
                pass
            self.ws.cell(row=22, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=22, column=antenne).value)
        elif liste[i].code == "A3131":
            if liste[i].antenne == debug_antenne:
                self.A3131.append(liste[i])
                pass
            self.ws.cell(row=25, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=25, column=antenne).value)
        elif liste[i].code == "A3132":
            if liste[i].antenne == debug_antenne:
                self.A3132.append(liste[i])
                pass
            self.ws.cell(row=26, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=26, column=antenne).value)
        elif liste[i].code == "A2041":
            if liste[i].antenne == debug_antenne:
                self.A2041.append(liste[i])
                pass
            self.ws.cell(row=29, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=29, column=antenne).value)
        elif liste[i].code == "A2042":
            if liste[i].antenne == debug_antenne:
                self.A2042.append(liste[i])
                pass
            self.ws.cell(row=30, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=30, column=antenne).value)
        elif liste[i].code == "A2011":
            if liste[i].antenne == debug_antenne:
                self.A2011.append(liste[i])
                pass
            self.ws.cell(row=33, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=33, column=antenne).value)
        elif liste[i].code == "A2012":
            if liste[i].antenne == debug_antenne:
                self.A2012.append(liste[i])
                pass
            self.ws.cell(row=34, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=34, column=antenne).value)
        elif liste[i].code == "A9010":
            if liste[i].antenne == debug_antenne:
                self.A9010.append(liste[i])
                pass
            self.ws.cell(row=37, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=37, column=antenne).value)
        elif liste[i].code == "A9011":
            if liste[i].antenne == debug_antenne:
                self.A9011.append(liste[i])
                pass
            self.ws.cell(row=38, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=38, column=antenne).value)
        elif liste[i].code == "A9012":
            if liste[i].antenne == debug_antenne:
                self.A9012.append(liste[i])
                pass
            self.ws.cell(row=39, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=39, column=antenne).value)
        elif liste[i].code == "A9013":
            if liste[i].antenne == debug_antenne:
                self.A9013.append(liste[i])
                pass
            self.ws.cell(row=40, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=40, column=antenne).value)
        elif liste[i].code == "A9014":
            if liste[i].antenne == debug_antenne:
                self.A9014.append(liste[i])
                pass
            self.ws.cell(row=41, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=41, column=antenne).value)
        elif liste[i].code == "A9015":
            if liste[i].antenne == debug_antenne:
                self.A9015.append(liste[i])
                pass
            self.ws.cell(row=42, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=42, column=antenne).value)
        elif liste[i].code == "A9016":
            if liste[i].antenne == debug_antenne:
                self.A9016.append(liste[i])
                pass
            self.ws.cell(row=43, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=43, column=antenne).value)
        elif liste[i].code == "A9032":
            if liste[i].antenne == debug_antenne:
                self.A9032.append(liste[i])
                pass
            self.ws.cell(row=45, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=45, column=antenne).value)
        elif liste[i].code == "A3030":
            if liste[i].antenne == debug_antenne:
                self.A3030.append(liste[i])
                pass
            self.ws.cell(row=47, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=47, column=antenne).value)
        elif liste[i].code == "21810None" or liste[i].code == "21810":
            if liste[i].antenne == debug_antenne:
                self.A21810.append(liste[i])
                pass
            print "   investissement en ligne : " + str(liste[i].ligne)
            self.ws.cell(row=52, column=antenne, value=liste[i].montant +
                         self.ws.cell(row=52, column=antenne).value)
        else:
            print "\n ERREUR : Transaction non traitee"
            print "code imputation = " + str(liste[i].code)
            exit()

    def peuple_balance_recettes(self, liste):
        '''
        - Peuple les depenses
        '''
        for i in range(0, len(liste)):
            if liste[i].antenne == 3969:
                column_antenne = 3
            elif liste[i].antenne == 4010:
                column_antenne = 4
            elif liste[i].antenne == 4011:
                column_antenne = 5
            elif liste[i].antenne == 4012:
                column_antenne = 6
            elif liste[i].antenne == 4013:
                column_antenne = 7
            elif liste[i].antenne == 4015:
                column_antenne = 8
            elif liste[i].antenne == 4016:
                column_antenne = 9
            else:
                print "\n ERREUR: Antenne INCONNUE dans \
                      methode peuple_balance_recettes"
                print "Antenne = " + str(liste[i].antenne)
                print "ligne du brouillard = " + str(liste[i].ligne)
                exit()
            self.peuple_balance_recettes_antenne(liste, i, column_antenne)

    def peuple_balance_recettes_antenne(self, liste, i, antenne):
        if liste[i].code == "A9031":
            val = liste[i].montant+self.ws.cell(row=7, column=antenne).value
            self.ws.cell(row=7, column=antenne, value=val)
        elif liste[i].code == "A9032":
            val = liste[i].montant+self.ws.cell(row=8, column=antenne).value
            self.ws.cell(row=8, column=antenne, value=val)
        elif liste[i].code == "A9033":
            val = liste[i].montant+self.ws.cell(row=9, column=antenne).value
            self.ws.cell(row=9, column=antenne, value=val)
        elif liste[i].code == "A9034":
            val = liste[i].montant+self.ws.cell(row=10, column=antenne).value
            self.ws.cell(row=10, column=antenne, value=val)
        elif liste[i].code == "A9035":
            val = liste[i].montant+self.ws.cell(row=11, column=antenne).value
            self.ws.cell(row=11, column=antenne, value=val)
        elif liste[i].code == "A9036":
            val = liste[i].montant+self.ws.cell(row=12, column=antenne).value
            self.ws.cell(row=12, column=antenne, value=val)
        elif liste[i].code == "A9030":
            val = liste[i].montant+self.ws.cell(row=13, column=antenne).value
            self.ws.cell(row=13, column=antenne, value=val)
        elif liste[i].code == "A3170":
            val = liste[i].montant+self.ws.cell(row=22, column=antenne).value
            self.ws.cell(row=22, column=antenne, value=val)
        elif liste[i].code == "A9037":
            val = liste[i].montant+self.ws.cell(row=24, column=antenne).value
            self.ws.cell(row=24, column=antenne, value=val)
        elif liste[i].code == "A9038":
            val = liste[i].montant+self.ws.cell(row=25, column=antenne).value
            self.ws.cell(row=25, column=antenne, value=val)
        elif liste[i].code == "A3160":
            val = liste[i].montant+self.ws.cell(row=26, column=antenne).value
            self.ws.cell(row=26, column=antenne, value=val)
        elif liste[i].code == "A3130":
            val = liste[i].montant+self.ws.cell(row=31, column=antenne).value
            self.ws.cell(row=31, column=antenne, value=val)
        elif liste[i].code == "A2040":
            val = liste[i].montant+self.ws.cell(row=34, column=antenne).value
            self.ws.cell(row=34, column=antenne, value=val)
        elif liste[i].code == "A2010":
            val = liste[i].montant+self.ws.cell(row=36, column=antenne).value
            self.ws.cell(row=36, column=antenne, value=val)
        elif liste[i].code == "A2013":
            val = liste[i].montant+self.ws.cell(row=37, column=antenne).value
            self.ws.cell(row=37, column=antenne, value=val)
        elif liste[i].code == "A3030":
            val = liste[i].montant+self.ws.cell(row=43, column=antenne).value
            self.ws.cell(row=43, column=antenne, value=val)
        elif liste[i].code == "A3010":
            val = liste[i].montant+self.ws.cell(row=45, column=antenne).value
            self.ws.cell(row=45, column=antenne, value=val)
        elif liste[i].code == "A9012":
            print "\n--> regularisation en ligne : " + str(liste[i].ligne)
            liste[i].imprime()
            val = -liste[i].montant+self.ws.cell(row=39,
                                                 column=antenne+10).value
            self.ws.cell(row=39, column=antenne+10, value=val)
        elif liste[i].code == "A9011" or liste[i].code == "A9018":
            print "--> interets financiers en ligne : " + str(liste[i].ligne)
            val = liste[i].montant + self.ws.cell(row=51, column=antenne).value
            self.ws.cell(row=51, column=antenne, value=val)
        else:
            print "\n ERREUR : Transaction non traitee dans methode \
                    peuple_balance_recettes_antenne"
            print "ligne du brouillard = " + str(liste[i].ligne)
            print "code imputation = " + str(liste[i].code)
            exit()

    def totaux_balance_depense(self):
        colonnes_antennes = [13, 14, 15, 16, 17, 18, 19]
        for antenne in colonnes_antennes:
            self.ws.cell(row=9, column=antenne,
                         value=self.ws.cell(row=8, column=antenne).value)
            self.ws.cell(row=18, column=antenne,
                         value=self.ws.cell(row=11, column=antenne).value +
                         self.ws.cell(row=12, column=antenne).value +
                         self.ws.cell(row=13, column=antenne).value +
                         self.ws.cell(row=14, column=antenne).value +
                         self.ws.cell(row=16, column=antenne).value +
                         self.ws.cell(row=17, column=antenne).value)
            self.ws.cell(row=23, column=antenne,
                         value=self.ws.cell(row=20, column=antenne).value +
                         self.ws.cell(row=21, column=antenne).value +
                         self.ws.cell(row=22, column=antenne).value)
            self.ws.cell(row=27, column=antenne,
                         value=self.ws.cell(row=25, column=antenne).value +
                         self.ws.cell(row=26, column=antenne).value)
            self.ws.cell(row=31, column=antenne,
                         value=self.ws.cell(row=29, column=antenne).value +
                         self.ws.cell(row=30, column=antenne).value)
            self.ws.cell(row=35, column=antenne,
                         value=self.ws.cell(row=33, column=antenne).value +
                         self.ws.cell(row=34, column=antenne).value)
            self.ws.cell(row=48, column=antenne,
                         value=self.ws.cell(row=37, column=antenne).value +
                         self.ws.cell(row=38, column=antenne).value +
                         self.ws.cell(row=39, column=antenne).value +
                         self.ws.cell(row=40, column=antenne).value +
                         self.ws.cell(row=41, column=antenne).value +
                         self.ws.cell(row=42, column=antenne).value +
                         self.ws.cell(row=43, column=antenne).value +
                         self.ws.cell(row=45, column=antenne).value +
                         self.ws.cell(row=47, column=antenne).value)
            self.ws.cell(row=49, column=antenne,
                         value=self.ws.cell(row=9, column=antenne).value +
                         self.ws.cell(row=18, column=antenne).value +
                         self.ws.cell(row=23, column=antenne).value +
                         self.ws.cell(row=27, column=antenne).value +
                         self.ws.cell(row=31, column=antenne).value +
                         self.ws.cell(row=35, column=antenne).value +
                         self.ws.cell(row=48, column=antenne).value)
            self.ws.cell(row=53, column=antenne,
                         value=self.ws.cell(row=49, column=antenne).value +
                         self.ws.cell(row=51, column=antenne).value +
                         self.ws.cell(row=52, column=antenne).value)

    def totaux_balance_recettes(self):
        column_antenne = [3, 4, 5, 6, 7, 8, 9]
        for antenne in column_antenne:
            self.ws.cell(row=16, column=antenne,
                         value=self.ws.cell(row=7, column=antenne).value +
                         self.ws.cell(row=8, column=antenne).value +
                         self.ws.cell(row=9, column=antenne).value +
                         self.ws.cell(row=10, column=antenne).value +
                         self.ws.cell(row=11, column=antenne).value +
                         self.ws.cell(row=12, column=antenne).value +
                         self.ws.cell(row=13, column=antenne).value)
            self.ws.cell(row=28, column=antenne,
                         value=self.ws.cell(row=22, column=antenne).value +
                         self.ws.cell(row=24, column=antenne).value +
                         self.ws.cell(row=25, column=antenne).value +
                         self.ws.cell(row=26, column=antenne).value)
            self.ws.cell(row=38, column=antenne,
                         value=self.ws.cell(row=36, column=antenne).value +
                         self.ws.cell(row=37, column=antenne).value)
            self.ws.cell(row=47, column=antenne,
                         value=self.ws.cell(row=43, column=antenne).value +
                         self.ws.cell(row=45, column=antenne).value)
            self.ws.cell(row=49, column=antenne,
                         value=self.ws.cell(row=16, column=antenne).value +
                         self.ws.cell(row=28, column=antenne).value +
                         self.ws.cell(row=31, column=antenne).value +
                         self.ws.cell(row=34, column=antenne).value +
                         self.ws.cell(row=38, column=antenne).value +
                         self.ws.cell(row=47, column=antenne).value)
            self.ws.cell(row=53, column=antenne,
                         value=self.ws.cell(row=49, column=antenne).value +
                         self.ws.cell(row=51, column=antenne).value +
                         self.ws.cell(row=52, column=antenne).value)

    def totaux_balance(self):
        l_recettes = range(7, 13)+[16, 22, 24, 25, 26, 28, 31, 34, 36, 37, 38,
                                   43, 45, 47, 48, 49, 51, 52, 53]
        for ligne in l_recettes:
            self.ws.cell(row=ligne, column=10,
                         value=self.ws.cell(row=ligne, column=3).value +
                         self.ws.cell(row=ligne, column=4).value +
                         self.ws.cell(row=ligne, column=5).value +
                         self.ws.cell(row=ligne, column=6).value +
                         self.ws.cell(row=ligne, column=7).value +
                         self.ws.cell(row=ligne, column=8).value +
                         self.ws.cell(row=ligne, column=9).value)
        c_resultat = range(3, 10)
        for colonne in c_resultat:
            self.ws.cell(row=50, column=colonne+10,
                         value=self.ws.cell(row=49, column=colonne).value -
                         self.ws.cell(row=49, column=colonne+10).value)
            self.ws.cell(row=54, column=colonne+10,
                         value=self.ws.cell(row=53, column=colonne).value -
                         self.ws.cell(row=53, column=colonne+10).value)
        l_depenses = [8, 9]+range(11, 15)+[16, 17, 18, 21, 22, 23, 25, 26, 27,
                                           29, 30, 31, 33, 34, 35] + \
            range(37, 44)+[45]+range(47, 55)
        for ligne in l_depenses:
            self.ws.cell(row=ligne, column=20,
                         value=self.ws.cell(row=ligne, column=13).value +
                         self.ws.cell(row=ligne, column=14).value +
                         self.ws.cell(row=ligne, column=15).value +
                         self.ws.cell(row=ligne, column=16).value +
                         self.ws.cell(row=ligne, column=17).value +
                         self.ws.cell(row=ligne, column=18).value +
                         self.ws.cell(row=ligne, column=19).value)
        self.resultat = self.ws.cell(row=54, column=20).value
        return self.resultat

    def cumul(self, ConfigFile=None):
        l_recettes = range(7, 13)+[16, 22, 24, 25, 26, 28, 31, 34, 36, 37, 38,
                                   43, 45, 47, 48, 49, 51, 52, 53]
        for ligne in l_recettes:
            for col in range(26, 34):
                self.ws.cell(row=ligne, column=col).value = \
                    self.ws.cell(row=ligne, column=col).value + \
                    self.ws.cell(row=ligne, column=col-23).value
        l_depenses = [8, 9]+range(11, 15)+range(16, 19)+range(21, 24) + \
            [25, 26, 27, 29, 30, 31, 33, 34, 35] + \
            range(37, 44)+[45]+range(47, 55)
        for ligne in l_depenses:
            for col in range(36, 44):
                self.ws.cell(row=ligne, column=col).value = \
                    self.ws.cell(row=ligne, column=col).value + \
                    self.ws.cell(row=ligne, column=col-23).value

        self.resultat_cumul = self.ws.cell(row=54, column=43).value

        self.ws.cell(row=1, column=41).value = self.date_finale
        self.ws.cell(row=1, column=41).number_format = self.date_Format
        for ligne in [55, 56]:
            self.ws.cell(row=ligne, column=36).value = self.date_finale
            self.ws.cell(row=ligne, column=36).number_format = self.date_Format
        if ConfigFile:
            self.solde_final = self.solde_initial + self.resultat
            self.ws.cell(row=56, column=15, value=self.solde_final)
            self.ws.cell(row=56, column=38, value=self.solde_final)
            self.ws.cell(row=55, column=15,
                         value=ConfigFile.solde_bancaire_CE +
                         ConfigFile.solde_bancaire_BP)
            self.ws.cell(row=55, column=38,
                         value=ConfigFile.solde_bancaire_CE +
                         ConfigFile.solde_bancaire_BP)


class brouillard:
    def __init__(self, filename, CEouBP):
        ''' "CE" ou "BP" '''
        self.CEouBP = CEouBP
        self.wb = openpyxl.load_workbook(filename, data_only=True)
        self.ws = self.wb.get_sheet_by_name('Feuil1')

    def decipher_brouillard(self):
        '''
        - Get all transactions from brouillard CE
        '''
        print "\nDECHIFFREMENT DU BROUILLARD DE LA BANQUE " + self.CEouBP
        liste_depenses = []
        liste_recettes = []
        liste_NDI_depenses = []
        liste_NDI_recettes = []
        i = 1
        # DEPENSES et RECETTES
        if self.CEouBP == "CE":  # le brouillard BP n'a que des NDI
            while self.ws.cell(row=i, column=1).value != "DEPENSES":
                i += 1
            i_premiere_depense = i + 1
            print "Les depenses commencent en ligne "+str(i_premiere_depense)
            i = i_premiere_depense
            while self.ws.cell(row=i, column=1).value != "RECETTES":
                T = transaction(i, "D", self.ws)
                liste_depenses.append(T)
                i += 1
            i_derniere_depense = i - 1
            print "Les depenses terminent en ligne " + str(i_derniere_depense)
            i_premiere_recette = i + 1
            print "Les recettes commencent en ligne " + str(i_premiere_recette)
            i = i_premiere_recette
            while not re.match("(NDI D).*",
                               str(self.ws.cell(row=i, column=1).value)):
                T = transaction(i, "R", self.ws)
                liste_recettes.append(T)
                i += 1
            i_derniere_recettes = i - 1
            print "Les recettes terminent en ligne " + str(i_derniere_recettes)
        elif self.CEouBP == "BP":
            while not re.match("(NDI D).*",
                               str(self.ws.cell(row=i, column=1).value)):
                i += 1
        else:
            print "Probleme d'identification du brouillard"
            exit()
        # NDI
        i_premiere_NDI_R = i + 1
        print "Les NDI depenses " + self.CEouBP + " commencent en ligne " + \
            str(i_premiere_NDI_R)
        i = i_premiere_NDI_R
        while not re.match("(NDI R).*",
                           str(self.ws.cell(row=i, column=1).value)):
            T = transaction(i, "D", self.ws)
            liste_NDI_depenses.append(T)
            i += 1
        i_derniere_NDI_D = i - 1
        print "Les NDI depenses " + self.CEouBP + " terminent en ligne " + \
            str(i_derniere_NDI_D)
        i_premiere_NDI_R = i + 1
        print "Les NDI recettes " + self.CEouBP + " commencent en ligne " + \
            str(i_premiere_NDI_R)
        i = i_premiere_NDI_R
        while re.match("^\d{4}\D\d{2}\D\d{2}\s.*",
                       str(self.ws.cell(row=i, column=1).value)):
            T = transaction(i, "R", self.ws)
            liste_NDI_recettes.append(T)
            i += 1
        i_derniere_NDI_R = i - 1
        print "Les NDI recettes " + self.CEouBP + " terminent en ligne " + \
            str(i_derniere_NDI_R)
        print "Le brouillard de la banque " + self.CEouBP + \
            " a ete dechifre sans trouver d'erreurs\n"
        self.depenses = liste_depenses
        self.recettes = liste_recettes
        self.NDI_depenses = liste_NDI_depenses
        self.NDI_recettes = liste_NDI_recettes

    def resultat(self, liste_depenses, liste_recettes,
                 antenne=None, Code=None):
        resultat = 0
        if liste_recettes:
            for i in range(0, len(liste_recettes)):
                if liste_recettes[i].antenne == antenne or not antenne:
                    if liste_recettes[i].code == Code or not Code:
                        resultat += liste_recettes[i].montant
        if liste_depenses:
            for i in range(0, len(liste_depenses)):
                if liste_depenses[i].antenne == antenne or not antenne:
                    if liste_depenses[i].code == Code or not Code:
                        resultat -= liste_depenses[i].montant
        return resultat


def debug_brouillard_balance(config, brouillard, balance):
    print "\n==================  DEBUG  ======================="
    print "==================   " + brouillard.CEouBP + \
        "    ======================="
    if brouillard.CEouBP == "CE":
        print "Resultat inscrit sur le brouillard   = " + \
            str(config.brouillard_CE_resulat)
    elif brouillard.CEouBP == "BP":
        print "Resultat inscrit sur le brouillard   = " + \
            str(config.brouillard_BP_resulat)
    else:
        print "ERREUR dans la fonction debug"
        exit()
    print "Resultat balance                     = "+str(balance.resultat)
    print "----      Dechiffrage du brouillard         ----"
    print "depenses     = " + str(brouillard.resultat(
        brouillard.depenses, None))
    print "recettes     = " + str(brouillard.resultat(
        None, brouillard.recettes))
    print "NDI_depenses = " + str(brouillard.resultat(
        brouillard.NDI_depenses, None))
    print "NDI_recettes = " + str(brouillard.resultat(
        None, brouillard.NDI_recettes))
    print "TOTAL RECETTES = " + str(brouillard.resultat(
        None, brouillard.recettes + brouillard.NDI_recettes))
    print "TOTAL DEPENSES = " + str(brouillard.resultat(
        brouillard.depenses + brouillard.NDI_depenses, None))
    print "Resultat dechiffrage brouillard       = " + \
        str(brouillard.resultat(brouillard.depenses + brouillard.NDI_depenses,
                                brouillard.recettes + brouillard.NDI_recettes))
    print "---- Dechiffrage du brouillard CE par antenne ----"
    print "Sous total Recettes CE : 3969 = " + \
        str(brouillard.resultat(None, brouillard.recettes +
            brouillard.NDI_recettes, antenne=3969))
    print "Sous total Recettes CE : 4010 = " + \
        str(brouillard.resultat(None, brouillard.recettes +
            brouillard.NDI_recettes, antenne=4010))
    print "Sous total Recettes CE : 4011 = " + \
        str(brouillard.resultat(None, brouillard.recettes +
            brouillard.NDI_recettes, antenne=4011))
    print "Sous total Recettes CE : 4012 = " + \
        str(brouillard.resultat(None, brouillard.recettes +
            brouillard.NDI_recettes, antenne=4012))
    print "Sous total Recettes CE : 4013 = " + \
        str(brouillard.resultat(None, brouillard.recettes +
            brouillard.NDI_recettes, antenne=4013))
    print "Sous total Recettes CE : 4015 = " + \
        str(brouillard.resultat(None, brouillard.recettes +
            brouillard.NDI_recettes, antenne=4015))
    print "Sous total Recettes CE : 4016 = " + \
        str(brouillard.resultat(None, brouillard.recettes +
            brouillard.NDI_recettes, antenne=4016))
    print "Sous total Depenses CE : 3969 = " + \
        str(brouillard.resultat(brouillard.depenses +
            brouillard.NDI_depenses, None, antenne=3969))
    print "Sous total Depenses CE : 4010 = " + \
        str(brouillard.resultat(brouillard.depenses +
            brouillard.NDI_depenses, None, antenne=4010))
    print "Sous total Depenses CE : 4011 = " + \
        str(brouillard.resultat(brouillard.depenses +
            brouillard.NDI_depenses, None, antenne=4011))
    print "Sous total Depenses CE : 4012 = " + \
        str(brouillard.resultat(brouillard.depenses +
            brouillard.NDI_depenses, None, antenne=4012))
    print "Sous total Depenses CE : 4013 = " + \
        str(brouillard.resultat(brouillard.depenses +
            brouillard.NDI_depenses, None, antenne=4013))
    print "Sous total Depenses CE : 4015 = " + \
        str(brouillard.resultat(brouillard.depenses +
            brouillard.NDI_depenses, None, antenne=4015))
    print "Sous total Depenses CE : 4016 = " + \
        str(brouillard.resultat(brouillard.depenses +
            brouillard.NDI_depenses, None, antenne=4016))
    print "Sous total Resultat CE : 3969 = " + \
        str(brouillard.resultat(brouillard.depenses + brouillard.NDI_depenses,
            brouillard.recettes + brouillard.NDI_recettes, antenne=3969))
    print "Sous total Resultat CE : 4010 = " + \
        str(brouillard.resultat(brouillard.depenses + brouillard.NDI_depenses,
            brouillard.recettes + brouillard.NDI_recettes, antenne=4010))
    print "Sous total Resultat CE : 4011 = " + \
        str(brouillard.resultat(brouillard.depenses + brouillard.NDI_depenses,
            brouillard.recettes + brouillard.NDI_recettes, antenne=4011))
    print "Sous total Resultat CE : 4012 = " + \
        str(brouillard.resultat(brouillard.depenses + brouillard.NDI_depenses,
            brouillard.recettes + brouillard.NDI_recettes, antenne=4012))
    print "Sous total Resultat CE : 4013 = " + \
        str(brouillard.resultat(brouillard.depenses + brouillard.NDI_depenses,
            brouillard.recettes + brouillard.NDI_recettes, antenne=4013))
    print "Sous total Resultat CE : 4015 = " + \
        str(brouillard.resultat(brouillard.depenses + brouillard.NDI_depenses,
            brouillard.recettes + brouillard.NDI_recettes, antenne=4015))
    print "Sous total Resultat CE : 4016 = " + \
        str(brouillard.resultat(brouillard.depenses + brouillard.NDI_depenses,
            brouillard.recettes + brouillard.NDI_recettes, antenne=4016))
    if brouillard.CEouBP == "CE":
        pass
    elif brouillard.CEouBP == "BP":
        pass
        balance_BP.wb_out.save("Balance_BP_DEBUG.xlsx")
        print "enregistrement de la balance : Balance_BP_DEBUG.xlsx"
    else:
        print "ERREUR dans la fonction debug"
        exit()
    print "===============   END DEBUG  ====================="

if __name__ == '__main__':
    config_values = configuration()
    set_configuration(config_values)

    brouillard_CE = brouillard(config_values.file_brouillard_CE, "CE")
    brouillard_CE.decipher_brouillard()
    brouillard_BP = brouillard(config_values.file_brouillard_BP, "BP")
    brouillard_BP.decipher_brouillard()

    if config_values.debug_CE:
        balance_CE = \
            Balance(config_values.file_balance_input,
                    (brouillard_CE.depenses + brouillard_CE.NDI_depenses,
                     brouillard_CE.recettes + brouillard_CE.NDI_recettes))
        print "enregistrement de la balance : Balance_CE_DEBUG.xlsx"
        balance_CE.wb_out.save("Balance_CE_DEBUG.xlsx")
        debug_brouillard_balance(config_values, brouillard_CE, balance_CE)
        print "Resultat balance CE = " + str(balance_CE.resultat)
        print "Resultat brouillards CE = " + \
            str(config_values.brouillard_CE_resulat) + "\n\n"

    if config_values.debug_BP:
        balance_BP = \
            Balance(config_values.file_balance_input,
                    (brouillard_BP.depenses + brouillard_BP.NDI_depenses,
                     brouillard_BP.recettes + brouillard_BP.NDI_recettes))
        debug_brouillard_balance(config_values, brouillard_BP, balance_BP)
        print "Resultat balance BP = " + str(balance_BP.resultat)
        print "Resultat brouillards BP = " + \
            str(config_values.brouillard_BP_resulat) + "\n\n"

    if config_values.balance_globale_BP_CE:
        balance = \
            Balance(config_values.file_balance_input,
                    (brouillard_CE.depenses + brouillard_CE.NDI_depenses +
                     brouillard_BP.depenses + brouillard_BP.NDI_depenses,
                     brouillard_CE.recettes + brouillard_CE.NDI_recettes +
                     brouillard_BP.recettes + brouillard_BP.NDI_recettes))
        balance.cumul(config_values)
        balance.wb_out.save(balance.file_balance_output)

        print "\n=============== VERIFICATION ====================="

        print "Resultat balance CE+BP     = " + str(balance.resultat)
        print "Resultat brouillards CE+BP = " + \
            str(config_values.brouillard_CE_resulat +
                config_values.brouillard_BP_resulat)
        print "Resultats cumules balance CE+BP     = " + \
            str(balance.resultat_cumul)
        print "Resultats cumules brouillards CE+BP = " + \
            str(config_values.brouillard_CE_resulat_cumul +
                config_values.brouillard_BP_resulat_cumul)
        print "\n=============== INFORMATIONS ====================="
        print "Solde comptable CE+BP = " + \
            str(config_values.solde_comptable_CE +
                config_values.solde_comptable_BP)
        print "Solde bancaire CE+BP = " + \
            str(config_values.solde_bancaire_CE +
                config_values.solde_bancaire_BP)
