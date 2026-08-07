#Crea data/ab_testing.db desde el archivo csv


import sqlite3
import pandas as pd

# ----------------------------
# Configuración
# ----------------------------

CSV_PATH = "data/ab_testing_teaching_dataset_chatgpt.csv" #donde tenemos nuestro archivo csv
DB_PATH = "data/ab_testing.db" #donde irá nuestra base de datos creada a partir del csv

TABLE_NAME = "experiment" #nombre de la tabla SQL

# ----------------------------
# Load CSV
# ----------------------------

df = pd.read_csv(CSV_PATH, sep=";") #sep indica el separador de columnas del archivo csv, por defecto es ","

print("Columns found:")
print(df.columns.tolist())

print(f"\nRows loaded: {len(df)}")

print("CSV loaded successfully.")
print(df.head())

# ----------------------------
# Crear base de datos SQLite
# ----------------------------

conn = sqlite3.connect(DB_PATH)

# ----------------------------
# Escribiendo dataframe en SQLite
# ----------------------------

df.to_sql(
    TABLE_NAME,
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print(f"Database created successfully!")
print(f"Table '{TABLE_NAME}' contains {len(df)} rows.")

#HACER UN RUN DE ESTE ARCHIVO PARA CREAR ab_testing.db EN LA CARPETA data
