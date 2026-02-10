from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    # avoid clashing with existing legacy app `accounts`
    label = "core_accounts"


