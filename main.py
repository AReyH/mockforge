from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from oydantic import BaseModel
from faker import Faker
import random
import json
import csv
import io
from typing import Optional, List, Any

app.FastAPI(title='MockForge')
app.mount('/static',StaticFiles(directory='static'),name='static')
templates = Jinja2Templates(directory='templates')
fake = Faker()

DATA_TYPES = {
    'string': {
        'label':'String/Text',
        'subtypes': {
            'full_name': {'label':'Full Name'},
            'first_name': {'label':'First Name'},
            'last_name': {'label':'Last Name'},
            'email': {'label':'Email'},
            'phone': {'label':'Phone'},
            'username': {'label':'Username'},
            'company': {'label':'Company'},
            'job': {'label':'Job'},
            'city': {'label':'City'},
            'country': {'label':'Country'},
            'address': {'label':'Address'},
            'url': {'label':'URL'},
            'ipv4': {'label':'IPv4 Address'},
            'uuid4': {'label':'UUID'},
            'color_name': {'label':'Color Name'},
            'hex_color': {'label':'Hex Color'},
            'custom': {'label':'Custom Categories (enter values)'}

        }
    },
    'number': {
        'label': 'Number',
        'subtypes': {
            'uniform': {'label': 'Uniform (min-max)'},
            'normal': {'label': 'Normal (mean, std)'},
            'integer': {'label': 'Integer (min-max)'},
            'boolean': {'label': 'Boolean (0/1)'},
        }
    },
    'date': {
        'label': 'Date/Time',
        'subtypes': {
            'date': {'label': 'Date (YYYY-MM-DD)'},
            'datetime': {'label': 'Datetime'},
            'year': {'label': 'Year'},
            'month': {'label':'Month'},
            'time': {'label': 'UTime (HH:MM:SS)'}
        }
    },
    'id': {
        'label': 'Identifiers',
        'subtypes': {
            'autoincrements': {'label': 'Auto-Increments (1, 2, 3, ...)'},
            'uuid4': {'label': 'UUID v4'},
            'ean13': {'label': 'EAN-13 Barcode'}
        }
    }
}

class ColumnSpec(BaseModel):
    name: str
    category: str
    subtype: str
    min_val: Optional[float] = 0
    max_val: Optional[float] = 100
    mean: Optional[float] = 50
    std: Optional[float] = 10
    decimals: Optional[float] = 2
    custom_values: Optional[List[str]] = []

class GenerateRequest(BaseModel):
    rows: int
    columns: List[ColumnSpec]
    format: str = 'json'


