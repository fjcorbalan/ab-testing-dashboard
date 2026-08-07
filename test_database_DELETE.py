from src.database import run_query


query = """

SELECT *

FROM experiment

LIMIT 10;

"""


df = run_query(query)

print(df)