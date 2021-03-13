from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	email=models.EmailField(default="")
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	image=models.ImageField(default='default.jpg',upload_to='profile-pics')
	address=models.TextField(default="None")
	contact=models.CharField(default="97******19",max_length=12)

	def __str__(self):
		return f"{self.user.username} Profile"

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img=Image.open(self.image.path)
		if img.height>300 or img.width>300:
			output_size=(300,300)
			img=img.resize(output_size)
			img.save(self.image.path)