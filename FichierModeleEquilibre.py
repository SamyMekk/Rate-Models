# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 22:57:04 2023

@author: samym
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.integrate as sciIntegr
from scipy import interpolate


class ModeleEquilibre():
    
    def __init__(self,kappa,theta,sigma):
        self.kappa=kappa  # Correspond à la vitesse de retour à la moyenne
        self.theta=theta  # Correspond au taux de retour à la moyenne
        self.sigma=sigma  # Correspond à la volatilité du taux 
        
        
        
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