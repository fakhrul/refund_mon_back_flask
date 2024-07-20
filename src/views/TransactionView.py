#/src/views/TransactionView.py
from flask import Flask, request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from flask_sqlalchemy import SQLAlchemy
from ..models import db
app = Flask(__name__)
transaction_api = Blueprint('transaction_api', __name__)
from sqlalchemy import text
import datetime

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
                "ResponseDesc": row[42],
                # "Details": get_refund_ref_trx_details(row[4])
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
def get_transaction_by_refno_and_vehicleno():
    ref_no = request.args.get('refNo', '')
    vehicle_no = request.args.get('vehicleNo', '')

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
                    "ResponseDesc": row[42],
                    "Details": get_refund_ref_trx_details(row[4])
                }
                transactions_list.append(transaction)
            return custom_response('success', '', transactions_list, 200)
        else:
            return custom_response('failure', 'Transactions not found', {}, 404)

@transaction_api.route('/transaction/<ref_no>', methods=['GET'])
def get_transaction_by_refno(ref_no):
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
    WHERE r."RefNo" = :ref_no
    ''')
    
    with db.engine.connect() as connection:
        result = connection.execute(query, {'ref_no': ref_no})
        transaction = result.fetchone()
        if transaction:
            transaction_data = {
                "OrgCode": transaction[0],
                "HighwayCode": transaction[1],
                "PlazaCode": transaction[2],
                "SPID": transaction[3],
                "RefNo": transaction[4],
                "Reason": transaction[5],
                "VehicleNo": transaction[6],
                "RFIDTagNo": transaction[7],
                "CardMfgno": transaction[8],
                "VehicleColour": transaction[9],
                "CarModel": transaction[10],
                "CustomerName": transaction[11],
                "CustomerSOFName": transaction[12],
                "EntryLocation": transaction[13],
                "ExitLocation": transaction[14],
                "EntrySPName": transaction[15],
                "ExitSPName": transaction[16],
                "TransactionID": transaction[17],
                "TransactionDateTime": transaction[18],
                "ActualFare": transaction[19],
                "TransactionAmount": transaction[20],
                "RefundAmount": transaction[21],
                "TotalRefundAmount": transaction[22],
                "PaymentDateTime": transaction[23],
                "RefundStatus": transaction[24],
                "BatchRefNo": transaction[25],
                "Verify": transaction[26],
                "RemarkDateTime": transaction[27],
                "SPReason": transaction[28],
                "SPReasonCode": transaction[29],
                "AdditionalInfo": transaction[30],
                "ActualEntryPlaza": transaction[31],
                "ActualEntryLane": transaction[32],
                "ActualEntryClassVehicle": transaction[33],
                "ActualExitPlaza": transaction[34],
                "ActualExitLane": transaction[35],
                "ActualExitClassVehicle": transaction[36],
                "ReceivedDateTime": transaction[37],
                "ResponseDateTime": transaction[38],
                "InvoiceDateTime": transaction[39],
                "TngPaymentDateTime": transaction[40],
                "ResponseCode": transaction[41],
                "ResponseDesc": transaction[42],
                "Details": get_refund_ref_trx_details(transaction[4])
            }
            return custom_response('success', '', transaction_data, 200)
        else:
            return custom_response('failure', 'Transaction not found', {}, 404)
        
# def get_refund_ref_trx_details(ref_no):
#     query = text('''
#     SELECT "OrgCode", "HighwayCode", "PlazaCode", "SPID", "RefNo", "SeqNo", "UpdateBy", 
#            "CodeStatus", "Reason", "ResponseDateTime"
#     FROM public."refund_reftrxdetails"
#     WHERE "RefNo" = :ref_no
#     ''')
    
#     with db.engine.connect() as connection:
#         result = connection.execute(query, {'ref_no': ref_no})
#         details_list = []
#         for row in result:
#             detail = {
#                 "OrgCode": row[0],
#                 "HighwayCode": row[1],
#                 "PlazaCode": row[2],
#                 "SPID": row[3],
#                 "RefNo": row[4],
#                 "SeqNo": row[5],
#                 "UpdateBy": row[6],
#                 "CodeStatus": row[7],
#                 "Reason": row[8],
#                 "ResponseDateTime": row[9]
#             }
#             details_list.append(detail)
#     return details_list

