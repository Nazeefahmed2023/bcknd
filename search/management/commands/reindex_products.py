from django.core.management.base import BaseCommand
from search.documents import ProductDocument


class Command(BaseCommand):
    help = 'Reindex all products'


def handle(self, *args, **options):
    ProductDocument().update()
    self.stdout.write('Reindex triggered')