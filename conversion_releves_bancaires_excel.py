#!/usr/bin/env python
'''
Copyright: Croix-Rouge Francaise 2016 (French Red Cross)
Author   : Julien Borghetti Sept 2016
'''

import re
import sys
# import ipdb
import subprocess


def ecrire_l_aide():
    print "python conversion_releves_bancaires_excel.py fichier.pdf"
    print "  1. converti fichier.pdf en releve_bancaire.txt"
    print "  2. converti releve_bancaire.txt en releve_bancaire.csv"
    print " "
    print "python conversion_releves_bancaires_excel.py"
    print "  1. converti releve_bancaire.txt en releve_bancaire.csv"

try:
    cmd = "ps2ascii " + str(sys.argv[1]) + " releve_bancaire.txt"
    print cmd
    subprocess.call(cmd, shell=True)
    print "releve_bancaire.txt created"
except IndexError:
    pass

try:
    inputfile = open('releve_bancaire.txt')
except IOError:
    print "Le fichier releve_bancaire.txt n'a pas probablement pas encore ete converti"
    ecrire_l_aide()
    exit()
outputfile = open('releve_bancaire.csv', 'w')

my_text = inputfile.readlines()  # [67:] skipping first 66 lines


class Transaction:
    ''' Transaction object '''
    def __init__(self):
        self.date1 = "01/01"
        self.date2 = "01/01"
        self.label = "INCONNU"
        self.type = "INCONNU"
        self.details = "INCONNU"
        self.montant = 0

    def remove_space_montant(self):
        decouverte = re.search('(\d*) ?(\d+[,]\d\d)', self.montant)
        self.montant = decouverte.group(1) + decouverte.group(2)

    def return_csv_line(self):
        ligne = transaction.date1 + ";"
        ligne += transaction.date2 + ";"
        ligne += transaction.montant + ";"
        ligne += transaction.type + ";"
        ligne += transaction.details + "\n"
        return ligne

transaction_list = []
transaction_nouvelle = True
i_lignes = 0
transaction_Nb = 0
Nb_erreur = 0

for line in my_text:
    i_lignes += 1
    if re.match("^[0-3]\d[/][0-1]\d\s[0-3]\d[/][0-1]\d[ ]", line):
        transaction_Nb += 1
        transaction = Transaction()
        regex = '(^[0-3]\d[/][0-1]\d) ([0-3]\d[/][0-1]\d) (.+) (\d+[,]\d\d)\n'
        decouverte = re.search(regex, line)
        transaction.date1 = decouverte.group(1)
        transaction.date2 = decouverte.group(2)
        transaction.label = decouverte.group(3)

        if re.match("CHEQUE N[.]?", transaction.label):
            transaction.type = "CHEQUE"
            regex = 'CHEQUE N[.]? ?(\d+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match("REMISE CHEQUES N[.] (\d+)", transaction.label):
            transaction.type = "REMISE CHEQUES"
            regex = 'REMISE CHEQUES N[.] (\d+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match("DEPOT ESP N[.] (\d+) VIR", transaction.label):
            transaction.type = "DEPOT ESPECES"
            regex = 'DEPOT ESP N[.] (\d+) VIR ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match("INTERETS CREDITEURS", transaction.label):
            transaction.type = "INTERETS CREDITEURS"
            regex = 'INTERETS CREDITEURS ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.montant = decouverte.group(1)
            transaction.remove_space_montant()

        if re.match("REGUL DEPOT ESP N:(\d+)", transaction.label):
            transaction.type = "REGUL DEPOT ESP"
            regex = 'REGUL DEPOT ESP N:(\d+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match("DPT VRAC ESP (\d+  \d+)", transaction.label):
            transaction.type = "DPT VRAC ESP"
            regex = 'DPT VRAC ESP (\d+  \d+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()
#           print "details = " + transaction.details

        if re.match("PRLV (\w+)", transaction.label):
            transaction.type = "PRLV"
            regex = 'PRLV ([ \w]+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
#           ipdb.set_trace() # BREAKPOINT
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match("CHEQUE IMPAYE N[.](\d+)", transaction.label):
            transaction.type = "CHEQUE IMPAYE"
            regex = 'CHEQUE IMPAYE N[.](\d+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match("VIR SEPA (.+)", transaction.label):
            transaction.type = "VIR SEPA"
