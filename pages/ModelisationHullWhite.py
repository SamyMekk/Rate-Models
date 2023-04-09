# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 23:52:06 2023

@author: samym
"""


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FichierModeleAOA import *

st.title("On va s'intéresser à la dynamique du modèle Hull White")

st.write('''On va modéliser le taux d'intérêt  $r(t)$ par un Processus Hull White dont on rappelle la dynamique:''')

         
class HullWhite(ModeleAOA1facteur):
    def __init__(self,kappa,sigma,r0,année):
        ModeleAOA1facteur.__init__(self,kappa,sigma)
        self.r0=r0
        self.dt=1/12
        self.année=année
        
    def FonctionCalibrationCourbeInitiale(self,t): # Fonction qui permet de se caler à la courbe des taux initiale
            if self.année==2019:
                 tck=interpolate.splrep(TauxNominauxSpot2019["Temps"],TauxNominauxSpot2019["Taux"],s=0)
                 ForwardRate=float(interpolate.splev(t,tck))+t*float(interpolate.splev(t,tck,der=1))
                 return ForwardRate+((pow(self.sigma,2))/2*pow(self.kappa,2))*pow((1-np.exp(-self.kappa*t)),2) 
            if self.année==2020:
                 tck=interpolate.splrep(TauxNominauxSpot2020["Temps"],TauxNominauxSpot2020["Taux"],s=0)
                 ForwardRate=float(interpolate.splev(t,tck))+t*float(interpolate.splev(t,tck,der=1))
                 return ForwardRate+((pow(self.sigma,2))/2*pow(self.kappa,2))*pow((1-np.exp(-self.kappa*t)),2)
            if self.année==2021:
                 tck=interpolate.splrep(TauxNominauxSpot2021["Temps"],TauxNominauxSpot2021["Taux"],s=0)
                 ForwardRate=float(interpolate.splev(t,tck))+t*float(interpolate.splev(t,tck,der=1))
                 return ForwardRate+((pow(self.sigma,2))/2*pow(self.kappa,2))*pow((1-np.exp(-self.kappa*t)),2)
            if self.année==2022:
                 tck=interpolate.splrep(TauxNominauxSpot2022["Temps"],TauxNominauxSpot2022["Taux"],s=0)
                 ForwardRate=float(interpolate.splev(t,tck))+t*float(interpolate.splev(t,tck,der=1))
                 return ForwardRate+((pow(self.sigma,2))/2*pow(self.kappa,2))*pow((1-np.exp(-self.kappa*t)),2)
    def Euler(self,T):
        N=int(T/self.dt)+1
        time, delta_t = np.linspace(0, T, num = N, retstep = True)
        Taux=np.ones(N)*self.r0
        FonctionCalibration=[]
        for t in time:
            FonctionCalibration.append(self.FonctionCalibrationCourbeInitiale(t))
        for t in range(1,N):
            Taux[t]=Taux[t-1]*np.exp(-self.kappa*self.dt)+FonctionCalibration[t]-FonctionCalibration[t-1]*np.exp(-self.kappa*self.dt)+self.sigma*np.sqrt((1-np.exp(-2*self.kappa*self.dt))/(2*self.kappa))*np.random.normal(loc=0,scale=1,size=1)
        dict1 = {'Time' : time, 'Interest Rate' : Taux}
        TauxCourt = pd.DataFrame.from_dict(data = dict1)
        TauxCourt.set_index('Time', inplace = True)

        return TauxCourt
        
    
def user_input():
    speed=st.sidebar.number_input("Choississez la vitesse de retour à la moyenne",value= 0.039)
    volatility=st.sidebar.number_input("Choississez la volatilité du taux réel",value=0.00539)
    initialrate=st.sidebar.number_input("Choississez le taux initial",value=0.0296)
    année=st.sidebar.selectbox("Choississez la courbe initiale sur laquelle le modèle va se fit",(2022,2021,2020,2019))
    data={    '''Vitesse de retour''':speed,
          '''Volatilité du taux''':volatility,
          '''Taux initial''':initialrate,
          '''Année de Calibration''':année}
    Parametres=pd.DataFrame(data,index=[0])
    return Parametres
            

df=user_input()


st.subheader("Voici les paramètres que vous avez choisi :")

st.write(df)

Speed=df['Vitesse de retour'][0]
Volatility=df['Volatilité du taux'][0]
Tauxinitial=df['Taux initial'][0]
Année=df['Année de Calibration'][0]
Horizon=30


st.subheader("Voici l'allure de la courbe sur laquelle le modèle va se fit :")

if Année==2019:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(TauxNominauxSpot2019["Temps"],TauxNominauxSpot2019["Taux"])
    st.pyplot(fig)

if Année==2020:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(TauxNominauxSpot2020["Temps"],TauxNominauxSpot2020["Taux"])
    st.pyplot(fig)
    
if Année==2021:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(TauxNominauxSpot2021["Temps"],TauxNominauxSpot2021["Taux"])
    st.pyplot(fig)

if Année==2022:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(TauxNominauxSpot2022["Temps"],TauxNominauxSpot2022["Taux"])
    st.pyplot(fig)


ModeleHullWhite=HullWhite(Speed,Volatility,Tauxinitial,Année)


st.subheader("Voici l'allure des Courbes de Taux obtenue par le modèle")


# Ajout de la Fonctionnalité Nombre de Simulations
# def user_input2():
#     Simulations=st.slider("Choissisez le nombre de simulations : ",100,1000,100)
#     data={'Nombre de Simulations': Simulations}
#     Parametres2=pd.DataFrame(data,index=[0])
#     return Parametres2


# df2=user_input2()
# st.write(df2)
# Simulations=df2["Nombre de Simulations"][0]

st.pyplot(ModeleHullWhite.DiffusionTaux(30,100))

