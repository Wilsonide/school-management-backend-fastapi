from pydantic import BaseModel, EmailStr


class SchoolOnboardingRequest(BaseModel):
    # School

    school_name: str
    website: str | None = None

    address: str
    state: str

    phone: str
    whatsapp_number: str | None = None

    description: str | None = None

    average_fee_range: str | None = None
    population_range: str | None = None

    referral_source: str | None = None

    # Admin

    admin_first_name: str
    admin_last_name: str

    admin_email: EmailStr
    admin_password: str
