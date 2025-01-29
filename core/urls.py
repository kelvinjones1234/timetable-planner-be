
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('plan_app.urls')),
    path('api/', include('user_app.urls')),

]

