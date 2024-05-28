import streamlit as st
import pandas as pd
import plost
import streamlit_extras
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.row import row
from streamlit_extras.no_default_selectbox import selectbox

st.set_page_config(layout="wide", page_title="Simulateur Engie")

st.image('static/logo_engie.png')

"""## Faire une simulation pour un projet """

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.subheader('Simulation du projet')
st.text_input('Nom du projet')
col1, col2 = st.columns(2)

with col1:
    nb_designer_senior_prod = selectbox(
        "Nombre de designer sénior en prod",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

    nb_designer_junior_prod = selectbox(
        "Nombre de designer junior en prod",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

    nb_dev_senior_prod = selectbox(
        "Nombre de développeur sénior en prod",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="---"
    )

    nb_dev_junior_prod = selectbox(
        "Nombre de développeur junior en prod",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

with col2:
    nb_designer_senior_maintenance = selectbox(
        "Nombre de designer sénior en maintenance",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="---"
   )

    nb_designer_junior_maintenance = selectbox(
        "Nombre de designer junior en maintenance",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

    nb_dev_senior_maintenance = selectbox(
        "Nombre de développeur sénior en maintenance",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

    nb_dev_junior_maintenance = selectbox(
        "Nombre de développeur junior en maintenance",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="---"
    )
    
tarification = selectbox(
    "Choisir la tarification en fonction du nombre de projets utilisant Fluid dans la BU",
    ["1 à 2 projets", "3 à 7 projets", "8 projets ou plus"],
    no_selection_label="---"
)
temps_prod = st.slider('Spécifier la durée du projet en prod', 6, 30, 60)

if tarification == "1 à 2 projets":
    cout_fluid = 0.17
elif tarification == "3 à 7 projets":
    cout_fluid = 0.16
elif tarification == "8 projets ou plus":
    cout_fluid = 0.15
else:
    cout_fluid = 0

## Calculs PROD
designer_prod_senior = nb_designer_senior_prod*int(55000)
designer_prod_junior = nb_designer_junior_prod*int(40000)
designer_prod = designer_prod_senior + designer_prod_junior

dev_prod_senior = nb_dev_senior_prod*int(60000)
dev_prod_junior = nb_dev_junior_prod*int(42000)
dev_prod = dev_prod_senior + dev_prod_junior

cout_prod_annuel_sf = designer_prod + dev_prod
cout_prod_mensuel_sf = cout_prod_annuel_sf/12

cout_prod_annuel_af = cout_prod_annuel_sf
cout_prod_mensuel_af = cout_prod_annuel_af/12

## Calculs MAINTENANCE
designer_maintenance_senior = nb_designer_senior_maintenance*int(55000)
designer_maintenance_junior = nb_designer_junior_maintenance*int(40000)
designer_maintenance = designer_maintenance_senior + designer_maintenance_junior

dev_maintenance_senior = nb_dev_senior_maintenance*int(60000)
dev_maintenance_junior = nb_dev_junior_maintenance*int(42000)
dev_maintenance = dev_maintenance_senior + dev_maintenance_junior

cout_maintenance_annuel_sf = designer_maintenance + dev_maintenance
cout_maintenance_mensuel_sf = cout_maintenance_annuel_sf/12

cout_maintenance_annuel_af = cout_maintenance_annuel_sf * 0.66
cout_maintenance_mensuel_af = cout_maintenance_annuel_af/12

# COUT FLUID FIXE
cout_fluid_fix = (cout_maintenance_annuel_sf + cout_prod_annuel_sf) * cout_fluid

## Temps de maintenance = 2 ans = 24 mois fixes
temps_maintenance = 24

x_axis = np.arange(0, temps_prod + temps_maintenance)

## POUR SANS FLUID
costs_without_fluid = np.zeros(len(x_axis))

# Ajout des coûts mensuel de production sans Fluid
for i in range(temps_prod):
    costs_without_fluid[i] = cout_prod_mensuel_sf

# Ajout des coûts mensuel de maintenance sans Fluid
for i in range(temps_prod, len(x_axis)):
    costs_without_fluid[i] = cout_maintenance_mensuel_sf

# Calcul des coûts cumulés sans Fluid
costs_without_fluid = np.cumsum(costs_without_fluid)

## POUR AVEC FLUID
temps_prod_af = int(temps_prod * 0.66)
temps_maintenance_af = 24 + temps_prod * 0.34

costs_with_fluid = np.zeros(len(x_axis))

# Ajout des coûts mensuel de production avec Fluid
for i in range(temps_prod_af):
    costs_with_fluid[i] = cout_prod_mensuel_af

# Ajout des coûts mensuel de maintenance avec Fluid
for i in range(temps_prod_af, len(x_axis)):
    costs_with_fluid[i] = cout_maintenance_mensuel_af

# Ajustement du premier mois Avec cout fluid fixe
costs_with_fluid[0] = cout_prod_mensuel_af + cout_fluid_fix

# Calcul des coûts cumulés avec Fluid
costs_with_fluid = np.cumsum(costs_with_fluid)

data = {'Avec Fluid': costs_with_fluid,
        'Sans Fluid': costs_without_fluid}

df = pd.DataFrame(data, index=x_axis)

st.line_chart(data, use_container_width=True, y=['Avec Fluid', 'Sans Fluid'])



