from fastapi import FastAPI
from pydantic import BaseModel, Field

from .normalizer import normalize_email, normalize_phone

app = FastAPI(title="Contact Cleanser API", version="1.0.0",
              description="Normalize contact details without persisting request data.")


class ContactRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    phone: str = Field(min_length=3, max_length=64)
    region: str = Field(default="US", min_length=2, max_length=2, pattern=r"^[A-Za-z]{2}$")


@app.get("/health", tags=["service"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/contacts/validate", tags=["contacts"])
def validate_contact(payload: ContactRequest) -> dict[str, object]:
    email_result = normalize_email(payload.email)
    phone_result = normalize_phone(payload.phone, payload.region)
    return {"email": email_result, "phone": phone_result,
            "valid": bool(email_result["valid"] and phone_result["valid"])}
