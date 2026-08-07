import requests
import json
from django.conf import settings


class ZarinPalSandbox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://localhost:8000/payment/verify"

    def __init__(self, merchant_id=settings.MERCHANT_ID):
        self.merchant_id = merchant_id

    def payment_request(self, amount, description="پرداختی کاربر"):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "callback_url": self._callback_url,
            "description": description,
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self._payment_request_url, json=payload, headers=headers
        )
        return response.json()

    def payment_verify(self, amount, authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": int(amount),
            "authority": authority,
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self._payment_verify_url, json=payload, headers=headers
        )
        return response.json()

    def generate_payment_url(self, authority):
        return f"{self._payment_page_url}{authority}"
