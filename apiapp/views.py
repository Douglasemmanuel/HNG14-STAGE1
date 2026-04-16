from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer, CreateProfileSerializer
from .services import get_gender, get_age, get_nationality, classify_age



class CreateProfileView(APIView):
    def post(self, request):
        serializer = CreateProfileSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"status": "error", "message": "Invalid type"},
                status=422
            )

        raw_name = serializer.validated_data.get("name", "")
        name = raw_name.strip().lower()

        if not name:
            return Response(
                {"status": "error", "message": "Missing or empty name"},
                status=400
            )

        # Idempotency
        existing = Profile.objects.filter(name=name).first()
        if existing:
            return Response({
                "status": "success",
                "message": "Profile already exists",
                "data": ProfileSerializer(existing).data
            })

        try:
            gender_data = get_gender(name)
            age_data = get_age(name)
            country_data = get_nationality(name)

        except Exception:
            return Response(
                {
                    "status": "error",
                    "message": "External API returned an invalid response"
                },
                status=502
            )

        profile = Profile.objects.create(
            name=name,
            gender=gender_data["gender"],
            gender_probability=gender_data["probability"],
            sample_size=gender_data["count"],
            age=age_data["age"],
            age_group=classify_age(age_data["age"]),
            country_id=country_data["country_id"],
            country_probability=country_data["probability"]
        )

        return Response({
            "status": "success",
            "data": ProfileSerializer(profile).data
        }, status=201)

class ProfileDetailView(APIView):
    def get(self , request , id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(
                 {"status": "error", "message": "Profile not found"},
                status=404
            )
        
        return Response({
            "status": "success",
            "data": ProfileSerializer(profile).data
        })
    
    def delete(self , request , id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=404
            )
        profile.delete()
        return Response(status=204)
    



class ProfileListView(APIView):

    def get(self,request):
        qs = Profile.objects.all()
        gender = request.GET.get("gender")
        country = request.GET.get("country_id")
        age_group = request.GET.get("age_group")

        if gender:
            qs = qs.filter(gender__iexact=gender)
        if country:
            qs = qs.filter(country_id__iexact=country)
        if age_group:
            qs = qs.filter(age_group__iexact=age_group)


        data = [
            {
                "id": str(p.id),
                "name": p.name,
                "gender": p.gender,
                "age": p.age,
                "age_group": p.age_group,
                "country_id": p.country_id
            }
            for p in qs
        ]

        return Response({
            "status": "success",
            "count": qs.count(),
            "data": data
        })