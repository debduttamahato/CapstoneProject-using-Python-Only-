import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Histogram of ConvertedCompYearly
df1=df[df['ConvertedCompYearly']<df['ConvertedCompYearly'].quantile(0.95)]
df2=df1['ConvertedCompYearly'].dropna()
bins,bin_edes=np.histogram(df2)
df2.plot(kind='hist', bins=bin_edes, edgecolor='black')
plt.xlabel('ConvertedCompYearly')
plt.ylabel('frequency')
plt.xticks(bin_edes,rotation=45)
plt.show()
print(df['Age'].unique())


#Vertical Bar Chart of Top 5 Programming Languages Respondents Want to Work With
df1=df
df1['Language']=df1['LanguageWantToWorkWith'].str.split(';')
df_exp=df1.explode('Language')
df_exp['Language']=df_exp['Language'].str.strip()
df1=df_exp['Language'].value_counts().head(5)
sns.barplot(x=df1.index,y=df1.values,hue=df1.index,legend=True)
plt.xlabel('Languages')
plt.ylabel('Frequency')
#plt.yticks(sorted(df.values))
#plt.tight_layout()
plt.legend(title='Languages', bbox_to_anchor=(1.05, 1), loc='upper left')  # Moves legend outside
plt.show()


#Bar Chart of Respondent Count by Country
df1=df['Country'].value_counts().head(5)
sns.barplot(x=df1.index,y=df1.values,hue=df1.index,legend=True)
plt.xlabel('Countries')
plt.ylabel('Frequency')
plt.xticks([])
#plt.tight_layout()
plt.legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')  # Moves legend outside
plt.show()


#Line Chart of Median ConvertedCompYearly by Age Group
dic={
    'Under 18 years old': 17,
    '18-24 years old': 21,
    '25-34 years old': 29.5,
    '35-44 years old': 39.5,
    '45-54 years old': 49.5,
    '55-64 years old': 59.5,
    '65 years or older': 66
}
df['Age1'] = df['Age'].map(dic)
df1=df[df['ConvertedCompYearly']<df['ConvertedCompYearly'].quantile(0.95)]
df1=df1[['Age1','ConvertedCompYearly']].dropna()
grouped=df1.groupby('Age1')['ConvertedCompYearly'].mean()
plt.plot(grouped.index, grouped.values, marker='o', linestyle='-', color='blue', label='Sample Line')
plt.xlabel('Age')
plt.ylabel('ConvertedCompYearly')
plt.title('Line Chart of Median ConvertedCompYearly by Age Group')
plt.legend()
plt.grid(True)
plt.show()


#Line Chart of Job Satisfaction (JobSatPoints_6) by Experience Level
df1=df[['WorkExp','JobSatPoints_6']].dropna()
grouped=df1.groupby('WorkExp')['JobSatPoints_6'].mean()
plt.figure(figsize=(10, 6))  # Wider plot
plt.plot(grouped.index, grouped.values, marker='o', linestyle='-', color='blue', label='Sample Line')
plt.xlabel('WorkExp')
plt.ylabel('JobSatPoints_6')
#plt.xticks(grouped.index,rotation=45)
#plt.yticks(grouped.values,rotation=45)
plt.title('Line Chart of Median JobSatPoints_6 by WorkExp Group')
plt.legend()
plt.grid(True)
plt.show()


#Pie Chart of Respondents Most Admired Programming Languages
df_lang['Adlang']=df_lang['LanguageAdmired'].str.split(';')
df_explod=df_lang.explode('Adlang')
df_explod['Adlang']=df_explod['Adlang'].str.strip()
lang_stats=df_explod.groupby('Adlang')['Adlang'].count()
lang_head=lang_stats.head(5)
plt.pie(lang_head.values,labels=lang_head.index,autopct='%1.1f%%')
plt.show()


#Stacked Chart for Compensation and Job Satisfaction by Age Group
df1=df[df['ConvertedCompYearly']<df['ConvertedCompYearly'].quantile(0.95)]
grouped=df1.groupby('Age1')[['ConvertedCompYearly','JobSatPoints_6']].mean()
grouped['ConvertedCompYearly'] = (grouped['ConvertedCompYearly'] - grouped['ConvertedCompYearly'].min()) / (grouped['ConvertedCompYearly'].max() - grouped['ConvertedCompYearly'].min())
grouped['JobSatPoints_6'] = (grouped['JobSatPoints_6'] - grouped['JobSatPoints_6'].min()) / (grouped['JobSatPoints_6'].max() - grouped['JobSatPoints_6'].min())
grouped.plot(kind='bar', stacked=True, color=['#4c72b0', '#55a868'])
plt.title('Stacked Bar Chart of Compensation and Job Satisfaction')
plt.ylabel('Value')
plt.xticks(rotation=0)
plt.legend(['Yearly Compensation', 'Job Satisfaction Score'])
plt.tight_layout()
plt.show()


#Stacked Chart of Preferred Databases by Age Group
df1=df.copy()
df1['Data']=df1['DatabaseWantToWorkWith'].str.split(';')
df_explode=df1.explode('Data')
df_explode['Data']=df_explode['Data'].str.strip()
df2=df_explode['Data'].value_counts().head(5).index.tolist()
df3=df_explode[df_explode['Data'].isin(df2)]
df4=df3.groupby(['Age1','Data']).size().unstack(fill_value=0)
df4.plot(kind='bar', stacked=True)
plt.title('Stacked Bar Chart of Top DatabaseLang across diff age groups')
plt.ylabel('Value')
plt.xticks(rotation=0)
plt.legend()
plt.tight_layout()
plt.show()


#Stacked Chart of Employment Type by Job Satisfaction
df1 = df.copy()
df1['EmploymentList'] = df1['Employment'].str.split(';')
df_explode = df1.explode('EmploymentList')
df_explode['EmploymentList'] = df_explode['EmploymentList'].str.strip()
df_explode = df_explode.dropna(subset=['JobSatPoints_6'])
bins = [0, 20, 40, 60, 80, 100]
labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
df_explode['SatisfactionGroup'] = pd.cut(df_explode['JobSatPoints_6'], bins=bins, labels=labels, include_lowest=True)
grouped = df_explode.groupby(['SatisfactionGroup', 'EmploymentList'], observed=True).size().unstack(fill_value=0)
grouped.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set3')
plt.title('Distribution of Employment Types Across Job Satisfaction Levels (Binned)')
plt.xlabel('Job Satisfaction Level')
plt.ylabel('Proportion of Employment Types')
plt.xticks(rotation=0)
plt.legend(title='Employment Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()