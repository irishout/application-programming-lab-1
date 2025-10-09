from userClasses import testus

class DigitalBook:
    def __init__(self, book_id: int, title, author, price, description, tags):
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
    
class ShoppingCart(DigitalBook):
    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance
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

testbook = DigitalBook('123','веды', 'дрочеслав', 300, 'погрузитесь в реальную историю', ['славяне', 'ящеры'])
testcart = ShoppingCart(testus.user_id, testus.balance)
testcart.add_book(testbook)
print(testcart.get_info())

