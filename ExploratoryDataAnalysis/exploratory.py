import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
data_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/n01PQ9pSmiRX6520flujwQ/survey-data.csv'
df = pd.read_csv(data_url)
# Set pandas option to display all columns
pd.set_option('display.max_columns', None)


#handling missing data
df['Employment']=df['Employment'].replace(np.nan,df['Employment'].value_counts().idxmax())
df['JobSat']=df['JobSat'].replace(np.nan,df['JobSat'].mean())
df['RemoteWork']=df['RemoteWork'].replace(np.nan,df['RemoteWork'].value_counts().idxmax())
df['RemoteWork'].unique()
df['JobSat'].unique()


#Analysis of Experience and Job Satisfaction
dic={'Less than 1 year':'1','More than 50 years':'51'}
df['YearsCodePro']=df['YearsCodePro'].map(dic).fillna(df['YearsCodePro'])
df['YearsCodePro']=df['YearsCodePro'].fillna(0)
df['YearsCodePro'].unique()
df['YearsCodePro']=df['YearsCodePro'].astype(int)
bins=[0,10,30,df['YearsCodePro'].max()]
groups=["Junior","Senior","Elite"]
df['YearsCodePro_binned']=pd.cut(df['YearsCodePro'],bins,labels=groups,include_lowest=True)
df_dr_jobset = df.groupby('YearsCodePro_binned')['JobSat'].mean()
df_dr_jobset.plot(kind='bar')
plt.title('Relationship between job sat and experience')
plt.xlabel("Experience Level")
plt.ylabel("Job Satisfaction Index")
plt.show()


#Visualize Job Satisfaction
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='JobSat', order=df['JobSat'].value_counts().index)
# Add labels and title
plt.xlabel('Job Satisfaction')
plt.ylabel('Count')
plt.title('Distribution of Job Satisfaction')
# Rotate x-axis labels if necessary
plt.xticks(rotation=45)
# Show the plot
plt.tight_layout()
plt.show()


#Educational Background and Employment Type
ct = pd.crosstab(df['EdLevel_Simple'],df['Employment'])
ct.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab20')

plt.title('Employment Type by Education Level')
plt.xlabel('Education Level')
plt.ylabel('Proportion')
plt.legend(title='Employment Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#finding how data is distributed

#focus on jobsat
df['JobSat'].value_counts()
bins=np.linspace(df['JobSat'].min(),df['JobSat'].max(),6)
group=["Very dissatisfied","Dissatisfied","Neutral","Satisfied","Very satisfied"]
df["jobsat_binned"]=pd.cut(df['JobSat'],bins,labels=group,include_lowest=True)
job_sat_counts = df['jobsat_binned'].value_counts()
labels = job_sat_counts.index
sizes = job_sat_counts.values
plt.figure(figsize=(8, 6))
wedges, texts, autotexts = plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Paired.colors
)
plt.title('Job Satisfaction Distribution')
plt.axis('equal')  # Keeps the pie circular
plt.legend(wedges, labels, title="JobSat Levels", loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()

#Programming Languages Analysis
worked = df['LanguageHaveWorkedWith'].dropna()
want = df['LanguageWantToWorkWith'].dropna()
# Split by semicolon and flatten the lists
worked_languages = [lang.strip() for row in worked for lang in row.split(';')]
want_languages = [lang.strip() for row in want for lang in row.split(';')]
# Count frequencies
worked_counter = Counter(worked_languages)
want_counter = Counter(want_languages)
# Convert to sets for Venn
worked_set = set(worked_languages)
want_set = set(want_languages)
# Create Venn diagram
plt.figure(figsize=(8, 6))
venn2([worked_set, want_set], set_labels=('Have Worked With', 'Want To Work With'))
plt.title('Overlap of Programming Languages')
plt.show()

#Correlation between Job Satisfaction and Experience
from scipy.stats import pearsonr
dic={'Less than 1 year':'1','More than 50 years':'51'}
df['YearsCodePro']=df['YearsCodePro'].map(dic).fillna(df['YearsCodePro'])
df['YearsCodePro']=df['YearsCodePro'].fillna(0)
df['YearsCodePro']=df['YearsCodePro'].astype(int)
pearson_coef,p_value=pearsonr(df['JobSat'],df['YearsCodePro'])
print(pearson_coef)
print(p_value)

#Cross-tabulation Analysis (Employment vs. Education Level)
pd.crosstab(df['Employment'],df['EdLevel'])