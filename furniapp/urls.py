from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
 
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('remove_from_cart/<int:order_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('user-login/', auth_views.LoginView.as_view(template_name='user_login.html'), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/complete/', views.order_confirmation, name='checkout_complete'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('upload-product/', views.upload_product, name='upload_product'),
    path('view-cart/', views.view_cart, name='view_cart'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)