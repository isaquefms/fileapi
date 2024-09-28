from .models import File
from rest_framework.serializers import Serializer, FileField, ModelSerializer


class FileSerializer(ModelSerializer):
    """Definição da apresentação do modelo File na api.
    """
    
    class Meta:
        model = File
        fields = ['file']


class BillingSerializer(Serializer):
    """Definição da apresentação do modelo Billing na api.
    """
    
    class Meta:
        fields = ['file', 'name', 'government_id', 'email', 'debt_amount', 'debt_due_date', 'debt_id', 'status']
