from rest_framework import permissions

class IsAdminFull(permissions.BasePermission):
    """
    Allocates full access to Superusers (Admin).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsStaffOrAdmin(permissions.BasePermission):
    """
    Allocates access to Staff and Superusers.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to public, but write access only to Admin.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to public, but write access only to Staff/Admin.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_staff or request.user.is_superuser)

class BookingPermission(permissions.BasePermission):
    """
    Custom permission for Bookings:
    - POST: AllowAny (Public)
    - GET/PUT/PATCH/DELETE: Staff or Admin only
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        # For other methods (GET, PUT, DELETE), require staff/admin
        return request.user and (request.user.is_staff or request.user.is_superuser)
