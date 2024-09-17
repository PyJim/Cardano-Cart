from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),  # Include the users app's URLs
    path('api/v1/products/', include('products.urls')), # Include the products app)
    path('api/v1/orders/', include('orders.urls')), # Include the orders app
    path('api/v1/cart/', include('cart.urls')), # Include the cart app
    path('api/v1/', include('reviews.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

