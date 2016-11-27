#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.2 on Sun Nov 27 00:57:04 2016
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
'''
La classe de l’application a pour nom :
MainCourante_Fenetre
'''
'''
A copier dans MainCourante_Fenetre.__init__()
        self.list_ctrl_ListeVictime = wx.ListCtrl(self, -1 , style=wx.LC_REPORT)
        self.list_ctrl_ListeVictime.InsertColumn(0, 'HH', width=30)
        self.list_ctrl_ListeVictime.InsertColumn(1, 'MM', width=30)
        self.list_ctrl_ListeVictime.InsertColumn(2, 'Nom', width=100)
        self.list_ctrl_ListeVictime.InsertColumn(3, 'Prenom', width=100)
        self.list_ctrl_ListeVictime.InsertColumn(4, 'Circonstances', width=200)
        self.list_ctrl_ListeVictime.InsertColumn(5, 'HH', width=30)
        self.list_ctrl_ListeVictime.InsertColumn(6, 'MM', width=30)
'''
# end wxGlade


class MainCourante_Fenetre(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainCourante_Fenetre.__init__
        wx.Frame.__init__(self, *args, **kwds)
        self.list_ctrl_ListeVictime = wx.ListCtrl(self, wx.ID_ANY)
        self.button_Nouvelle = wx.Button(self, wx.ID_ANY, _("Nouvelle"))
        self.button_Editer = wx.Button(self, wx.ID_ANY, _("Raffraichir"))
        self.button_Enregistrer = wx.Button(self, wx.ID_ANY, _("Enregistrer"))
        self.button_Ouvrir = wx.Button(self, wx.ID_ANY, _("Ouvrir"))

        self.list_ctrl_ListeVictime = wx.ListCtrl(self, -1 , style=wx.LC_REPORT)
        self.list_ctrl_ListeVictime.InsertColumn(0, 'HH', width=30)
        self.list_ctrl_ListeVictime.InsertColumn(1, 'MM', width=30)
        self.list_ctrl_ListeVictime.InsertColumn(2, 'Nom', width=100)
        self.list_ctrl_ListeVictime.InsertColumn(3, 'Prenom', width=100)
        self.list_ctrl_ListeVictime.InsertColumn(4, 'Circonstances', width=200)
        self.list_ctrl_ListeVictime.InsertColumn(5, 'HH', width=30)
        self.list_ctrl_ListeVictime.InsertColumn(6, 'MM', width=30)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClic, self.list_ctrl_ListeVictime)
        self.Bind(wx.EVT_BUTTON, self.Nouvelle, self.button_Nouvelle)
        self.Bind(wx.EVT_BUTTON, self.Raffraichir, self.button_Editer)
        self.Bind(wx.EVT_BUTTON, self.Enregistrer, self.button_Enregistrer)
        self.Bind(wx.EVT_BUTTON, self.Ouvrir, self.button_Ouvrir)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainCourante_Fenetre.__set_properties
        self.SetTitle(_("frame_1"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainCourante_Fenetre.__do_layout
        sizer_Fenetre = wx.BoxSizer(wx.VERTICAL)
        sizer_CadreFenetre = wx.BoxSizer(wx.VERTICAL)
        sizer_CadreBoutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("MAIN COURANTE")), wx.HORIZONTAL)
        sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("VICTIMES")), wx.HORIZONTAL)
        sizer_CadreFenetre.Add(self.list_ctrl_ListeVictime, 1, 0, 0)
        sizer_4.Add(self.button_Nouvelle, 0, 0, 0)
        sizer_4.Add(self.button_Editer, 0, 0, 0)
        sizer_CadreBoutons.Add(sizer_4, 1, 0, 0)
        sizer_5.Add(self.button_Enregistrer, 0, 0, 0)
        sizer_5.Add(self.button_Ouvrir, 0, 0, 0)
        sizer_CadreBoutons.Add(sizer_5, 1, 0, 0)
        sizer_CadreFenetre.Add(sizer_CadreBoutons, 1, 0, 0)
        sizer_Fenetre.Add(sizer_CadreFenetre, 1, 0, 0)
        self.SetSizer(sizer_Fenetre)
        sizer_Fenetre.Fit(self)
        self.Layout()
        # end wxGlade

    def DoubleClic(self, event):  # wxGlade: MainCourante_Fenetre.<event_handler>
        print "Event handler 'DoubleClic' not implemented!"
        event.Skip()

    def Nouvelle(self, event):  # wxGlade: MainCourante_Fenetre.<event_handler>
        print "Event handler 'Nouvelle' not implemented!"
        event.Skip()

    def Raffraichir(self, event):  # wxGlade: MainCourante_Fenetre.<event_handler>
        print "Event handler 'Raffraichir' not implemented!"
        event.Skip()

    def Enregistrer(self, event):  # wxGlade: MainCourante_Fenetre.<event_handler>
        print "Event handler 'Enregistrer' not implemented!"
        event.Skip()

    def Ouvrir(self, event):  # wxGlade: MainCourante_Fenetre.<event_handler>
        print "Event handler 'Ouvrir' not implemented!"
        event.Skip()

# end of class MainCourante_Fenetre
