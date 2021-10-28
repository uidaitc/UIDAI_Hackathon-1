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

def get_eKYC(txn_ID: str, otp: str, password: str, uid: str) -> Response:
    body = {
        "txnNumber": txn_ID,
        "otp": otp,
        "shareCode": password, #4digits only
        "uid": uid,
    }
    return requests.post(
        "https://stage1.uidai.gov.in/eAadhaarService/api/downloadOfflineEkyc",
        headers={"Content-Type": "application/json"},
        json=body,
    )


# print(get_captcha().text)

# print(generate_OTP("D4dQHohdVfN4", "6vh2j1", "999918760558").text)
# with open("file.txt", "w+") as f:
#     f.write(get_eKYC("mAadhaar:0aa66355-f817-4f26-b31a-c23adfc20fbe", "913795", "1234", "999918760558").text)