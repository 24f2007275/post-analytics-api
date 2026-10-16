# POST Analytics API

A stateless FastAPI service for the TDS POST `/analytics` assignment.

## Endpoint

`POST /analytics`

Headers:

- `X-API-Key: <assigned API key>`
- `Content-Type: application/json`

Example body:

```json
{
  "events": [
    {"user": "alice", "amount": 42.5, "ts": 1700000000},
    {"user": "bob", "amount": -2, "ts": 1700000001},
    {"user": "alice", "amount": 5, "ts": 1700000002}
  ]
}
```

The response computes:

- `email`: `24f2007275@ds.study.iitm.ac.in`
- `total_events`: length of `events`
- `unique_users`: number of distinct user values in all events
- `revenue`: sum of amounts strictly greater than zero
- `top_user`: user with the largest total of strictly positive amounts

Missing/wrong API keys receive HTTP 401. CORS is enabled for browser grading.

## Run locally

```bash
python -m pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Test the endpoint:

```bash
curl -i -X POST http://localhost:8000/analytics \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: ak_nkpytjsylhlq933tugmesimu' \
  -d '{"events":[{"user":"alice","amount":42.5,"ts":1700000000},{"user":"bob","amount":-2,"ts":1700000001},{"user":"alice","amount":5,"ts":1700000002}]}'
```

Expected computed fields for that sample: `total_events: 3`, `unique_users: 2`, `revenue: 47.5`, `top_user: "alice"`.

## Deploy on Render

Create a new **Web Service** from this repository. Use:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

In the Render service settings, add environment variables `ANALYTICS_API_KEY` (set it to the key assigned on your assignment page) and `STUDENT_EMAIL=24f2007275@ds.study.iitm.ac.in`. Keep the repository private so you do not publish your assigned API key.

Submit the full endpoint URL, including `/analytics`, e.g. `https://your-service.onrender.com/analytics`.
