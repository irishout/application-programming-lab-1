from exeptions import *

class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.validate_user_id(user_id)
        self.validate_name(name)
        self.validate_email(email)
        
        self.user_id = user_id
        self.name = name
        self.email = email

    def validate_user_id(self, user_id: int) -> None:
        """Валидация ID пользователя"""
        if not isinstance(user_id, int) or user_id <= 0:
            raise UserError(f"Неверный ID пользователя: {user_id}", 1003)    
    
    def validate_name(self, name: str) -> None:
        """Валидация имени"""
        if not name or not isinstance(name, str):
            raise UserError("Имя не может быть пустым", 1004)
        if len(name) < 2:
            raise UserError("Имя должно содержать минимум 2 символа", 1005)    

    def validate_email(self, email: str) -> None:
        """Валидация email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise InvalidEmailError(email)
        
class Author(User):
    def __init__(self, user_id: int, name: str, email: str, biography: str, rating: float, social_media: dict, books_id: list[int]): 
        super().__init__(user_id, name, email)

        self.validate_rating(rating)

        self.biography = biography
        self.rating = rating
        self.social_media = social_media
        self.books_id = books_id  
        
    def validate_rating(self, rating: float) -> None:
        """Валидация рейтинга"""
        if not isinstance(rating, (int, float)) or rating < 0 or rating > 5:
            raise UserError("Рейтинг должен быть числом от 0 до 5", 1006)

    def publish_book(self, book_id):
        if not isinstance(book_id, int) or book_id <= 0:
            raise BookError(f"Неверный ID книги: {book_id}", 2004)

        if book_id not in self.books_id:
            self.books_id.append(book_id)
        else:
            raise BookError(f"Эта книга уже добавленна: {book_id}", 2005)


    def get_books(self):
        return self.books_id

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

    def validate_balance(self, balance: float):
            """Валидация баланса"""
            if not isinstance(balance, (int, float)) or balance < 0:
                raise PaymentError("Баланс не может быть отрицательным", 3003)



    def get_info(self):                                  
        return {
            'Имя': self.name,
            'Баланс': self.balance,
            'Библеотека': self.library,
        }
    
    def add_funds(self, replenishment):                  #Пополнение баланса 
        if not isinstance(replenishment, (int,float)) or replenishment < 0:
            raise PaymentError(f'Сумма пополнения должна быть числом и не может быть меньше нуля', 3004)
        self.balance += replenishment

    def cant_afford(self, price):         
        if price > self.balance:
            raise PaymentError(f'Недостаточно средств на балансе', 3005)





