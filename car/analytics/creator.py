from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings
import os
def Create_df():
    engine=create_engine("sqlite:///"+"C:/Users/Bilal/PycharmProjects/car-analysis/car/db.sqlite3")
    df= pd.read_sql_query(sql="SELECT * from Car",con=engine)
    lst1=['Model','Make','Year']
    lst2=[col for col in df if col.startswith('Views')]
    lst3=[col for col in df if col.startswith("Days")]
    columns=lst1+lst2+lst3
    print(df.columns)
    print(columns)
    clean_df=df[columns]
    return clean_df
def Create_df_Days():
    engine = create_engine("sqlite:///" + "C:/Users/Bilal/PycharmProjects/car-analysis/car/db.sqlite3")
    df = pd.read_sql_query(sql="SELECT * from Car_Days", con=engine)
    lst1 = ['Model', 'Make', 'Year']
    lst3 = list(df.filter(like="Days").columns)
    columns = lst1 + lst3
    clean_df=df[columns]
    return clean_df
def Plot(df,constraints):
    main = pd.DataFrame(df.loc[(df['Make'] == constraints[0]) & (df['Model'] == constraints[1]) & (df['Year'] == constraints[2])])
    columns=[col for col in df if col.startswith("Days")]
    main=main[columns]
    main=main.iloc[0]
    l=len(main)
    plt.figure(figsize=(9, 6))
    plt.plot(range(1,l+1),[i for i in main])
    plt.xlabel('Time')
    plt.ylabel('Days Online')
    plt.title("{} {} {}".format(constraints[0], constraints[1], constraints[2]))
    path = settings.MEDIA_ROOT + "/"
    plt.savefig(path+"Days Online.jpg")
def Plot_Views(df,constraints):
    main = pd.DataFrame(df.loc[(df['Make'] == constraints[0]) & (df['Model'] == constraints[1]) & (df['Year'] == constraints[2])])
    columns=[col for col in df if col.startswith("Views Per Day")]
    main = main[columns]
    main = main.iloc[0]
    l = len(main)
    plt.figure(figsize=(9, 6))
    plt.plot(range(1, l + 1), [i for i in main])
    plt.xlabel('Time')
    plt.ylabel('Views Per Day')
    plt.title("{} {} {}".format(constraints[0], constraints[1], constraints[2]))
    path = settings.MEDIA_ROOT+"/"

    plt.savefig(path+"Views Per Day.jpg")
