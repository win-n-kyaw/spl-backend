from fastapi import APIRouter, HTTPException, Depends, status
from auth import utils
from schemas.user import UserResponse, UserCreate, UserShow, UserUpdate
from typing import List
from db.session import get_db
from db.models import Admin
from auth import jwt

router = APIRouter(tags=["Admins"])


## Get all users
@router.get("/admin", response_model=List[UserShow])
async def get_all_user(
    db=Depends(get_db), current_user: Admin = Depends(jwt.get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not Authorized to perform this action",
        )
    users = db.query(Admin).all()
    return users


## Create User only by admin
@router.post("/admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db=Depends(get_db),
    current_user: Admin = Depends(jwt.get_current_user),
):
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to perform this action",
        )

    # Check if email already exists
    if db.query(Admin).filter(Admin.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = Admin(
        username=user.username,
        email=user.email,
        hashed_password=utils.hash_password(user.password),
        role=user.role.value,  # type: ignore
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


## Edit User Credientials
@router.patch("/admin/edit/{admin_id}", response_model=UserShow)
async def edit_user(
    admin_id: int,
    user_update: UserUpdate,
    db=Depends(get_db),
    current_user: Admin = Depends(jwt.get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not Authorized to perform this action",
        )
    user_to_edit = db.query(Admin).filter(Admin.id == admin_id).first()

    if not user_to_edit:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role == "operator" and current_user.id != admin_id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operators can only edit their own account",
        )
    elif current_user.role != "admin" and current_user.id != admin_id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this account",
        )

    update_data = user_update.model_dump(exclude_unset=True)
    # Hash the password if provided
    if "password" in update_data:
        update_data["password"] = utils.hash_password(update_data["password"])
    # Apply updates
    for key, value in update_data.items():
        setattr(user_to_edit, key, value)
    db.commit()
    db.refresh(user_to_edit)

    return user_to_edit


## Delete User Admin delete any record, Operator allow self-deletion
@router.delete("/admin/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    admin_id, db=Depends(get_db), current_user: Admin = Depends(jwt.get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not Authorized to perform this action",
        )

    user_to_delete = db.query(Admin).filter_by(id=admin_id).first()
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {admin_id} not found",
        )
    # Role-based access control
    if current_user.role == "operator" and current_user.id != admin_id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operators can only delete their own account",
        )
    elif current_user.role != "admin" and current_user.id != admin_id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this account",
        )

    db.delete(user_to_delete)
    db.commit()
    return
