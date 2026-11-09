from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Students & invite codes"

    def ready(self):
        from config.apps import rename_auth_section
        rename_auth_section()
