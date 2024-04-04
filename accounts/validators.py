from django.core.exceptions import ValidationError
import os


def allow_only_images_validators(value):
    ext=os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions=['.png','.jpg','.jpeg','.png'.upper(),'.jpg'.upper(),'.jpeg'.upper()]
    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension, Allows extension" +str(valid_extensions))