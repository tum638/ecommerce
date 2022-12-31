from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name='create_listing'),
    path("view_listing/<int:listing_id>", views.view_listing, name='view_listing'),
    path('add_to_watchlist/<int:listing_id>', views.add_to_watchlist, name='add_to_watchlist'),
    path('view_watchlist', views.view_watchlist, name='view_watchlist'),
    path('remove_from_watchlist/<int:listing_id>', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('bid/<int:listing_id>', views.bid , name='bid'),
    path('close_listing/<int:listing_id>', views.close_listing, name='close_listing'),
    path('add_comment/<int:listing_id>' , views.add_comment, name='add_comment')
    
]

