# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 12:23:32 2023

@author: samym
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.integrate as sciIntegr
from scipy import interpolate


# Données 2019

TauxNominauxSpot2019=pd.read_excel(r"Rate-Models\TauxSpotFin2019to2022\TauxNominauxSpot2019to2022.xlsx",sheet_name="2019",index_col=0).iloc[1:]
ZCISspot2019=pd.read_excel(r"Rate-Models\TauxSpotFin2019to2022\TauxInflaSpot2019to2022.xlsx",sheet_name="2019",index_col=0).iloc[1:]
TauxReelSpot2019=pd.read_excel(r"Rate-Models\TauxSpotFin2019to2022\TauxNominauxSpot2019to2022.xlsx",sheet_name="2019",index_col=0).iloc[1:]
TauxReelSpot2019["Taux"]=(TauxNominauxSpot2019["Taux"]-ZCISspot2019["Taux"])/(1+ZCISspot2019["Taux"])

# Données 2020
TauxNominauxSpot2020=pd.read_excel(r"Rate-Models\TauxSpotFin2019to2022\TauxNominauxSpot2019to2022.xlsx",sheet_name="2020",index_col=0).iloc[1:]
ZCISspot2020=pd.read_excel(r"Rate-Models\TauxSpotFin2019to2022\TauxInflaSpot2019to2022.xlsx",sheet_name="2020",index_col=0).iloc[1:]
TauxReelSpot2020=pd.read_excel(r"Rate-Models\TauxSpotFin2019to2022\TauxNominauxSpot2019to2022.xlsx",sheet_name="2019",index_col=0).iloc[1:]
TauxReelSpot2020["Taux"]=(TauxNominauxSpot2020["Taux"]-ZCISspot2020["Taux"])/(1+ZCISspot2020["Taux"])

#  Données 2021
TauxNominauxSpot2021=pd.read_excel(r"C:\Users\samym\OneDrive - GENES\Documents\Modeles de Taux\TauxSpotFin2019to2022\TauxNominauxSpot2019to2022.xlsx",sheet_name="2021",index_col=0).iloc[1:]
ZCISspot2021=pd.read_excel(r"C:\Users\samym\OneDrive - GENES\Documents\Modeles de Taux\TauxSpotFin2019to2022\TauxInflaSpot2019to2022.xlsx",sheet_name="2021",index_col=0).iloc[1:]
TauxReelSpot2021=pd.read_excel(r"C:\Users\samym\OneDrive - GENES\Documents\Modeles de Taux\TauxSpotFin2019to2022\TauxNominauxSpot2019to2022.xlsx",sheet_name="2019",index_col=0).iloc[1:]
TauxReelSpot2021["Taux"]=(TauxNominauxSpot2021["Taux"]-ZCISspot2021["Taux"])/(1+ZCISspot2021["Taux"])

#  Données 2022
TauxNominauxSpot2022=pd.read_excel(r"C:\Users\samym\OneDrive - GENES\Documents\Modeles de Taux\TauxSpotFin2019to2022\TauxNominauxSpot2019to2022.xlsx",sheet_name="2022",index_col=0).iloc[1:]
ZCISspot2022=pd.read_excel(r"C:\Users\samym\OneDrive - GENES\Documents\Modeles de Taux\TauxSpotFin2019to2022\TauxInflaSpot2019to2022.xlsx",sheet_name="2022",index_col=0).iloc[1:]
TauxReelSpot2022=pd.read_excel(r"C:\Users\samym\OneDrive - GENES\Documents\Modeles de Taux\TauxSpotFin2019to2022\TauxNominauxSpot2019to2022.xlsx",sheet_name="2019",index_col=0).iloc[1:]
TauxReelSpot2022["Taux"]=(TauxNominauxSpot2022["Taux"]-ZCISspot2022["Taux"])/(1+ZCISspot2022["Taux"])
class ModeleAOA1facteur():
    def __init__(self,kappa,sigma):
        self.kappa=kappa
        self.sigma=sigma
        
        
    def Euler(self,T):
        pass
     
    def CalculTaux(self,T):
        Rates=self.Euler(T)
        ShortRates=Rates["Interest Rate"]
        # CalculTemps = [x/12 for x in range(0,12)] + [*range(1,T+1,1/12)]
        CalculTemps=np.arange(0,30+1/12,1/12)
        ZC=[]
        for element in CalculTemps:
            VectorTime=np.array(ShortRates.loc[:element].index) # Index de temps
            Rateto=np.array(ShortRates.loc[:element]) # On récupère la liste des taux courts réels jusqu'à la période de temps considérée
            priceelement=np.exp(-(sciIntegr.simps(Rateto , VectorTime))) # Calcul de l'intégrale du Zéro-Coupon Nominal par la méthode de Simpson
            ZC.append(priceelement)
        dictTaux = {'Temps' : CalculTemps, 'PrixZC' : ZC}
        Prix = pd.DataFrame.from_dict(data = dictTaux)
        Prix["Taux"]=-np.log(Prix["PrixZC"])/Prix["Temps"]
        return Prix[["Temps","Taux"]]
                
    def DiffusionTaux(self,T,N):
        # N est le nombre de courbes de taux que l'on veut simuler
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
     
        for i in (range(1,N)): # On Plot N courbes de taux 
            A=self.CalculTaux(T)
            ax.plot(A["Temps"],A["Taux"])            
        ax.set_ylabel("Taux d'intéret")
        ax.set_title("Diffusion de " +str(N) + " courbes de taux")
        ax.set_xlabel("Temps en années")
      
        
        return fig 
    

    
    
    
        
class ModeleAOA2facteurs():
    def __init__(self,kappax,kappay,sigmax,sigmay):
        self.kappax=kappax
        self.kappay=kappay
        self.sigmax=sigmax
        self.sigmay=sigmay
        
    def Euler(self,T):
        pass
        
    
    def CalculTaux(self,T):
        Rates=self.Euler(T)
        ShortRates=Rates["Interest Rate"]
        # CalculTemps = [x/12 for x in range(0,12)] + [*range(1,T+1,1/12)]
        CalculTemps=np.arange(0,30+1/12,1/12)
        ZC=[]
        for element in CalculTemps:
            VectorTime=np.array(ShortRates.loc[:element].index) # Index de temps
            Rateto=np.array(ShortRates.loc[:element]) # On récupère la liste des taux courts réels jusqu'à la période de temps considérée
            priceelement=np.exp(-(sciIntegr.simps(Rateto , VectorTime))) # Calcul de l'intégrale du Zéro-Coupon Nominal par la méthode de Simpson
            ZC.append(priceelement)
        dictTaux = {'Temps' : CalculTemps, 'PrixZC' : ZC}
        Prix = pd.DataFrame.from_dict(data = dictTaux)
        Prix["Taux"]=-np.log(Prix["PrixZC"])/Prix["Temps"]
        return Prix[["Temps","Taux"]]
                
    def DiffusionTaux(self,T,N):
        # N est le nombre de courbes de taux que l'on veut simuler
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        for i in (range(1,N)): # On Plot N courbes de taux 
            A=self.CalculTaux(T)
            ax.plot(A["Temps"],A["Taux"])
            
        ax.set_ylabel("Taux d'intéret")
        ax.set_title("Diffusion des courbes de taux")
        ax.set_xlabel("Temps en années")
        return fig 
    
 

