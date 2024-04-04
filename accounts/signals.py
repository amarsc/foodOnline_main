from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import User,UserProfile
    
@receiver(post_save, sender=User)    
def post_save_create_profile_reciever(sender,instance,created,**kwargs):
    print(created)
    if created:
        print('create the user profile')
        UserProfile.objects.create(user=instance)
        print("user profile is created")
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
            
        except:
            UserProfile.objects.create(user=instance)
            print("profile is not exist ,but created one")
    print("user is updated")
    
    
# Connect receiver to sender
#post_save.connect(post_save_create_profile_reciever,sender=User)
    
@receiver(pre_save,sender=User)    
def pre_save_profile_receiver(sender,instance,**kwargs):
    print(instance.username,'this user is save')

