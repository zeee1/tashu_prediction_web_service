from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
#from models import tashuCrawler
from .models import tashuCrawler
import json
from datetime import datetime
import os

# Create your views here.
def index(request):
	return render(request, 'tashu/index.html',)

def tashuStatus(request):
	input_stationNum = request.GET['input_stationNum']
	with open('/home/minjiwon/Documents/tashu_crawler/tashu_crawler/crawl_data/test.json') as crnt_Data:
		oneday_feature_data = json.load(crnt_Data)

	context ={}
	context = oneday_feature_data['hour_'+str(datetime.now().hour)]
	context['input_stationNum'] = input_stationNum
	#context = {'temperature': '2.0', 'input_stationNum': '1', 'humidity': '56', 'rainfall': 0, 'snowfall': 0, 'hour': 11, 'month': 1, 'windspeed': '1.2', 'weekday': 2, 'season': '4'}

	#execute R prediction code
	os.system("Rscript /home/minjiwon/tashuPrediction/test.R")
	
	return render(request, 'tashu/tashuStatus.html',context)
