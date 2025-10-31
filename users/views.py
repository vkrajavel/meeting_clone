from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .serializers import UserSerializer

# =============================
# COMMON OPENAPI PARAMS / AUTH
# =============================

bearer_auth = openapi.Parameter(
    name='Authorization',
    in_=openapi.IN_HEADER,
    description='JWT Authorization header. Example: "Bearer <your_token>"',
    type=openapi.TYPE_STRING,
)

# =============================
# USER LIST (ADMIN ONLY)
# =============================
class UserListView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=[bearer_auth],
        responses={200: UserSerializer(many=True)},
        operation_summary="List all users (Admin only)",
        operation_description="Retrieve a list of all users. Requires admin privileges.",
        tags=['User Management']
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# =============================
# USER DETAIL (AUTH REQUIRED)
# =============================
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[bearer_auth],
        responses={
            200: UserSerializer(),
            404: 'User not found'
        },
        operation_summary="Get user by ID",
        operation_description="Retrieve a user's details by ID. Requires authentication.",
        tags=['User Management']
    )
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# =============================
# CREATE USER (ADMIN ONLY)
# =============================
class UserCreateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=[bearer_auth],
        request_body=UserSerializer,
        responses={
            201: 'User created successfully',
            400: 'Invalid data'
        },
        operation_summary="Create new user (Admin only)",
        operation_description="Allows an admin to create a new user.",
        tags=['User Management']
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================
# UPDATE USER (AUTH REQUIRED)
# =============================
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[bearer_auth],
        request_body=UserSerializer,
        responses={
            200: 'User updated successfully',
            400: 'Invalid data',
            404: 'User not found'
        },
        operation_summary="Update user details",
        operation_description="Allows an authenticated user to update their details (or an admin to update any user).",
        tags=['User Management']
    )
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User updated'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# =============================
# DELETE USER (ADMIN ONLY)
# =============================
class UserDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=[bearer_auth],
        responses={
            204: 'User deleted successfully',
            404: 'User not found'
        },
        operation_summary="Delete a user (Admin only)",
        operation_description="Deletes a user by ID. Requires admin privileges.",
        tags=['User Management']
    )
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
