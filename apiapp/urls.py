# core/urls.py
from django.urls import path
from .views import CreateProfileView, ProfileDetailView, ProfileListView

urlpatterns = [
    # 🔹 Create profile (POST)
    path('create-profile/', CreateProfileView.as_view()),

    # 🔹 Get all profiles (GET)
    path('all-profiles/', ProfileListView.as_view()),

    # 🔹 Single profile (GET + DELETE)
    path('profile/<uuid:id>/', ProfileDetailView.as_view()),
]