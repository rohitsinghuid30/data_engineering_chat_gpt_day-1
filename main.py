import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME=os.getenv("USERNAME")
PASSWORD=os.getenv("PASSWORD")
DATABASE=os.getenv("DATABASE")
PORT=os.getenv("PORT")
HOST=os.getenv("HOST")

engine=create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

print("DB is Connected")


#2 EXTRACT

employee_df=pd.read_sql_query(
    "select * from employees",
    engine
)


department_df = pd.read_sql_query(
    "select * from departments",
    engine
)

print(employee_df)
print(department_df)


#3 VALIDATE
merged_df=employee_df.merge(
    department_df,
    on="department_id",
    how="left"
) 

print(merged_df)


#4 — Separate VALID and REJECTED records

valid_df=merged_df[
    merged_df["department_name"].notna()
].copy()


rejected_df=merged_df[
    merged_df["department_name"].isna()
].copy()

rejected_df['rejected_reason']="Invalid Department"

print("valid records")
print(valid_df)

print()
print("rejected records")
print(rejected_df)

print()

# Step 5 — TRANSFORM

# clean employee name
valid_df["name"]=(valid_df["name"].str.strip().str.title())

# Standarize department
valid_df['department_name']=(valid_df['department_name'].str.strip().str.lower())

print()
print("Transformed data")
print(valid_df)
print()

# Step 6 — Create the final dataset
final_df=valid_df[
    [
        "id",
        "name",
        "department_id",
        "department_name",
        "salary"
    ]
].copy()

print("FINAL DF")
# print(final_df)
print()

# Step 7 — LOAD

final_df.to_sql(
    "employee_clean",
    con=engine,
    if_exists="replace",
    index=False
)

# check df verify

check_df=pd.read_sql_query(
    "select * from employee_clean",
    engine
)

print(check_df)



rejected_df.to_csv("rejected_employee.csv", index=False)

rejected_df.to_sql("employee_rejected", con=engine, if_exists="replace", index=False)


check_rejected_df=pd.read_sql_query(
    "select * from employee_rejected",
    engine
)




print()
print(check_rejected_df)


