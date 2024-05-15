# uname() error回避
import platform
print("platform", platform.uname())

from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd

from db_control.connect import engine
from db_control.mymodels import Customers

def myinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = insert(mymodel).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "inserted"

def myselect(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for customer_info in result:
            result_dict_list.append({
                "customer_id": customer_info.customer_id,
                "user_name": customer_info.user_name,
                "email": customer_info.email,
                "password": customer_info.password,
                "user_role": customer_info.user_role,
                "invoice_number": customer_info.invoice_number,
                "invoice_url": customer_info.invoice_url,
                "invoice_image_url": customer_info.invoice_image_url,
                "product": customer_info.product,
                "total_amount": customer_info.total_amount,
                "issue_date": customer_info.issue_date.isoformat() if customer_info.issue_date else None,
                "open_date": customer_info.open_date.isoformat() if customer_info.open_date else None,
                "payment_due_date": customer_info.payment_due_date.isoformat() if customer_info.payment_due_date else None,
                "sales_rep_code": customer_info.sales_rep_code,
                "sales_rep_email": customer_info.sales_rep_email,
                "user_type_code": customer_info.user_type_code,
                "user_type_description": customer_info.user_type_description,
                "seminar_code": customer_info.seminar_code,
                "seminar_title": customer_info.seminar_title,
                "seminar_url": customer_info.seminar_url,
                "content_code": customer_info.content_code,
                "content_title": customer_info.content_title,
                "content_text": customer_info.content_text,
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、処理に失敗しました")
        result_json = None
    finally:
        session.close()
    return result_json

def myselectAll(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            df = pd.read_sql_query(query, con=engine)
            result_json = df.to_json(orient='records', force_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        result_json = None
    # セッションを閉じる
    session.close()
    return result_json

def myupdate(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    customer_id = values.pop("customer_id")
    query = update(mymodel).where(mymodel.customer_id == customer_id).values(**values)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "updated"

def mydelete(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = delete(mymodel).where(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return customer_id + " is deleted"