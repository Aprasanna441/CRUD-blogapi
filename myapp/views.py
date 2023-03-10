from rest_framework.response import  Response
from  rest_framework import status,viewsets
from rest_framework.views import APIView
from myapp.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from myapp.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from myapp.serializers import BlogPostSerializer
from myapp.models import Blog,Category,User
from django.shortcuts import get_object_or_404


from django.views.generic import TemplateView


 


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)

            return Response({'token':token,'msg':'Registration done'},status=status.HTTP_201_CREATED)

        return Response({'msg':'Registration failed'},status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
    
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
              token=get_tokens_for_user(user)
              return Response({'token':token,'msg':'Login success'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}},status=status.HTTP_400_BAD_REQUEST)


        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
     renderer_classes=[UserRenderer]
     permission_classes=[IsAuthenticated]
     def get(self,request,format=None):          
          serializer=UserProfileSerializer(request.user)
          return Response(serializer.data,status=status.HTTP_200_OK)
     

class ChangePasswordView(APIView):
     renderer_classes=[UserRenderer]
     permission_classes=[IsAuthenticated]
     def post(self,request):
          serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
          if serializer.is_valid(raise_exception=True):
               return Response({'msg':"Password change success"},status=status.HTTP_200_OK)
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
               
          
class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':"password reset link sent.Please check your email"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    



class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    queryset=Blog.objects.all()
    serializer_class=BlogPostSerializer
        



class CreateBlogViewSet(viewsets.ModelViewSet):
    
    serializer_class = BlogPostSerializer
    http_method_names = [ 'get','post','patch','delete',]

    # def get_queryset(self):
    #     pass

    def list(self, request):
        queryset = Blog.objects.all()
        serializer = BlogPostSerializer(queryset, many=True)
        return Response(serializer.data)
        
        

    # def retrieve(self, request, pk=None):
    #     pass

    def create(self, request, *args, **kwargs):
        user = request.user
        email=request.data['author_name']
        cat=request.data['category']
        data1=User.objects.get(email=email).getid()
        data2=Category.objects.get(category_name=cat).getid()

        
        
        data={
            "title":request.data['title'],
            "author_name":data1,
            "category":data2,
            "content":request.data['content']
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request,pk=None):

        idd=Blog.objects.get(title__icontains=pk).getid()
        item = get_object_or_404(Blog, id=idd)
       
        serializer = BlogPostSerializer(item,many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

    def update(self,request,pk=None,**kwargs):
        idd=Blog.objects.get(title__icontains=pk).getid()
        item = get_object_or_404(Blog, id=idd)
        print(item)
        data={
            "content":request.data['content']
            
        }
        print(data)


       
        serializer = BlogPostSerializer(instance=item,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def destroy(self, request, pk=None, *args, **kwargs):
        idd=Blog.objects.get(title__icontains=pk).getid()
        item = get_object_or_404(Blog, id=idd)
        self.perform_destroy(item)
        
        
        return Response(status=status.HTTP_200_OK)

        
        


















