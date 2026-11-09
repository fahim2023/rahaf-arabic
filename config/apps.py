from django.contrib.admin.apps import AdminConfig


class RahafAdminConfig(AdminConfig):
    default_site = "config.admin.RahafAdminSite"


def rename_auth_section():
    """Show Django's built-in 'Authentication and Authorization' as 'All accounts'."""
    from django.apps import apps
    apps.get_app_config("auth").verbose_name = "All accounts"
