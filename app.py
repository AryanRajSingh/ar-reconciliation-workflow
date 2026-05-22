from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse

from database import SessionLocal, engine
from models import Base, Workflow
from workflow import run_workflow
from fastapi.responses import JSONResponse


# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(

    title="AR Reconciliation Workflow Engine",

    description="""
ERP Accounts Receivable Workflow System

Features:

✅ Async processing

✅ Retry mechanism

✅ Resume from last successful stage

✅ Duplicate handling

✅ Workflow persistence

✅ Parallel execution
""",

    version="1.0.0",

    docs_url="/api-docs",

    redoc_url="/documentation"

)



# Home page
@app.get(
    "/",
    response_class=HTMLResponse
)
def home():

    return """

<!DOCTYPE html>

<html>

<head>

<title>
AR Workflow Engine
</title>

<style>

body{

font-family:Arial,sans-serif;
margin:0;
padding:0;
background:#f4f7fc;

}


.header{

background:#0f172a;
color:white;
padding:30px;
text-align:center;

}


.container{

width:80%;
margin:auto;
margin-top:30px;

}


.card{

background:white;

padding:25px;

margin-top:20px;

border-radius:15px;

box-shadow:
0px 4px 15px rgba(
0,0,0,0.2
);

}


.button{

background:#2563eb;

padding:15px;

color:white;

text-decoration:none;

border-radius:10px;

display:inline-block;

margin-top:10px;

}


ul{

line-height:35px;

}

</style>

</head>

<body>

<div class="header">

<h1> Linkederp Assignment </h1>
<h1>
AR Reconciliation Workflow Engine
</h1>

<p>
Async ERP Workflow System
</p>
<p>
--By Aryan Raj
</p>

</div>


<div class="container">


<div class="card">

<h2>
Features
</h2>

<ul>

<li>
Async workflow execution
</li>

<li>
Retry support
</li>

<li>
Resume from failed stage
</li>

<li>
Duplicate handling
</li>

<li>
Parallel execution
</li>

<li>
SQLite persistence
</li>

</ul>

</div>


<div class="card">

<h2>
API Documentation
</h2>

<a
class="button"
href="/api-docs"
>

Open API Docs

</a>

</div>

</div>

</body>

</html>

"""


# Submit workflow
@app.post(
    "/submit/{customer_id}"
)
async def submit(

    customer_id:str,

    background_tasks:BackgroundTasks

):

    db=SessionLocal()


    try:

        existing=db.query(
            Workflow
        ).filter(
            Workflow.customer_id==
            customer_id
        ).first()


        # Duplicate handling
        if existing:

            if existing.status=="completed":

                return {

                    "message":
                    "Already completed"
                }


            elif existing.status=="pending":

                return {

                    "message":
                    "Already running"
                }


            elif existing.status=="failed":

                background_tasks.add_task(

                    run_workflow,
                    customer_id
                )

                return {

                    "message":
                    "Resuming failed workflow"
                }


        workflow=Workflow(

            customer_id=
            customer_id,

            current_stage=
            "ingestion",

            status=
            "pending",

            retries=0
        )


        db.add(
            workflow
        )

        db.commit()


        background_tasks.add_task(

            run_workflow,
            customer_id
        )


        return {

            "message":
            "Workflow started"
        }


    finally:

        db.close()



# Check workflow status
@app.get(
"/status/{customer_id}"
)
def status(

customer_id:str

):

    db=SessionLocal()


    try:

        workflow=db.query(
            Workflow
        ).filter(
            Workflow.customer_id==
            customer_id
        ).first()


        if not workflow:

            return {

                "message":
                "Customer not found"
            }


        return {

            "customer":
            workflow.customer_id,

            "current_stage":
            workflow.current_stage,

            "status":
            workflow.status,

            "retries":
            workflow.retries

        }


    finally:

        db.close()



# Get all workflows
@app.get(
"/workflows"
)
def all_workflows():

    db=SessionLocal()

    try:

        workflows=db.query(
            Workflow
        ).all()


        results=[]


        for w in workflows:

            results.append({

                "customer":
                w.customer_id,

                "stage":
                w.current_stage,

                "status":
                w.status,

                "retries":
                w.retries
            })


        return results


    finally:

        db.close()

@app.get(
    "/.well-known/appspecific/com.chrome.devtools.json"
)
async def chrome_devtools():

    return JSONResponse(
        content={}
    )