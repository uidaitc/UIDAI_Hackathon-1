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
    txn_ID = uuid4()
    headers = {
        "x-request-id": str(txn_ID),
        "appid": "MYAADHAAR",
        "Accept-Language": "en_in",
        "Content-Type": "application/json",
    }
    body = {
        "uidNumber": uid_number,
        "captchaTxnId": captcha_txn_id,
        "captchaValue": captcha_value,
        "transactionId": "MYAADHAAR:"+str(txn_ID),
    }
    return requests.post(
        url="https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/generate/aadhaar/otp",
        json=body,
        headers=headers,
    )


def generate_VID(uid: str, mobile_no: str, otp: str, txn_ID: str):
    body = {"uid": uid, "mobile": mobile_no, "otp": otp, "otpTxnId": txn_ID}
    return requests.post(
        "https://stage1.uidai.gov.in/vidwrapper/generate",
        json=body,
        headers={"Content-Type": "application/json"},
    )


# print(get_captcha().text)
# {"status":"Success","captchaBase64String":"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","captchaTxnId":"Vl4KBH04PVmd","requestedDate":"2021-10-27","statusCode":200,"message":"SUCCESS"}
# print(generate_OTP("xz0p6RGWFViL", "XNoPAl", "999918760558").text)
# {"uidNumber":999918760558,"mobileNumber":0,"txnId":"mAadhaar:d747e572-b173-4cc1-a7af-603742dc16cd","status":"Success","message":"OTP generation done successfully"}

print(
    generate_VID(
        "999918760558",
        "8697307367",
        "650598",
        "mAadhaar:681576b7-3fba-4f15-8697-5c422b0d5f33",
    ).text
)
# {"status":"Success","vid":"9189003736522532","message":"Successfully generated the Vid for Aadhaar: 999918760558","ErrorCode":null}