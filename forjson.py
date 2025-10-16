import json
from userClasses import Customer, Author
from digbook import DigitalBook, ShoppingCart, Purchase

class JSONDataManager:
    def __init__(self, filename="jsondata.json"):
        self.filename = filename
    
    def save_data(self, customers: Customer, authors: Author, books: DigitalBook, shopping_carts: ShoppingCart, purchases: Purchase):
        try:
            data = {
                "bookstore": {
                    "customers": self.save_customers(customers),
                    "authors": self.save_authors(authors),
                    "books": self.save_books(books),
                    "shopping_carts": self.save_shopping_carts(shopping_carts),
                    "purchases": self.save_purchases(purchases)
                }
            }
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Данные успешно сохранены в {self.filename}")
            
        except Exception as e:
            print(f"Ошибка при сохранении JSON: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            bookstore_data = data.get("bookstore", {})
            
            customers = self.load_customers(bookstore_data.get("customers", []))
            authors = self.load_authors(bookstore_data.get("authors", []))
            books_data = bookstore_data.get("books", [])
            shopping_carts_data = bookstore_data.get("shopping_carts", [])
            purchases_data = bookstore_data.get("purchases", [])
            
            books = self.load_books(books_data)
            shopping_carts = self.load_shopping_carts(shopping_carts_data, customers, books)
            purchases = self.load_purchases(purchases_data, customers, books)
            
            print(f"Данные успешно загружены из {self.filename}")
            return customers, authors, books, shopping_carts, purchases
            
        except Exception as e:
            print(f"Ошибка при загрузке JSON: {e}")
            return [], [], [], [], []
    
    def save_customers(self, customers: list[Customer]):
        """Сериализация покупателей"""
        result = []
        for customer in customers:
            result.append({
                "user_id": customer.user_id,
                "name": customer.name,
                "email": customer.email,
                "balance": customer.balance,
                "library": customer.library
            })
        return result
    
    def save_authors(self, authors: list[Author]):
        """Сериализация авторов"""
        result = []
        for author in authors:
            result.append({
                "user_id": author.user_id,
                "name": author.name,
                "email": author.email,
                "biography": author.biography,
                "rating": author.rating,
                "social_media": author.social_media,
                "books_id": author.books_id
            })
        return result
    
    def save_books(self, books: list[DigitalBook]):
        """Сериализация книг"""
        result = []
        for book in books:
            result.append({
                "book_id": book.book_id,
                "title": book.title,
                "author_id": book.author_id,
                "price": book.price,
                "description": book.description,
                "tags": book.tags
            })
        return result
    
    def save_shopping_carts(self, shopping_carts: list[ShoppingCart]):
        """Сериализация корзин"""
        result = []
        for cart in shopping_carts:
            result.append({
                "customer_id": cart.customer.user_id,
                "items": [book.book_id for book in cart.items]
            })
        return result
    
    def save_purchases(self, purchases: list[Purchase]):
        """Сериализация покупок"""
        result = []
        for purchase in purchases:
            result.append({
                "purchase_id": purchase.purchase_id,
                "customer_id": purchase.shop_cart.customer.user_id,
                "purchased_books": [book.book_id for book in purchase.purchased_books],
                "total_amount": purchase.shop_cart.get_sum() if purchase.shop_cart else 0
            })
        return result
    
    def load_customers(self, customers_data):
        """Десериализация покупателей"""
        customers = []
        for data in customers_data:
            try:
                customer = Customer(
                    user_id=data["user_id"],
                    name=data["name"],
                    email=data["email"],
                    balance=data["balance"]
                )
                customer.library = data.get("library", [])
                customers.append(customer)
            except Exception as e:
                print(f"Ошибка при создании покупателя: {e}")
        return customers
    
    def load_authors(self, authors_data):
        """Десериализация авторов"""
        authors = []
        for data in authors_data:
            try:
                author = Author(
                    user_id=data["user_id"],
                    name=data["name"],
                    email=data["email"],
                    biography=data["biography"],
                    rating=data["rating"],
                    social_media=data.get("social_media", {}),
                    books_id=data.get("books_id", [])
                )
                authors.append(author)
            except Exception as e:
                print(f"Ошибка при создании автора: {e}")
        return authors
    
    def load_books(self, books_data):
        """Десериализация книг"""
        books = []
        
        for data in books_data:
            try:
                book = DigitalBook(
                    book_id=data["book_id"],
                    title=data["title"],
                    author_id=data["author_id"],
                    price=data["price"],
                    description=data["description"],
                    tags=data.get("tags", [])
                )
                books.append(book)
            except Exception as e:
                print(f"Ошибка при создании книги: {e}")
        return books
    
    def load_shopping_carts(self, carts_data, customers, books):
        """Десериализация корзин"""
        shopping_carts = []
        customer_dict = {customer.user_id: customer for customer in customers}
        book_dict = {book.book_id: book for book in books}
        
        for data in carts_data:
            try:
                customer_id = data["customer_id"]
                customer = customer_dict.get(customer_id)
                
                if customer:
                    cart = ShoppingCart(customer)
                    for book_id in data.get("items", []):
                        book = book_dict.get(book_id)
                        if book:
                            cart.items.append(book)
                    shopping_carts.append(cart)
                else:
                    print(f"Покупатель с ID {customer_id} не найден")
            except Exception as e:
                print(f"Ошибка при создании корзины: {e}")
        return shopping_carts
    
    def load_purchases(self, purchases_data, customers, books):
        """Десериализация покупок"""
        purchases = []
        customer_dict = {customer.user_id: customer for customer in customers}
        book_dict = {book.book_id: book for book in books}
        
        for data in purchases_data:
            try:
                customer_id = data["customer_id"]
                customer = customer_dict.get(customer_id)
                
                if customer:
                    # Создаем временную корзину для покупки
                    temp_cart = ShoppingCart(customer)
                    for book_id in data.get("purchased_books", []):
                        book = book_dict.get(book_id)
                        if book:
                            temp_cart.items.append(book)
                    
                    purchase = Purchase(
                        purchase_id=data["purchase_id"],
                        shop_cart=temp_cart
                    )
                    purchase.purchased_books = temp_cart.items.copy()
                    purchases.append(purchase)
                else:
                    print(f"Покупатель с ID {customer_id} не найден")
            except Exception as e:
                print(f"Ошибка при создании покупки: {e}")
        return purchases