from model.Item import Book, Magazine, Movie, Music


class Catalog:

    def __init__(self):
        self.item_catalog = []

    def get_item_by_id(self, item_id):
        int_id = item_id
        if item_id is not int:
            int_id = int(item_id)

        for item in self.item_catalog:
            if item.id == int_id:
                return item
        return None

    def get_all_items(self):
        pass

    def populate(self, books, magazines, movies, music):
        if books is not None:
            for book in books:
                self.item_catalog.append(Book(book[0], "bb", book[1], book[2], book[3], book[4], book[5], book[6], book[7], book[8], book[9]))

        if magazines is not None:
            for magazine in magazines:
                self.item_catalog.append(Magazine(magazine[0], "ma", magazine[1], magazine[2], magazine[3], magazine[4], magazine[5], magazine[6]))

        if movies is not None:
            for movie in movies:
                self.item_catalog.append(Movie(movie[0], "mo", movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], movie[7], movie[8], movie[9], movie[10]))

        if music is not None:
            for item in music:
                self.item_catalog.appen(Music(item[0], "mu", item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

    # [Testing] This function is required for testing add/remove/edit
    def insert_item(self, item):
        if item is None:
            return False

        self.item_catalog.append(item)
        return True

    def add_item(self, item):
        if item is not None:
            self.item_catalog.append(item)

    def edit_item(self, item_id, form):
        item = self.get_item_by_id(item_id)
        if item is None:
            return None

        selected_item_prefix = item.prefix

        if selected_item_prefix == "bb":
            item.title = form.title.data
            item.author = form.author.data
            item.format = form.format.data
            item.pages = form.pages.data
            item.publisher = form.publisher.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data
            return True
        elif selected_item_prefix == "ma":
            item.title = form.title.data
            item.publisher = form.publisher.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data
            return True
        elif selected_item_prefix == "mo":
            item.title = form.title.data
            item.director = form.director.data
            item.producers = form.producers.data
            item.actors = form.actors.data
            item.language = form.language.data
            item.subs = form.subtitles.data
            item.dubbed = form.dubbed.data
            item.release_date = form.releaseDate.data
            item.runtime = form.runtime.data
            return True
        elif selected_item_prefix == "mu":
            item.title = form.title.data
            item.media_type = form.media_type.data
            item.artist = form.artist.data
            item.label = form.label.data
            item.release_date = form.releaseDate.data
            item.asin = form.asin.data
            return True

        return False

    def delete_item(self, item_id):
        item = self.get_item_by_id(item_id)
        if item is not None:
            self.item_catalog.remove(item)
            return True
        else:
            return False

    # [Testing] Used to remove objects added to catalog while testing
    def delete_last_item(self):
        if len(self.item_catalog) == 0:
            return None
        self.item_catalog = self.item_catalog[:-1]