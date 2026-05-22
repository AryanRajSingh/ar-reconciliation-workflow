from sqlalchemy import Column,Integer,String
from database import Base

class Workflow(Base):

    __tablename__="workflows"

    id=Column(Integer,primary_key=True)

    customer_id=Column(
        String,
        unique=True
    )

    current_stage=Column(
        String,
        default="ingestion"
    )

    status=Column(
        String,
        default="pending"
    )

    retries=Column(
        Integer,
        default=0
    )