"""healthid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from .apps.authentication.views import activate, PasswordResetView
from .views import HandleCSV, HandleCsvExport, EmptyProductCsvExport

admin.site.site_header = "HealthID Admin"
admin.site.site_title = "HealthID Admin"
admin.site.index_title = "Welcome to HealthID"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthid/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('healthid/activate/<uidb64>/<token>', activate, name='activate'),
    path('healthid/csv/<param>', HandleCSV.as_view(), name='handle_csv'),
    path('healthid/export_csv/<param>', HandleCsvExport.as_view(),
         name='export_csv'),
    path('healthid/sample_product_csv', EmptyProductCsvExport.as_view(),
         name='export_product_csv'),
    path('healthid/password_reset/<uidb64>/<token>',
         csrf_exempt(PasswordResetView.as_view()), name='password_reset')
]
