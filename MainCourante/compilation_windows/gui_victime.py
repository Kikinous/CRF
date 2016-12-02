#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.2 on Sun Nov 27 17:20:32 2016
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# fermer_gui_victime()
# —> Ajouter self.Close()
# —> Ajouter setValue()
# end wxGlade


class GUI_Victime(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GUI_Victime.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.text_ctrl_Arrivee_HH = wx.TextCtrl(self, wx.ID_ANY, _("HH"))
        self.text_ctrl_Arrivee_MM = wx.TextCtrl(self, wx.ID_ANY, _("MM"))
        self.label_radio = wx.StaticText(self, wx.ID_ANY, _("(message radio)"))
        self.text_ctrl_origine = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_acheminement = wx.StaticText(self, wx.ID_ANY, _("(ou acheminement)"))
        self.text_ctrl_destination = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_ctrl_Nom = wx.TextCtrl(self, wx.ID_ANY, _("Nom"))
        self.text_ctrl_Prenom = wx.TextCtrl(self, wx.ID_ANY, _(u"Pr\u00e9nom"))
        self.text_ctrl_Circonstances = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_ctrl_Traitement = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_NumeroBilan = wx.StaticText(self, wx.ID_ANY, _(u"Num\u00e9ro de bilan"))
        self.text_ctrl_Numero_Bilan = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_NumeroDecharge = wx.StaticText(self, wx.ID_ANY, _(u"Num\u00e9ro de d\u00e9charge"))
        self.text_ctrl_Numero_Decharge = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_ctrl_Depart_HH = wx.TextCtrl(self, wx.ID_ANY, _("HH"))
        self.text_ctrl_Depart_MM = wx.TextCtrl(self, wx.ID_ANY, _("MM"))
        self.button_enregistrer_victime = wx.Button(self, wx.ID_ANY, _("enregistrer"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.enregistrer_fermer_gui_victime, self.button_enregistrer_victime)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: GUI_Victime.__set_properties
        self.SetTitle(_("Dossier d'une victime"))
        self.SetSize((613, 519))
        self.text_ctrl_Arrivee_HH.SetMinSize((50, 22))
        self.text_ctrl_Arrivee_MM.SetMinSize((50, 22))
        self.text_ctrl_origine.SetMinSize((200, 66))
        self.text_ctrl_destination.SetMinSize((169, 66))
        self.text_ctrl_Circonstances.SetMinSize((300, 88))
        self.text_ctrl_Traitement.SetMinSize((300, 110))
        self.text_ctrl_Depart_HH.SetMinSize((50, 22))
        self.text_ctrl_Depart_MM.SetMinSize((50, 22))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GUI_Victime.__do_layout
        sizer_GUI_Victime = wx.BoxSizer(wx.VERTICAL)
        sizer_Suite = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("SUITE & TRAITEMENT | DEPART")), wx.HORIZONTAL)
        sizer_heure_depart = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Heure de d\u00e9part")), wx.VERTICAL)
        sizer_numeros = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Num\u00e9ros")), wx.VERTICAL)
        sizer_traitement = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Suite et traitement donn\u00e9s")), wx.HORIZONTAL)
        sizer_Victime = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("VICTIME | CIRCONSTANCES")), wx.HORIZONTAL)
        sizer_circonstances = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Description succinte de l'\u00e9v\u00eanement")), wx.VERTICAL)
        sizer_identite = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Identit\u00e9 d\u00e9clar\u00e9e de la victime")), wx.VERTICAL)
        sizer_Heure = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("HEURE | ORIGINE | DESTINATION")), wx.HORIZONTAL)
        sizer_destination = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Destination")), wx.VERTICAL)
        sizer_origine = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Origine")), wx.VERTICAL)
        sizer_Heure_arrivee = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Heure d'arriv\u00e9e")), wx.VERTICAL)
        sizer_Heure_arrivee.Add(self.text_ctrl_Arrivee_HH, 0, 0, 0)
        sizer_Heure_arrivee.Add(self.text_ctrl_Arrivee_MM, 0, 0, 0)
        sizer_Heure.Add(sizer_Heure_arrivee, 1, 0, 0)
        sizer_origine.Add(self.label_radio, 0, 0, 0)
        sizer_origine.Add(self.text_ctrl_origine, 0, 0, 0)
        sizer_Heure.Add(sizer_origine, 1, 0, 0)
        sizer_destination.Add(self.label_acheminement, 0, 0, 0)
        sizer_destination.Add(self.text_ctrl_destination, 0, 0, 0)
        sizer_Heure.Add(sizer_destination, 1, 0, 0)
        sizer_GUI_Victime.Add(sizer_Heure, 1, 0, 0)
        sizer_identite.Add(self.text_ctrl_Nom, 0, 0, 0)
        sizer_identite.Add(self.text_ctrl_Prenom, 0, 0, 0)
        sizer_Victime.Add(sizer_identite, 1, 0, 0)
        sizer_circonstances.Add(self.text_ctrl_Circonstances, 0, 0, 0)
        sizer_Victime.Add(sizer_circonstances, 1, 0, 0)
        sizer_GUI_Victime.Add(sizer_Victime, 1, 0, 0)
        sizer_traitement.Add(self.text_ctrl_Traitement, 0, 0, 0)
        sizer_Suite.Add(sizer_traitement, 1, 0, 0)
        sizer_numeros.Add(self.label_NumeroBilan, 0, 0, 0)
        sizer_numeros.Add(self.text_ctrl_Numero_Bilan, 0, 0, 0)
        sizer_numeros.Add(self.label_NumeroDecharge, 0, 0, 0)
        sizer_numeros.Add(self.text_ctrl_Numero_Decharge, 0, 0, 0)
        sizer_Suite.Add(sizer_numeros, 1, 0, 0)
        sizer_heure_depart.Add(self.text_ctrl_Depart_HH, 0, 0, 0)
        sizer_heure_depart.Add(self.text_ctrl_Depart_MM, 0, 0, 0)
        sizer_heure_depart.Add(self.button_enregistrer_victime, 0, 0, 0)
        sizer_Suite.Add(sizer_heure_depart, 1, 0, 0)
        sizer_GUI_Victime.Add(sizer_Suite, 1, 0, 0)
        self.SetSizer(sizer_GUI_Victime)
        self.Layout()
        # end wxGlade

    def enregistrer_fermer_gui_victime(self, event):  # wxGlade: GUI_Victime.<event_handler>
        print "Event handler 'enregistrer_fermer_gui_victime' not implemented!"
        event.Skip()

# end of class GUI_Victime
if __name__ == "__main__":
    gettext.install("DialogVictime") # replace with the appropriate catalog name

    DialogVictime = wx.PySimpleApp()
    Fiche_Victime = GUI_Victime(None, wx.ID_ANY, "")
    DialogVictime.SetTopWindow(Fiche_Victime)
    Fiche_Victime.Show()
    DialogVictime.MainLoop()