from src.database import run_query

from pathlib import Path



query_path = Path("sql/select_all.sql") #lugar donde tenemos nuestra query sql

query = query_path.read_text(encoding="utf-8")





df = run_query(query)

print(df)