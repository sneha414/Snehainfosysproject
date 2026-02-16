print("Program started")

import pandas as pd
import dask.dataframe as dd
from faker import Faker
import random

fake = Faker()


rows = 1000   
departments = ["HR", "IT", "Sales", "Finance", "Marketing"]

data = []

for i in range(rows):

    # progress indicator
    if i % 200 == 0:
        print(f"Generating row: {i}")

    data.append([
        i,
        fake.name(),
        random.randint(21, 60),
        random.randint(30000, 120000),
        random.choice(departments)
    ])


df = pd.DataFrame(
    data,
    columns=["id", "name", "age", "salary", "department"]
)


csv_file = "employees.csv"
df.to_csv(csv_file, index=False)

print("\nCSV file created!")


dask_df = dd.read_csv(csv_file)


print("First 10 rows:")
print(dask_df.head(10))

print("Number of partitions:")
print(dask_df.npartitions)


# print("\n✅ Program completed successfully!")
