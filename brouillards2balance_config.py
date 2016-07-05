#!/usr/bin/env python


'''
Configuration pour le mois d'avril Mars
'''

def set_configuration(config):
    config.debug_CE                 = True
    config.debug_BP                 = True
    config.balance_globale_BP_CE    = True
    config.file_balance_input       = "Balance_ana_04_2016_python.xlsx"
    config.file_brouillard_CE       = "Brouillard_05_CE.xlsx"
    config.file_brouillard_BP       = "Brouillard_05_BP_DT_65.xlsx"
    config.brouillard_CE_resulat    = XXXX.XX   #note sur le brouillard
    config.brouillard_BP_resulat    = XXXX.XX   #note sur le brouillard
    config.solde_comptable_CE       = XXXX.XX #note sur le brouillard
    config.solde_comptable_BP       = XXXX.XX   #note sur le brouillard
    config.solde_bancaire_CE        = XXXX.XX #note sur le releves bancaire
    config.solde_bancaire_BP        = XXXX.XX   #note sur le rapprochement d'Anne-Lise
    config.brouillard_CE_resulat_cumul = XXXXX.XX  #note sur le brouillard
    config.brouillard_BP_resulat_cumul = XXXX.XX   #note sur le brouillard
