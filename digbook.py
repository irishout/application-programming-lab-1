from userClasses import Castomer, Author, testus

class DigitalBook:
    def __init__(self, book_id: int, title: str, author: Author, price: float, description: str, tags: list):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.description = description
        self.tags = tags        

    def get_info(self):
        return {
            'Название': self.title,
            'Автор': self.author,
            'Теги': self.tags,
            'Описание': self.description,
            'Цена': self.price
        }
    
class ShoppingCart:
    def __init__(self, castomer: Castomer):
        self.castomer = castomer
        self.items = []

    def add_book(self, book: DigitalBook):
        self.items.append(book)

    def remove_book(self, book: DigitalBook):
        self.items.remove(book)


    def get_sum(self):
        sum = 0
        for book in self.items:
            sum += book.price
        return sum

    def checkout(self):
        return self.items
    
    def get_info(self):
        return {
            'Список покупок': self.items,
            'Сумма': self.get_sum()
        }
    
class Purchase:
    def __init__(self, purchase_id: int, payment_method: str, shop_cart: ShoppingCart):
        self.purchase_id = purchase_id
        self.shop_cart = shop_cart
    
    def payment(self):
        self.shop_cart.castomer.balance -= self.shop_cart.get_sum()
        self.shop_cart.castomer.library += self.shop_cart.items


    def get_recepit(self):
        recepit = {
            'id операции': self.purchase_id,
            'информация': self.shop_cart.get_info()
        }

        self.shop_cart.items = []
        return recepit

testbook = DigitalBook('123','веды', 'дрочеслав', 300, 'погрузитесь в реальную историю', ['славяне', 'ящеры'])
testcart = ShoppingCart(testus)
testcart.add_book(testbook)
print(testbook.get_info())

