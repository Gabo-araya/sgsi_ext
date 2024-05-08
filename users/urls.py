""" this document defines the users app urls """

from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path

from users.views import groups as group_views
from users.views import users as user_views

group_urlpatterns = [
    path(
        "",
        group_views.GroupListView.as_view(),
        name="group_list",
    ),
    path(
        "create/",
        group_views.GroupCreateView.as_view(),
        name="group_create",
    ),
    path(
        "<int:pk>/",
        group_views.GroupDetailView.as_view(),
        name="group_detail",
    ),
    path(
        "<int:pk>/update/",
        group_views.GroupUpdateView.as_view(),
        name="group_update",
    ),
    path(
        "<int:pk>/delete/",
        group_views.GroupDeleteView.as_view(),
        name="group_delete",
    ),
]

user_urlpatterns = [
    path(
        "",
        user_views.UserListView.as_view(),
        name="user_list",
    ),
    path("<int:pk>/", user_views.UserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/update/", user_views.UserUpdateView.as_view(), name="user_update"),
    path("<int:pk>/delete/", user_views.UserDeleteView.as_view(), name="user_delete"),
    path("login/", user_views.LoginView.as_view(), name="login"),
    path(
        "password-change/",
        user_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        user_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "register/",
        user_views.UserCreateView.as_view(),
        name="register",
    ),
    path(
        "password-reset/",
        user_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "reset/<uidb64>/<token>/",
        user_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "verify/<uidb36>/<token>/",
        user_views.user_new_confirm,
        name="user_new_confirm",
    ),
    path(
        "reset/done/",
        user_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password-reset/done/",
        user_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path("edit/", user_views.UserProfileEditView.as_view(), name="user_profile_edit"),
    path("profile/", user_views.UserProfileView.as_view(), name="user_profile"),
]

urlpatterns = [
    path("accounts/", include(user_urlpatterns)),
    path("groups/", include(group_urlpatterns)),
]
