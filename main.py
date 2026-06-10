import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# CONNECT TO MYSQL
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2003",
    database="hr_data"
)

print("Connected Successfully!")

# ==========================================
# LOAD DATA
# ==========================================

query = "SELECT * FROM employee_attrition"

df = pd.read_sql(query, conn)
print(df.columns.tolist())

# Clean column names
df.columns = df.columns.str.strip()

print("\nColumns Available:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

# ==========================================
# DATASET INFORMATION
# ==========================================

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())

# ==========================================
# DATA CLEANING
# ==========================================

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

df = df.drop_duplicates()

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_employees = len(df)

employees_left = len(
    df[df['Attrition'] == 'Yes']
)

attrition_rate = round(
    (employees_left / total_employees) * 100,
    2
)

avg_salary = round(
    df['MonthlyIncome'].mean(),
    2
)

avg_years = round(
    df['YearsAtCompany'].mean(),
    2
)

print("\n==============================")
print("KPI SUMMARY")
print("==============================")
print("Total Employees :", total_employees)
print("Employees Left  :", employees_left)
print("Attrition Rate  :", attrition_rate, "%")
print("Average Salary  :", avg_salary)
print("Average Years at Company :", avg_years)

# ==========================================
# DEPARTMENT ATTRITION
# ==========================================

dept_attrition = (
    df.groupby('Department')['Attrition']
    .apply(lambda x: (x == 'Yes').sum())
    .sort_values(ascending=False)
)

print("\nDepartment-wise Attrition:")
print(dept_attrition)

# ==========================================
# JOB ROLE ATTRITION
# ==========================================

job_attrition = (
    df.groupby('JobRole')['Attrition']
    .apply(lambda x: (x == 'Yes').sum())
    .sort_values(ascending=False)
)

print("\nJob Role Attrition:")
print(job_attrition)

# ==========================================
# GENDER ATTRITION
# ==========================================

gender_attrition = pd.crosstab(
    df['Gender'],
    df['Attrition']
)

print("\nGender Attrition:")
print(gender_attrition)

# ==========================================
# OVERTIME ATTRITION
# ==========================================

overtime_attrition = pd.crosstab(
    df['OverTime'],
    df['Attrition']
)

print("\nOvertime Attrition:")
print(overtime_attrition)

# ==========================================
# AGE GROUP ANALYSIS
# ==========================================

if 'Age' in df.columns:

    df['AgeGroup'] = pd.cut(
        df['Age'],
        bins=[18,25,35,45,55,65],
        labels=['18-25','26-35','36-45','46-55','56-65']
    )

    age_attrition = pd.crosstab(
        df['AgeGroup'],
        df['Attrition']
    )

    print(age_attrition)

    age_attrition.plot(kind='bar')
    plt.title('Age Group Attrition')
    plt.show()

else:
    print("Age column not found in database table.")

# ==========================================
# SALARY GROUP ANALYSIS
# ==========================================

df['SalaryGroup'] = pd.cut(
    df['MonthlyIncome'],
    bins=[0, 5000, 10000, 20000],
    labels=[
        'Low',
        'Medium',
        'High'
    ]
)

salary_group_attrition = pd.crosstab(
    df['SalaryGroup'],
    df['Attrition']
)

print("\nSalary Group Attrition:")
print(salary_group_attrition)

# ==========================================
# VISUALIZATION 1
# Department Attrition
# ==========================================

plt.figure(figsize=(8,5))

dept_attrition.plot(kind='bar')

plt.title('Department Wise Attrition')
plt.xlabel('Department')
plt.ylabel('Attrition Count')

plt.tight_layout()
plt.show()

# ==========================================
# VISUALIZATION 2
# Job Role Attrition
# ==========================================

plt.figure(figsize=(10,5))

job_attrition.plot(kind='bar')

plt.title('Job Role Attrition')
plt.xlabel('Job Role')
plt.ylabel('Attrition Count')

plt.tight_layout()
plt.show()

# ==========================================
# VISUALIZATION 3
# Gender Attrition
# ==========================================

gender_attrition.plot(
    kind='bar',
    figsize=(6,5)
)

plt.title('Gender Wise Attrition')
plt.xlabel('Gender')
plt.ylabel('Employee Count')

plt.tight_layout()
plt.show()

# ==========================================
# VISUALIZATION 4
# Overtime Attrition
# ==========================================

overtime_attrition.plot(
    kind='bar',
    figsize=(6,5)
)

plt.title('Overtime vs Attrition')
plt.xlabel('OverTime')
plt.ylabel('Employee Count')

plt.tight_layout()
plt.show()

# ==========================================
# VISUALIZATION 5
# Age Group Attrition
# ==========================================

age_attrition.plot(
    kind='bar',
    figsize=(8,5)
)

plt.title('Age Group Attrition')
plt.xlabel('Age Group')
plt.ylabel('Employee Count')

plt.tight_layout()
plt.show()

# ==========================================
# VISUALIZATION 6
# Salary Distribution
# ==========================================

plt.figure(figsize=(8,5))

plt.hist(
    df['MonthlyIncome'],
    bins=20
)

plt.title('Salary Distribution')
plt.xlabel('Monthly Income')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# ==========================================
# VISUALIZATION 7
# Salary Group Attrition
# ==========================================

salary_group_attrition.plot(
    kind='bar',
    figsize=(8,5)
)

plt.title('Salary Group Attrition')
plt.xlabel('Salary Group')
plt.ylabel('Employee Count')

plt.tight_layout()
plt.show()

# ==========================================
# EXPORT DATA
# ==========================================

df.to_csv(
    "employee_attrition_analysis.csv",
    index=False
)

print("\nCSV Exported Successfully!")

# ==========================================
# CLOSE CONNECTION
# ==========================================

conn.close()

print("Database Connection Closed!")