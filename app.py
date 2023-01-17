import json
import os
import mercadopago

def lambda_handler(event, context):
    sdk = mercadopago.SDK(os.environ.get("ACCESS_TOKEN"))
    
    data = json.loads(event["body"])

    payment_data = {
        "transaction_amount": float(data["transaction_amount"]),
        "token": data["token"],
        "installments": int(data["installments"]),
        "payment_method_id": data["payment_method_id"],
        "issuer_id": data["issuer_id"],
        "payer": {
            "email": data["payer"]["email"],
            "identification": {
                "type": data["payer"]["identification"]["type"],
                "number": data["payer"]["identification"]["number"],
            },
        },
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    print("status =>", payment["status"])
    print("status_detail =>", payment["status_detail"])
    print("id =>", payment["id"])

    return {
        "statusCode": 201,
        "body": json.dumps({"status": payment["status"], "status_detail": payment["status_detail"], "id": payment["id"]})
    }

