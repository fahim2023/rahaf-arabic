from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """Log in with email address (case-insensitive) or username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        if username is None:
            username = kwargs.get("email")
        if not username or not password:
            return None
        user = (
            User.objects.filter(email__iexact=username).order_by("id").first()
            or User.objects.filter(username__iexact=username).first()
        )
        if user is None:
            User().set_password(password)  # equalise timing
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
