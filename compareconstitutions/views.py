from django.shortcuts import render
from django.shortcuts import render_to_response
import pymongo
from pymongo import MongoClient
from django.core import serializers
from django.http import HttpResponse
import json

def index(request,):
    return render_to_response("compareconstitutions/index.html")

def proceso(request,):
    return render_to_response("compareconstitutions/proceso.html")

def map(request,):
    return render_to_response("compareconstitutions/map.html")

def directory(request,):
    return render_to_response("compareconstitutions/directory.html")

def projects(request,):
    return render_to_response("compareconstitutions/projects.html")


def aboutus(request,):
    return render_to_response("compareconstitutions/aboutus.html")

def compareconstitutions(request,):
    try:
        client = pymongo.MongoClient('ds033484.mongolab.com:33484')
        client["compare_constitutions"].authenticate('user', 'observatorio1', mechanism='SCRAM-SHA-1')
        db = client['compare_constitutions']
        collections = db.constitutions.find({},{"_id": 0})
        unique_tag = db.constitutions.distinct("keyword")
        unique_country = db.constitutions.distinct("codigo_pais")
        const_dict = {}
        i = 1
        for each in collections:
            const_dict[i] = each
            i=i+1
        print type(const_dict)
    except Exception as e:
        print e
    return render_to_response("compareconstitutions/compareconstitutions.html", 
        {"unique_tag":unique_tag,"unique_country":unique_country})



def get_new_data(request,*args,**kwards):
    id_ = request.GET['id'].split(",")
    keyword = request.GET["tag"].split(",")

    print id_
    print keyword
    print "test"
    client = pymongo.MongoClient('ds033484.mongolab.com:33484')

    client["compare_constitutions"].authenticate('user', 'observatorio1', mechanism='SCRAM-SHA-1')
    db = client['compare_constitutions']
    collections = db.constitutions.find({"$and": [{"keyword":{"$in":list(keyword)}},
                                                  {"codigo_pais":{"$in":list(id_)}}]},{"_id":0})
    const_dict = {}
    i = 1
    for each in collections:
        const_dict[i] = each
        i=i+1
    print "mongo query"
    print const_dict  
    return HttpResponse(json.dumps( const_dict ) )

