
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel, ValidationError, EmailStr, HttpUrl

class Validator:
    """Generic validation utilities leveraging Pydantic models."""

    @staticmethod
    def validate(model: Type[BaseModel], data: Dict[str, Any]) -> BaseModel:
        """Validate `data` against a Pydantic `model` and return instance."""
        return model(**data)

class UserSchema(BaseModel):
    """Example schema."""
    email: EmailStr
    website: Optional[HttpUrl] = None

def main() -> None:
    try:
        ok = Validator.validate(UserSchema, {"email": "x@y.com", "website": "https://a.b"})
        print("Valid:", ok.model_dump())
    except ValidationError as e:
        print("Invalid:", e)

if __name__ == "__main__":
    main()
