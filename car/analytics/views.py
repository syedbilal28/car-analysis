from django.shortcuts import render
from django.http import HttpResponse
from . import creator
import pandas as pd
from django.conf import settings
import os
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