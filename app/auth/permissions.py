from fastapi import Depends, HTTPException, status
from app.models.user import User, UserRole
from app.auth.jwt_handler import get_current_user


def _role_guard(*allowed_roles: UserRole):
    """Factory that returns a FastAPI dependency enforcing one of the given roles."""
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Access denied. Required role(s): "
                    f"{', '.join(r.value for r in allowed_roles)}. "
                    f"Your role: {current_user.role.value}."
                ),
            )
        return current_user
    return dependency


# Convenience dependencies ─ use these in routers
require_any_role = Depends(get_current_user)                         # authenticated only

require_analyst_or_above = _role_guard(UserRole.analyst, UserRole.admin)
require_admin = _role_guard(UserRole.admin)

# Viewer can access dashboard; analyst and admin can also access it
require_dashboard_access = _role_guard(
    UserRole.viewer, UserRole.analyst, UserRole.admin
)
