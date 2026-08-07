from src.database import run_query
from src.statistics import (
    conversion_rate,
    calculate_uplift,
    z_test
)

query = """

SELECT *

FROM experiment;

"""

df = run_query(query)

print(df.head())


results = conversion_rate(df)

print(results)

print()

print("Uplift")

print(calculate_uplift(results))

print()

print("Z test")

test_results = z_test(results)

print(f"Z-score: {test_results['z_score']:.3f}")
print(f"P-value: {test_results['p_value']:.6f}")
print(f"Alpha: {test_results['alpha']}")
print(f"Significant: {test_results['significant']}")

