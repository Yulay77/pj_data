import streamlit as st
import pandas as pd
import plost
import streamlit_extras
import numpy as np
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
    nb_designer_senior_build_phase = selectbox(
        "Nombre de designer sénior en build phase",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

    nb_designer_junior_build_phase = selectbox(
        "Nombre de designer junior en build phase",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

    nb_dev_senior_build_phase = selectbox(
        "Nombre de développeur sénior en build phase",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="---"
    )

    nb_dev_junior_build_phase = selectbox(
        "Nombre de développeur junior en build phase",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

with col2:
    nb_designer_senior_run_phase = selectbox(
        "Nombre de designer sénior en run phase",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="---"
   )

    nb_designer_junior_run_phase = selectbox(
        "Nombre de designer junior en run phase",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

    nb_dev_senior_run_phase = selectbox(
        "Nombre de développeur sénior en run phase",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        no_selection_label="---"
    )

    nb_dev_junior_run_phase = selectbox(
        "Nombre de développeur junior en run phase",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="---"
    )
    
tarification = selectbox(
    "Choisir la tarification en fonction du nombre de projets utilisant Fluid dans la BU",
    ["1 à 2 projets", "3 à 7 projets", "8 projets ou plus"],
    no_selection_label="---"
)
temps_build_phase = st.slider('Spécifier la durée du projet en build phase', 6, 60, 24)

if tarification == "1 à 2 projets":
    cout_fluid = 0.17
elif tarification == "3 à 7 projets":
    cout_fluid = 0.16
elif tarification == "8 projets ou plus":
    cout_fluid = 0.15
else:
    cout_fluid = 0

## Calculs build_phase
designer_build_phase_senior = nb_designer_senior_build_phase*int(55000)
designer_build_phase_junior = nb_designer_junior_build_phase*int(40000)
designer_build_phase = designer_build_phase_senior + designer_build_phase_junior

dev_build_phase_senior = nb_dev_senior_build_phase*int(60000)
dev_build_phase_junior = nb_dev_junior_build_phase*int(42000)
dev_build_phase = dev_build_phase_senior + dev_build_phase_junior

cout_build_phase_annuel_sf = designer_build_phase + dev_build_phase
cout_build_phase_mensuel_sf = cout_build_phase_annuel_sf/12

cout_build_phase_annuel_af = cout_build_phase_annuel_sf
cout_build_phase_mensuel_af = cout_build_phase_annuel_af/12

## Calculs run_phase
designer_run_phase_senior = nb_designer_senior_run_phase*int(55000)
designer_run_phase_junior = nb_designer_junior_run_phase*int(40000)
designer_run_phase = designer_run_phase_senior + designer_run_phase_junior

dev_run_phase_senior = nb_dev_senior_run_phase*int(60000)
dev_run_phase_junior = nb_dev_junior_run_phase*int(42000)
dev_run_phase = dev_run_phase_senior + dev_run_phase_junior

cout_run_phase_annuel_sf = designer_run_phase + dev_run_phase
cout_run_phase_mensuel_sf = cout_run_phase_annuel_sf/12

cout_run_phase_annuel_af = cout_run_phase_annuel_sf * 0.66
cout_run_phase_mensuel_af = cout_run_phase_annuel_af/12

# COUT FLUID FIXE
cout_fluid_fix = (cout_run_phase_annuel_sf + cout_build_phase_annuel_sf) * cout_fluid

## Temps de run_phase = 2 ans = 24 mois fixes
temps_run_phase = 24

x_axis = np.arange(0, temps_build_phase + temps_run_phase)

## POUR SANS FLUID
costs_without_fluid = np.zeros(len(x_axis))

# Ajout des coûts mensuel de build_phaseuction sans Fluid
for i in range(temps_build_phase):
    costs_without_fluid[i] = cout_build_phase_mensuel_sf

# Ajout des coûts mensuel de run_phase sans Fluid
for i in range(temps_build_phase, len(x_axis)):
    costs_without_fluid[i] = cout_run_phase_mensuel_sf

# Calcul des coûts cumulés sans Fluid
costs_without_fluid = np.cumsum(costs_without_fluid)

## POUR AVEC FLUID
temps_build_phase_af = int(temps_build_phase * 0.66)
temps_run_phase_af = 24 + temps_build_phase * 0.34

costs_with_fluid = np.zeros(len(x_axis))

# Ajout des coûts mensuel de build_phaseuction avec Fluid
for i in range(temps_build_phase_af):
    costs_with_fluid[i] = cout_build_phase_mensuel_af

# Ajout des coûts mensuel de run_phase avec Fluid
for i in range(temps_build_phase_af, len(x_axis)):
    costs_with_fluid[i] = cout_run_phase_mensuel_af

# Ajustement du premier mois Avec cout fluid fixe
costs_with_fluid[0] = cout_build_phase_mensuel_af + cout_fluid_fix

# Calcul des coûts cumulés avec Fluid
costs_with_fluid = np.cumsum(costs_with_fluid)

data = {'Avec Fluid': costs_with_fluid,
        'Sans Fluid': costs_without_fluid}

df = pd.DataFrame(data, index=x_axis)

st.line_chart(data, use_container_width=True, y=['Avec Fluid', 'Sans Fluid'])

st.write(df.round(0))



