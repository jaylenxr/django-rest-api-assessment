from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, Song


class GenreView(ViewSet):
    # GET REQUEST FOR SINGLE GENRE WITH ASSOCIATED SONGS
    def retrieve(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        serializer = SingleGenreSerializer(genre)
        return Response(serializer.data)

    # GET REQUEST FOR ALL GENRES
    def list(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    # POST REQUEST TO CREATE GENRE
    def create(self, request):
        genre = Genre.objects.create(
            description=request.data["description"]
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # PUT REQUEST TO UPDATE GENRE
    def update(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # DELETE REQUEST TO DESTROY GENRE
    def destroy(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'description')

class SingleGenreSerializer(serializers.ModelSerializer):
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')

    def get_songs(self, obj):
        songs = Song.objects.filter(songgenre__genre=obj)
        return [{"id": song.id, "title": song.title, "artist": song.artist.name} for song in songs]