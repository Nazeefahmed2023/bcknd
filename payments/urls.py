from django.urls import path
from .views import CreateRazorpayOrderView, RazorpayWebhookView


urlpatterns = [
path('create/', CreateRazorpayOrderView.as_view()),
path('webhook/', RazorpayWebhookView.as_view()),
]