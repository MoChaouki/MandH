from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from . views import payment_completed_view
from . views import payment_failed_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-completed/', payment_completed_view, name="payment-completed"),
    path('payment-failed/', payment_failed_view, name="payment-failed"),
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Your store URLs

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import include
