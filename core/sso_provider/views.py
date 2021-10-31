from functools import partial
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4
import xml.etree.ElementTree as ET
from domain_user.models import Domain


def index(request):
    return render(request, "sso_provider/sso.html")


def vid(request):
    return render(request, "sso_provider/get_vid_test.html")


def data(request):
    return render(request, "sso_provider/get_data_test.html")


def ekyc(request):
    return render(request, "sso_provider/get_ekyc_test.html")
def uploadekyc(request):
    return render(request, "sso_provider/upload_ekyc.html")


@api_view(["GET"])
def get_captcha(request):
    """
    used to generate captcha

    Method
    ------
    GET

    Returns
    -------
    Response
        data = {
            "status": "Success",
            "captchaBase64String": "xxxxx",                     # base64 encoded string of a photo
            "captchaTxnId": "JQ7lDnCazDEO",
            "requestedDate": "2021-10-29",
            "statusCode": 200,
            "message": "SUCCESS",
        }
    """

    try:
        data = requests.post(
                "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/get/captcha",
                json={"langCode": "en", "captchaLength": "3", "captchaType": "2"},
                headers={"Content-Type": "application/json"},
            ).text
        print(str(data))
        data = json.loads(data)
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def get_otp(request):
    """
    used to generate otp

    Method
    ------
    POST
        Parameters
        ----------
            uid: uid or aadhaar number of the user
            captchaTxnId: captchaTxnId generated during captcha creation
            captcha_value: value of the captcha entered byt he user

    Returns
    -------
    Response
        data = {
            "uidNumber": xxxxx,
            "mobileNumber": 0,
            "txnId": "mAadhaar:xxx-xxxx-xx-xx-xxx",
            "status": "Success",
            "message": "OTP generation done successfully",
        }
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
            "transactionId": f"MYAADHAAR:{txn_ID}",
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

    Method
    ------
    POST
        Parameters
        ----------
            uid: uid or aadhaar number of the user
            mobile_no: mobile number of the user
            otp: otp received by the user
            txnId: txnId generated during otp creation

    Returns
    -------
    Response
        data = {
            "status": "Success",
            "vid": "xxxxx",
            "message": "Successfully generated the Vid for Aadhaar: xxxxx",
            "ErrorCode": None,
        }
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
    Used to get all the data of a user

    Method
    ------
    POST
        Parameters
        ----------
            uid: uid or aadhaar number of the user
            otp: otp received by the user
            txnId: txnId generated during otp creation

    Returns
    -------
    Response
        data = {
            "poi": {
                "dob": "dd-mm-yyyy",
                "gender": "M",
                "name": "xxxxx",
                "phone": "xxxxxxxxxx",
            },
            "poa": {
                "co": "C/O Barnali Guha Ghosh Dastidar",
                "country": "India",
                "dist": "Kolkata",
                "house": "75",
                "lm": "BEHIND 8B BUS STAND",
                "pc": "700032",
                "state": "West Bengal",
                "street": "IBRAHIMPUR ROAD",
                "vtc": "Jadavpur University",
            },
            "photo": "xxxxx"                                    # base64 encoded string of a photo
        }
    """

    try:
        if(request.data["uid"]):
            uid = request.data["uid"]
            vid = ""
        else:
            uid = request.data["vid"]
            vid = request.data["vid"]
        body = {
            "txnId": request.data["txnId"],
            "otp": request.data["otp"],
            "uid": uid,
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
        # 'vid', 'personal_data', 'address', 'photo'
        data["personal_data"] = poi
        data["address"] = poa
        data["photo"] = photo_base64
        data["vid"] = vid
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def get_ekyc(request):
    """
    Used to get offline eKyc zip file of a user

    Method
    ------
    POST
        Parameters
        ----------
            uid: uid or aadhaar number of the user
            otp: otp received by the user
            txnId: txnId generated during otp creation
            password: password for the zip file given by the user

    Returns
    -------
        data = {
            "eKycXML": "xxxxx",                                 # base64 encoded string of offline eKyc zip file of a user
            "fileName": "offlineaadhaarxxxxx.zip",
            "status": "Success",
            "requestDate": "2021-10-28",
            "uidNumber": "xxxxx",
        }
    """
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


def scan_qr(request):
    return render(request, "sso_provider/scan_qr.html")


@csrf_exempt
@api_view(["POST"])
def post_qr(request):
    """
    Used to post data of a user

    Method
    ------
    POST
        Parameters
        ----------
            eKycXML: content of the xml file
            apiKey: apiKey of the QR scan

    Returns
    -------
        data = { "status": "Success", "message": "Successfully uploaded the file" }
    """
    try:
        print(request.data)
        domain = Domain.objects.filter(
            domain_key=request.data["apiKey"]
        )
        if domain:
            # print(domain)
            body = {
                "eKycXML": request.data["eKycXML"],
            }
            requests.post(
                domain[0].ekycxml_endpoint,
                headers={"Content-Type": "application/json"},
                json=body,
            )
            return Response(
                data={"status": "Success", "message": "Successfully uploaded the file"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={"status": "Failure", "message": "Invalid API key"},
            )
    except Exception as e:
        print(e)
        return Response(
            data={
                "status": "Error",
                "message": "Error occured while uploading the file",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
