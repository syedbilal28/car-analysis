import pandas as pd
import re
df=[]
files=[]
import os 
directory=os.path.join("C://","Users/Bilal/PycharmProjects/car-analysis")
for root,dirs,files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            df.append(pd.read_csv(file,error_bad_lines=False))
            
l=len(df)
for i in range(l):
    df[i]=df[i][["Make","Model","Year","Views","Days Online"]]
aggregate_functions={"Views":'sum','Days Online':'sum'}
clean_df=[i for i in range(l)]
for i in range(l):
    clean_df[i]=df[i].dropna()
    for index,row in clean_df[i].iterrows():
        
        row["Days Online"]=row["Days Online"].strip()
        if row["Days Online"][-4:]=="hour" or row["Days Online"][-5:]=="hours":
            num=eval(re.sub('[^0-9]','', row["Days Online"]))/24
            row["Days Online"]=num
        elif row["Days Online"][-4:]=="mins" or row["Days Online"][-3:]=="min":
            num=eval(re.sub('[^0-9]','', row["Days Online"]))/(60*24)
            row["Days Online"]= num
        elif row["Days Online"][-3:]=="day" or row["Days Online"][-4:]=="days":
            num=eval(re.sub('[^0-9]','', row["Days Online"]))
            row["Days Online"]= num
    
            
        
        row["Views"]=row["Views"].replace(r',','')
        row["Views"]=eval(row["Views"])
        if row['Days Online']<1:
            row['Days Online']=1
    clean_df[i]=clean_df[i].groupby(["Model","Make","Year"],as_index=False,sort=False).aggregate(aggregate_functions)
    clean_df[i]['Views Per Day']=clean_df[i]["Views"]/clean_df[i]['Days Online']
    clean_df[i]["Views Per Day"]=clean_df[i]["Views Per Day"].astype(float)
    clean_df[i]=clean_df[i].sort_values(by=["Views"],ascending=False)

for i in range(1,l):
    clean_df[i]=clean_df[i].rename(columns={'Views Per Day':'Views Per Day {}'.format(i)})
final_df=[clean_df[0]]
for i in range(1,l-1):
    print(i)
    final_df.append(pd.merge(final_df[i-1],clean_df[i],how="inner",on=['Model','Make','Year']))
    final_df[i]['Views']=final_df[i]["Views_x"]+final_df[i]["Views_y"]
    final_df[i]['Days Online']=final_df[i]["Days Online_x"]+final_df[i]["Days Online_y"]
    final_df[i].drop(["Views_x","Views_y","Days Online_x","Days Online_y"],axis =1,inplace= True)