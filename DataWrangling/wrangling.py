#finding duplicate
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
file_path = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/VYPrOu0Vs3I0hKLLjiPGrA/survey-data-with-duplicate.csv"
df = pd.read_csv(file_path)


#identify duplicate row
num=df.duplicated().sum()
df_dup=df[df.duplicated()]


#Analyze Characteristics of Duplicates
duplicate_rows=df[df.duplicated(subset=['MainBranch', 'Employment', 'RemoteWork'],keep=False)]
#duplicate_rows.head()
# Group duplicates
grouped = duplicate_rows.groupby(['MainBranch', 'Employment', 'RemoteWork'])
# Count identical values across groups for each column
identical_counts = Counter()
for _, group in grouped:
    for col in df.columns:
        if col in ['MainBranch', 'Employment', 'RemoteWork']:
            continue
        if group[col].nunique(dropna=False) == 1:
            identical_counts[col] += 1
for col, count in identical_counts.most_common():
    print(f"{col}: {count} groups have identical values")


#removing duplicate
df_cleaned = df.drop_duplicates()


#handling missing values
missing_values = df_cleaned.isnull().sum()
print("Missing values per column:\n", missing_values)
common=df_cleaned['EdLevel'].value_counts().idxmax()
df_cleaned['EdLevel']=df_cleaned['EdLevel'].replace(np.nan,common)

#Normalization
#print(df_cleaned['ConvertedCompYearly'].dtype)
mean=df_cleaned['ConvertedCompYearly'].mean()
df_cleaned['ConvertedCompYearly']=df_cleaned['ConvertedCompYearly'].replace(np.nan,mean)
missing_converted = df_cleaned['ConvertedCompYearly'].isnull().sum()
df['ConvertedCompYearly_MinMax']=(df['ConvertedCompYearly']-df['ConvertedCompYearly'].min())/(df['ConvertedCompYearly'].max()-df['ConvertedCompYearly'].min())
df['ConvertedCompYearly_Zscore']=(df['ConvertedCompYearly']-df['ConvertedCompYearly'].mean())/df['ConvertedCompYearly'].std()



#finding and handling missing values
missing=df_cleaned.isnull().sum()
df=df_cleaned.copy()
df['RemoteWork']=df['RemoteWork'].replace(np.nan,common)
df['ConvertedCompYearly']=df['ConvertedCompYearly'].replace(np.nan,df['ConvertedCompYearly'].mean())
common=df['RemoteWork'].value_counts().idxmax()
df['RemoteWork']=df['RemoteWork'].replace(np.nan,common)
df['CodingActivities']=df['CodingActivities'].fillna(method='ffill')


#feature engineering
df['YearsCodePro']=df['YearsCodePro'].astype(int)
bins=np.linspace(df['YearsCodePro'].min(),df['YearsCodePro'].max(),4)
groups=["Begginer","Professional","Pro"]
df['ExperienceLevel']=pd.cut(df['YearsCodePro'],bins,labels=groups,include_lowest=True)
df['ExperienceLevel'].unique()