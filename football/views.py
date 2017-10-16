from django.shortcuts import render
from django.http import HttpResponse
from .backend.database import DBAdapter
# Create your views here.

def index(request):
    db = DBAdapter()
    summaries_sd = db.get_all_summary()
    summaries = []

    for i in range(len(summaries_sd)):
        response = {'id': summaries_sd[i][0]}
        response['summary'+str(i)] = []
        response['summary'+str(i)].append(summaries_sd[i][1])
        response['summary'+str(i)].append(summaries_sd[i][2])
        summaries.append(response)


    return render(request, 'index.html', {'summaries': summaries })
