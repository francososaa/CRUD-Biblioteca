from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import AutorSerializer, LibroSerializer

''' CRUD AUTOR '''
class AutorAPIView(viewsets.ModelViewSet):
    serializer_class = AutorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'nombre' : ['contains'],
        'apellido' : ['exact'],
    }
    
    def get_permissions(self):
        if self.request.method in ['POST','DELETE','PUT','PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self, pk=None):
        if pk == None:
            return self.get_serializer().Meta.model.objects.filter(estado=True)
        else:
            return self.get_serializer().Meta.model.objects.filter(estado=True).filter(id = pk).first()

    def list(self, request):
        autor = self.get_queryset()
        
        nombre = self.request.query_params.get('nombre',None)
        apellido = self.request.query_params.get('apellido',None)

        if nombre:
            autor = autor.filter(nombre=nombre)
        if apellido:
            autor = autor.filter(apellido=apellido)

        autor_serializer = AutorSerializer(autor, many = True)
        return Response(autor_serializer.data, status = status.HTTP_200_OK)

    def retrieve(self, request, pk = None):
        autor = self.get_queryset(pk)
        if autor:
            autor_serializer = AutorSerializer(autor)
            return Response(autor_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe el autor indicado!'}, status = status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        
        autor_serializer = AutorSerializer(data = request.data)
        if autor_serializer.is_valid():
            autor_serializer.save()
            return Response({'message':'Autor creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response(autor_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None):
        if self.get_queryset(pk):
            autor_serializer = AutorSerializer(self.get_queryset(pk), data = request.data, partial=True)
            if autor_serializer.is_valid():
                autor_serializer.save()
                return Response(autor_serializer.data, status = status.HTTP_200_OK)
            return Response(autor_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None):
        autor = self.get_queryset(pk)
        if autor:
            autor.estado = False
            autor.save()
            return Response({'message':'El autor se elimino correctamente'}, status = status.HTTP_200_OK)
        return Response({'error','No existe el autor!'}, status = status.HTTP_400_BAD_REQUEST)
       
''' CRUD LIBRO '''
class LibroAPIView(viewsets.ModelViewSet):
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['titulo','paginas','clasificacion','publicacion']
        

    def get_permissions(self):
        if self.request.method in ['POST','DELETE','PUT','PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self, pk=None):
        if pk == None:
            return self.get_serializer().Meta.model.objects.filter(estado=True)
        return self.get_serializer().Meta.model.objects.filter(estado=True, id=pk).first()

    def list(self, request):
        queryset = self.get_queryset()
        titulo = self.request.query_params.get('titulo',None)
        paginas = self.request.query_params.get('paginas',None)
        genero = self.request.query_params.get('clasificacion',None)
        publicacion = self.request.query_params.get('publicacion',None)

        if titulo:
            queryset = queryset.filter(titulo=titulo)
        if paginas:
            queryset = queryset.filter(paginas=paginas)
        if genero:
            queryset = queryset.filter(clasificacion=genero)
        if publicacion:
            queryset = queryset.filter(publicacion=publicacion)

        libro_serealizer = LibroSerializer(queryset, many=True)
        return Response(libro_serealizer.data, status= status.HTTP_200_OK)

    def retrieve(self, request, pk = None):
        libro = self.get_queryset(pk)
        if libro:
            libro_serializer = self.serializer_class(libro)
            return Response(libro_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe un libro con estos datos'}, status = status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        libro_serializer = self.get_serializer(data = request.data)
        if libro_serializer.is_valid():
            libro_serializer.save()
            return Response({'message':'Libro creado correctamente!!'}, status = status.HTTP_201_CREATED)
        return Response(libro_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None):
        if self.get_queryset(pk):
            libro_serializer = self.serializer_class(self.get_queryset(pk), data = request.data, partial = True)
            if libro_serializer.is_valid():
                libro_serializer.save()
                return Response(libro_serializer.data, status = status.HTTP_200_OK)
            return Response(libro_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None):
        libro = self.get_queryset(pk)
        if libro:
            libro.estado = False
            libro.save()
            return Response({'message':'Libro eliminado correctamente!'}, status = status.HTTP_200_OK)
        return Response({'error':'No existe un libro con estos datos'}, status = status.HTTP_400_BAD_REQUEST)