#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Main Courante
# Croix rouge Francaise 65
# 25 Nov 2016
# Julien Borghetti

import time
from gui_victime import *
from gui_MainCourante import *
#import pdb ; pdb.set_trace()

Liste_Victimes = []

class Victime:
    def __init__(self):
        self.Arrivee_HH      = None
        self.Arrivee_MM      = None
        self.Origine         = None
        self.Destination     = None
        self.Nom             = None
        self.Prenom          = None
        self.Circonstances   = None
        self.Traitement      = None
        self.Numero_Bilan    = None
        self.Numero_Decharge = None
        self.Depart_HH       = None
        self.Depart_MM       = None
    def Set_defaut(self):
        self.Arrivee_HH      = str(time.localtime()[3])
        self.Arrivee_MM      = str(time.localtime()[4])
        self.Origine         = " "
        self.Destination     = " "
        self.Nom             = " "
        self.Prenom          = " "
        self.Circonstances   = " "
        self.Traitement      = " "
        self.Depart_HH       = " "
        self.Depart_MM       = " "
    def Set_paul_durant(self):
        self.Arrivee_HH      = "17"
        self.Arrivee_MM      = "03"
        self.Origine         = "signaleur"
        self.Destination     = "L.S.P."
        self.Nom             = "Durant"
        self.Prenom          = "Paul"
        self.Circonstances   = "Tombe a velo"
        self.Traitement      = "Desinfection et pansement"
        self.Numero_Bilan    = None
        self.Numero_Decharge = None
        self.Depart_HH       = "17"
        self.Depart_MM       = "10"
    def afficher(self):
        print self.Arrivee_HH
        print self.Arrivee_MM
        print self.Origine
        print self.Destination
        print self.Nom
        print self.Prenom
        print self.Circonstances
        print self.Traitement
        print self.Numero_Bilan
        print self.Numero_Decharge
        print self.Depart_HH
        print self.Depart_MM

class GUI_Victime_Edition(GUI_Victime):
    def __init__(self, _victime_gui):
        print "Creation d'une nouvelle fiche pour : " + str(_victime_gui.Nom)
        GUI_Victime.__init__(self, None, wx.ID_ANY, "")
        self.victime_gui = _victime_gui
        self.montrer_victime()
    def enregistrer_fermer_gui_victime(self, event):  # wxGlade: GUI_Victime.<event_handler>
        self.enregistrer_victime()
        self.Close()
        event.Skip()
    def enregistrer_victime(self):
        print "enregistrer_victime()"
        self.victime_gui.Arrivee_HH      = self.text_ctrl_Arrivee_HH.GetValue()
        self.victime_gui.Arrivee_MM      = self.text_ctrl_Arrivee_MM.GetValue()
        self.victime_gui.Origine         = self.text_ctrl_origine.GetValue()
        self.victime_gui.Destination     = self.text_ctrl_destination.GetValue()
        self.victime_gui.Nom             = self.text_ctrl_Nom.GetValue()
        self.victime_gui.Prenom          = self.text_ctrl_Prenom.GetValue()
        self.victime_gui.Circonstances   = self.text_ctrl_Circonstances.GetValue()
        self.victime_gui.Traitement      = self.text_ctrl_Traitement.GetValue()
        self.victime_gui.Numero_Bilan    = self.text_ctrl_Numero_Bilan.GetValue()
        self.victime_gui.Numero_Decharge = self.text_ctrl_Numero_Decharge.GetValue()
        self.victime_gui.Depart_HH       = self.text_ctrl_Depart_HH.GetValue()
        self.victime_gui.Depart_MM       = self.text_ctrl_Depart_MM.GetValue()
        self.victime_gui.afficher()
    def montrer_victime(self):
        print "montrer_victime()"
        self.text_ctrl_Arrivee_HH.SetValue(str(self.victime_gui.Arrivee_HH))
        self.text_ctrl_Arrivee_MM.SetValue(str(self.victime_gui.Arrivee_MM))
        self.text_ctrl_origine.SetValue(self.victime_gui.Origine)
        self.text_ctrl_destination.SetValue(self.victime_gui.Destination)
        self.text_ctrl_Nom.SetValue(self.victime_gui.Nom)
        self.text_ctrl_Prenom.SetValue(self.victime_gui.Prenom)
        self.text_ctrl_Circonstances.SetValue(self.victime_gui.Circonstances)
        self.text_ctrl_Traitement.SetValue(self.victime_gui.Traitement)
        self.text_ctrl_Numero_Bilan.SetValue(str(self.victime_gui.Numero_Bilan))
        self.text_ctrl_Numero_Decharge.SetValue(str(self.victime_gui.Numero_Decharge))
        self.text_ctrl_Depart_HH.SetValue(str(self.victime_gui.Depart_HH))
        self.text_ctrl_Depart_MM.SetValue(str(self.victime_gui.Depart_MM))

