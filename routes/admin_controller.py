from fastapi import APIRouter, Depends, status
from schemas.admin import AdminResponse, AdminCreate, AdminUpdate
from typing import List
from auth import dependencies
from services.admin_service import AdminService
from services.dependencies import get_admin_service

router = APIRouter(tags=["Admins"])


## Get all users
@router.get("/admin", response_model=List[AdminResponse])
async def get_all_user(
    admin_service: AdminService = Depends(get_admin_service),
    current_user=Depends(dependencies.get_current_user),
):
    return admin_service.get_all_admins()


## Create User only by admin
@router.post("/admin", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    new_admin: AdminCreate,
    admin_service: AdminService = Depends(get_admin_service),
    current_user=Depends(dependencies.get_current_user),
):
    return admin_service.create_admin(new_admin, current_user)


## Edit User Credientials
@router.patch("/admin/edit/{edit_id}", response_model=AdminResponse)
async def edit_user(
    edit_id: int,
    admin_update: AdminUpdate,
    admin_service: AdminService = Depends(get_admin_service),
    current_user=Depends(dependencies.get_current_user),
):
    updated = admin_service.update_admin(edit_id, admin_update, current_user)
    return updated


## Delete User Admin delete any record, Operator allow self-deletion
@router.delete("/admin/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    admin_id,
    admin_service: AdminService = Depends(get_admin_service),
    current_user=Depends(dependencies.get_current_user),
):
    admin_service.delete_admin(admin_id, current_user)
    return
