from sqlalchemy import ForeignKey, Column, String, Float, Date, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
from . import db

Base = declarative_base()

class Customers(Base):
    __tablename__ = 'invoices'

    customer_id = Column(String(120), nullable=False)
    user_name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    user_role = Column(String(120), nullable=False)
    invoice_number = Column(String(120), primary_key=True)
    invoice_url = Column(String(120), nullable=False)
    invoice_image_url = Column(String(120), nullable=False)
    product = Column(String(120), nullable=False)
    total_amount = Column(Float, nullable=False)
    issue_date = Column(Date, nullable=False)
    open_date = Column(Date, nullable=False)
    payment_due_date = Column(Date, nullable=False)
    sales_rep_code = Column(String(120), nullable=False)
    sales_rep_email = Column(String(120), nullable=False)
    user_type_code = Column(String(120), nullable=False)
    user_type_description = Column(String(120), nullable=False)
    seminar_code = Column(String(120), nullable=False)
    seminar_title = Column(String(120), nullable=False)
    seminar_url = Column(String(120), nullable=False)
    content_code = Column(String(120), nullable=False)
    content_title = Column(String(120), nullable=False)
    content_text = Column(Text, nullable=False)

    def __repr__(self):
        return f'<Customer {self.customer_id}>'
