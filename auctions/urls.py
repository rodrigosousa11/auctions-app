from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path('close_listing/<int:listing_id>/', views.close_listing, name='close_listing'),
    path('add_watchlist/<int:listing_id>/', views.add_watchlist, name='add_watchlist'),
    path('remove_watchlist/<int:listing_id>/', views.remove_watchlist, name='remove_watchlist'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('categories', views.categories, name='categories'),
    path('category/<str:category_name>/', views.category_listings, name='category_listings')
]
