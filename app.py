import streamlit as st
from pathlib import Path

# Importando funciones creadas en src/

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


# ---------------------------------------------------------
# STREAMLIT: CONFIGURACIÓN
# ---------------------------------------------------------

st.set_page_config(
    page_title="A/B Testing Dashboard",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# PORTADA
# ---------------------------------------------------------

st.title("A/B Testing Dashboard")

st.write(
    "Análisis de experimento A/B comparando "
    "grupos de control y tratamiento."
)


# ---------------------------------------------------------
# CREANDO DATAFRAME DESDE SQLITE
# ---------------------------------------------------------

query_path = Path("sql/select_all.sql")

query = query_path.read_text(encoding="utf-8")

df = run_query(query)


# ---------------------------------------------------------
# CÁLCULO DE MÉTRICAS
# ---------------------------------------------------------

results = conversion_rate(df)

uplift = calculate_uplift(results)

test_results = z_test(results)

daily_df = daily_conversion(df)


# Conversiones

control_cvr = results.loc["control", "conversion_rate"]

treatment_cvr = results.loc["treatment", "conversion_rate"]


# Métricas del test estadístico

significant = test_results["significant"]


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Control conversion",
        f"{control_cvr:.1%}"
    )


with col2:
    st.metric(
        "Treatment conversion",
        f"{treatment_cvr:.1%}"
    )


with col3:
    st.metric(
        "Uplift",
        f"{uplift:.1%}"
    )



# ---------------------------------------------------------
# RESULTADOS DEL EXPERIMENTO
# ---------------------------------------------------------

st.subheader("Resultado del experimento")

significance_label = (
    "ESTADÍSTICAMENTE SIGNIFICATIVO"
    if significant
    else "NO ESTADÍSTICAMENTE SIGNIFICATIVO"
)

st.metric(
        "",
        significance_label
    )


# ---------------------------------------------------------
# CONCLUSIÓN
# ---------------------------------------------------------

if significant:

    st.success(
        "El grupo de tratamiento o variante muestra diferencias "
        "estadísticamente significativas en conversion rate "
        "comparado con el grupo de control."
    )

else:

    st.info(
        "El experimento no muestra una diferencia estadísticamente "
        "significativa en conversion rate."
    )



# ---------------------------------------------------------
# RESUMEN DEL EXPERIMENTO
# ---------------------------------------------------------

st.subheader("Seguimiento de Muestra y Conversion Rate")

col1, col2 = st.columns(2)


# Tamaño de muestra acumulado

with col1:

    fig_sample = cumulative_sample_size(df)

    st.plotly_chart(
        fig_sample,
        width="stretch"
    )


# Conversion rate final

with col2:

    fig_conversion = conversion_bar(results)

    st.plotly_chart(
        fig_conversion,
        width="stretch"
    )


# ---------------------------------------------------------
# CONVERSIÓN A LO LARGO DEL TIEMPO
# ---------------------------------------------------------

st.subheader("Evolución del Conversion Rate")

fig_daily = daily_conversion_chart(daily_df)

st.plotly_chart(
    fig_daily,
    width="stretch"
)