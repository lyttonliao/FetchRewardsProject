from rest_framework import viewsets
from core.models import Payer
from payers.serializers import PayerSerializer


class PayerViewSet(viewsets.ModelViewSet):
    """Viewset to Create, List, Retrieve, Delete Payer"""
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer