from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
def list_users():
    return [
        {"id": "1", "email": "admin@proofpath.example", "role": "admin", "active": True},
        {"id": "2", "email": "reviewer@proofpath.example", "role": "reviewer", "active": True},
    ]
