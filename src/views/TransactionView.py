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
                "OrgCode": row["OrgCode"],
                "HighwayCode": row["HighwayCode"],
                "PlazaCode": row["PlazaCode"],
                "SPID": row["SPID"],
                "RefNo": row["RefNo"],
                "Reason": row["Reason"],
                "TransactionDateTime": row["TransactionDateTime"],
                "ExitLocation": row["ExitLocation"],
                "TransactionAmount": row["TransactionAmount"],
                "ResponseCode": row["ResponseCode"],
                "ResponseDesc": row["ResponseDesc"]
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
                "ResponseCode": row["ResponseCode"],
                "ResponseDesc": row["ResponseDesc"]
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
                "OrgCode": updated_transaction["OrgCode"],
                "HighwayCode": updated_transaction["HighwayCode"],
                "PlazaCode": updated_transaction["PlazaCode"],
                "SPID": updated_transaction["SPID"],
                "RefNo": updated_transaction["RefNo"],
                "Reason": updated_transaction["Reason"],
                "TransactionDateTime": updated_transaction["TransactionDateTime"],
                "ExitLocation": updated_transaction["ExitLocation"],
                "TransactionAmount": updated_transaction["TransactionAmount"],
                "ResponseCode": updated_transaction["ResponseCode"],
                "ResponseDesc": updated_transaction["ResponseDesc"]
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