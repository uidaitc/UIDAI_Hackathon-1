from django.shortcuts import render
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4


def index(request):
    return render(request, "captcha.html")


@api_view(["GET"])
def get_captcha(request):
    try:
        data = json.loads(
            requests.post(
                "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/get/captcha",
                json={"langCode": "en", "captchaLength": "3", "captchaType": "2"},
                headers={"Content-Type": "application/json"},
            ).text
        )
        print(data)
        return Response(data=data, status=status.HTTP_200_OK)
    except:
        return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def get_otp(request):
    if request.method == "POST":
        try:
            txn_ID = str(uuid4())
            headers = {
                "x-request-id": txn_ID,
                "appid": "MYAADHAAR",
                "Accept-Language": "en_in",
                "Content-Type": "application/json",
            }
            body = {
                "uidNumber": request.data["uid"],
                "captchaTxnId": request.data["captchaTxnId"],
                "captchaValue": request.data["captcha_value"],
                "transactionId": "MYAADHAAR:" + txn_ID,
            }
            data = json.loads(
                requests.post(
                    url="https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/generate/aadhaar/otp",
                    json=body,
                    headers=headers,
                ).text
            )
            print(data)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def get_vid(request):
    body = {
        "uid": request.data["uid"],
        "mobile": request.data["mobile_no"],
        "otp": request.data["otp_value"],
        "otpTxnId": request.data["txnId"],
    }
    data = json.loads(requests.post(
        "https://stage1.uidai.gov.in/vidwrapper/generate",
        json=body,
        headers={"Content-Type": "application/json"},
    ).text)
    print(data)
    return Response(data=data)
