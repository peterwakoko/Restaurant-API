from rest_framework import permissions
from django.contrib.auth.models import Group


class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        manager_group = Group.objects.get(name="Manager")
        return manager_group in request.user.groups.all()


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        manager_group = Group.objects.get(name="Manager")
        return manager_group in request.user.groups.all()
    
class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        delivery_group = Group.objects.get(name="Delivery crew")
        return delivery_group in request.user.groups.all()