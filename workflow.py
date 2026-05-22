import asyncio
import random
import pandas as pd
import os

from database import SessionLocal
from models import Workflow


# Workflow stages
stages = [

    "ingestion",
    "matching",
    "validation",
    "decision"
]


# Get current project directory
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# CSV file location
CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "erp_export.csv"
)


async def execute_stage(stage, row):

    print(f"\nRunning {stage}")

    await asyncio.sleep(2)

    # simulate random failure (30%)
    if random.random() < 0.3:

        raise Exception(
            f"{stage} failed"
        )

    # -------------------------
    # Ingestion
    # -------------------------
    if stage == "ingestion":

        print(
            f"Loaded customer: {row['Customer ID']}"
        )


    # -------------------------
    # Matching
    # -------------------------
    elif stage == "matching":

        invoice = (

            row["Invoice Total"]
            -
            row["Invoice applied amount"]

        ) * row["Invoice exchange rate"]


        payment = (

            row["Payment Total"]
            -
            row["Payment applied amount"]

        ) * row["Payment exchange rate"]


        credit = (

            row["Credit Total"]
            -
            row["Credit applied amount"]

        ) * row["Credit exchange rate"]


        adjustment = (

            row["Adjustment Total"]
            -
            row["Adjustment applied amount"]

        ) * row["Adjustment exchange rate"]


        calculated = (

            invoice
            -
            payment
            -
            credit
            +
            adjustment
        )


        row["calculated_balance"] = round(
            calculated,
            2
        )


        print(
            f"Calculated Balance: {row['calculated_balance']}"
        )


    # -------------------------
    # Validation
    # -------------------------
    elif stage == "validation":

        difference = abs(

            row["calculated_balance"]
            -
            row["Customer Balance"]
        )


        row["difference"] = round(
            difference,
            2
        )


        print(
            f"Difference: {row['difference']}"
        )


    # -------------------------
    # Decision Routing
    # -------------------------
    elif stage == "decision":

        if row["difference"] > 5:

            print(
                "Mismatch detected"
            )

        else:

            print(
                "Valid balance"
            )



async def run_workflow(customer_id):

    db=SessionLocal()

    MAX_RETRIES=3

    try:

        workflow=db.query(
            Workflow
        ).filter(
            Workflow.customer_id==customer_id
        ).first()


        if not workflow:

            return


        data=pd.read_csv(
            CSV_PATH
        )


        customer_rows=data[
            data["Customer ID"].astype(str)
            ==
            str(customer_id)
        ]


        if customer_rows.empty:

            workflow.status="failed"

            db.commit()

            return


        row=customer_rows.iloc[0]


        current=workflow.current_stage

        start=stages.index(
            current
        )


        for stage in stages[start:]:

            success=False

            while(
                workflow.retries
                <
                MAX_RETRIES
            ):

                try:

                    await execute_stage(
                        stage,
                        row
                    )

                    workflow.current_stage=stage

                    workflow.retries=0

                    db.commit()

                    success=True

                    break


                except Exception as e:

                    workflow.retries+=1

                    db.commit()

                    print(
                        f"Retry {workflow.retries}: {e}"
                    )

                    await asyncio.sleep(2)


            if not success:

                workflow.status="failed"

                db.commit()

                print(
                    f"{stage} permanently failed"
                )

                return


        workflow.status="completed"

        db.commit()

        print(
            f"Workflow completed for {customer_id}"
        )


    finally:

        db.close()