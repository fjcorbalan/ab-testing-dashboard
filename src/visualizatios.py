import plotly.express as px

#CONVERSIÓN DIARIA: evolución del experimento por día de observación

def daily_conversion_chart(daily_df): #dayly_df vendrá de la función statistics/daily_conversion(df)

    fig = px.line(
        daily_df,
        x="observation_date",
        y="conversion_rate",
        color="con_treat",
        markers=True,
        title="Daily Conversion Rate"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Conversion Rate",
        template="plotly_white"
    )

    return fig

#TAMAÑO DE MUESTRA ACUMULADO: número de usuarios por día de observación

def cumulative_sample_size(df): 

    cumulative = (
        df.groupby(
            ["observation_date", "con_treat"]
        )
        .size()
        .reset_index(name="users")
    )

    cumulative["cumulative_users"] = (
        cumulative
        .groupby("con_treat")["users"]
        .cumsum()
    )

    fig = px.line(
        cumulative,
        x="observation_date",
        y="cumulative_users",
        color="con_treat",
        title="Cumulative Sample Size"
    )

    fig.update_layout(template="plotly_white")

    return fig


#CONVERSIÓN POR GRUPO: resumen final

def conversion_bar(results): #results vendrá de la función src/conversion_rate(df)

    chart = results.reset_index()

    fig = px.bar(
        chart,
        x="con_treat",
        y="conversion_rate",
        color="con_treat",
        title="Conversion Rate by Group",
        text="conversion_rate"
    )

    fig.update_traces(texttemplate="%{text:.2%}")

    fig.update_layout(
        template="plotly_white",
        showlegend=False
    )

    return fig