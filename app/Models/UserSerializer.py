from Models.UserModel import User


def user_serializer(user: User) -> dict:
    """
    Convert a User database object into a JSON-safe dictionary.
    Same idea as customer_serializer() in your Customer microservice.
    """
    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "role": user.role,
    }
