from rest_framework import routers

from django.urls import path, include
from people.views import UserAPI, TestAPIResponse, RelationAPI

router = routers.DefaultRouter()
router.register(r"users", UserAPI)
router.register(r"relation", RelationAPI)

urlpatterns = [
    path("", include(router.urls)),
    path("test", TestAPIResponse.as_view(), name="response"),
]
