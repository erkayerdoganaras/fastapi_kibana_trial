from typing import Optional

from fastapi import APIRouter
from datetime import datetime
import time
from fastapi import FastAPI, Depends,Query
import timestamp
from datetime import timedelta
import requests
from elasticsearch import Elasticsearch,helpers

router = APIRouter()
es=Elasticsearch(['http://168.119.224.222:32072'])


@router.get("/all/paginated")
async def arama(*, er: int = Query(None)):
    try:
        liste1 = []
        if er != None:

            formula = (int(er) * 100 - 100)
        elif er == None:
            formula = 0

        query_body = {
            "from": formula,
            "size": 1000,
            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "_index": {
                                    "query": "logstash*"}

                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }

        liste = []
        res = es.search(body=query_body)
        data = res["hits"]["hits"]

        return {
            "status": "SUCCESS",
            "message": "DONDU",
            "data": data}


    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI" + str(e)
        }

@router.get("/number-queries")
async def log_num():
    try:
        liste1=[]
        query_body2 = {
        "query": {
            "bool": {
                "must":
                    {
                        "match_phrase": {
                            "_index": {
                                "query": "logstash*"}

                        }
                    },
                "filter": [
                    {
                        "match_all": {}
                    }
                ],
                "should": [],
                "must_not": []
            }
        }
    }

        res = es.count(body=query_body2)["count"]
        return {
                "status":"SUCCESS",
                "message":"DONDU",
                "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }