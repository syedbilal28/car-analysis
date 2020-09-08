from django.shortcuts import render
from django.http import HttpResponse
from . import creator
from django.conf import settings
import os
import re
import pandas as pd
from sqlalchemy import create_engine

# Create your views here.
def index(request):
    df=creator.Create_df()
    table_1=pd.DataFrame(df["Make"]+[' ']+df["Model"]+[' ']+df["Year"])
    table_1["Views"]=df["Views"]
    table_1=table_1.sort_values(by=['Views'],ascending=False)
    table_1=str(table_1.to_html(justify="center",index=False,header=False))
    infile=open("analytics/templates/table_views.html",'w')
    infile.write(table_1)
    infile.close()
    table_2 = pd.DataFrame(df["Make"] +[" "]+ df["Model"]+[' ']+df["Year"])
    table_2["Days Online"]=df["Days Online"]
    table_2=table_2.sort_values(by=["Days Online"],ascending=True)
    table_2=str(table_2.to_html(justify="center",index=False,header=False))
    infile = open("analytics/templates/table_days.html", 'w')
    infile.write(table_2)
    infile.close()
    path=settings.MEDIA_ROOT
    img_list=os.listdir(path+"/")
    Days_image="http://127.0.0.1:8000/media/"+img_list[0]
    Views_image = "http://127.0.0.1:8000/media/" + img_list[1]
    context={'Views_Image':Views_image,'Days_Image':Days_image}
    return render(request,'index.html',context)
def search(request):
    constraints=request.POST['Container']
    print(constraints)
    print(request.session.keys())

    constraints=constraints.split(" ")
    df=creator.Create_df_Days()
    creator.Plot(df,constraints)
    df_1=creator.Create_df()
    creator.Plot_Views(df_1,constraints)
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + "/")
    Days_image = "http://127.0.0.1:8000/media/" + img_list[0]
    Views_image = "http://127.0.0.1:8000/media/" + img_list[1]
    context = {'Views_Image': Views_image, 'Days_Image': Days_image}
    return render(request,'index.html',context)
def csv(request,file):
    df1=creator.Create_df()
    l=len([col for col in df1 if col.startswith("Views Per Day")])
    file = file[["Make", "Model", "Year", "Views", "Days Online"]]
    clean_df=file.dropna()
    for index, row in clean_df.iterrows():
        row["Days Online"] = row["Days Online"].strip()
        if row["Days Online"][-4:] == "hour" or row["Days Online"][-5:] == "hours":
            num = eval(re.sub('\D', '', row["Days Online"])) / 24
            clean_df.at[index, 'Days Online'] = num
        elif row["Days Online"][-4:] == "mins" or row["Days Online"][-3:] == "min":
            num = eval(re.sub('\D', '', row["Days Online"])) / (60 * 24)
            clean_df.at[index, 'Days Online'] = num
        elif row["Days Online"][-3:] == "day" or row["Days Online"][-4:] == "days":
            num = eval(re.sub('\D', '', row["Days Online"]))
            clean_df.at[index, 'Days Online'] = num
        new = row["Views"].replace(r',', '')
        clean_df.at[index, 'Views'] = eval(new)
    clean_df["Days Online"] = clean_df["Days Online"].astype(float)
    aggregate_functions = {"Views": 'sum', 'Days Online': 'mean'}
    clean_df = clean_df.groupby(["Model", "Make", "Year"], as_index=False, sort=False).aggregate(aggregate_functions)
    clean_df["Year"] = clean_df["Year"].astype(object)
    clean_df['Views Per Day'] = clean_df["Views"] / clean_df['Days Online']
    clean_df["Views Per Day"] = clean_df["Views Per Day"].astype(float)
    clean_df = clean_df.sort_values(by=["Views"], ascending=False)
    clean_df = clean_df.rename(columns={'Views Per Day': 'Views Per Day {}'.format(l)})
    final_df=pd.merge(df1, clean_df, how="outer", on=['Model', 'Make', 'Year'])
    final_df = final_df.fillna(0)
    final_df['Views'] = final_df["Views_x"] + final_df["Views_y"]
    final_df['Days Online'] = final_df["Days Online_x"] + final_df["Days Online_y"]
    final_df.drop(["Views_x", "Views_y", "Days Online_x", "Days Online_y"], axis=1, inplace=True)
    final_df["Views"] = (final_df["Views"] *l)/l+1
    engine=create_engine(settings.BASE_DIR+"db.sqlite3")
    engine.execute("DROP TABLE Car")
    final_df.to_sql(con=engine, name="Car")
    df2 = creator.Create_df_Days()
    l = len([col for col in df2 if col.startswith("Days")])
    clean_df = clean_df[["Model", "Make", "Year", "Days Online"]]
    clean_df = clean_df.rename(columns={'Days Online': 'Days Online {}'.format(l)})
    final_df_Days=pd.merge(df2, clean_df, how="outer", on=['Model', 'Make', 'Year'])
    final_df_Days = final_df_Days.fillna(0)
    engine.execute("DROP TABLE Car_Days")
    final_df_Days.to_sql(con=engine, name="Car_Days")