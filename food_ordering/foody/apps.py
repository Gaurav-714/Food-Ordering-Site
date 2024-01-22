from django.apps import AppConfig


class FoodyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foody'
    
    def ready(self):
        def cart_count(self):
            from .models import CartItems
            return CartItems.objects.filter(cart__is_paid = False, cart__user = self).count()
        
        from django.contrib.auth.models import User
        User.add_to_class("cart_count", cart_count)