class GUI_MainCourante_Fenetre(MainCourante_Fenetre):
    def __init__(self):
        MainCourante_Fenetre.__init__(self, None, wx.ID_ANY, "")
    def MetAJour_Victime(self, _victime, ligne):
        self.list_ctrl_ListeVictime.DeleteItem(ligne)
        print _victime.Arrivee_HH
        self.Insere_Victime(_victime,ligne)
    def Insere_Victime(self, _victime,ligne):
        _index = self.list_ctrl_ListeVictime.InsertStringItem(ligne, _victime.Arrivee_HH)
        print _index
        self.list_ctrl_ListeVictime.SetStringItem(_index, 1, _victime.Arrivee_MM )
        self.list_ctrl_ListeVictime.SetStringItem(_index, 2, _victime.Nom )
        self.list_ctrl_ListeVictime.SetStringItem(_index, 3, _victime.Prenom )
        self.list_ctrl_ListeVictime.SetStringItem(_index, 4, _victime.Circonstances )
        self.list_ctrl_ListeVictime.SetStringItem(_index, 5, _victime.Depart_HH )
        self.list_ctrl_ListeVictime.SetStringItem(_index, 6, _victime.Depart_MM )
    def Nouvelle(self, event):  # wxGlade: MainCourante_Fenetre.<event_handler>
        print "Event handler 'Nouvelle'"
        gettext.install("DialogVictime")
        DialogVictime = wx.App()
        Liste_Victimes.append(Victime())
        Liste_Victimes[len(Liste_Victimes)-1].Set_defaut()
        Fiche_Victime = GUI_Victime_Edition(Liste_Victimes[len(Liste_Victimes)-1])
        DialogVictime.SetTopWindow(Fiche_Victime)
        Fiche_Victime.Show()
        DialogVictime.MainLoop()
        event.Skip()
    def DoubleClic(self, event):  # wxGlade: MainCourante_Fenetre.<event_handler>
        print "Event handler 'DoubleClic'"
        ligne = event.GetItem().GetId()
        print "Selection : " + str(ligne)
        gettext.install("DialogVictime")
        DialogVictime = wx.App()
        Fiche_Victime = GUI_Victime_Edition(Liste_Victimes[ligne])
        DialogVictime.SetTopWindow(Fiche_Victime)
        Fiche_Victime.Show()
        DialogVictime.MainLoop()
        event.Skip()
    def Raffraichir(self, event):  # wxGlade: MainCourante_Fenetre.<event_handler>
        print "Event handler 'Raffraichir' "
        if self.list_ctrl_ListeVictime.GetItemCount() < len(Liste_Victimes):
            print "Affichage de la victime enregistrée à l'instant"
            self.Insere_Victime(Liste_Victimes[len(Liste_Victimes)-1], len(Liste_Victimes))
        else:
            for i in range(len(Liste_Victimes)):
                self.MetAJour_Victime( Liste_Victimes[i], i)
        event.Skip()

def main_test_GUI_Victime_Edition():
    gettext.install("DialogVictime")
    victime_1 = Victime()
    victime_1.Set_paul_durant()

    DialogVictime = wx.App()
    Fiche_Victime = GUI_Victime_Edition(victime_1)
    DialogVictime.SetTopWindow(Fiche_Victime)
    Fiche_Victime.Show()
    DialogVictime.MainLoop()
def main_TEST_MainCourante_Fenetre():
    gettext.install("MainCourante")
    MainCourante = wx.App()
    frame_1 = MainCourante_Fenetre(None, wx.ID_ANY, "")
    MainCourante.SetTopWindow(frame_1)
    frame_1.Show()
    MainCourante.MainLoop()
def main_TEST_GUI_MainCourante_Fenetre():
    gettext.install("MainCourante_GUI")
    MainCourante_App     = wx.App()
    MainCourante_App_GUI = GUI_MainCourante_Fenetre()
    MainCourante_App.SetTopWindow(MainCourante_App_GUI)
    Liste_Victimes.append(Victime())
    Liste_Victimes[0].Set_defaut()
    Liste_Victimes.append(Victime())
    Liste_Victimes[1].Set_paul_durant()
    MainCourante_App_GUI.Insere_Victime(Liste_Victimes[0], 0)
    MainCourante_App_GUI.Insere_Victime(Liste_Victimes[1], 1)
    MainCourante_App_GUI.Show()
    MainCourante_App.MainLoop()

if __name__ == "__main__":
    print "Programme MainCouranteCRF65.py lancé"
#   main_test_GUI_Victime_Edition()
    main_TEST_GUI_MainCourante_Fenetre()
