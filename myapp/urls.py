from django.urls import path,include
from myapp import views
from myapp.views import UserRegistrationView,UserLoginView,UserProfileView,ChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView
from myapp.views import CreateBlogViewSet


from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('blogapi',views.CreateBlogViewSet,basename='blog')



urlpatterns = [    
      path('user/register/',UserRegistrationView.as_view(),name="registeruser" ),
      path('user/login/',UserLoginView.as_view(),name="login"),
      path('user/profile/',UserProfileView.as_view(),name="profile"),
      path('user/changepassword',ChangePasswordView.as_view(),name="changepassword"),
      path('user/send-reset-password-email/',SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
      path('user/reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password'),
      
      path('',include(router.urls)),
      # path('auth',include('rest_framework.urls',namespace='rest_framework'))
      

       
]