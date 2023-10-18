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



st.title('''On s'intéresse ici au modèle Hull & White dont on donne la dynamique ci-dessous''')



st.latex("dr(t)=(\\theta(t)-\kappa r(t))dt+\sigma  dWt")

st.write("Avec  : ")

st.write(" $\kappa$ : la vitesse de retour à la moyenne ")
st.write("$\sigma$ : le taux de retour à la moyenne " )
st.write("$\\theta(t)$ une fonction déterministe qui permet de reproduire la courbe des taux initiale")

st.subheader("Voici la manière dont on discrétise le modèle : ")

st.latex("r(t+\Delta)=r(t)e^{-\kappa \Delta}+\\alpha(t+\Delta)-\\alpha(t)e^{-\kappa\Delta}+\sqrt{U(t,t+\Delta)}\epsilon(t)")


st.subheader("Avec  : ")


st.write("$\\alpha(t)=f(0,t)+\\frac{\sigma^{2}}{2\kappa^{2}}(1-e^{-\kappa t})^{2}$")
st.write("$U(t,t+\Delta)=\\frac{\sigma^{2}}{2 \kappa}(1-e^{-2 \kappa \Delta})$")
st.write("$\epsilon(t)$ : une loi normale centrée réduite")
st.write("$\Delta$ : l'intervalle de temps choisi pour la modélisation du taux court")
st.write("$f(0,t)$ : le taux forward instantané en t")


st.subheader("Choississez ci-dessous la courbe initiale sur laquelle le modèle va se fit ( Courbes de début janvier de l'année)")


         
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
    année=st.selectbox("Choississez la courbe initiale sur laquelle le modèle va se fit",(2022,2021,2020,2019))
    data={    '''Vitesse de retour''':speed,
          '''Volatilité du taux''':volatility,
          '''Année de Calibration''':année}
    Parametres=pd.DataFrame(data,index=[0])
    return Parametres
            

df=user_input()


st.subheader("Choississez les paramètres du modèle sur le menu à gauche et ils s'afficheront sur le tableau ci-dessous :")

st.write(df)

Speed=df['Vitesse de retour'][0]
Volatility=df['Volatilité du taux'][0]
Année=df['Année de Calibration'][0]
Horizon=30


st.subheader("Voici l'allure de la courbe sur laquelle le modèle va se fit :")

if Année==2019:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(TauxNominauxSpot2019["Temps"],TauxNominauxSpot2019["Taux"])
    Tauxinitial=TauxNominauxSpot2019["Taux"][0]
    st.pyplot(fig)

if Année==2020:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(TauxNominauxSpot2020["Temps"],TauxNominauxSpot2020["Taux"])
    Tauxinitial=TauxNominauxSpot2020["Taux"][0]
    st.pyplot(fig)
    
if Année==2021:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(TauxNominauxSpot2021["Temps"],TauxNominauxSpot2021["Taux"])
    Tauxinitial=TauxNominauxSpot2021["Taux"][0]
    st.pyplot(fig)

if Année==2022:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(TauxNominauxSpot2022["Temps"],TauxNominauxSpot2022["Taux"])
    Tauxinitial=TauxNominauxSpot2022["Taux"][0]
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

def user_input3():
    Nombre=st.number_input("Choississez le nombre de courbes de taux vous souhaitez diffuser",value=10)
    data={'Nombre de Courbe de Taux': Nombre}
    Parametres2=pd.DataFrame(data,index=[0])
    return Parametres2


if st.button('Cliquer sur le Bouton pour diffuser des Courbes de Taux'):
    df3=user_input3()
    st.write(df3)
    Nombre=df3['Nombre de Courbe de Taux'][0]
    st.pyplot(ModeleHullWhite.DiffusionTaux(Horizon,Nombre))



