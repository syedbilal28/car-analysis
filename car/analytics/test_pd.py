import pandas as pd
import re
from sqlalchemy import create_engine
import os
import pathlib
from . import creator
def set_Views():
    engine=create_engine("sqlite:///"+"C:/Users/Bilal/PycharmProjects/car-analysis/car/db.sqlite3")
    
    cwd=str(os.getcwd())
    df=pd.read_csv(cwd+'/file1.csv',error_bad_lines=False)
    df= df[["Make","Model","Year","Views","Days Online"]]
    clean_df=df.dropna()
    df= pd.read_sql_query(sql="SELECT * from Car",con=engine)
    df=df.drop('index',axis=1)
    l=len(df.keys())-5
    for index,row in clean_df.iterrows():
        
        row["Days Online"]=row["Days Online"].strip()
        if row["Days Online"][-4:]=="hour" or row["Days Online"][-5:]=="hours":
            num=eval(re.sub('\D','', row["Days Online"]))/24    
            clean_df.at[index,'Days Online']=num
        elif row["Days Online"][-4:]=="mins" or row["Days Online"][-3:]=="min":
            num=eval(re.sub('\D','', row["Days Online"]))/(60*24)
            clean_df.at[index,'Days Online']=num
        elif row["Days Online"][-3:]=="day" or row["Days Online"][-4:]=="days":
            num=eval(re.sub('\D','', row["Days Online"]))
            clean_df.at[index,'Days Online']=num

        new=row["Views"].replace(r',','')
        clean_df.at[index,'Views']=eval(new)
    clean_df["Views"]=clean_df["Views"].astype(int)
    clean_df["Days Online"]=clean_df["Days Online"].astype(float)
    aggregate_functions={"Views":'sum','Days Online':'mean'}
    clean_df=clean_df.groupby(["Model","Make","Year"],as_index=False,sort=False).aggregate(aggregate_functions)
    clean_df["Year"]=clean_df["Year"].astype(object)
    to_process=clean_df
    clean_df['Views Per Day']=clean_df["Views"]/clean_df['Days Online']
    clean_df["Views Per Day"]=clean_df["Views Per Day"].astype(float)
    clean_df=clean_df.sort_values(by=["Views"],ascending=False)
    clean_df=clean_df.rename(columns={'Views Per Day':'Views Per Day {}'.format(l)})
    # df= pd.read_sql_query(sql="SELECT * from Car",con=engine)
    # df=df.drop('index',axis=1)
    final_df=pd.merge(clean_df,df,how="outer",on=["Model","Make",'Year'])
    to_cal=get_fill_value(final_df)
    final_df=final_df.fillna(value=to_cal)
    cols= list(final_df.filter(like='Views'))
    aggregate_functions={}
    for i in cols:
        if i[0:5]=="Views":
            aggregate_functions[i]='sum'
        elif i[0:4]=="Days":
            aggregate_functions[i]='sum'
            

    final_df=final_df.groupby(["Model","Make","Year"],as_index=False,sort=False).aggregate(aggregate_functions)
    final_df["Views"]=((final_df["Views_x"]+final_df["Views_y"])*l).div(l+1)
    #final_df["Days Online"]=((final_df["Days Online_x"]+final_df["Days Online_y"])*l).div(l+1)
    final_df=final_df.drop(['Views_x','Views_y'],axis=1)
    final_df=final_df.sort_values(by="Views",ascending=False)
    engine.execute("DROP TABLE Car")
    final_df.to_sql(con=engine,name="Cars")
    return to_process
def Set_Days_Online(clean_df):
    
    engine=create_engine("sqlite:///"+"C:/Users/Bilal/PycharmProjects/car-analysis/car/db.sqlite3")
    df= pd.read_sql_query(sql="SELECT * from Car_Days",con=engine)
    df=df.drop('index',axis=1)
    l=len(df.keys())-4
    clean_df = clean_df[["Model", "Make", "Year", "Days Online"]]
    clean_df = clean_df.rename(columns={'Days Online': 'Days Online {}'.format(l)})
    final_df=pd.merge(clean_df,df, how="outer", on=['Model', 'Make', 'Year'])
    to_cal=get_fill_value(final_df)
    final_df=final_df.fillna(value=to_cal)
    aggregate_functions={}
    cols=final_df.filter(like="Days")
    for i in cols:
        if i [0:4]=="Days":
            aggregate_functions[i]='sum'
    final_df=final_df.groupby(["Model","Make","Year"],as_index=False,sort=False).aggregate(aggregate_functions)
    
    final_df['Average Days Online']=0
    final_df['Average Days Online']=(final_df.filter(like="Days").sum(axis=1)).div(l+1)
    final_df=final_df.sort_values(by="Average Days Online")
    engine.execute("DROP TABLE Car_Days")
    final_df.to_sql(con=engine,name="Car_Days")

def get_fill_value(df):
    to_cal={}
    for i in df.columns:
        if i[0:5]=="Views":
            to_cal[i]=0
        elif i[0:4]=="Days":
            to_cal[i]=0
    return to_cal
