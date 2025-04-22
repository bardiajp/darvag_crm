from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from accounts.views import CustomTokenObtainPairView, RegisterView, ProtectedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('order.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
