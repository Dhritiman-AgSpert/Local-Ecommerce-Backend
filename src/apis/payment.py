from fastapi import Request, APIRouter, HTTPException
from typing import Any, Dict

import razorpay

import json

client = razorpay.Client(auth=("rzp_test_vdMDnNv4ti7PPY", "pma6yie7E9PKpyriozPweyLU"))


router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):
    try:
        request_data: Dict[str, Any] = await request.json()
        print(request_data)
        return {"message": "Webhook received"}
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")


@router.post("/create_order")
async def create_order():
    return client.order.create({
        "amount": 50000,
        "currency": "INR",
        "receipt": "receipt#1",
        "partial_payment":False,
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    })