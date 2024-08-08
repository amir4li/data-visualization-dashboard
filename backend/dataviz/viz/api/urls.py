from django.contrib import admin
from django.urls import path
from viz.api.views import insight_list, insight_detail

urlpatterns = [
    path('', insight_list, name='insight_list'),
    path('<str:id>', insight_detail, name='insight_detail')
]
