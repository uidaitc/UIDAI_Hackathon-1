import requests
from requests.models import Response
from uuid import uuid4


def get_captcha() -> Response:
    return requests.post(
        "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/get/captcha",
        json={"langCode": "en", "captchaLength": "3", "captchaType": "2"},
        headers={"Content-Type": "application/json"},
    )

def generate_OTP(captcha_txn_id: str, captcha_value: str, uid_number: str) -> Response:
    txn_ID = str(uuid4())
    headers = {
        "x-request-id": txn_ID,
        "appid": "MYAADHAAR",
        "Accept-Language": "en_in",
        "Content-Type": "application/json",
    }
    body = {
        "uidNumber": uid_number,
        "captchaTxnId": captcha_txn_id,
        "captchaValue": captcha_value,
        "transactionId": "MYAADHAAR:59142477-3f57-465d-8b9a-75b28fe48725",
    }
    return requests.post(
        url="https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/generate/aadhaar/otp",
        json=body,
        headers=headers,
    )

def get_eKYC(txn_ID: str, otp: str, uid: str) -> Response:
    body = {
        "txnId": txn_ID,
        "otp": otp,
        "uid": uid,
    }
    return requests.post(
        "https://stage1.uidai.gov.in/onlineekyc/getEkyc/",
        headers={"Content-Type": "application/json"},
        json=body,
    )


# print(get_captcha().text)

# print(generate_OTP("ZHlsm8BDcPdb", "yFFLw3", "999918760558").text)
with open("online_ekyc.txt", "w+") as f:
    f.write(get_eKYC("mAadhaar:70f32fad-50d4-4b78-9fc3-887706695d53", "396483", "999918760558").text)