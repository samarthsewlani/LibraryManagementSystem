from django.urls import path,include
from . import views
from .views import BookTypeListView,BookTypeDetailView,BookCreateView,BookUpdateView,SearchListView

from rest_framework import routers
from .views import BookViewSet

#router=routers.DefaultRouter()
#router.register(r'books',BookViewSet.as_view({'get':'list'}),basename="bookviewset")

urlpatterns = [
    path('',views.home,name="home"),
    path('booklist/',BookTypeListView.as_view(),name='booklist'),
    path('book/<int:pk>/',BookTypeDetailView.as_view(),name='bookdetail'),
    path('bookcreate/',BookCreateView.as_view(),name='bookcreate'),
    path('bookupdate/<int:pk>/',BookUpdateView.as_view(),name='bookupdate'),
    path('bookadd/<int:pk>/',views.addBooks,name='bookadd'),
    path('issue/<int:pk>/',views.issue,name='issue'),
    path('issuedbooks/',views.issuedbooks,name='issuedbooks'),
    path('return/<int:pk>/',views.returnpage,name='return'),
    path('returnconfirm/<int:pk>/',views.returnconfirm,name='returnconfirm'),
    path('reissue/<int:pk>/',views.reissue,name='reissue'),
    path('searchresults/<str:query>/',SearchListView.as_view(),name='searchresults'),
    path('booksapi/',BookViewSet.as_view({'get':'list'})),


]
