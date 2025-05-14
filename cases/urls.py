from django.urls import path
from .views import create_case, get_case_list,  get_case_detail

urlpatterns = [
    path('', create_case),  # /api/cases/로 요청 받음
    path('list/', get_case_list),
    path('<int:case_id>/', get_case_detail),
]
