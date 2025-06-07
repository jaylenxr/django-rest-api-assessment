from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song


class ArtistView(ViewSet):
    # GET REQUEST FOR SINGLE ARTIST
    def retrieve(self, request, pk):

        artist = Artist.objects.get(pk=pk)
        serializer = SingleArtistSerializer(artist)
        return Response(serializer.data)

    # GET REQUEST FOR ALL ARTISTS
    def list(self, request):

        artist = Artist.objects.all()
        serializer = ArtistSerializer(artist, many=True)
        return Response(serializer.data)

    # POST REQUEST TO CREATE ARTIST
    def create(self, request):

        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"]
    )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # PUT REQUEST TO UPDATE ARTIST
    def update(self, request, pk):

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # DELETE REQUEST TO DESTROY ARTIST
    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')

class SingleArtistSerializer(serializers.ModelSerializer):
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'songs')

    def get_songs(self, obj):
        # Get all songs by this artist
        songs = Song.objects.filter(artist=obj)
        return [{"id": song.id, "title": song.title, "album": song.album, "length": song.length} for song in songs]