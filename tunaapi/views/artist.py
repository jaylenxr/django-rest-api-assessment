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

        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

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
    song_count = serializers.SerializerMethodField()
    songs = serializers.SerializerMethodField()
    #the SerializerMethodField creates a new logic that will look up the get_songs method to show songs by the artist requested.
    #this field (songs) doesn't exist within the Artist model so it has to be created dynamically
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')

    def get_song_count(self, obj):
        return Song.objects.filter(artist=obj).count()

    def get_songs(self, obj):
        # get all songs by this artist
        songs = Song.objects.filter(artist=obj)
        return [{"id": song.id, "title": song.title, "album": song.album, "length": song.length} for song in songs]