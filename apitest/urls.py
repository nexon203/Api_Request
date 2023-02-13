from django.urls import path
from apitest.views import index, api_request, DATAView

urlpatterns = [
    path('', index, name='index'),
    path('testdata/api/', DATAView.as_view(), name='dataview'),
    path('test/api/', api_request, name='apitest'),
]