# Code qui marche avec les milliers
            regex = 'VIR SEPA (\D+) (\d{0,3}[ ]?\d{1,3},\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
#           print " "
#           sys.stdout.write(line)
#           print decouverte.group(1)
#           print decouverte.group(2)
            transaction.remove_space_montant()

        if re.match("RET DAB (.+)", transaction.label):
            transaction.type = "RET DAB"
            regex = 'RET DAB (.+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match(".*FRAIS FORFAIT ASSOCIATIS 2", transaction.label):
            transaction.type = "FRAIS FORFAIT ASSOCIATIS 2"
            regex = 'FRAIS FORFAIT ASSOCIATIS 2 ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.montant = decouverte.group(1)
            transaction.remove_space_montant()

        if re.match(".*VERSEMENT CREDIT", transaction.label):
            transaction.type = "VERSEMENT CREDIT"
            regex = 'VERSEMENT CREDIT (N> \d+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match(".*ACHAT DEVISE", transaction.label):
            transaction.type = "ACHAT DEVISE"
            regex = 'ACHAT DEVISE MTLA(\d+ \d+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match(".*REVERST PRLV", transaction.label): #new
            transaction.type = "REVERST PRLV"
            regex = 'REVERST PRLV (.+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match(".*ECH PRET", transaction.label): # new
            transaction.type = "ECH PRET"
            regex = 'ECH PRET   (.+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if re.match(".*VERSEMENT ESPECES", transaction.label): # new
            transaction.type = "VERSEMENT ESPECES"
            regex = 'VERSEMENT ESPECES       (.+) ([ \d]+[,]\d\d)\n'
            decouverte = re.search(regex, line)
            transaction.details = decouverte.group(1)
            transaction.montant = decouverte.group(2)
            transaction.remove_space_montant()

        if transaction.type == "INCONNU":
            print "...::: ERREUR :::..."
            print line
            print "Type de depense inconnu"
            print "--> LABEL = " + transaction.label
            print "--> MONTANT = " + transaction.montant
            Nb_erreur += 1

        transaction_list.append(transaction)

#   if( i_lignes == 880 ): #Nb lignes sautees = 112
#       print "Nb transactions = " + str(transaction_Nb)
#       print "len(transaction_list) = " + str(len(transaction_list))
#       print "Nb ERREURS = " + str(Nb_erreur)
#       break

print "Nb lignes = " + str(i_lignes)
print "Nb transactions = " + str(transaction_Nb)
print "len(transaction_list) = " + str(len(transaction_list))
print "Nb ERREURS = " + str(Nb_erreur)

'''
Sortie en fichier csv
'''
transaction_written = 0

for transaction in transaction_list:  # DPT VRAC ESP
    if transaction.type == "DPT VRAC ESP":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # REMISE CHEQUES
    if transaction.type == "REMISE CHEQUES":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # VIR SEPA
    if transaction.type == "VIR SEPA":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # RET DAB
    if transaction.type == "RET DAB":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # CHEQUE
    if transaction.type == "CHEQUE":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # PRLV
    if transaction.type == "PRLV":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # FRAIS FORFAIT ASSOCIATIS 2
    if transaction.type == "FRAIS FORFAIT ASSOCIATIS 2":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # ECH PRET
    if transaction.type == "ECH PRET":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # DEPOT ESPECES
    if transaction.type == "DEPOT ESPECES":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # INTERETS CREDITEURS
    if transaction.type == "INTERETS CREDITEURS":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # CHEQUE IMPAYE
    if transaction.type == "CHEQUE IMPAYE":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # VERSEMENT CREDIT
    if transaction.type == "VERSEMENT CREDIT":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # REGUL DEPOT ESP
    if transaction.type == "REGUL DEPOT ESP":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # VERSEMENT CREDIT
    if transaction.type == "ACHAT DEVISE":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # REVERST PRLV
    if transaction.type == "REVERST PRLV":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1

for transaction in transaction_list:  # VERSEMENT ESPECES
    if transaction.type == "VERSEMENT ESPECES":
        outputfile.writelines(transaction.return_csv_line())
        transaction_written += 1


print "Nb transaction written in releve_bancaire.csv = " + str(transaction_written)
