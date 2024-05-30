from django.urls import path
from .views import get_all_classes, get_all_teachers, add_credit, remove_credit, get_class, get_quarter_credits

urlpatterns = [
    path("teachers/",get_all_teachers),
    path("classes/",get_all_classes),
    path("get_class/", get_class ),
    path("add_credit/", add_credit),
    path("remove_credit/", remove_credit),
    path("quarter/", get_quarter_credits),

]    