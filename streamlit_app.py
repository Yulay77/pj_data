import streamlit as st
import pandas as pd
import plost
import streamlit_extras
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.row import row

st.set_page_config(layout="wide", page_title="Simulateur Engie")

st.image('static/logo_engie.png')

"""## Faire une simulation pour un projet """

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# Row A
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

st.subheader('Simulation du projet')
st.text_input('Nom du projet')
time_hist_color = st.selectbox('Color by', ('temp_min', 'temp_max')) 

st.markdown('Donut chart parameter')
donut_theta = st.selectbox('Select data', ('q2', 'q3'))

st.markdown('Line chart parameters')
plot_data = st.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.slider('Specify plot height', 200, 500, 250)


st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)

add_vertical_space(15)

# Row B
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Row C
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




