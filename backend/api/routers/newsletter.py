from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from blog.models import Subscriber
from ..deps import verify_unsubscribe_token

router = APIRouter()


class SubscribeRequest(BaseModel):
    email: EmailStr


@router.post("/subscribe", status_code=201)
def subscribe(data: SubscribeRequest):
    _, created = Subscriber.objects.get_or_create(email=data.email)
    if not created:
        raise HTTPException(status_code=400, detail="Already subscribed")
    return {"message": "Subscribed successfully"}


@router.get("/unsubscribe")
def unsubscribe(token: str):
    email = verify_unsubscribe_token(token)
    deleted, _ = Subscriber.objects.filter(email=email).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Email not found")
    return {"message": "Unsubscribed successfully"}
