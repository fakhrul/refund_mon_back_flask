#/src/views/TransactionView.py
from flask import Flask, request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from flask_sqlalchemy import SQLAlchemy
from ..models import db
app = Flask(__name__)
transaction_api = Blueprint('transaction_api', __name__)
from sqlalchemy import text
import datetime
from ..shared.GMailing import GMailing

mail = GMailing()

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

@transaction_api.route('/send_email/<email>', methods=['PUT'])
def send_email(email):
    transaction_data = request.get_json()
    # Convert to text
    text_content = f"""
    Transaction Details:
    - Transaction ID: {transaction_data['TransactionID']}
    - Batch Reference Number: {transaction_data['BatchRefNo']}
    - Transaction Date and Time: {transaction_data['TransactionDateTime']}
    - Customer Name: {transaction_data['CustomerName']}
    - Customer SOF Name: {transaction_data['CustomerSOFName']}
    - Vehicle No.: {transaction_data['VehicleNo']}
    - Vehicle Colour: {transaction_data['VehicleColour']}
    - Car Model: {transaction_data['CarModel']}
    - RFID Tag No.: {transaction_data['RFIDTagNo']}
    - Reason: {transaction_data['Reason']}
    - Refund Amount: {transaction_data['RefundAmount']}
    - Total Refund Amount: {transaction_data['TotalRefundAmount']}
    - Refund Status: {transaction_data['RefundStatus']}
    - Response Code: {transaction_data['ResponseCode']}
    - Response Description: {transaction_data['ResponseDesc']}
    - Transaction Amount: {transaction_data['TransactionAmount']}
    - Highway Code: {transaction_data['HighwayCode']}
    - Service Provider ID (SPID): {transaction_data['SPID']}
    - Entry Location: {transaction_data['EntryLocation']}
    - Entry Service Provider Name: {transaction_data['EntrySPName']}
    - Exit Location: {transaction_data['ExitLocation']}
    - Exit Service Provider Name: {transaction_data['ExitSPName']}
    - Plaza Code: {transaction_data['PlazaCode']}
    - Organization Code (OrgCode): {transaction_data['OrgCode']}

    Date and Time Fields:
    - Invoice Date and Time: {transaction_data['InvoiceDateTime']}
    - Payment Date and Time: {transaction_data['PaymentDateTime']}
    - Received Date and Time: {transaction_data['ReceivedDateTime']}
    - Remark Date and Time: {transaction_data['RemarkDateTime']}
    - Response Date and Time: {transaction_data['ResponseDateTime']}
    - Tng Payment Date and Time: {transaction_data['TngPaymentDateTime']}

    Additional Information:
    - Actual Entry Class Vehicle: {transaction_data['ActualEntryClassVehicle']}
    - Actual Entry Lane: {transaction_data['ActualEntryLane']}
    - Actual Entry Plaza: {transaction_data['ActualEntryPlaza']}
    - Actual Exit Class Vehicle: {transaction_data['ActualExitClassVehicle']}
    - Actual Exit Lane: {transaction_data['ActualExitLane']}
    - Actual Exit Plaza: {transaction_data['ActualExitPlaza']}
    - Actual Fare: {transaction_data['ActualFare']}
    - Additional Info: {transaction_data['AdditionalInfo']}
    - Verify: {transaction_data['Verify']}
    - Service Provider Reason: {transaction_data['SPReason']}
    - Service Provider Reason Code: {transaction_data['SPReasonCode']}
    """


    # Convert to HTML
    html_content = f"""
    <html>
    <body>
        <h2>Transaction Details</h2>
        <ul>
            <li><strong>Transaction ID:</strong> {transaction_data['TransactionID']}</li>
            <li><strong>Batch Reference Number:</strong> {transaction_data['BatchRefNo']}</li>
            <li><strong>Transaction Date and Time:</strong> {transaction_data['TransactionDateTime']}</li>
            <li><strong>Customer Name:</strong> {transaction_data['CustomerName']}</li>
            <li><strong>Customer SOF Name:</strong> {transaction_data['CustomerSOFName']}</li>
            <li><strong>Vehicle No.:</strong> {transaction_data['VehicleNo']}</li>
            <li><strong>Vehicle Colour:</strong> {transaction_data['VehicleColour']}</li>
            <li><strong>Car Model:</strong> {transaction_data['CarModel']}</li>
            <li><strong>RFID Tag No.:</strong> {transaction_data['RFIDTagNo']}</li>
            <li><strong>Reason:</strong> {transaction_data['Reason']}</li>
            <li><strong>Refund Amount:</strong> {transaction_data['RefundAmount']}</li>
            <li><strong>Total Refund Amount:</strong> {transaction_data['TotalRefundAmount']}</li>
            <li><strong>Refund Status:</strong> {transaction_data['RefundStatus']}</li>
            <li><strong>Response Code:</strong> {transaction_data['ResponseCode']}</li>
            <li><strong>Response Description:</strong> {transaction_data['ResponseDesc']}</li>
            <li><strong>Transaction Amount:</strong> {transaction_data['TransactionAmount']}</li>
            <li><strong>Highway Code:</strong> {transaction_data['HighwayCode']}</li>
            <li><strong>Service Provider ID (SPID):</strong> {transaction_data['SPID']}</li>
            <li><strong>Entry Location:</strong> {transaction_data['EntryLocation']}</li>
            <li><strong>Entry Service Provider Name:</strong> {transaction_data['EntrySPName']}</li>
            <li><strong>Exit Location:</strong> {transaction_data['ExitLocation']}</li>
            <li><strong>Exit Service Provider Name:</strong> {transaction_data['ExitSPName']}</li>
            <li><strong>Plaza Code:</strong> {transaction_data['PlazaCode']}</li>
            <li><strong>Organization Code (OrgCode):</strong> {transaction_data['OrgCode']}</li>
        </ul>
        <h3>Date and Time Fields</h3>
        <ul>
            <li><strong>Invoice Date and Time:</strong> {transaction_data['InvoiceDateTime']}</li>
            <li><strong>Payment Date and Time:</strong> {transaction_data['PaymentDateTime']}</li>
            <li><strong>Received Date and Time:</strong> {transaction_data['ReceivedDateTime']}</li>
            <li><strong>Remark Date and Time:</strong> {transaction_data['RemarkDateTime']}</li>
            <li><strong>Response Date and Time:</strong> {transaction_data['ResponseDateTime']}</li>
            <li><strong>Tng Payment Date and Time:</strong> {transaction_data['TngPaymentDateTime']}</li>
        </ul>
        <h3>Additional Information</h3>
        <ul>
            <li><strong>Actual Entry Class Vehicle:</strong> {transaction_data['ActualEntryClassVehicle']}</li>
            <li><strong>Actual Entry Lane:</strong> {transaction_data['ActualEntryLane']}</li>
            <li><strong>Actual Entry Plaza:</strong> {transaction_data['ActualEntryPlaza']}</li>
            <li><strong>Actual Exit Class Vehicle:</strong> {transaction_data['ActualExitClassVehicle']}</li>
            <li><strong>Actual Exit Lane:</strong> {transaction_data['ActualExitLane']}</li>
            <li><strong>Actual Exit Plaza:</strong> {transaction_data['ActualExitPlaza']}</li>
            <li><strong>Actual Fare:</strong> {transaction_data['ActualFare']}</li>
            <li><strong>Additional Info:</strong> {transaction_data['AdditionalInfo']}</li>
            <li><strong>Verify:</strong> {transaction_data['Verify']}</li>
            <li><strong>Service Provider Reason:</strong> {transaction_data['SPReason']}</li>
            <li><strong>Service Provider Reason Code:</strong> {transaction_data['SPReasonCode']}</li>
        </ul>
    </body>
    </html>
    """    
    mail.send([email],'E-Refund Monitoring Info', text=text_content, html= html_content )    
    return custom_response('success', '', '', 200)


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
    data['seqno'] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data['updateby'] = 0
    data['responsedatetime'] = datetime.datetime.utcnow()

    insert_query = text('''
    INSERT INTO public."refund_reftrxdetails" ("orgcode", "highwaycode", "plazacode", "spid", "refno", "seqno", 
                                               "updateby", "codestatus", "reason", "responsedatetime")
    VALUES (:orgcode, :highwaycode, :plazacode, :spid, :refno, :seqno, :updateby, :codestatus, :reason, :responsedatetime)
    ''')

    print("Data to insert:", data)
    print("Insert query:", insert_query)

    try:
        with db.engine.begin() as connection:  # Using `begin` to ensure transaction commit
            connection.execute(insert_query, data)
        print("Insert successful")
        return custom_response('success', 'Detail added successfully', {}, 201)
    except Exception as e:
        print(f"Insert error: {e}")
        return custom_response('failure', str(e), {}, 500)
            