def get_refund_ref_trx_details(ref_no):
    query = text('''
    SELECT d."orgcode", d."highwaycode", d."plazacode", d."spid", d."refno", d."seqno", d."updateby", 
           d."codestatus", d."reason", d."responsedatetime", r."ResponseDesc"
    FROM public."refund_reftrxdetails" d
    LEFT JOIN public."Mst_ResponseCode" r ON d."codestatus" = r."ResponseCode"
    WHERE d."refno" = :ref_no
    ORDER BY d."responsedatetime"
    ''')
    
    with db.engine.connect() as connection:
        result = connection.execute(query, {'ref_no': ref_no})
        details_list = []
        for row in result:
            detail = {
                "orgcode": row[0],
                "highwaycode": row[1],
                "plazacode": row[2],
                "spid": row[3],
                "refno": row[4],
                "seqno": row[5],
                "updateby": row[6],
                "codestatus": row[7],
                "reason": row[8],
                "responsedatetime": row[9],
                "ResponseDesc": row[10]
            }
            details_list.append(detail)
    return details_list

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
           r."ResponseCode", m."ResponseDesc", array_agg(d.*) as "Details"
    FROM public."Refund_RefTrx" r
    LEFT JOIN public."Mst_ResponseCode" m ON r."ResponseCode" = m."ResponseCode"
    LEFT JOIN public."refund_reftrxdetails" d ON r."RefNo" = d."RefNo"
    WHERE r."RefNo" = :ref_no
    GROUP BY r."OrgCode", r."HighwayCode", r."PlazaCode", r."SPID", r."RefNo", r."Reason", r."VehicleNo", 
             r."RFIDTagNo", r."CardMfgno", r."VehicleColour", r."CarModel", r."CustomerName", r."CustomerSOFName]", 
             r."EntryLocation", r."ExitLocation", r."EntrySPName", r."ExitSPName", r."TransactionID", 
             r."TransactionDateTime", r."ActualFare", r."TransactionAmount", r."RefundAmount", r."TotalRefundAmount", 
             r."PaymentDateTime", r."RefundStatus", r."BatchRefNo", r."Verify", r."RemarkDateTime", r."SPReason", 
             r."SPReasonCode", r."AdditionalInfo", r."ActualEntryPlaza", r."ActualEntryLane", 
             r."ActualEntryClassVehicle", r."ActualExitPlaza", r."ActualExitLane", r."ActualExitClassVehicle]", 
             r."ReceivedDateTime", r."ResponseDateTime", r."InvoiceDateTime", r."TngPaymentDateTime", 
             r."ResponseCode", m."ResponseDesc"
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
                "ResponseDesc": updated_transaction[42],
                "Details": get_refund_ref_trx_details(ref_no)
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

def get_next_seqno(ref_no):
    query = text('''
    SELECT MAX(CAST("SeqNo" AS INTEGER))
    FROM public."refund_reftrxdetails"
    WHERE "RefNo" = :ref_no
    ''')
    
    with db.engine.connect() as connection:
        result = connection.execute(query, {'ref_no': ref_no}).scalar()
        if result is None:
            return 1
        else:
            return result + 1
        
@transaction_api.route('/add_detail', methods=['POST'])
def add_refund_ref_trx_detail():
    data = request.get_json()
    # print(data)
    # data['SeqNo'] = str(get_next_seqno(data['RefNo']))
    data['seqno'] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data['updateby'] = 0
    data['responsedatetime'] =  datetime.datetime.utcnow()
    # data['ResponseDateTime'] =  datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    insert_query = text('''
    INSERT INTO public."refund_reftrxdetails" ("orgcode", "highwaycode", "plazacode", "spid", "refno", "seqno", 
                                               "updateby", "codestatus", "reason", "responsedatetime")
    VALUES (:orgcode, :highwaycode, :plazacode, :spid, :refno, :seqno, :updateby, :codestatus, :reason, :responsedatetime)
    ''')

    print(data)
    print(insert_query)

    # try:
    #     with db.engine.connect() as connection:
    #         connection.execute(insert_query, data)
    #     return custom_response('success', 'Detail added successfully', {}, 201)
    # except Exception as e:
    #     return custom_response('failure', str(e), {}, 500)


    with db.engine.connect() as connection:
        connection.execute(insert_query, data)
    return custom_response('success', 'Detail added successfully', {}, 201)

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