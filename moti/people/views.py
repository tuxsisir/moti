from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from people.models import User, UserRelation
from people.serializers import UserSerializer, UserRelationSerializer


# Create your views here.
class UserAPI(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=["get"], url_path="nodes")
    def nodes(self, _):
        queryset = self.filter_queryset(self.get_queryset())
        relations = UserRelation.objects.all()

        nodes = self.build_nodes(queryset)
        edges = self.build_edges(relations)

        return Response({"nodes": nodes, "edges": edges})

    def build_nodes(self, queryset):
        nodes = {}
        for user in queryset:
            nodes[f"{user.username}"] = {
                "username": user.username,
                "name": user.name,
                "age": user.age,
                "active": False,
                "id": user.id,
            }
        return nodes

    def build_edges(self, relations):
        edges = {}
        for edge in relations:
            key = f"edge{edge.id}"
            edges[key] = {
                "id": edge.id,
                "source": edge.source.username,
                "target": edge.target.username,
                "label": edge.relation_type
            }
        return edges


class RelationAPI(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    model = UserRelation
    serializer_class = UserRelationSerializer
    queryset = UserRelation.objects.all()


class TestAPIResponse(APIView):
    def get(self, *args, **kwargs):
        return Response({"test": "success"})
