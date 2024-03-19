from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        super(AccountsConfig,self).ready()
        import accounts.signals
        

# def ready(self):
#     import accounts.signals