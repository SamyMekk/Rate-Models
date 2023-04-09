# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:08:29 2023

@author: smekkaoui
"""

""


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FichierModeleAOA import *

st.title("On va s'intéresser à la dynamique du modèle G2++")

st.write('''On va modéliser le taux d'intérêt  $r(t)$ par un Processus G2++ dont on rappelle la dynamique:''')




class G2(ModeleAOA2facteurs):
    def __init__(self,kappax,kappay,sigmax,sigmay,rho,r0,année):
        ModeleAOA2facteurs.__init__(self,kappax,kappay,sigmax,sigmay)
        self.rho=rho
        self.r0=r0
        self.année=année
        self.dt=1/12
        
        
        
    def FonctionCalibrationCourbeInitiale(self,t): # Fonction qui permet de se caler à la courbe des taux initiale
            if self.année==2019:
                 tck=interpolate.splrep(TauxNominauxSpot2019["Temps"],TauxNominauxSpot2019["Taux"],s=0)
                 ForwardRate=float(interpolate.splev(t,tck))+t*float(interpolate.splev(t,tck,der=1))
                 return  ForwardRate+((pow(self.sigmax,2))/2*pow(self.kappax,2))*pow((1-np.exp(-self.kappax*t)),2) +((pow(self.sigmay,2))/2*pow(self.kappay,2))*pow((1-np.exp(-self.kappay*t)),2)+((self.rho*self.sigmax*self.sigmay)/(self.kappax*self.kappay))*(1-np.exp(-self.kappay*t))*(1-np.exp(-self.kappax*t))           

            if self.année==2020:
                 tck=interpolate.splrep(TauxNominauxSpot2020["Temps"],TauxNominauxSpot2020["Taux"],s=0)
                 ForwardRate=float(interpolate.splev(t,tck))+t*float(interpolate.splev(t,tck,der=1))
                 return  ForwardRate+((pow(self.sigmax,2))/2*pow(self.kappax,2))*pow((1-np.exp(-self.kappax*t)),2) +((pow(self.sigmay,2))/2*pow(self.kappay,2))*pow((1-np.exp(-self.kappay*t)),2)+((self.rho*self.sigmax*self.sigmay)/(self.kappax*self.kappay))*(1-np.exp(-self.kappay*t))*(1-np.exp(-self.kappax*t))           
            if self.année==2021:
                 tck=interpolate.splrep(TauxNominauxSpot2021["Temps"],TauxNominauxSpot2021["Taux"],s=0)
                 ForwardRate=float(interpolate.splev(t,tck))+t*float(interpolate.splev(t,tck,der=1))
                 return  ForwardRate+((pow(self.sigmax,2))/2*pow(self.kappax,2))*pow((1-np.exp(-self.kappax*t)),2) +((pow(self.sigmay,2))/2*pow(self.kappay,2))*pow((1-np.exp(-self.kappay*t)),2)+((self.rho*self.sigmax*self.sigmay)/(self.kappax*self.kappay))*(1-np.exp(-self.kappay*t))*(1-np.exp(-self.kappax*t))           
            if self.année==2022:
                 tck=interpolate.splrep(TauxNominauxSpot2022["Temps"],TauxNominauxSpot2022["Taux"],s=0)
                 ForwardRate=float(interpolate.splev(t,tck))+t*float(interpolate.splev(t,tck,der=1))
                 return  ForwardRate+((pow(self.sigmax,2))/2*pow(self.kappax,2))*pow((1-np.exp(-self.kappax*t)),2) +((pow(self.sigmay,2))/2*pow(self.kappay,2))*pow((1-np.exp(-self.kappay*t)),2)+((self.rho*self.sigmax*self.sigmay)/(self.kappax*self.kappay))*(1-np.exp(-self.kappay*t))*(1-np.exp(-self.kappax*t))           
        
        
    def Euler(self,T):
        N=int(T/self.dt)+1
        time, delta_t = np.linspace(0, T, num = N, retstep = True)
        Taux=np.ones(N)*self.r0
        x=np.ones(N)*0
        y=np.ones(N)*0
        FonctionCalibration=[]
        mean = [0, 0] # mean vector
        cov = [[1, self.rho], [self.rho, 1]] # covariance matrix
        for t in time:
            FonctionCalibration.append(self.FonctionCalibrationCourbeInitiale(t))
        for t in range(1,N):
            Gaussian=np.random.multivariate_normal(mean, cov, 1)
            x[t]=np.exp(-self.kappax*self.dt)*x[t-1]+self.sigmax*np.sqrt((1-np.exp(-2*self.kappax*self.dt))/(2*self.kappax))*Gaussian[0][0]
            y[t]=np.exp(-self.kappay*self.dt)*y[t-1]+self.sigmay*np.sqrt((1-np.exp(-2*self.kappay*self.dt))/(2*self.kappay))*Gaussian[0][1]
            Taux[t]=x[t]+y[t]+FonctionCalibration[t]
        dict1 = {'Time' : time, 'Interest Rate' : Taux}
        TauxCourt = pd.DataFrame.from_dict(data = dict1)
        TauxCourt.set_index('Time', inplace = True)
        return TauxCourt


def user_input():
    speedx=st.sidebar.number_input("Choississez la vitesse de retour à la moyenne du 1er facteur Gaussien",value= 0.039)
    volatilityx=st.sidebar.number_input("Choississez la volatilité du 1er facteur Gaussien",value=0.00539)
    speedy=st.sidebar.number_input("Choississez la vitesse de retour à la moyenne du 2nd facteur Gaussien",value= 0.039)
    volatilityy=st.sidebar.number_input("Choississez la volatilité du 2nd facteur Gaussien",value=0.00539)
    rho=st.sidebar.number_input("Choississez la corrélation entre les 2 facteurs gaussiens",value=0.5)
    initialrate=st.number_input("Choississez le taux initial",value=0.024)
    année=st.selectbox("Choississez la courbe initiale sur laquelle le modèle va se fit",(2022,2021,2020,2019))
    data={    '''Vitesse de retour du 1er facteur Gaussien''':speedx,
          '''Vitesse de retour du 2nd facteur Gaussien''':speedy,
          '''Volatilité du 1er Facteur Gaussien''':volatilityx,
          '''Volatilité du 2nd Facteur Gaussien''':volatilityy,
          '''Corrélation entre les 2 facteurs gaussiens''':rho,
          '''Taux initial''':initialrate,
          '''Année de Calibration''':année}
    Parametres=pd.DataFrame(data,index=[0])
    return Parametres
            
df=user_input()
st.subheader("Voici les paramètres que vous avez choisi :")

st.write(df)

Speedx=df['Vitesse de retour du 1er facteur Gaussien'][0]
Speedy=df['Vitesse de retour du 2nd facteur Gaussien'][0]
Volatilityx=df['Volatilité du 1er Facteur Gaussien'][0]
Volatilityy=df['Volatilité du 2nd Facteur Gaussien'][0]
rho=df['Corrélation entre les 2 facteurs gaussiens'][0]
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
    
    
ModeleG2=G2(Speedx,Speedy,Volatilityx,Volatilityy,rho,Tauxinitial,Année)


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

st.pyplot(ModeleG2.DiffusionTaux(30,100))


