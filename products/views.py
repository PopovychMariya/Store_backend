from .models import Product
from .serializers import PreviewSerializer, DetailsSerializer
from rest_framework import viewsets

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PreviewSerializer
        return DetailsSerializer