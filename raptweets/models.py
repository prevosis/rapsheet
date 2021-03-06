from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist)
    release_date = models.DateTimeField()
    image_url = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.artist.name + ' - ' + self.title

    class Meta:
        unique_together = ('artist', 'title')

class Tweet(models.Model):
    text = models.CharField(max_length=140, unique=True)
    sentiment = models.FloatField()
    pub_date = models.DateTimeField('date published')
    album = models.ForeignKey(Album)

    def __str__(self):
        return str(self.text)


# TODO more relevant tweets
# TODO styling
# TODO if tweets already loaded, do not make another query (i.e. coming from graph view)