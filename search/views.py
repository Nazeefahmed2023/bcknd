from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django_elasticsearch_dsl.search import Search
from search.documents import ProductDocument
from catalog.models import Product
from catalog.serializers import ProductSerializer


class SearchView(APIView):
    def get(self, request):
        q = request.GET.get('q', '')

        if not q:
            return Response({'results': []})

        # Elasticsearch query
        s = ProductDocument.search().query(
            'multi_match',
            query=q,
            fields=['title', 'description']
        )[:50]

        hits = s.execute()

        # extract IDs from elasticsearch hits
        ids = [int(h.meta.id) for h in hits]

        # fetch products from DB
        products = list(Product.objects.filter(id__in=ids))

        # preserve order
        products_map = {p.id: p for p in products}
        ordered = [products_map.get(i) for i in ids if products_map.get(i)]

        return Response({
            'results': ProductSerializer(ordered, many=True).data
        })
