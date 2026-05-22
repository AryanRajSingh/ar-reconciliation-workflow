import pandas as pd
import random
import os

os.makedirs("data", exist_ok=True)

rows=[]

for i in range(1,1001):

    customer=f"CUST_{i:04d}"

    invoice_total=round(
        random.uniform(500,5000),2
    )

    invoice_applied=round(
        random.uniform(0,invoice_total*0.5),2
    )

    payment_total=round(
        random.uniform(100,2000),2
    )

    payment_applied=round(
        random.uniform(0,payment_total*0.5),2
    )

    credit_total=round(
        random.uniform(0,500),2
    )

    credit_applied=round(
        random.uniform(0,credit_total),2
    )

    adjustment_total=round(
        random.uniform(0,200),2
    )

    adjustment_applied=round(
        random.uniform(
            0,
            adjustment_total
        ),2
    )

    exchange_rate=1.0


    balance=(

        (invoice_total-invoice_applied)
        -
        (payment_total-payment_applied)
        -
        (credit_total-credit_applied)
        +
        (adjustment_total-adjustment_applied)

    )*exchange_rate


    rows.append({

        "Customer ID":customer,

        "Invoice Total":
        invoice_total,

        "Invoice applied amount":
        invoice_applied,

        "Invoice exchange rate":
        exchange_rate,

        "Payment Total":
        payment_total,

        "Payment applied amount":
        payment_applied,

        "Payment exchange rate":
        exchange_rate,

        "Credit Total":
        credit_total,

        "Credit applied amount":
        credit_applied,

        "Credit exchange rate":
        exchange_rate,

        "Adjustment Total":
        adjustment_total,

        "Adjustment applied amount":
        adjustment_applied,

        "Adjustment exchange rate":
        exchange_rate,

        "Customer Balance":
        round(balance,2)
    })


df=pd.DataFrame(rows)

df.to_csv(
    "data/erp_export.csv",
    index=False
)

print("CSV created")