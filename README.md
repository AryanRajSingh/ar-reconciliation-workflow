# AR Reconciliation Workflow Engine

## Project Overview

This project is an asynchronous Accounts Receivable (AR) reconciliation workflow engine built using Python and FastAPI.

The system processes customer ERP records through multiple workflow stages:

- Ingestion
- Matching
- Validation
- Decision Routing

The workflow supports retries, persistence, duplicate handling, and resuming execution from the last successful stage.

This project focuses on workflow orchestration and backend system design rather than ML accuracy.

---

## Features

✅ Modular workflow stages

✅ Asynchronous processing

✅ Parallel worker execution

✅ Retry mechanism with max retry limit

✅ Resume from last successful stage

✅ Persistence using SQLite

✅ Duplicate/repeated submission handling

✅ Workflow execution logs/history

✅ Dataset-based reconciliation logic

✅ REST API endpoints

---

## Tech Stack

**Backend**
- Python
- FastAPI
- SQLAlchemy

**Database**
- SQLite

**Data Processing**
- Pandas

**Workflow Processing**
- Asyncio Queue
- Background Workers

---

## Dataset Used

Kaggle Dataset:

AI Powered ERP AR Reconciliation Dataset

https://www.kaggle.com/datasets/asiryi/ai-powered-erp-ar-reconciliation

Dataset contains:

- Invoice Total
- Payment Total
- Credit Total
- Adjustment Total
- Customer Balance
- Exchange Rates

---

## Workflow Architecture

```text
User Request
      ↓

FastAPI API
      ↓

Async Queue
      ↓

Worker Pool
      ↓

Ingestion
      ↓

Matching
      ↓

Validation
      ↓

Decision Routing
      ↓

SQLite Database
```

---

## Project Structure

```text
Linkederp/

├── data/
│     erp_export.csv
├── app.py
├── database.py
├── generate_ar.py
├── models.py
├── README.md
├── requirements.txt
├── task_queue.py
├── workflow.db
├── workflow.py
```

---

## Installation

Clone repository:

```bash
git clone
```

Move into folder:

```bash
cd Linkederp
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

Windows:

```bash
.\.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
python -m uvicorn app:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/api-docs
```

---

## API Endpoints

Submit workflow:

```http
POST /submit/{customer_id}
```

Example:

```http
POST /submit/CUST_0011
```

Check workflow status:

```http
GET /status/{customer_id}
```

Example:

```http
GET /status/CUST_0011
```

Get workflow logs:

```http
GET /logs/{customer_id}
```

Get all workflows:

```http
GET /workflows
```

---

## Retry Logic

If a stage fails:

- Retry automatically
- Maximum retry count = 3
- Resume from last successful stage
- Prevent complete restart

---

## Duplicate Request Handling

The system safely handles duplicate requests:

- Already running → returns running status
- Already completed → returns completed status
- Failed workflow → resumes processing

---

## Future Improvements

- Celery + Redis queue
- PostgreSQL database
- Docker deployment
- Authentication
- Monitoring dashboard
- Kubernetes deployment

---

## Screenshots

Add screenshots here:

- Homepage
- API Docs
- Workflow execution
- Status API output

---

## Author

Aryan Raj