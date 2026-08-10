import streamlit as st
import pandas as pd

#Importando funciones creadas en src/

from src.database import run_query
from src.statistics import (
    conversion_rate,
    calculate_uplift,
    z_test,
    daily_conversion
)

from src.visualizations import (
    daily_conversion_chart,
    cumulative_sample_size,
    conversion_bar
)


#Streamlit: portada

st.set_page_config(
    page_title="A/B Testing Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("A/B Testing Dashboard")

st.write(
    "Analisis de experimento A/B comparando "
    "grupos de control y tratamiento."
)



#CREANDO DATAFRAME a partir del warehouse creado en "data/ab_testing.db"

query = """
SELECT *
FROM experiment;
"""

df = run_query(query)

# visualizando el dataframe en streamlit

st.subheader("Experiment Data")

st.dataframe(df)

# --------------------------------------------------------------------------------------

#CONVERSION RATE

results = conversion_rate(df)

#visualizándolas en streamlit

st.subheader("Conversion Results")

st.dataframe(results)

# --------------------------------------------------------------------------------------


#TEST ESTADÍSTICO (Z-TEST)

test_results = z_test(results)

#visualizándolo en streamlit

st.subheader("Statistical Test")

st.write(test_results)


# --------------------------------------------------------------------------------------

#CÁLCULO DE UPLIFT

uplift = calculate_uplift(results)


#visualizándolo en streamlit

st.write(f"Uplift: {uplift:.2%}")


# ---------------------------------------------------------------------------------------

#CONVERSIÓN DIARIA

daily_df = daily_conversion(df)

#visualizándolo en streamlit

st.subheader("Daily Conversion")

st.dataframe(daily_df)

# ---------------------------------------------------------------------------------------



#GRÁFICO DE CONVERSIÓN DIARIA

fig_daily = daily_conversion_chart(daily_df)

st.plotly_chart(
    fig_daily,
    use_container_width=True
)

#GRÁFICO DE TAMAÑO DE MUESTRA ACUMULADO

fig_sample = cumulative_sample_size(df)

st.plotly_chart(
    fig_sample,
    use_container_width=True
)

#GRÁFICO DE CONVERSIÓN POR GRUPO

fig_conversion = conversion_bar(results)

st.plotly_chart(
    fig_conversion,
    use_container_width=True
)