from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout', views.signout, name='logout'),
    path('doc/create', views.registerdoc, name='registerdoc'),
    path('doc/search', views.searchdoc, name='searchdoc'),
    path('doc/update/<int:doc_id>', views.updatedoc, name='updatedoc'),
    path('doc/delete/<int:doc_id>', views.deletedoc, name='deletedoc'),
    path('doc/preview/<int:doc_id>', views.previewdoc, name='previewdoc'),
]
