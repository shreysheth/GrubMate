from fastapi import APIRouter

from models.api_response import ApiResponseModel
from models.auth import SignUpModel, LoginModel
from utils.sql.mongo_operations import create_document, get_user_by_email, authernticate_user

router = APIRouter()


@router.post("/signup", response_model=ApiResponseModel)
def signup(user: SignUpModel):
    if user.password != user.confirm_password:
        return ApiResponseModel(
            status=400, message="Passwords do not match", is_error=True
        ).to_dict()

    existing_user = get_user_by_email(user.email)
    if existing_user:
        return ApiResponseModel(
            status=409, message="User already exists", is_error=True
        ).to_dict()

    result = create_document("users", user.to_dict())

    return ApiResponseModel(
        data=result, message="User created successfully", is_error=False, status=200
    ).to_dict()


@router.post("/login", response_model=ApiResponseModel)
def login(user: LoginModel):
    existing_user = authernticate_user(user.email, user.password)
    if not existing_user:
        return ApiResponseModel(message="Invalid credentials",status=401, is_error=True).to_dict()

    existing_user["_id"] = str(existing_user["_id"])

    return ApiResponseModel(
        message="Login successful", data=existing_user, status=200, is_error=False
    ).to_dict()
