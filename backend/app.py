from flask import Flask, request, jsonify
from flask_cors import CORS
from db_control import crud, mymodels
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'
jwt = JWTManager(app)

@app.route("/")
def index():
    return "<p>MilleBill_Flask</p>"

@app.route('/login', methods=['POST'])
def login():
    customer_id = request.json.get('customer_id', None)
    password = request.json.get('password', None)  # ここでフロントから送られたハッシュ化パスワードを受け取る

    # CRUDを使用して顧客情報を取得
    customer_json = crud.myselect(mymodels.Customers, customer_id)
    if customer_json:   # JSON文字列から辞書リストに変換
        customer_info_list = json.loads(customer_json)
        if customer_info_list:
            customer_info = customer_info_list[0]
            if customer_info['password'] == password:
                access_token = create_access_token(identity=customer_id)
                return jsonify(access_token=access_token), 200
            else:
                return jsonify({"msg": "Customer IDまたはパスワードが間違っています"}), 401
    return jsonify({"msg": "Customer情報が見つかりません"}), 404

@app.route('/customer-info', methods=['GET'])
@jwt_required()
def customer_info():
    current_customer_id = get_jwt_identity()
    customer_json = crud.myselect(mymodels.Customers, current_customer_id)
    if customer_json:
        # myselectが返すJSON文字列を直接クライアントに返します。
        return customer_json, 200
    else:
        return jsonify({"msg": "Customer情報の取得に失敗しました"}), 500

####### 既存のコード

@app.route("/customers", methods=['POST'])
def create_customer():
    values = request.get_json()
    tmp = crud.myinsert(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['GET'])
def read_one_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.myselect(mymodels.Customers, target_id)
    return result, 200

@app.route("/allcustomers", methods=['GET'])
def read_all_customer():
    model = mymodels.Customers
    result = crud.myselectAll(mymodels.Customers)
    return result, 200

@app.route("/customers", methods=['PUT'])
def update_customer():
    print("I'm in")
    values = request.get_json()
    values_original = values.copy()
    model = mymodels.Customers
    tmp = crud.myupdate(model, values)
    result = crud.myselect(mymodels.Customers, values_original.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['DELETE'])
def delete_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.mydelete(model, target_id)
    return result, 200

@app.route("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json(), 200
