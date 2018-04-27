from django.apps import AppConfig


class NewadminConfig(AppConfig):
    name = 'newadmin'

    def ready(self):
        super(NewadminConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules("yg")