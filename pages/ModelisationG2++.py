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
from pandas_datareader.data import DataReader


st.title("On va s'intéresser à la dynamique du modèle G2++")

st.write('''On va modéliser le taux d'intérêt réel $r_{R}(t)$ par un Processus G2++ dont on rappelle la dynamique:''')

