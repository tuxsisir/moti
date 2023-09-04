from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ChoiceField,
    CharField,
    IntegerField,
    ValidationError,
    BooleanField,
)

from people.models import User, UserRelation

BLANK_CHOICE = (("", "---------"),)


class UserThinSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class UserRelationSerializer(ModelSerializer):
    source = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=False,
        required=True,
        write_only=True,
        allow_null=False,
    )
    target = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=False,
        required=True,
        write_only=True,
        allow_null=False,
    )

    class Meta:
        model = UserRelation
        fields = ("source", "target", "relation_type",)

    def validate(self, data):
        validated_data = super().validate(data)
        source = validated_data["source"]
        target = validated_data["target"]
        if source == target:
            raise ValidationError(
                {
                    "relation": "Cannot assign relation to same person."
                }
            )
        return validated_data


    def to_representation(self, instance):
        if self.context["request"].method == "GET":
            self.fields["source"] = UserThinSerializer()
            self.fields["target"] = UserThinSerializer()
        return super().to_representation(instance)


class UserSerializer(ModelSerializer):
    name = CharField(required=True)
    age = IntegerField(required=True, min_value=1, max_value=99)
    relations = UserThinSerializer(read_only=True, many=True)

    # source = PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     many=False,
    #     required=False,
    #     write_only=True,
    #     allow_null=True,
    # )
    # target = PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     many=False,
    #     required=False,
    #     write_only=True,
    #     allow_null=True,
    # )
    # relation_type = ChoiceField(
    #     choices=BLANK_CHOICE + UserRelation.RELATION_TYPES, write_only=True
    # )
    # new_source = BooleanField(write_only=True)
    # new_target = BooleanField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "age",
            "relations"
        )

#     def validate(self, data):
#         validated_data = super().validate(data)
#         new_source = validated_data["new_source"]
#         new_target = validated_data["new_target"]
#         source = validated_data["source"]
#         target = validated_data["target"]
#         relation_type = validated_data["relation_type"]
#         if all([new_source, new_target]):
#             raise ValidationError(
#                 {
#                     "source": "Please select either new user as source or target but not BOTH."
#                 }
#             )
#
#         if not all([new_source, new_target]) and any([source, target, relation_type]) and not all(
#             [source, target, relation_type]
#         ):
#             raise ValidationError(
#                 {
#                     "relation": "All the fields (source, target, relation) are required."
#                 }
#             )
#
#         return validated_data
#
#     def create(self, validated_data):
#         new_source = validated_data.pop("new_source")
#         new_target = validated_data.pop("new_target")
#         source = validated_data.pop("source")
#         target = validated_data.pop("target")
#         relation_type = validated_data.pop("relation_type")
#         created = User.objects.create(**validated_data)
#         if new_source:
#             source = created
#         elif new_target:
#             target = created
#
#         if all([source, target, relation_type]):
#             UserRelation.objects.create(
#                 source=source, target=target, relation_type=relation_type
#             )
#         return created

#
#    def get_relation_help(self, instance):
#        if instance.relation:
#            return f"{instance.username} is {instance.relation_type} of {instance.relation.username}"
#        return f""
#
#    def validate(self, data):
#        validated_data = super().validate(data)
#        relation = validated_data.get("relation")
#        relation_type = validated_data.get("relation_type")
#
#        if relation and not relation_type:
#            raise ValidationError("Relation type is required for every relation added.")
#
#        return data

# class UserSerializer(ModelSerializer):
#     relations = UserThinSerializer(many=True)
#     as_a_target = UserRelationSerializer(many=True)
#     class Meta:
#         model = User
#         fields = ("id", "username", "relations", "as_a_target")
#
