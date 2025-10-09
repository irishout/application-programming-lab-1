
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

class Author(User):
    def __init__(self, user_id: int, name: str, email: str, biography: str, rating: float, social_media: dict, books: list):
        super().__init__(user_id, name, email)
        self.biography = biography
        self.rating = rating
        self.social_media = social_media
        self.books = books 
        

    def publish_book(self):
        pass

    def get_books(self):
        return self.books

    def get_info(self):
        return {
            'Имя': self.name,
            'Биография': self.biography,
            'Написано книг': len(self.books),
            'Cоц. сети': self.social_media
        }

class Castomer(User):
    def __init__(self, user_id: int, name: str, email: str, balance: float):
        super().__init__(user_id, name, email)
        self.balance = balance
        self.library = []

    def get_info(self):                                  
        return {
            'Имя': self.name,
            'Баланс': self.balance,
            'Библеотека': self.library,
        }
    
    def add_funds(self, replenishment):                  #Пополнение баланса 
        self.balance += replenishment

testus = Castomer(251521, 'klark', 'dsfsdf', 100)



