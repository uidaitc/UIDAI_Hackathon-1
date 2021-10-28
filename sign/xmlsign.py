from datetime import datetime
from lxml import etree
from signxml import XMLSigner, XMLVerifier

# uid="12345678"
# ts=datetime.now().strftime("%Y-%m-%dT%X")
# data_to_sign = f'<?xml version="1.0" encoding="UTF-8"?><ns2:Otp xmlns:ns2="http://www.uidai.gov.in/authentication/otp/1.0" ac="public" lk="MAElpSz56NccNf11_wSM_RrXwa7n8_CaoWRrjYYWouA1r8IoJjuaGYg" sa="public" ts="{ts}" txn="test" type="A" uid="{uid}" ver="2.5"><Opts ch="01"/></ns2:Otp>'.encode('utf-8')
# cert = open("cer.pem").read()
# key = open("key.key").read()
# # load OpenSSL.crypto
# # data_to_sign = "<test/>"
# root = etree.fromstring(data_to_sign)

# signed_root = XMLSigner().sign(root, key=key, cert=cert)
# print(etree.tostring(signed_root))
# verified_data = XMLVerifier().verify(signed_root).signed_xml
# print(verified_data)

from datetime import datetime
from lxml import etree
from requests.models import Response
from signxml import XMLSigner
import requests


def generate_OTP(url,data_to_sign,uid: str = "999918760558") -> Response:
    urls = {
        0:f"https://otp-stage.uidai.gov.in/uidotpserver/2.5/public/{uid[0]}/{uid[1]}/MEY2cG1nhC02dzj6hnqyKN2A1u6U0LcLAYaPBaLI-3qE-FtthtweGuk",
        1:f"https://vid-stage.uidai.gov.in/uidauthvidserviceinboundsms/vidserviceinbound/1.0/{uid[0]}/{uid[1]}",
    }
    url=urls[url]
    ts = datetime.now().strftime("%Y-%m-%dT%X")
    cert = open("cer.pem").read()
    key = open("key.key").read()
    # load OpenSSL.crypto
    # data_to_sign = "<test/>"
    root = etree.fromstring(data_to_sign)
    # return root
    signed_root = XMLSigner().sign(root, key=key, cert=cert)
    xml = etree.tostring(signed_root)
    # verified_data = XMLVerifier().verify(signed_root).signed_xml
    # print(verified_data)
    headers = {"Content-Type": "application/xml"}
    return requests.post(url,
        data=xml,
        headers=headers,
    )
data_to_sign = f'<?xml version="1.0" encoding="UTF-8"?><ns2:Otp xmlns:ns2="http://www.uidai.gov.in/authentication/otp/1.0" ac="public" lk="MAElpSz56NccNf11_wSM_RrXwa7n8_CaoWRrjYYWouA1r8IoJjuaGYg" sa="public" ts="{ts}" txn="test" type="A" uid="{uid}" ver="2.5"><Opts ch="01"/></ns2:Otp>'.encode(
        "utf-8"
    )

print(generate_OTP(1,data_to_sign).text)
# from lxml import objectify
# root = generate_OTP()
# obj = objectify.fromstring(etree.tostring(root))