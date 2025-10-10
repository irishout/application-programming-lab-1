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
    pass

testbook = DigitalBook('123','веды', 'дрочеслав', 300, 'погрузитесь в реальную историю', ['славяне', 'ящеры'])
testcart = ShoppingCart(testus)
testcart.add_book(testbook)
print(testbook.get_info())

