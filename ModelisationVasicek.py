# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 23:05:37 2023

@author: samym
"""

import pandas as pd
import streamlit as st
import numpy as np
from FichierModeleEquilibre import *

st.title(''' Application Simple faite par  Samy Mekkaoui  pour la Modélisation des Taux d'intérêts par différents modèles''')

class Vasicek(ModeleEquilibre):
    def __init__(self,kappa,theta,sigma,r0):
        ModeleEquilibre.__init__(self,kappa,theta,sigma)
        self.r0=r0
        self.dt=1/12
        
        
    def Euler(self,T):
        N=int(T/self.dt)+1
        time, delta_t = np.linspace(0, T, num = N, retstep = True)
        Taux=np.ones(N)*self.r0
        for t in range(1,N):
            Taux[t] = Taux[t-1] * np.exp(-self.kappa*self.dt)+self.theta*(1-np.exp(-self.kappa*self.dt))+self.sigma*np.sqrt((1-np.exp(-2*self.kappa*self.dt))/(2*self.kappa))*np.random.normal(loc=0,scale=1,size=1)
        dict1 = {'Time' : time, 'Interest Rate' : Taux}
        TauxCourt = pd.DataFrame.from_dict(data = dict1)
        TauxCourt.set_index('Time', inplace = True)

        return TauxCourt


# Partie Streamlit dans le code 


def user_input():
    meanreversion=st.sidebar.number_input("Choississez le taux de retour",value= 0.0186)
    speed=st.sidebar.number_input("Choississez la vitesse de retour à la moyenne",value= 0.039)
    volatility=st.sidebar.number_input("Choississez la volatilité du taux réel",value=0.00539)
    initialrate=st.sidebar.number_input("Choississez le taux initial",value=0.0296)
    data={'''Taux de retour''': meanreversion,
          '''Vitesse de retour''':speed,
          '''Volatilité du taux''':volatility,
          '''Taux initial''':initialrate}
    Parametres=pd.DataFrame(data,index=[0])
    return Parametres

df=user_input()


st.header("On va  s'intéresser à la modélisation de trajectoires dont on donne la dynamique ci-dessous : ")

st.latex("dr(t)=a(b-r(t))dt+\sigma dWt")

st.write("Avec  : ")

st.write("a : la vitesse de retour à la moyenne ")
st.write("b : le taux de retour à la moyenne " )
st.write(" $\sigma$ la volatilité du taux ")

st.subheader("Voici la manière dont on modélise les trajectoires de proche en proche : ")

st.latex("r(t+\Delta)=r(t)e^{- a \Delta}+ b (1-e^{- a \Delta}) + \\frac{\sigma^{2}(1-e^{-2a \Delta})}{2} \epsilon(t)  ")

st.subheader("Choississez l'échelle de temps de projection dans la construction du modèle qui est faite de proche ")

st.write("Avec  : ")

st.write("$\epsilon$ : Une loi Normale centrée réduite")
st.write("$\Delta$ : l'intervalle de temps choisi pour la modélisation du taux court")




st.subheader("Voici les paramètres que vous avez choisi :")

st.write(df)


st.subheader("Vous pouvez également choisir l'horizon temporel dans le calcul via la fonctionnalité suivante : ")

def user_input2():
    duree=st.slider("Choissisez le temps : ",20,80,50)
    data={'Horizon Temporel': duree}
    Parametres2=pd.DataFrame(data,index=[0])
    return Parametres2

df2=user_input2()
st.write(df2)


MeanReversion=df['Taux de retour'][0]
Speed=df['Vitesse de retour'][0]
Volatility=df['Volatilité du taux'][0]
Tauxinitial=df['Taux initial'][0]
Horizon=df2['Horizon Temporel'][0]


ModeleVasicek=Vasicek(Speed,MeanReversion,Volatility,Tauxinitial)

def user_input3():
    Nombre=st.number_input("Choississez le nombre de courbes de taux vous souhaitez diffuser",value=30)
    data={'Nombre de Courbe de Taux': Nombre}
    Parametres2=pd.DataFrame(data,index=[0])
    return Parametres2

if st.button('Cliquer sur le Bouton pour diffuser des Courbes de Taux'):
    df3=user_input3()
    st.write(df3)
    Nombre=df3['Nombre de Courbe de Taux'][0]
    st.pyplot(ModeleVasicek.DiffusionTaux(Horizon,Nombre))


