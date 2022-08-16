from rest_framework.serializers import ModelSerializer
from base.models import Room, Option


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'
