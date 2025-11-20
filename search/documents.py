from django_elasticsearch_dsl import Document, Index, fields
from catalog.models import Product


products_index = Index('products')
products_index.settings(number_of_shards=1, number_of_replicas=0)


@products_index.document
class ProductDocument(Document):
    title = fields.TextField()
    description = fields.TextField()
    price = fields.FloatField()

    class Django:
        model = Product
        fields = ['id', ]
