from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist


class SongView(ViewSet):
    # GET REQUEST FOR SINGLE SONG
    def retrieve(self, request, pk):
        song = Song.objects.get(pk=pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    # GET REQUEST FOR ALL SONGS
    def list(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    # POST REQUEST TO CREATE SONG
    def create(self, request):
        artist = Artist.objects.get(pk=request.data["artist_id"])

        song = Song.objects.create(
            title=request.data["title"],
            artist=artist,
            album=request.data["album"],
            length=request.data["length"]

        )
        serializer = SongSerializer(song)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # PUT REQUEST TO UPDATE SONG
    def update(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]

        artist= Artist.objects.get(pk=request.data["artist_id"])
        song.artist = artist
        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # DELETE REQUEST TO DESTROY SONG
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'length')