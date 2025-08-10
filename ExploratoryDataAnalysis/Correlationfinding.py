import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/n01PQ9pSmiRX6520flujwQ/survey-data.csv"
df = pd.read_csv(file_url)

#Calculate Median Compensation for Full-Time Employees
df['Employment'] = df['Employment'].apply(lambda x: [lan.strip() for lan in x.split(';')] if pd.notnull(x) else [])
full_time_df = df[df['Employment'].apply(lambda x: 'Employed, full-time' in x)]
median_comp = full_time_df['ConvertedCompYearly'].median()
print("Median compensation for 'Employed, full-time.':", median_comp)

#Removing Outliers from the Dataset
q1=df['ConvertedCompYearly'].quantile(0.25)
q2=df['ConvertedCompYearly'].quantile(0.75)
iqr=q2-q1
lower_bound=q1-1.5*iqr
upper_bound=q2+1.5*iqr
df1=df[(df['ConvertedCompYearly']>lower_bound) | (df['ConvertedCompYearly']<upper_bound)]

#Finding Correlations Between Key Variables
data=df1[['ConvertedCompYearly','WorkExp','JobSatPoints_1']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(data, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix: Compensation, Work Experience, Job Satisfaction', fontsize=14)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Scatter Plot for Correlations
fig,axs=plt.subplots(1,2,sharey=True)
axs[0].scatter(df1['WorkExp'],df1['ConvertedCompYearly'])
axs[0].set_title('ConvertedCompYearly and WorkExp')
axs[0].set_xlabel('WorkExp')
axs[0].set_ylabel('ConvertedCompYearly')
axs[1].scatter(df1['JobSatPoints_1'],df1['ConvertedCompYearly'])
axs[1].set_title('ConvertedCompYearly and JobSatPoints_1')
axs[1].set_xlabel('JobSatPoints_1')
axs[1].set_ylabel('ConvertedCompYearly')
fig.tight_layout()
plt.show()
df1[['ConvertedCompYearly','WorkExp','JobSatPoints_1']].corr()