
class BookStoreError(Exception): #Базовое исключение
    
    def __init__(self, message: str, error_code: int = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self) -> str: #Строковое представление исключения

        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message
    
    def get_error_info(self) -> dict: #информация об ошибки 
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code
        }

# Категории исключений
class UserError(BookStoreError):
    pass

class BookError(BookStoreError):
    pass

class PaymentError(BookStoreError):
    pass

# Конкретные исключения для пользователей
class InvalidEmailError(UserError):
    #Неверный формат email
    def __init__(self, email: str):
        super().__init__(f"Неверный формат email: {email}", 1001)

class UserNotFoundError(UserError):
    #Пользователь не найден
    def __init__(self, user_id: int = None):
        if user_id: 
            message = f"Пользователь с ID {user_id} не найден"
        else:
            message = "Пользователь не найден"
        super().__init__(message, 1002)

class InsufficientFundsError(PaymentError):
    #Недостаточно средств на счете
    def __init__(self, current_balance: float, required_amount: float):
        super().__init__(
            f"Недостаточно средств. На счете: {current_balance}, требуется: {required_amount}",
            3001
        )

class EmptyCartError(PaymentError):
    #Корзина пуста
    def __init__(self):
        super().__init__("Корзина пуста. Добавьте книги перед покупкой", 3002)

class BookNotFoundError(BookError):
    #Книга не найдена
    def __init__(self, book_id: int = None):
        message = f"Книга с ID {book_id} не найдена" if book_id else "Книга не найдена"
        super().__init__(message, 2001)

class NegativePriceError(BookError):
    #Цена книги отрицательная
    def __init__(self, price: float):
        super().__init__(f"Цена не может быть отрицательной: {price}", 2002)

class InvalidBookDataError(BookError):
    #Неверные данные книги
    def __init__(self, field: str, value: str):
        super().__init__(f"Неверное значение в поле '{field}': {value}", 2003)