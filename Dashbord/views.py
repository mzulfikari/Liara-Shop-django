from django.contrib.auth import logout
from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, View, TemplateView
from .forms import AddressAdd, Change_Password, Change_Profile
from .models import *
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from Products.models import Comment


@login_required
def UserProfile(request):
    user = request.user
    context = {
        "profile": user,
    }
    return render(request, "profile/profile.html", context)


@login_required
def Change_profile(request):
    user = request.user
    form = Change_Profile(instance=user)
    if request.method == "POST":
        form = Change_Profile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات با موفقیت ویرایش شد.")
            print(type(request))
            return redirect("Profile:Profile_View")
    return render(request, "profile/profile-change.html", {"form": form})


class NotificationList(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user

        Notification.delete_expired_notifications()

        now = timezone.now()
        notifications = (
            Notification.objects.filter(is_active=True)
            .filter(Q(is_for_all_users=True) | Q(users=user))
            .filter(Q(expiration_date__isnull=True) | Q(expiration_date__gte=now))
            .distinct()
            .order_by("-created_at")
        )

        return render(
            request,
            "profile/notification.html",
            {
                "notifications": notifications,
            },
        )


class AddressView(LoginRequiredMixin, ListView):
    template_name = "profile/profile-address.html"
    model = Address
    context_object_name = "Address"

    def post(self, request):
        user = request.user

        if "delete_address" in request.POST:
            address_id = request.POST.get("delete_address")
            address = get_object_or_404(Address, pk=address_id, user=user)
            address.delete()

        elif "set_default" in request.POST:
            address_id = request.POST.get("set_default")
            address = get_object_or_404(Address, pk=address_id, user=user)

            Address.objects.filter(user=user, is_default=True).update(is_default=False)

            address.is_default = True
            address.save()

        return redirect("Profile:Address")


class Address_Add(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        if Address.objects.filter(user=user).count() >= 3:
            messages.error(request, "شما فقط می‌توانید ۳ آدرس ثبت کنید.")
            return redirect("Profile:Address")

        form = AddressAdd(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user

            address.save()

            return redirect("Profile:Address")
        else:
            return render(request, "profile/profile-address-edit.html", {"form": form})

    def get(self, request):
        form = AddressAdd()
        return render(request, "profile/profile-address-edit.html", {"form": form})


class ChangePasswordView(LoginRequiredMixin, FormView):

    template_name = "profile/change-password.html"
    form_class = Change_Password
    success_url = reverse_lazy("account:Login-user")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        old_password = form.cleaned_data["old_password"]
        new_password = form.cleaned_data["new_password"]

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(self.request, user)
            logout(self.request)
            messages.success(
                self.request,
                "رمز عبور شما با موفقیت تغییر یافت. لطفاً با رمز عبور جدید وارد شوید.",
            )
            return super().form_valid(form)

        else:
            form.add_error("old_password", "رمز عبور فعلی نادرست است.")
            return self.form_invalid(form)


class CommentViews(ListView):

    model = Comment
    template_name = "profile/profile-comments.html"
    context_object_name = "comments"
    paginate_by = 4

    def get_queryset(self):
        return Comment.objects.filter(
            user=self.request.user, parent__isnull=True
        ).order_by("-created_at")


class DeleteCommentView(View):

    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get("comment_id")
        comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
        comment.delete()
        return redirect("Profile:CommentViews")


class FavoriteViews(ListView):

    model = Favorites
    template_name = "profile\profile-favorites.html"
    context_object_name = "favorites"
    paginate_by = 4

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user).order_by("-created_at")
