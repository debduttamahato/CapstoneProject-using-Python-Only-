import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/n01PQ9pSmiRX6520flujwQ/survey-data.csv"
df = pd.read_csv(file_url)


#Identify High Compensation Outliers
meanval=df['ConvertedCompYearly'].mean()
medianval=df['ConvertedCompYearly'].median()
standarval=df['ConvertedCompYearly'].std()
threshold=meanval+3*standarval
df1=df[df['ConvertedCompYearly']>threshold]
df1.shape[0]

#Detect Outliers in Compensation
Q1 = df['ConvertedCompYearly'].quantile(0.25)
Q3 = df['ConvertedCompYearly'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['ConvertedCompYearly'] < lower_bound) | (df['ConvertedCompYearly'] > upper_bound)]
num_outliers = outliers.shape[0]
plt.figure(figsize=(10, 5))
sns.boxplot(x='Industry',y='ConvertedCompYearly', color='skyblue',data=df)
plt.title('Boxplot of ConvertedCompYearly (with Outliers)')
plt.xlabel('Converted Compensation Yearly')
plt.xticks(rotation=45, ha='right')
plt.ylim(0.0,1000000)
plt.show()

#Remove Outliers and Create a New DataFrame
not_outliers = df[(df['ConvertedCompYearly'] > lower_bound) | (df['ConvertedCompYearly'] < upper_bound)]
num_outliers = not_outliers.shape[0]
print(num_outliers)

#Correlation Analysis
dic={'Under 18 years old':'17','35-44 years old':'39.5','45-54 years old':'49.5','18-24 years old':'21','25-34 years old':'29.5','55-64 years old':'59.5','65 years or older':'66'}
df['Age1']=df['Age'].map(dic)
df['Age1']=df['Age1'].astype(float)
lists=[]
for item in df.columns:
    if df[item].dtype=='int64' or df[item].dtype=='float64':
        lists.append(item)
lists.append('Age1')
df[lists].corr()


