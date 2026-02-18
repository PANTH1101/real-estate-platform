from django.urls import path

from .views import WishlistAddView, WishlistListView, WishlistRemoveView


urlpatterns = [
    path("wishlist/", WishlistListView.as_view()),
    path("wishlist/add/", WishlistAddView.as_view()),
    path("wishlist/remove/<uuid:property_id>/", WishlistRemoveView.as_view()),
]


