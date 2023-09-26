from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("manager-view", views.manager_view),
    path("api/token/login", obtain_auth_token),
    path("groups/manager/users", views.manager),
    path("groups/manager/users", views.delivery_crew),
    path("groups/managers", views.access_manager_group),
    path("menu-items", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    path("categories", views.CategoriesView.as_view()),
    path("cart-items", views.CartItemCreate.as_view()),
    path("order-items", views.OrderItemCreate.as_view()),
    path("manager-assign-order", views.ManagerOrderDeliveryCrew.as_view()),
    path("delivery-order", views.DeliveryCrewOrderView.as_view()),
    path("delivery-order-update", views.DeliveryUpdateView.as_view()),
    path("customer-orders", views.CustomerCreateOrder.as_view()),
]
