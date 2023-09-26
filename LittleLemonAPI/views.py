from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth.models import User, Group
from .serializers import (
    CartSerializer,
    UserSerializer,
    MenuItemSerializer,
    CategorySerializer,
    OrderSerializer,
)
from rest_framework import generics, permissions
from .models import MenuItem, Category, Cart, Order
from .permissions import IsManagerOrAdmin, IsManager, IsDeliveryCrew


# Create your views here.
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Only Managers Should See This"})
    else:
        return Response({"message": "You are not authorized"}, 403)


@api_view(["POST", "DELETE"])
@permission_classes([IsAdminUser])
def manager(request):
    username = request.data["username"]
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == "POST":
            managers.user_set.add(user)
        elif request.method == "DELETE":
            managers.user_set.remove(user)
        return Response({"message": "ok"})

    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if request.user.groups.filter(name="Manager").exists():
        username = request.data["username"]
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew = Group.objects.get(name="Delivery crew")
            if request.method == "POST":
                delivery_crew.user_set.add(user)
            elif request.method == "DELETE":
                delivery_crew.user_set.remove(user)
            return Response({"message": "ok"})

        return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"message": "You are not authorized"}, 403)


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def order(request):
    if request.user.groups.filter(name="Manager").exists():
        username = request.data["username"]
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew = Group.objects.get(name="Delivery crew")
            if request.method == "POST":
                delivery_crew.user_set.add(user)
            elif request.method == "DELETE":
                delivery_crew.user_set.remove(user)
            return Response({"message": "ok"})

        return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"message": "You are not authorized"}, 403)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def access_manager_group(request):
    try:
        manager_group = Group.objects.get(name="Manager")
    except Group.DoesNotExist:
        return Response(
            {"message": "Manager group does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Get a list of users in the Manager group
    manager_users = manager_group.user_set.all()

    # Serialize the user data using UserSerializer
    serializer = UserSerializer(manager_users, many=True)
    return Response(
        {
            "message": "Admin access to Manager group granted",
            "manager_users": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ["price", "category"]
    filterset_fields = ["price"]
    search_fields = ["title"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManagerOrAdmin()]
        return super(MenuItemsView, self).get_permissions()


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsManagerOrAdmin()]
        if self.request.method == "DELETE":
            return [IsManagerOrAdmin()]
        return super(SingleMenuItemView, self).get_permissions()


class CartItemCreate(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        menu_item_id = self.request.data.get("menuitem")
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        user = self.request.user
        serializer.save(user=user, menuitem=menu_item)


class OrderItemCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        delivery_crew_id = self.request.data.get("delivery_crew")
        delivery_crew = User.objects.get(pk=delivery_crew_id)
        user = self.request.user
        serializer.save(user=user, delivery_crew=delivery_crew)

class ManagerOrderDeliveryCrew(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsManager]
    
class DeliveryCrewOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsDeliveryCrew] 
    
class DeliveryUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsDeliveryCrew] 

class CustomerCreateOrder(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]   

    def get_queryset(self):
        # Return only the orders that belong to the currently authenticated customer
        return Order.objects.filter(user=self.request.user)
