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

#Row A
st.subheader('Simulation du projet')
st.text_input('Nom du projet')
col1, col2 = st.columns(2)

with col1:
    nb_designer_senior_prod = selectbox(
        "Nombre de designer sénior en prod",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="...",
    )

    nb_designer_junior_prod = selectbox(
        "Nombre de designer junior en prod",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="...",
    )

    nb_dev_senior_prod = selectbox(
        "Nombre de développeur sénior en prod",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="...",
    )

    nb_dev_junior_prod = selectbox(
        "Nombre de développeur junior en prod",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="...",
    )

with col2:
    nb_designer_senior_maintenance = selectbox(
        "Nombre de designer sénior en maintenance",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="...",
    )

    nb_designer_junior_maintenance = selectbox(
        "Nombre de designer junior en maintenance",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="...",
    )

    nb_dev_senior_maintenance = selectbox(
        "Nombre de développeur sénior en maintenance",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="...",
    )

    nb_dev_junior_maintenance = selectbox(
        "Nombre de développeur junior en maintenance",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        no_selection_label="...",
    )
    
tarification = selectbox(
    "Choisir la tarification en fonction du nombre de projets utilisant Fluid dans la BU",
    ["1 à 2 projets", "3 à 5 projets", "6 à 7 projets", "Plus de 8 projets"],
    no_selection_label="...",
)
plot_time = st.slider('Spécifier la durée du projet en prod', 6, 30, 60)

if tarification == "1 à 2 projets":
    cout_fluid = 40000
elif tarification == "3 à 5 projets":
    cout_fluid = 35000
elif tarification == "6 à 7 projets":
    cout_fluid = 30000
elif tarification == "Plus de 8 projets":
    cout_fluid = 25000
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

cout_prod_annuel_af = cout_prod_annuel_sf+cout_fluid
cout_prod_mensuel_af = cout_prod_annuel_af/12

##Calculs MAINTENANCE

designer_maintenance_senior = nb_designer_senior_maintenance*int(55000)
designer_maintenance_junior = nb_designer_junior_maintenance*int(40000)
designer_maintenance = designer_maintenance_senior + designer_maintenance_junior

dev_maintenance_senior = nb_dev_senior_maintenance*int(60000)
dev_maintenance_junior = nb_dev_junior_maintenance*int(42000)
dev_maintenance = dev_maintenance_senior + dev_maintenance_junior

cout_maintenance_annuel_sf = designer_maintenance + dev_maintenance
cout_maintenance_mensuel_sf = cout_maintenance_annuel_sf/12

cout_maintenance_annuel_af = cout_maintenance_annuel_sf
cout_maintenance_mensuel_af = cout_maintenance_annuel_af/12
## /!\ les cout af et sf sont les mêmes pour la maintenance

# Create a sample dataframe
data = {'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
        'Avec Fluid': np.random.rand(60000),
        'Sans Fluid': np.random.rand(60000)}
df = pd.DataFrame(data)

# Add a slider for the y-axis
#min_cost, max_cost = st.slider("Select a range of costs", 0, 1, (0, 1))

min_cost = 0
max_cost = 50000

# Filter the dataframe based on the selected range
df_filtered = df[(df['Avec Fluid'] >= min_cost) & (df['Avec Fluid'] <= max_cost) &
                 (df['Sans Fluid'] >= min_cost) & (df['Sans Fluid'] <= max_cost)]

# Plot the line chart
st.line_chart(df_filtered, x='Month', y=['Avec Fluid', 'Sans Fluid'])


#st.line_chart(CSV A METTRE, x = plot_time+int(24), y = plot_data, height = plot_height)


add_vertical_space(10)

# Row B
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

time_hist_color = st.selectbox('Color by', ('temp_min', 'temp_max')) 

st.markdown('Donut chart parameter')
donut_theta = st.selectbox('Select data', ('q2', 'q3'))

st.markdown('Line chart parameters')
plot_data = st.multiselect('Avec et sans Fluid', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.slider('Specify plot height', 200, 500, 250)


st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)

add_vertical_space(15)

# Row C
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Row D
c1, c2 = st.columns((7,3))
with c1:
    st.markdown('### Heatmap')
    plost.time_hist(
    data=seattle_weather,
    date='date',
    x_unit='week',
    y_unit='day',
    color=time_hist_color,
    aggregate='median',
    legend=None,
    height=345,
    use_container_width=True)
with c2:
    st.markdown('### Donut chart')
    plost.donut_chart(
        data=stocks,
        theta=donut_theta,
        color='company',
        legend='bottom', 
        use_container_width=True)




