from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import creator
from django.conf import settings
import os
import re
import pandas as pd
from sqlalchemy import create_engine
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import requests
import pathlib
from . import test_pd
# Create your views here.
def index(request):
    df=creator.Create_df()
    table_1=pd.DataFrame(df["Make"]+[' ']+df["Model"]+[' ']+str(df["Year"]))
    table_1["Views"]=df["Views"]
    table_1=table_1.sort_values(by=['Views'],ascending=False)
    table_1=str(table_1.to_html(justify="center",index=False,header=False))
    infile=open("analytics/templates/table_views.html",'w')
    infile.write(table_1)
    infile.close()
    df1=creator.Create_df_Days()
    table_2 = pd.DataFrame(df1["Make"] +[" "]+ df1["Model"]+[' ']+str(df1["Year"]))
    table_2["Average Days Online"]=df1["Average Days Online"] 
    table_2=table_2.sort_values(by=["Average Days Online"],ascending=True)
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
@csrf_exempt
def csv(request):
    #file =request.POST['file']
    file=request.POST['link']
    r=requests.get(file)
    url_content=r.content
    csv_file=open('file1.csv','wb')
    csv_file.write(url_content)
    csv_file.close()
    Days_df= test_pd.set_Views()
    test_pd.Set_Days_Online(Days_df)
    return HttpResponse("Uploaded")