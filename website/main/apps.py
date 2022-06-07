from tokenize import group
from django.apps import AppConfig
from django.conf import settings

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.contrib.auth.models import Group
        from django.db.models.signals import post_save

        # Vo fkcii prida user do groupy
        def add_to_default_group(sender, **kwargs):
            user = kwargs["instance"]
            if kwargs["created"]:
                group, ok = Group.objects.get_or_create(name="default")
                group.user_set.add(user)

        # Vzdy ked sa vytvori user tak sa prida to default skupiny a zavola fkciu hore
        post_save.connect(add_to_default_group, sender=settings.AUTH_USER_MODEL)