# @transaction_api.route('/add_detail', methods=['POST'])
# def add_refund_ref_trx_detail():
#     data = request.get_json()
#     data['seqno'] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     data['updateby'] = 0
#     data['responsedatetime'] = datetime.datetime.utcnow()

#     insert_query = text('''
#     INSERT INTO public."refund_reftrxdetails" ("orgcode", "highwaycode", "plazacode", "spid", "refno", "seqno", 
#                                                "updateby", "codestatus", "reason", "responsedatetime")
#     VALUES (:orgcode, :highwaycode, :plazacode, :spid, :refno, :seqno, :updateby, :codestatus, :reason, :responsedatetime)
#     ''')

#     print("Data to insert:", data)
#     print("Insert query:", insert_query)

#     try:
#         with db.engine.connect() as connection:
#             connection.execute(insert_query, data)
#         print("Insert successful")
#         return custom_response('success', 'Detail added successfully', {}, 201)
#     except Exception as e:
#         print(f"Insert error: {e}")
#         return custom_response('failure', str(e), {}, 500)

# Additional function to test database connection on the server
@transaction_api.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        with db.engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("Database connection successful:", result.fetchone())
            return custom_response('success', 'Database connection successful', {}, 200)
    except Exception as e:
        print(f"Database connection error: {e}")
        return custom_response('failure', str(e), {}, 500)



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