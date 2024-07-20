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
    SELECT r."OrgCode", r."HighwayCode", r."PlazaCode", r."SPID", r."RefNo", r."Reason", r."VehicleNo", 
           r."RFIDTagNo", r."CardMfgno", r."VehicleColour", r."CarModel", r."CustomerName", r."CustomerSOFName]", 
           r."EntryLocation", r."ExitLocation", r."EntrySPName", r."ExitSPName", r."TransactionID", 
           r."TransactionDateTime", r."ActualFare", r."TransactionAmount", r."RefundAmount", r."TotalRefundAmount", 
           r."PaymentDateTime", r."RefundStatus", r."BatchRefNo", r."Verify", r."RemarkDateTime", r."SPReason", 
           r."SPReasonCode", r."AdditionalInfo", r."ActualEntryPlaza", r."ActualEntryLane", 
           r."ActualEntryClassVehicle", r."ActualExitPlaza", r."ActualExitLane", r."ActualExitClassVehicle]", 
           r."ReceivedDateTime", r."ResponseDateTime", r."InvoiceDateTime", r."TngPaymentDateTime", 
           r."ResponseCode", m."ResponseDesc"
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
                "VehicleNo": row[6],
                "RFIDTagNo": row[7],
                "CardMfgno": row[8],
                "VehicleColour": row[9],
                "CarModel": row[10],
                "CustomerName": row[11],
                "CustomerSOFName": row[12],
                "EntryLocation": row[13],
                "ExitLocation": row[14],
                "EntrySPName": row[15],
                "ExitSPName": row[16],
                "TransactionID": row[17],
                "TransactionDateTime": row[18],
                "ActualFare": row[19],
                "TransactionAmount": row[20],
                "RefundAmount": row[21],
                "TotalRefundAmount": row[22],
                "PaymentDateTime": row[23],
                "RefundStatus": row[24],
                "BatchRefNo": row[25],
                "Verify": row[26],
                "RemarkDateTime": row[27],
                "SPReason": row[28],
                "SPReasonCode": row[29],
                "AdditionalInfo": row[30],
                "ActualEntryPlaza": row[31],
                "ActualEntryLane": row[32],
                "ActualEntryClassVehicle": row[33],
                "ActualExitPlaza": row[34],
                "ActualExitLane": row[35],
                "ActualExitClassVehicle": row[36],
                "ReceivedDateTime": row[37],
                "ResponseDateTime": row[38],
                "InvoiceDateTime": row[39],
                "TngPaymentDateTime": row[40],
                "ResponseCode": row[41],
                "ResponseDesc": row[42]
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

@transaction_api.route('/search', methods=['GET'])
def get_transaction_by_refno():
    ref_no = request.args.get('refNo', 'UNKNOWN')
    vehicle_no = request.args.get('vehicleNo', 'UNKNOWN')
    print(ref_no, vehicle_no)
    query = text('''
    SELECT r."OrgCode", r."HighwayCode", r."PlazaCode", r."SPID", r."RefNo", r."Reason", r."VehicleNo", 
           r."RFIDTagNo", r."CardMfgno", r."VehicleColour", r."CarModel", r."CustomerName", r."CustomerSOFName]", 
           r."EntryLocation", r."ExitLocation", r."EntrySPName", r."ExitSPName", r."TransactionID", 
           r."TransactionDateTime", r."ActualFare", r."TransactionAmount", r."RefundAmount", r."TotalRefundAmount", 
           r."PaymentDateTime", r."RefundStatus", r."BatchRefNo", r."Verify", r."RemarkDateTime", r."SPReason", 
           r."SPReasonCode", r."AdditionalInfo", r."ActualEntryPlaza", r."ActualEntryLane", 
           r."ActualEntryClassVehicle", r."ActualExitPlaza", r."ActualExitLane", r."ActualExitClassVehicle]", 
           r."ReceivedDateTime", r."ResponseDateTime", r."InvoiceDateTime", r."TngPaymentDateTime", 
           r."ResponseCode", m."ResponseDesc"
    FROM public."Refund_RefTrx" r
    LEFT JOIN public."Mst_ResponseCode" m ON r."ResponseCode" = m."ResponseCode"
    WHERE r."RefNo" LIKE :ref_no AND r."VehicleNo" LIKE :vehicle_no
    ''')
    ref_no_like = f'%{ref_no}%'
    vehicle_no_like = f'%{vehicle_no}%'

    with db.engine.connect() as connection:
        result = connection.execute(query, {'ref_no': ref_no_like, 'vehicle_no': vehicle_no_like})
        transactions = result.fetchall()
        if transactions:
            transactions_list = []
            for row in transactions:
                transaction = {
                    "OrgCode": row[0],
                    "HighwayCode": row[1],
                    "PlazaCode": row[2],
                    "SPID": row[3],
                    "RefNo": row[4],
                    "Reason": row[5],
                    "VehicleNo": row[6],
                    "RFIDTagNo": row[7],
                    "CardMfgno": row[8],
                    "VehicleColour": row[9],
                    "CarModel": row[10],
                    "CustomerName": row[11],
                    "CustomerSOFName": row[12],
                    "EntryLocation": row[13],
                    "ExitLocation": row[14],
                    "EntrySPName": row[15],
                    "ExitSPName": row[16],
                    "TransactionID": row[17],
                    "TransactionDateTime": row[18],
                    "ActualFare": row[19],
                    "TransactionAmount": row[20],
                    "RefundAmount": row[21],
                    "TotalRefundAmount": row[22],
                    "PaymentDateTime": row[23],
                    "RefundStatus": row[24],
                    "BatchRefNo": row[25],
                    "Verify": row[26],
                    "RemarkDateTime": row[27],
                    "SPReason": row[28],
                    "SPReasonCode": row[29],
                    "AdditionalInfo": row[30],
                    "ActualEntryPlaza": row[31],
                    "ActualEntryLane": row[32],
                    "ActualEntryClassVehicle": row[33],
                    "ActualExitPlaza": row[34],
                    "ActualExitLane": row[35],
                    "ActualExitClassVehicle": row[36],
                    "ReceivedDateTime": row[37],
                    "ResponseDateTime": row[38],
                    "InvoiceDateTime": row[39],
                    "TngPaymentDateTime": row[40],
                    "ResponseCode": row[41],
                    "ResponseDesc": row[42]
                }
                transactions_list.append(transaction)
            return custom_response('success', '', transactions_list, 200)
        else:
            return custom_response('failure', 'Transactions not found', {}, 404)

