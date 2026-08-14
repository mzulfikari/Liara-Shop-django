from django.urls import path
from . import views

app_name = "Profile"

urlpatterns = [
    path("profile/view", views.UserProfile,name="Profile_View"),
    path("profile/address", views.AddressView.as_view(),name="Address"),
    path("profile/address/add", views.Address_Add.as_view(),name="Address_add"),
    path("profile/change", views.Change_profile,name="ChangeProfile"),
    path("profile/change/password",views.ChangePasswordView.as_view(),name="ChangePassword", ),
    path("profile/notifications", views.NotificationList.as_view(),name="Notification"),
    path("profile/comment", views.CommentViews.as_view(),name="CommentViews"),
    path("profile/comment/delete/<int:comment_id>/", views.DeleteCommentView.as_view(),name="DeleteCommentView",),
    path("profile/favorite", views.FavoriteViews.as_view(),name="FavoriteViews"),
    path("order/list/",views.CustomerOrderListView.as_view(),name="order-list"),
    path("order/<int:pk>/detail",views.CustomerOrderDetailView.as_view(),name="order-detail"),
]
