from userClasses import Customer, Author
from exeptions import *

class DigitalBook:
    def __init__(self, book_id: int, title: str, author_id: int, price: float, description: str, tags: list):
        self.book_id = book_id
        self.title = title
        self.author_id = author_id
        self.price = price
        self.description = description
        self.tags = tags 

        self._validate_book_data(book_id, title, price)   

    def _validate_book_data(self, book_id: int, title: str, price: float): #Валидация данных книги
        if not isinstance(book_id, int) or book_id <= 0:
            raise InvalidBookDataError("book_id", f"Должен быть положительным числом: {book_id}")
        
        if not title or not isinstance(title, str):
            raise InvalidBookDataError("title", "Не может быть пустым")
        
        if len(title) < 2:
            raise InvalidBookDataError("title", "Должен содержать минимум 2 символа")
        
        if not isinstance(price, (int, float)) or price < 0:
            raise NegativePriceError(price)

    def get_info(self) -> dict:
        return {
            'Название': self.title,
            'ID_Автор': self.author_id,
            'Теги': self.tags,
            'Описание': self.description,
            'Цена': self.price
        }
    
class ShoppingCart:
    def __init__(self, customer: Customer):
        if not isinstance(customer, Customer):
            raise UserError("Корзина должна быть привязана к покупателю", 1008)
        self.customer = customer
        self.items = []
        

    def add_book(self, book: DigitalBook):
        if not isinstance(book, DigitalBook):
            raise BookError("Можно добавлять только объекты DigitalBook", 1009)
        
        if not book in self.items:
            self.items.append(book)
        else: 
            raise BookError(f"Книга '{book.title}' уже в корзине", 2007) 

    def remove_book(self, book: DigitalBook):
        if not isinstance(book, DigitalBook):
            raise BookError("Можно удалять только объекты DigitalBook", 1009)     

        if book in self.items:
            self.items.remove(book)
        else:
            raise BookError(f"Книга '{book.title}' не найдена в корзине", 2008) 

    def get_sum(self) -> int:
        sum = 0
        for book in self.items:
            sum += book.price
        return sum

    def checkout(self) -> list:
        if self.items:
            return self.items
        else:
            raise EmptyCartError()
    
    def get_info(self) -> dict:
        return {
            'Список покупок': self.items,
            'Сумма': self.get_sum()
        }
    
class Purchase:
    def __init__(self, purchase_id: int, shop_cart: ShoppingCart):
        self._validate_purchase_data(purchase_id, shop_cart)

        self.purchase_id = purchase_id
        self.shop_cart = shop_cart
        self.purchased_books = []

    def _validate_purchase_data(self, purchase_id: int, shop_cart: ShoppingCart): #Валидация данных покупки
            if not isinstance(purchase_id, int) or purchase_id <= 0:
                raise PaymentError(f"Неверный ID покупки: {purchase_id}", 3005)
            
            if not isinstance(shop_cart, ShoppingCart):
                raise PaymentError("Неверный объект корзины", 3006)        
        
    def payment(self):

        try:
            books_to_buy = self.shop_cart.checkout()
            total_ammount= self.shop_cart.get_sum()

            if not self.shop_cart.customer.cant_afford(total_ammount):
                self.shop_cart.customer.balance -= total_ammount
                self.shop_cart.customer.library += books_to_buy
                self.purchased_books = books_to_buy
                self.info = self.shop_cart.get_info() 
                self.shop_cart.items = []

            else:
                raise InsufficientFundsError(self.shop_cart.customer.balance, self.shop_cart.get_sum())
            
        except (EmptyCartError, InsufficientFundsError) as e: #известные исключения
            raise e
        
        except Exception as e: #неизвестные исключения
            raise PaymentError(f"Ошибка при обработке платежа: {e}", 3007)

    def get_recepit(self) -> dict:
        if not self.purchased_books:
            raise PaymentError("Покупка не была совершена", 3008)
        recepit = {
            'id операции': self.purchase_id,
            'инфо': self.info
        }
        return recepit