def update_response_code(ref_no, response_code):
    update_query = text('''
    UPDATE public."Refund_RefTrx"
    SET "ResponseCode" = :response_code
    WHERE "RefNo" = :ref_no
    ''')
    select_query = text('''
    SELECT r."OrgCode", r."HighwayCode", r."PlazaCode", r."SPID", r."RefNo", r."Reason", r."VehicleNo", 
           r."RFIDTagNo", r."CardMfgno", r."VehicleColour", r."CarModel", r."CustomerName", r."CustomerSOFName]", 
           r."EntryLocation", r."ExitLocation", r."EntrySPName", r."ExitSPName", r."TransactionID", 
           r."TransactionDateTime", r."ActualFare", r."TransactionAmount", r."RefundAmount", r."TotalRefundAmount", 
           r."PaymentDateTime", r."RefundStatus", r."BatchRefNo", r."Verify", r."RemarkDateTime", r."SPReason", 
           r."SPReasonCode", r."AdditionalInfo", r."ActualEntryPlaza", r."ActualEntryLane", 
           r."ActualEntryClassVehicle", r."ActualExitPlaza", r."ActualExitLane", r."ActualExitClassVehicle]", 
           r."ReceivedDateTime", r."ResponseDateTime", r."InvoiceDateTime", r."TngPaymentDateTime", 
           r."ResponseCode", m."ResponseDesc"
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
                "VehicleNo": updated_transaction[6],
                "RFIDTagNo": updated_transaction[7],
                "CardMfgno": updated_transaction[8],
                "VehicleColour": updated_transaction[9],
                "CarModel": updated_transaction[10],
                "CustomerName": updated_transaction[11],
                "CustomerSOFName": updated_transaction[12],
                "EntryLocation": updated_transaction[13],
                "ExitLocation": updated_transaction[14],
                "EntrySPName": updated_transaction[15],
                "ExitSPName": updated_transaction[16],
                "TransactionID": updated_transaction[17],
                "TransactionDateTime": updated_transaction[18],
                "ActualFare": updated_transaction[19],
                "TransactionAmount": updated_transaction[20],
                "RefundAmount": updated_transaction[21],
                "TotalRefundAmount": updated_transaction[22],
                "PaymentDateTime": updated_transaction[23],
                "RefundStatus": updated_transaction[24],
                "BatchRefNo": updated_transaction[25],
                "Verify": updated_transaction[26],
                "RemarkDateTime": updated_transaction[27],
                "SPReason": updated_transaction[28],
                "SPReasonCode": updated_transaction[29],
                "AdditionalInfo": updated_transaction[30],
                "ActualEntryPlaza": updated_transaction[31],
                "ActualEntryLane": updated_transaction[32],
                "ActualEntryClassVehicle": updated_transaction[33],
                "ActualExitPlaza": updated_transaction[34],
                "ActualExitLane": updated_transaction[35],
                "ActualExitClassVehicle": updated_transaction[36],
                "ReceivedDateTime": updated_transaction[37],
                "ResponseDateTime": updated_transaction[38],
                "InvoiceDateTime": updated_transaction[39],
                "TngPaymentDateTime": updated_transaction[40],
                "ResponseCode": updated_transaction[41],
                "ResponseDesc": updated_transaction[42]
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