from model.Item import Book, Magazine, Movie, Music
from model.Uow import Uow
from model.Catalog import Catalog
from model.Tdg import Tdg
from copy import deepcopy


class ItemMapper:
    def __init__(self, tdg):
        self.uow = None
        self.catalog = Catalog()
        self.tdg = tdg
        self.catalog.populate(self.tdg.get_books(), self.tdg.get_magazines(),
                              self.tdg.get_movies(), self.tdg.get_music())

    def get_catalog(self):
        return self.catalog

    def get_saved_changes(self):
        if self.uow is None:
            return None
        else:
            return self.uow.get_saved_changes()

    def find(self, item_id):
        if self.uow is None:
            self.uow = Uow()
        item = self.uow.get(item_id)
        if item is not None:
            print("in item mapper find: Item was NOT none")
            clone = deepcopy(item)
            return clone
        else:
            item = self.catalog.get_item_by_id(item_id)
            print("in item mapper find: Item was none")
            clone = deepcopy(item)
            self.uow.add(clone)
            return clone

    def delete_item(self, item_id):
        if self.uow is None:
            self.uow = Uow()
        item = self.uow.get(item_id)
        if item is None:
            item = self.catalog.get_item_by_id(item_id)
            clone = deepcopy(item)
            self.uow.add(clone)

        self.uow.register_deleted(item)
        return True

    def set_item(self, item_id, form):
        item = self.uow.get(item_id)
        item_prefix = item.prefix
        if item_prefix == "bb":
            item.title = form.title.data
            item.author = form.author.data
            item.format = form.format.data
            item.pages = form.pages.data
            item.publisher = form.publisher.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data

        elif item_prefix == "ma":
            item.title = form.title.data
            item.publisher = form.publisher.data
            item.language = form.language.data
            item.isbn10 = form.isbn1.data
            item.isbn13 = form.isbn13.data

        elif item_prefix == "mo":
            item.title = form.title.data
            item.director = form.director.data
            item.producers = form.producers.data
            item.actors = form.actors.data
            item.language = form.language.data
            item.subs = form.subtitles.data
            item.dubbed = form.dubbed.data
            item.release_date = form.releaseDate.data
            item.runtime = form.runtime.data

        elif item_prefix == "mu":
            item.title = form.title.data
            item.media_type = form.media_type.data
            item.artist = form.artist.data
            item.label = form.label.data
            item.release_date = form.releaseDate.data
            item.asin = form.asin.data

        self.uow.register_dirty(item)

    def add_book(self, form):
        title = form.title.data
        prefix = "bb"
        status = "avail"
        author = form.author.data
        book_format = form.format.data
        pages = form.pages.data
        publisher = form.publisher.data
        language = form.language.data
        isbn10 = form.isbn10.data
        isbn13 = form.isbn13.data
        book = Book(None, title, prefix, status, author, book_format, pages,
                    publisher, language, isbn10, isbn13)
        if self.uow is None:
            self.uow = Uow()
        self.uow.add(book)
        self.uow.register_new(book)

    def add_magazine(self, form):
        title = form.title.data
        publisher = form.publisher.data
        prefix = "ma"
        status = "avail"
        language = form.language.data
        isbn10 = form.isbn10.data
        isbn13 = form.isbn13.data
        magazine = Magazine(None, title, prefix, status, publisher, language,
                            isbn10, isbn13)
        if self.uow is None:
            self.uow = Uow()
        self.uow.add(magazine)
        self.uow.register_new(magazine)

    def add_movie(self, form):
        title = form.title.data
        prefix = "mo"
        status = "avail"
        director = form.director.data
        producers = form.producers.data
        actors = form.actors.data
        language = form.language.data
        subtitles = form.subtitles.data
        dubbed = form.dubbed.data
        release_date = form.releaseDate.data
        run_time = form.runtime.data
        movie = Movie(None, title, prefix, status, director, producers, actors,
                      language, subtitles, dubbed, release_date, run_time)
        if self.uow is None:
            self.uow = Uow()
        self.uow.add(movie)
        self.uow.register_new(movie)

    def add_music(self, form):
        media_type = form.media_type.data
        title = form.title.data
        prefix = "mu"
        status = "avail"
        artist = form.artist.data
        label = form.label.data
        release_date = form.releaseDate.data
        asin = form.asin.data
        music = Music(None, title, prefix, status, media_type, artist, label,
                      release_date, asin)
        if self.uow is None:
            self.uow = Uow()
        self.uow.add(music)
        self.uow.register_new(music)

    def end(self):
        items_to_commit = self.uow.get_saved_changes()
        self.uow = None

        modified_books = []
        modified_magazines = []
        modified_movies = []
        modified_music = []

        deleted_books = []
        deleted_magazines = []
        deleted_movies = []
        deleted_music = []

        # Add
        if items_to_commit[0] is not None:
            for item in items_to_commit[0]:
                if item.prefix == "bb":
                    item_id = self.tdg.add_book(item)
                    item.id = item_id
                    self.catalog.add_item(item)
                elif item.prefix == "ma":
                    item_id = self.tdg.add_magazine(item)
                    item.id = item_id
                    self.catalog.add_item(item)
                elif item.prefix == "mo":
                    item_id = self.tdg.add_movie(item)
                    item.id = item_id
                    self.catalog.add_item(item)
                elif item.prefix == "mu":
                    item_id = self.tdg.add_music(item)
                    item.id = item_id
                    self.catalog.add_item(item)

        # Modify
        if items_to_commit[1] is not None:
            for item in items_to_commit[1]:
                if item.prefix == "bb":
                    modified_books.append(item)
                elif item.prefix == "ma":
                    modified_magazines.append(item)
                elif item.prefix == "mo":
                    modified_movies.append(item)
                elif item.prefix == "mu":
                    modified_music.append(item)
            self.catalog.edit_items(items_to_commit[1])
            if len(modified_books) != 0:
                self.tdg.modify_books(modified_books)
            if len(modified_magazines) != 0:
                self.tdg.modify_magazines(modified_magazines)
            if len(modified_movies) != 0:
                self.tdg.modify_movies(modified_movies)
            if len(modified_music) != 0:
                self.tdg.modify_music(modified_music)

        # Delete
        if items_to_commit[2] is not None:
            for item in items_to_commit[2]:
                if item.prefix == "bb":
                    deleted_books.append(item)
                elif item.prefix == "ma":
                    deleted_magazines.append(item)
                elif item.prefix == "mo":
                    deleted_movies.append(item)
                elif item.prefix == "mu":
                    deleted_music.append(item)
            self.catalog.delete_items(items_to_commit[2])
            if len(deleted_books) != 0:
                self.tdg.delete_books(deleted_books)
            if len(deleted_magazines) != 0:
                self.tdg.delete_magazines(deleted_magazines)
            if len(deleted_movies) != 0:
                self.tdg.delete_movies(deleted_movies)
            if len(deleted_music) != 0:
                self.tdg.delete_music(deleted_music)
