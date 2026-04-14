# MockForge

A web app for generating custom mock datasets. Define your schema, pick your data types, and download realistic fake data in JSON or CSV.

This project has been deployed using [Render](https://render.com/). Please check it out here: [MockForge](https://mockforge-pmue.onrender.com/).

## Features

- **4 data categories** — String/Text, Number, Date/Time, and Identifiers
- **25+ subtypes** — names, emails, addresses, UUIDs, barcodes, dates, numeric distributions, and more
- **Custom categories** — supply your own list of values for random selection
- **Numeric distributions** — uniform, normal (Gaussian), integer range, or boolean
- **Export formats** — JSON (inline preview) or CSV download
- **Up to 10,000 rows** and **10 columns** per request

## Tech Stack

- **Backend:** FastAPI + Faker
- **Frontend:** Jinja2 templates
- **Runtime:** Python 3.10+

## Getting Started

### 1. Create the environment

```bash
conda env create -f environment.yml
conda activate mockforge
```

### 2. Run the server

```bash
uvicorn main:app --reload
```

### 3. Open the app

Navigate to `http://localhost:8000` in your browser.

## API

### `GET /api/data-types`

Returns the full map of supported categories and subtypes.

### `POST /api/generate`

Generate a mock dataset.

**Request body:**

```json
{
  "rows": 100,
  "format": "json",
  "columns": [
    {
      "name": "id",
      "category": "id",
      "subtype": "autoincrements"
    },
    {
      "name": "email",
      "category": "string",
      "subtype": "email"
    },
    {
      "name": "score",
      "category": "number",
      "subtype": "uniform",
      "min_val": 0,
      "max_val": 100,
      "decimals": 2
    }
  ]
}
```

| Field | Type | Description |
| --- | --- | --- |
| `rows` | int | Number of rows to generate (1–10,000) |
| `format` | string | `"json"` or `"csv"` |
| `columns` | array | List of column specs (1–10 columns) |

**Column spec fields:**

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Column header name |
| `category` | string | `string`, `number`, `date`, or `id` |
| `subtype` | string | Subtype within the category |
| `min_val` | float | Min value (uniform/integer distributions) |
| `max_val` | float | Max value (uniform/integer distributions) |
| `mean` | float | Mean (normal distribution) |
| `std` | float | Standard deviation (normal distribution) |
| `decimals` | int | Decimal places for float output |
| `custom_values` | array | Values to sample from (custom subtype) |

## License

[LICENSE](LICENSE)
