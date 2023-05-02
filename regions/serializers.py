# rest framework
# others libraries
from rest_framework import serializers

from regions.models import Commune


class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = (
            "id",
            "name",
        )
