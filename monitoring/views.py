from django.http import HttpResponse
from django.shortcuts import render
from prometheus_client import generate_latest, CollectorRegistry, multiprocess
from prometheus_client.core import CollectorRegistry
# Create your views here.


def metrics_view(request):
    registry = CollectorRegistry()
    # If you run gunicorn with prometheus_multiproc_dir, you must use multiprocess to collect metrics.
    from prometheus_client import multiprocess
    multiprocess.MultiProcessCollector(registry)
    output = generate_latest(registry)
    return HttpResponse(output, content_type="text/plain; version=0.0.4")

def metrics_view(request):
    registry = CollectorRegistry()
try:
    multiprocess.MultiProcessCollector(registry)
except Exception:
    pass
    output = generate_latest(registry)
    return HttpResponse(output, content_type="text/plain; version=0.0.4")