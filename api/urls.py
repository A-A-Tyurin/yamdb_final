from django.urls import include, re_path

urlpatterns = [
    re_path(r'(?P<version>(v1))/', include('api.reviews_api.urls')),
    re_path(r'(?P<version>(v1))/auth/', include('api.authentication.urls')),
    re_path(r'(?P<version>(v1))/', include('api.user.urls'))
]
