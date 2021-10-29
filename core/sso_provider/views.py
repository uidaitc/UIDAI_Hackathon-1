from django.shortcuts import render
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4
import xml.etree.ElementTree as ET


def index(request):
    return render(request, "sso_provider/index.html")


def vid(request):
    return render(request, "sso_provider/get_vid_test.html")


def data(request):
    return render(request, "sso_provider/get_data_test.html")


def ekyc(request):
    return render(request, "sso_provider/get_ekyc_test.html")


@api_view(["GET"])
def get_captcha(request):
    """
    used to generate captcha
    """
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
    """
    used to generate otp
    """
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
            "transactionId": "MYAADHAAR:59142477-3f57-465d-8b9a-75b28fe48725",
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
    """
    used to generate vid for a user
    """
    try:
        body = {
            "uid": request.data["uid"],
            "mobile": request.data["mobile_no"],
            "otp": request.data["otp"],
            "otpTxnId": request.data["txnId"],
        }
        data = json.loads(
            requests.post(
                "https://stage1.uidai.gov.in/vidwrapper/generate",
                json=body,
                headers={"Content-Type": "application/json"},
            ).text
        )
        print(data)
        return Response(data=data)
    except Exception as e:
        print(e)
        return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def get_data(request):
    """
    Used to get the data of a user
    """
    try:
        body = {
            "txnId": request.data["txnId"],
            "otp": request.data["otp"],
            "uid": request.data["uid"],
        }
        data = json.loads(
            requests.post(
                "https://stage1.uidai.gov.in/onlineekyc/getEkyc/",
                headers={"Content-Type": "application/json"},
                json=body,
            ).text
        )
        print(data)
        data = ET.fromstring(data["eKycString"])[1]

        poi = data[0].attrib
        # *** poi format ***
        # {"dob": "dd-mm-yyyy", "gender": "M", "name": "xxxxx", "phone": "xxxxxxxxxx"}

        poa = data[1].attrib
        # *** poa format ***
        # {
        #     "co": "C/O Barnali Guha Ghosh Dastidar",
        #     "country": "India",
        #     "dist": "Kolkata",
        #     "house": "75",
        #     "lm": "BEHIND 8B BUS STAND",
        #     "pc": "700032",
        #     "state": "West Bengal",
        #     "street": "IBRAHIMPUR ROAD",
        #     "vtc": "Jadavpur University",
        # }
        photo_base64 = data[3].text
        data = dict()
        data["poi"] = poi
        data["poa"] = poa
        data["photo"] = photo_base64
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def get_ekyc(request):
    try:
        body = {
            "txnNumber": request.data["txnId"],
            "otp": request.data["otp"],
            "shareCode": request.data["password"],  # 4digits only
            "uid": request.data["uid"],
        }
        data = json.loads(
            requests.post(
                "https://stage1.uidai.gov.in/eAadhaarService/api/downloadOfflineEkyc",
                headers={"Content-Type": "application/json"},
                json=body,
            ).text
        )
        print(data)
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
