from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch,helpers
from datetime import datetime

import time
import datetime
import os,sys
import json
import requests
from typing import List
from fastapi import FastAPI, Depends,Query
from pydantic import BaseModel, Field
from datetime import datetime
import os
import sys
import timestamp
from datetime import timedelta
from version.v0 import vo_main

es=Elasticsearch(['http://168.119.224.222:32072'])

app = FastAPI(
    title="ProvEdge Cloud Robotics API - Metrics",
    description="Backend service for DevOps features of Cloud Robotics Simulation Platform written in Python, using FastAPI.",
    version="0.0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    vo_main.router,
    prefix="/api/v0",
    #responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {
        "status": "SUCCESS",
        "message": "Welcome, It's ProvEdge Cloud Robotics API - DevOps.",
        "quote": {
            "quote": "If I had asked people what they wanted, they would have said faster horses.",
            "owner": "Henry Ford"
        }
    }