from django.shortcuts import render,redirect
from .models import BookType,Book,Review,ReviewForm
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django import forms
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
#from .models import BookSerializer
from rest_framework.request import Request
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model=Book
		fields='__all__'



class BookViewSet(viewsets.ModelViewSet):
	queryset=Book.objects.all()
	serializer_class=BookSerializer
	

class SearchBar(forms.Form):
	searchbar=forms.CharField(max_length=100,label='')

def home(request):
	if request.method=="POST":
		form=SearchBar(request.POST)
		if form.is_valid():
			query=form.cleaned_data['searchbar']
			return redirect('searchresults',query)
		else:
			print("SearchBar form invalid")
			return redirect('home')
	form=SearchBar()
	cats=BookType.objects.values('category').distinct()
	lst=[]
	for i in cats:
		lst.append(i['category'])
	print(lst)
	context=dict()
	context['cats']=lst
	context['object_list']=BookType.objects.all().order_by('-issues')[:8]
	context['s_form']=form
	context['flag_home']=True
	return render(request,'library/home.html',context)

class BookTypeListView(ListView):
	model=BookType
	paginate_by=12

	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(*args,**kwargs)
		cats=BookType.objects.values('category').distinct()
		lst=[]
		for i in cats:
			lst.append(i['category'])
		print(lst)
		context['cats']=lst
		return context

class BookTypeDetailView(DetailView):
	model=BookType

	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(*args,**kwargs)
		print(self)
		print(self.object)
		reviews=Review.objects.filter(booktype=self.object)
		count,rating=0,0
		for i in reviews:
			rating+=i.rating
			count+=1
		if count>1:
			rating=round(rating/count,2)
		else:
			rating=4
		context['rating']=rating
		context['reviews']=reviews
		return context


class BookCreateView(UserPassesTestMixin,CreateView):
	model=BookType
	fields=['bookname','author','category','description','issues','image','pub_date']

	def test_func(self):
		if self.request.user.is_superuser:
			return True
		return False

class BookUpdateView(UserPassesTestMixin,UpdateView):
	model=BookType
	fields=['bookname','author','category','description','issues','image','pub_date']

	def test_func(self):
		if self.request.user.is_superuser:
			return True
		return False


class AddBooksForm(forms.Form):
	number=forms.IntegerField()

def addBooks(request,pk):
	obj=BookType.objects.filter(id=pk).first()
	if request.method=="POST":
		form=AddBooksForm(request.POST)
		if form.is_valid():
			num=form.cleaned_data['number']
			for i in range(num):
				Book.objects.create(booktype=obj)
			messages.success(request,"Books Added")
			return redirect('bookdetail',pk)
		else:
			print("Add books form invalid")
			print(form.errors)
	else:
		form=AddBooksForm()
	return render(request,'library/addbooks.html',{'form':form,'object':obj})

@login_required
def issue(request,pk):
	obj=BookType.objects.filter(id=pk).first()
	print(obj)
	if obj.quantity<1:
		print("Not enough stock")
		messages.error(request,"Not enough stock")
		return redirect('bookdetail',pk)
	book=Book.objects.filter(booktype=obj)
	book=book.filter(issued_by=None).first()
	book.issued_by=request.user
	book.issued_on=datetime.date.today()
	book.returndate=book.issued_on+datetime.timedelta(days=7)
	book.save()
	print("BOOK issued id:",book.id)
	messages.success(request,"Book Issued")
	obj.issues+=1
	obj.quantity-=1
	obj.save()
	return redirect('booklist')

def issuedbooks(request):
	obj=Book.objects.filter(issued_by=request.user)
	print(obj)
	lst=[]
	for i in obj:
		ob=BookType.objects.filter(bookname=i.booktype.bookname).first()
		print(ob)
		lst.append(ob)
	print(lst)
	flag=False
	if len(lst)==0:
		flag=True
	#returndate=obj.first().issued_on+datetime.timedelta(days=7*(obj.first().reissue+1))
	return render(request,'library/issuedbooks.html',{'books':lst,'flag':flag,'objects':obj})

def returnpage(request,pk):
	book=Book.objects.filter(id=pk).first()
	booktype=BookType.objects.filter(bookname=book.booktype.bookname).first()
	date=book.issued_on
	perday=2
	limit=7
	print(date,datetime.date.today())
	diff=datetime.date.today()-(date+datetime.timedelta(days=7*(book.reissue+1)))
	print(diff.days)
	fine=0
	if diff.days>0:
		fine+=perday*(diff.days)
	if fine>0:
		flag=True
	else:
		flag=False
	if request.method=="POST":
		form=ReviewForm(request.POST)
		if form.is_valid():
			ratings=form.cleaned_data['rating']
			reviews=form.cleaned_data['review']
			obj=Review.objects.create(rating=ratings,rev=reviews,booktype=booktype,user=request.user)
			obj.save()
		else:
			print("Review Form invalid")
			print(form.errors)
		return redirect('returnconfirm',pk)
	else:
		form=ReviewForm()
	return render(request,'library/return.html',{'book':book,'booktype':booktype,'fine':fine,'flag':flag,'days':diff.days,'form':form})


def returnconfirm(request,pk):
	book=Book.objects.filter(id=pk).first()
	booktype=BookType.objects.filter(bookname=book.booktype.bookname).first()
	book.issued_by=None
	book.issued_on=None
	book.reissue=0
	book.save()
	booktype.quantity+=1
	booktype.save()
	messages.success(request,"Book returned")
	return redirect('issuedbooks')


def reissue(request,pk):
	book=Book.objects.filter(id=pk).first()
	booktype=BookType.objects.filter(bookname=book.booktype.bookname).first()
	limit=3
	if book.reissue>=limit:
		messages.error(request,"You have re-issued book upto limit.Cannot re-issue again.Please return the book")
		return redirect('issuedbooks')
	book.reissue+=1
	book.returndate+=datetime.timedelta(days=7)
	book.save()
	messages.success(request,"Book reissued")
	return redirect('issuedbooks')

#Helper Function
def match(bookname,stringy):
	count=0
	for i in stringy.split():
		bname=[x.lower() for x in bookname.split()]
		if i.lower() in bname:
			count+=1
	return count

class SearchListView(ListView):
	model=BookType
	template_name='library/searchresults.html'
	paginate_by=12

	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(*args,**kwargs)
		stringy=self.kwargs['query']
		objects=BookType.objects.all()
		mapping=dict()
		for i in objects:
			bookname=i.bookname
			#nums=2
			nums=match(bookname,stringy)
			if nums>0:
				mapping[i]=nums
		answer=sorted(mapping,key=mapping.get)
		lst=[]
		for i in answer:
			lst.append(i)
		context['object_list']=lst
		print(lst)
		return context