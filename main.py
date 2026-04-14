from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from faker import Faker
import random
import json
import csv
import io
from typing import Optional, List, Any

app = FastAPI(title='MockForge')
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
    decimals: Optional[int] = 2
    custom_values: Optional[List[str]] = []

class GenerateRequest(BaseModel):
    rows: int
    columns: List[ColumnSpec]
    format: str = 'json'


_ai = {} # This is the autoincrement state per session, it restse each request

def generate_value(col: ColumnSpec, row_index: int) -> Any:
    cat = col.category
    sub = col.subtype

    if cat == 'string':
        fn_map = {
            'full_name': fake.name,
            'first_name': fake.first_name,
            'last_name': fake.last_name,
            'email': fake.email,
            'phone': fake.phone_number,
            'username': fake.user_name,
            'company': fake.company,
            'job': fake.job,
            'city': fake.city,
            'country': fake.country,
            'address': fake.address,
            'url': fake.url,
            'ipv4': fake.ipv4,
            'uuid4': fake.uuid4,
            'color_name': fake.color_name,
            'hex_color': fake.hex_color
        }
        if sub == 'custom':
            vals = col.custom_values or ['A','B','C']
            return random.choice(vals)
        return fn_map.get(sub,fake.word)()
    
    elif cat == 'number':
        if sub == 'uniform':
            # Generates a number from a uniform distribution where col.min_val and col.max_val are the min and max params
            v = random.uniform(col.min_val, col.max_val) 
            # Returns the rounded version, with col.decimals
            return round(v,col.decimals)
        elif sub == 'normal':
            v = random.gauss(col.mean,col.std)
            return round(v,col.decimals)
        elif sub == 'integer':
            v = random.randint(int(col.min_val), int(col.max_val))
            return v
        elif sub == 'boolean':
            v = random.randint(0,1)
            return v
    elif cat == 'date':
        if sub == 'date':
            return fake.date()
        elif sub == 'datetime':
            return fake.datetime().isoformat()
        elif sub == 'year':
            return fake.year()
        elif sub == 'month':
            return fake.month()
        elif sub == 'time':
            return fake.time()
    
    elif cat == 'id':
        if sub == 'autoincrements':
            return row_index + 1
        elif sub == 'uuid4':
                return fake.uuid4()
        elif sub == 'ean13':
            return fake.ean13()
    
    return None



@app.get('/',response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse('index.html', {
        'request':request,
        'data_types':DATA_TYPES
    })

@app.get('/api/data-types')
async def get_data_types():
    return DATA_TYPES

@app.post('/api/generate')
async def generate(req: GenerateRequest):
    # This handles crazy requests like less than 1 or more than 10000 rows.
    if req.rows < 1 or req.rows > 10000:
        return JSONResponse({"error":"rows must be between 1 and 10000"},400)
    if len(req.columns) < 1 or len(req.columns) > 10:
        return JSONResponse({"error": "1-10 columns allowed"},400)
    
    records = []
    for i in range(req.rows):
        row = {}
        for col in req.columns:
            row[col.name or f'col_{i}'] = generate_value(col,i)
        records.append(row)
    
    if req.format == 'csv':
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=[c.name for c in req.columns])
        writer.writeheader()
        writer.writerows(records)
        buf.seek(0)
        return StreamingResponse(
            iter([buf.getvalue()]),
            media_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=mock_data.csv'}
        )
    
    return {'rows':req.rows, 'columns':len(req.columns), 'data':records}