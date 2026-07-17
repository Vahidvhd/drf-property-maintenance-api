from rest_framework import serializers
from .models import Property, MaintenanceRequest, RequestComment



class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']

class RequestCommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = RequestComment
        fields = [
            "id",
            "request",
            "author",
            "author_username",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "author", "created_at"]


class MaintenanceRequestListSerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source="property", read_only = True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    class Meta:
        model = MaintenanceRequest
        fields = [
            'id',
            'property',
            'property_detail',
            'created_by',
            'created_by_username',
            'title',
            'category',
            'priority',
            'status',
            'created_at',
                  ]
        read_only_fields = ['id', 'created_by', 'created_at']




class MaintenanceRequestDetailSerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source="property", read_only=True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    comments = RequestCommentSerializer(many=True, read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = [
            "id",
            "property",
            "property_detail",
            "created_by",
            "created_by_username",
            "title",
            "description",
            "category",
            "priority",
            "status",
            "created_at",
            "updated_at",
            "comments",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class MaintenanceRequestCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields =  [
            "id",
            "property",
            "title",
            "description",
            "category",
            "priority",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]