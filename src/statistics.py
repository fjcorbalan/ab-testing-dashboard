#importando LIBRERÍAS necesarias de python

import pandas as pd
import numpy as np
from scipy.stats import norm



#FUNCIÓN CONVERSION RATE: suma de conversiones dividido entre el conteo de usuarios

def conversion_rate(df):

    results = (
        df.groupby("con_treat")
          .agg(
              users=("user_id", "count"),
              conversions=("converted", "sum")
          )
    )

    results["conversion_rate"] = (
        results["conversions"] /
        results["users"]
    )

    return results



#FUNCIÓN CALCULATE UPLIFT: de momento sin test estadístico, solo diferencia entre control y treatment, a partir de los results de la funcion conversion_rate

def calculate_uplift(results):

    control = results.loc["control", "conversion_rate"]

    treatment = results.loc["treatment", "conversion_rate"]

    uplift = (treatment - control) / control

    return uplift



#FUNCIÓN Z-TEST: Aquí sí realizamos el test estadístico (z-test), también a partir de los results de la funciónconversion_rate

def z_test(results):

    c_users = results.loc["control", "users"]
    t_users = results.loc["treatment", "users"]

    c_conv = results.loc["control", "conversions"]
    t_conv = results.loc["treatment", "conversions"]

    p1 = c_conv / c_users
    p2 = t_conv / t_users

    pooled = (c_conv + t_conv) / (c_users + t_users) #calculando la conversion total

    se = np.sqrt(  #standard error o diferencia aleatoria esperada
        pooled *
        (1 - pooled) *
        (
            1 / c_users +
            1 / t_users
        )
    )

    z = (p2 - p1) / se #puntuación z: diferencia observada/diferencia aleatoria esperada

    p_value = 2 * (1 - norm.cdf(abs(z)))

    return {
    "z_score": z,
    "p_value": p_value,
    "alpha": 0.05,
    "significant": p_value < 0.05
    }




#CONVERSIÓN DIARIA

def daily_conversion(df):

    daily = (
        df
        .groupby(
            [
                "observation_date",
                "con_treat"
            ]
        )
        .agg(
            users=("user_id", "count"),
            conversions=("converted", "sum")
        )
        .reset_index()
    )

    daily["conversion_rate"] = (

        daily["conversions"]

        /

        daily["users"]

    )

    return daily