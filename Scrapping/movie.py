class Movie:
    def __init__(self, name="", genre=None, poster=""):
        self.name = name
        self.genre = genre if genre is not None else []
        self.poster = poster

    def __str__(self):
        """Return a readable string representation of the Movie instance."""
        genre_list = ", ".join(self.genre)
        poster_preview = str(self.poster)[:30]
        return f"Movie: {self.name}  |  Genre(s): {genre_list}  |  Poster: {poster_preview}"
    
    def __repr__(self):
        return self.__str__()