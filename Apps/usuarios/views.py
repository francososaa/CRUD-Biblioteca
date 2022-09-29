from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.authtoken.models import Token 
from rest_framework.permissions import IsAdminUser
from rest_framework.settings import api_settings
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UsuarioSerializer, UsuarioTokenSerializer
from .permissions import UsuarioPerfil

class Login(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request': 'request'})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user = user) 
                user_serializer = UsuarioTokenSerializer(user)   
                if created: 
                    return Response({
                        'token': token.key,
                        'message':'Inicio de Sesion Exitoso',
                        }, status = status.HTTP_201_CREATED)   
                else:
                    # Se eliminan todas las sesiones que tenga el usuario abiertas
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'message':'Inicio de Sesion Exitoso',
                        }, status = status.HTTP_201_CREATED)         
            else:
                return Response({'error':'Este usuario no puede iniciar sesion'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error':'Nombre de usuario o contraseña incorrectos'}, status = status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()

            if token:
                user = token.user

                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()
                return Response({'token_message':'Token eliminado','session_message':'Sesiones de usuario eliminadas'}, status = status.HTTP_200_OK)
        
            return Response({'error':'No se ha encontrado un usuario con estas credenciales'}, status = status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error':'No se ha encontrado token en la peticion'}, status = status.HTTP_409_CONFLICT)

class CreateUser(generics.CreateAPIView):
    serializer_class = UsuarioSerializer
   
    @action(detail=True, methods=['post'])
    def create_user(self, request):
        usuario_serializer = self.serializer_class(data = request.data)
        
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response({'message':'Usuario creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response(usuario_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UsuarioApiView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = (IsAdminUser,UsuarioPerfil,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre','apellido','is_Active'] 

    def get_queryset(self, pk=None):
        if pk == None:
            return self.get_serializer().Meta.model.objects.all().values('id','password','username','nombre','apellido','email','is_active')
        else:
            return self.get_serializer().Meta.model.objects.filter(is_active = True).filter(id = pk).first()
          
    def list(self, request):
        usuario = self.get_queryset()

        nombre = self.request.query_params.get('nombre',None)
        apellido = self.request.query_params.get('apellido',None)
        is_active = self.request.query_params.get('is_active',None)

        if nombre:
            usuario = usuario.filter(nombre=nombre)
        if apellido:
            usuario = usuario.filter(apellido=apellido)
        if is_active:
            usuario = usuario.filter(is_active=is_active)

        usuario_serializer = UsuarioSerializer(usuario, many = True)
        return Response(usuario_serializer.data, status = status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        usuario = self.get_queryset(pk)
        if usuario:
            autor_serializer = self.serializer_class(usuario)
            return Response(autor_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe el usuario indicado!'}, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            usuario_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
                return Response(usuario_serializer.data, status = status.HTTP_200_OK)
            return Response(usuario_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        usuario = self.get_queryset(pk)
        if usuario:
            usuario.is_active = False
            usuario.save()
            return Response({'message':'Usuario eliminado...'}, status = status.HTTP_200_OK)
        return Response({'error':'No se pudo eliminar el usuario...'}, status = status.HTTP_400_BAD_REQUEST)

