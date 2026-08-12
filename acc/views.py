from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from .serializers import LoginSerializer, UserSerializer,RegisterSerializer
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from doc.models import Document
from django.contrib.auth.decorators import login_required


#login
@api_view(["POST"])
@permission_classes([AllowAny])
def api_login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )

    if user is None:
        return Response(
            {"message": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response(UserSerializer(request.user).data)


#register
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=201,
        )

    return Response(serializer.errors, status=400)


#change password
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    user = request.user

    if not user.check_password(old_password):
        return Response(
            {"message": "Old password is incorrect"},
            status=400,
        )

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password changed successfully"})

#update user data
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserSerializer(
        request.user,
        data=request.data,
        partial=True
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

def home(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    return redirect("login")




def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:

            login(request, user)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "auth/login.html",
    )


from django.contrib.auth.models import User
from django.contrib import messages


def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        User.objects.create_user(
            username=username,
            first_name=first_name,
            email=email,
            password=password,
        )

        messages.success(request, "Account created successfully.")

        return redirect("login")

    return render(
        request,
        "auth/register.html",
    )





def logout_view(request):

    logout(request)

    return redirect("login")




from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .models import Profile


@login_required
def profile(request):

    profile = request.user.profile

    if request.method == "POST":

        request.user.first_name = request.POST["first_name"]

        request.user.last_name = request.POST["last_name"]

        request.user.email = request.POST["email"]

        request.user.username = request.POST["username"]

        profile.phone = request.POST["phone"]

        if request.FILES.get("avatar"):

            profile.avatar = request.FILES["avatar"]

        request.user.save()

        profile.save()

        messages.success(
            request,
            "Profile Updated Successfully"
        )

        return redirect("profile")

    total_documents = Document.objects.filter(
        owner=request.user
    ).count()

    recent_documents = Document.objects.filter(
        owner=request.user
    ).order_by("-created_at")[:5]

    return render(
        request,
        "dashboard/profile.html",
        {
            "profile": profile,
            "total_documents": total_documents,
            "recent_documents": recent_documents,
        },
    )

from django.contrib.auth.forms import PasswordChangeForm


@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password Updated."
            )

        else:

            messages.error(
                request,
                "Invalid Password."
            )

    return redirect("profile")