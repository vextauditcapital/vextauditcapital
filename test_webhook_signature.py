import urllib.request
import json
import hmac
import hashlib

url = "https://script.google.com/macros/s/AKfycbxihuqTbKLbt6bdCnbO2nI8htEJh1rMcVdztQko_TYSfpZUqDbZpKP2a0uY_ASztU5DDQ/exec"
secret = "aweS7hK5_nrAL7W"

# Simulated Razorpay payment.captured webhook payload
webhook_payload = {
    "entity": "event",
    "account_id": "acc_BF4948f949",
    "event": "payment.captured",
    "contains": ["payment"],
    "payload": {
        "payment": {
            "entity": {
                "id": "pay_WARROOM1234567",
                "entity": "payment",
                "amount": 2500000,  # INR 25,000 in paise
                "currency": "INR",
                "status": "captured",
                "order_id": "order_WARROOM123",
                "invoice_id": None,
                "international": False,
                "method": "card",
                "amount_refunded": 0,
                "refund_status": None,
                "captured": True,
                "description": "GST Audit & Compliance - War Room Live Webhook Verification",
                "card_id": "card_123",
                "bank": None,
                "wallet": None,
                "vpa": "warroom@upi",
                "email": "warroom@test.com",
                "contact": "+1234567890",
                "notes": {
                    "client_name": "War Room Live Test",
                    "service": "GST Audit & Compliance",
                    "ref_no": "VAC-2026-99999"
                },
                "fee": 500,
                "tax": 90,
                "error_code": None,
                "error_description": None,
                "created_at": 1780336692
            }
        }
    },
    "created_at": 1780336692
}

try:
    print("Testing simulated Razorpay webhook signature calculation...")
    raw_body = json.dumps(webhook_payload)
    
    # Calculate HMAC-SHA256 signature
    signature = hmac.new(
        secret.encode("utf-8"),
        raw_body.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    print(f"Calculated Signature: {signature}")
    
    # Send request with the computed signature in the URL parameter
    webhook_url = f"{url}?x-razorpay-signature={signature}"
    data_bytes = raw_body.encode("utf-8")
    
    req = urllib.request.Request(
        webhook_url,
        data=data_bytes,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        body = response.read().decode("utf-8")
        print(f"Webhook POST Status Code: {status_code}")
        print(f"Webhook POST Response Body: {body}")
        
except Exception as e:
    print(f"Webhook POST failed: {e}")
