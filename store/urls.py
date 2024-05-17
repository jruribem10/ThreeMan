from django.urls import path
from .import views
from .views import filter_products
from .views import ProductListView
urlpatterns=[
    path('', views.home,name='home'),
    path('about/', views.about,name='about'),
    path('login/', views.login_user,name='login'),
    path('logout/', views.logout_user,name='logout'),
    path('register/', views.register_user,name='register'),
    path('update_user/', views.update_user,name='update_user'),
    path('update_password/', views.update_password,name='update_password'),
    path('update_info/', views.update_info,name='update_info'),
    path('product/<int:pk>', views.product,name='product'),
    path('category/<str:foo>', views.category,name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search,name='search'),
    path('filter/', filter_products, name='filter_products'),
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('set_language/', views.set_language, name='set_language'),
]