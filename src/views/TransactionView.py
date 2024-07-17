#/src/views/TransactionView.py
from flask import Flask, request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from flask_sqlalchemy import SQLAlchemy
from ..models import db
app = Flask(__name__)
transaction_api = Blueprint('transaction_api', __name__)
from sqlalchemy import text

@transaction_api.route('/', methods=['GET'])
# @Auth.auth_required
def get_all():
    query = text('''
    SELECT r."OrgCode", r."HighwayCode", r."PlazaCode", r."SPID", r."RefNo", r."Reason", r."TransactionDateTime", 
           r."ExitLocation", r."TransactionAmount", r."ResponseCode", m."ResponseDesc"
    FROM public."Refund_RefTrx" r
    LEFT JOIN public."Mst_ResponseCode" m ON r."ResponseCode" = m."ResponseCode"
    ''')
    transactions_list = []
    with db.engine.connect() as connection:
        result = connection.execute(query)
        for row in result:
            transaction = {
                "OrgCode": row[0],
                "HighwayCode": row[1],
                "PlazaCode": row[2],
                "SPID": row[3],
                "RefNo": row[4],
                "Reason": row[5],
                "TransactionDateTime": row[6],
                "ExitLocation": row[7],
                "TransactionAmount": row[8],
                "ResponseCode": row[9],
                "ResponseDesc": row[10]
            }
            transactions_list.append(transaction)
    return custom_response('success', '', transactions_list, 200)

@transaction_api.route('/response_codes', methods=['GET'])
def get_response_codes():
    query = text('''
    SELECT "ResponseCode", "ResponseDesc"
    FROM public."Mst_ResponseCode"
    ''')
    response_codes_list = []
    with db.engine.connect() as connection:
        result = connection.execute(query)
        for row in result:
            response_code = {
                "ResponseCode": row[0],
                "ResponseDesc": row[1]
            }
            response_codes_list.append(response_code)
    return custom_response('success', '', response_codes_list, 200)

def update_response_code(ref_no, response_code):
    update_query = text('''
    UPDATE public."Refund_RefTrx"
    SET "ResponseCode" = :response_code
    WHERE "RefNo" = :ref_no
    ''')
    select_query = text('''
    SELECT r."OrgCode", r."HighwayCode", r."PlazaCode", r."SPID", r."RefNo", r."Reason", r."TransactionDateTime", 
           r."ExitLocation", r."TransactionAmount", r."ResponseCode", m."ResponseDesc"
    FROM public."Refund_RefTrx" r
    LEFT JOIN public."Mst_ResponseCode" m ON r."ResponseCode" = m."ResponseCode"
    WHERE r."RefNo" = :ref_no
    ''')
    try:
        with db.engine.connect() as connection:
            connection.execute(update_query, {'response_code': response_code, 'ref_no': ref_no})
            result = connection.execute(select_query, {'ref_no': ref_no})
            updated_transaction = result.fetchone()
            transaction = {
                "OrgCode": updated_transaction[0],
                "HighwayCode": updated_transaction[1],
                "PlazaCode": updated_transaction[2],
                "SPID": updated_transaction[3],
                "RefNo": updated_transaction[4],
                "Reason": updated_transaction[5],
                "TransactionDateTime": updated_transaction[6],
                "ExitLocation": updated_transaction[7],
                "TransactionAmount": updated_transaction[8],
                "ResponseCode": updated_transaction[9],
                "ResponseDesc": updated_transaction[10]
            }
            return {"status": "success", "transaction": transaction}
    except Exception as e:
        return {"status": "failure", "message": str(e)}

@transaction_api.route('/update_response_code', methods=['PUT'])
def update_response():
    data = request.get_json()
    ref_no = data.get('RefNo')
    response_code = data.get('ResponseCode')
    result = update_response_code(ref_no, response_code)
    if result['status'] == 'success':
        return custom_response('success', '', result['transaction'], 200)
    else:
        return custom_response('failure', result['message'], {}, 500)

def custom_response(status, errorMsg, data, status_code):
    """
    Custom Response Function
    """
    info = {
        'status': status, 
        'errorMsg': errorMsg,
        'data': data
    }

    response = Response(
        mimetype="application/json",
        response=json.dumps(info),
        status=status_code
    )

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response