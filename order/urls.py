from django.urls import path
from .views import QuoteView

urlpatterns = [
    path('quote-details/<int:pk>', QuoteView.as_view(), name='quote'),
]