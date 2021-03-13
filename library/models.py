from django.db import models
from PIL import Image
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms
# Create your models here.


class BookType(models.Model):
	bookname=models.CharField(max_length=50)
	author=models.CharField(max_length=40)
	category=models.CharField(max_length=50)
	description=models.TextField()
	issues=models.IntegerField()
	image=models.ImageField(default='defaultbook.jpg',upload_to='bookimages')
	pub_date=models.CharField(max_length=10,default="2000-01-01")
	publication_date=models.DateField(null=True,blank=True)
	#rating=models.DecimalField()
	quantity=models.IntegerField(default=0)

	def __str__(self):
		return f"BookName:{self.bookname},author:{self.author},Category:{self.category}"

	def save(self,*args,**kwargs):
		stringy=str(self.pub_date)
		y,m,d=[int(x) for x in stringy.split('-')]
		dt=datetime.date(y,m,d)
		self.publication_date=dt

		super().save(*args,**kwargs)
		img=Image.open(self.image.path)
		output_size=(200,300)
		img=img.resize(output_size)
		img.save(self.image.path)

	def get_absolute_url(self):
		return reverse('bookdetail',kwargs={'pk':self.pk})



class Book(models.Model):
	booktype=models.ForeignKey(BookType,on_delete=models.CASCADE)
	issued_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	issued_on=models.DateField(null=True,blank=True)
	issuedate=models.CharField(max_length=10,null=True,blank=True)
	reissue=models.IntegerField(default=0)
	returndate=models.DateField(null=True,blank=True)

	def save(self,*args,**kwargs):
		self.booktype.quantity+=1
		self.booktype.save()
		super().save(*args,**kwargs)

	def __str__(self):
		return f"Book object of  {self.booktype.bookname}"


class Review(models.Model):
	rating=models.IntegerField()
	rev=models.CharField(max_length=150,null=True,blank=True)
	booktype=models.ForeignKey(BookType,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return f"Review of {self.booktype.bookname}"

class ReviewForm(forms.Form):
	RATING_CHOICES=[(1,1),(2,2),(3,3),(4,4),(5,5)]
	rating=forms.IntegerField(widget=forms.Select(choices=RATING_CHOICES))
	review=forms.CharField(max_length=150,required=False)