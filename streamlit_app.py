import streamlit as st
import pandas as pd
import plost
import streamlit_extras
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




