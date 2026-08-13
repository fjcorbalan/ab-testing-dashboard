import streamlit as st
import pandas as pd
from pathlib import Path

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

query_path = Path("sql/select_all.sql") #lugar donde tenemos nuestra query sql

query = query_path.read_text(encoding="utf-8")

df = run_query(query)


#CÁLCULO MÉTRICAS

results = conversion_rate(df)

uplift = calculate_uplift(results)

test_results = z_test(results)

daily_df = daily_conversion(df)

#conversiones
control_cvr = results.loc["control", "conversion_rate"]
treatment_cvr = results.loc["treatment", "conversion_rate"]

#número de usuarios
control_users = results.loc["control", "users"]
treatment_users = results.loc["treatment", "users"]

#métricas test estadístico (z-test)
p_value = test_results["p_value"]
z_score = test_results["z_score"]
significant = test_results["significant"]


#STREAMLIT: 

# indicadores (conversion de control, conversion de test, uplift y p-value del z-test)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Control conversion",
        f"{control_cvr:.2%}"
    )

with col2:
    st.metric(
        "Treatment conversion",
        f"{treatment_cvr:.2%}"
    )

with col3:
    st.metric(
        "Uplift",
        f"{uplift:.2%}"
    )

with col4:
    st.metric(
        "P-value",
        f"{p_value:.4g}"
    )

# conclusiones

if significant:
    st.success(
        "El grupo de tratamiento o variante muestra diferencias estadísticamente "
        "significativas en conversion rate comparando con el grupo de control."
    )
else:
    st.info(
        "El experimento no muestra una diferencia significativa "
        "en conversion rate."
    )


#GRÁFICOS

#conversión diaria: vemos si hay fluctuaciones importantes

st.subheader("Conversion Rate por Fecha de Observación")

fig_daily = daily_conversion_chart(daily_df)

st.plotly_chart(
    fig_daily,
    use_container_width=True
)


#tamaño de muestra acumulado (usuarios): al tiempo que vamos sumando usuarios, ¿qué pasa con la conversión?

st.subheader("Tamaño de muestra acumulado")

fig_sample = cumulative_sample_size(df)

st.plotly_chart(
    fig_sample,
    use_container_width=True
)


#resumen experimento

st.subheader("Conversion Rate Final")

fig_conversion = conversion_bar(results)

st.plotly_chart(
    fig_conversion,
    use_container_width=True
) 