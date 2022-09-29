from rest_framework import serializers

from .models import Libro, Autor


class LibroSerializer(serializers.ModelSerializer):  
    autor = serializers.StringRelatedField()
    class Meta:
        model = Libro
        exclude = ['estado']

    '''def to_representation(self, instance):
        return {
            'id': instance.id,
            'isbn': instance.isbn,
            'titulo': instance.titulo,
            'autor': instance.autor.nombre,
            'editorial': instance.editorial,
            'paginas': instance.paginas,
            'clasificacion': instance.clasificacion,   
        }
    '''
class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        exclude = ['estado','fecha_creacion']

   
'''
class LibroListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
          
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'isbn': instance['isbn'],
            'titulo': instance['titulo'],
            'autor': instance['autor'],
            'editorial': instance['editorial'],
            'paginas': instance['paginas'],
            'clasificacion': instance['clasificacion'],   
        }
'''
