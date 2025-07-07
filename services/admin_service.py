from repository.admin_repository import ImplAdminRepositoryInterface
from fastapi import HTTPException, status
from schemas.admin import AdminOut, AdminResponse, AdminCreate, AdminUpdate
from db.models import Admin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    def __init__(self, admin_repo: ImplAdminRepositoryInterface):
        self.admin_repo = admin_repo

    def authenticate_admin(self, email, password):
        admin = AdminOut.model_validate(self.admin_repo.get_admin_by_email(email))
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not pwd_context.verify(password, admin.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        return admin
    
    def get_all_admins(self):
        admins = [AdminResponse.model_validate(admin) for admin in self.admin_repo.get_all_admins()]
        return admins
    
    def create_admin(self, admin: AdminCreate, current_user: Admin):
        if current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action"
            )
        
        if self.admin_repo.get_admin_by_email(admin.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        new_admin = Admin(
            username=admin.username,
            email=admin.email,
            hashed_password=pwd_context.hash(admin.password),
            role=admin.role
        )
        return self.admin_repo.create_admin(new_admin)
    
    def update_admin(self, edit_id: int, data: AdminUpdate, current_user: Admin):
        admin_to_edit = self.admin_repo.get_admin_by_id(edit_id)
        if not admin_to_edit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
        
        if current_user.role.value == "operator" and current_user.id.value != edit_id:
            raise HTTPException(status_code=403, detail="Operators can only edit themselves")
        elif current_user.role.value != "admin" and current_user.id.value != edit_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = pwd_context.hash(update_data["password"])
        return self.admin_repo.update_admin(edit_id, update_data)
    
    def delete_admin(self, delete_id: int, current_user: Admin):
        to_delete = self.admin_repo.get_admin_by_id(delete_id)
        if not to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
        
        if current_user.role.value == "operator" and current_user.id.value != delete_id:
            raise HTTPException(status_code=403, detail="Operators can only delete themselves")
        elif current_user.role.value != "admin" and current_user.id.value != delete_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        return self.admin_repo.delete_admin(delete_id)