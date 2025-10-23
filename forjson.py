import json
from userClasses import Customer, Author
from digbook import DigitalBook, ShoppingCart, Purchase

class JSONDataManager:
    def __init__(self, filename="jsondata.json"):
        self.filename = filename
    
    #тщетные попытки сделать проверку на id
    # def __id_check(self, id, classforcheck: str):
    #     with open(self.filename, 'r', encoding='utf-8') as f:             
    #         data = json.load(f)
            
    #     bookstore_data = data.get("bookstore", {})        
    #     objects = bookstore_data[classforcheck]
    #     print(objects)
    #     if classforcheck == "customers" or classforcheck == "authors":
    #         ids = [object["user_id"] for object in objects]
    #     elif classforcheck == "books":
    #         ids = [object.book_id for object in objects]
    #     elif classforcheck == "purchases":
    #         ids = [object.purchase_id for object in objects]

        
    #     if id in ids:
    #         return True
    #     else: False


    def save_data(self, customers: Customer, authors: Author, books: DigitalBook, shopping_carts: ShoppingCart, purchases: Purchase):
        try:
            data = {
                "bookstore": {
                    "customers": self.__save_customers(customers),
                    "authors": self.__save_authors(authors),
                    "books": self.__save_books(books),
                    "shopping_carts": self.__save_shopping_carts(shopping_carts),
                    "purchases": self.__save_purchases(purchases)
                }
            }
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Данные успешно сохранены в {self.filename}")
            
        except Exception as e:
            print(f"Ошибка при сохранении JSON: {e}")
    
    def load_data(self):
        #Загрузка данных из JSON файла
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            bookstore_data = data.get("bookstore", {})
            
            customers = self.__load_customers(bookstore_data.get("customers", []))
            authors = self.__load_authors(bookstore_data.get("authors", []))
            books_data = bookstore_data.get("books", [])
            shopping_carts_data = bookstore_data.get("shopping_carts", [])
            purchases_data = bookstore_data.get("purchases", [])
            
            books = self.__load_books(books_data)
            shopping_carts = self.__load_shopping_carts(shopping_carts_data, customers, books)
            purchases = self.__load_purchases(purchases_data, customers, books)
            
            print(f"Данные успешно загружены из {self.filename}")
            return customers, authors, books, shopping_carts, purchases
            
        except Exception as e:
            print(f"Ошибка при загрузке JSON: {e}")
            return [], [], [], [], []
    
    
    def __save_customers(self, customers: list[Customer]):
        #Сериализация покупателей

        # for c in customers:
        #     if self.__id_check(c.user_id, "customers"):
        #         print("Пользователь с таким ID уже существует")
        #         return customers_list
            

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
    
    def __save_authors(self, authors: list[Author]):
        #Сериализация автороd
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
    
    def __save_books(self, books: list[DigitalBook]):
        #Сериализация книг
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
    
    def __save_shopping_carts(self, shopping_carts: list[ShoppingCart]):
        #Сериализация корзин
        result = []
        for cart in shopping_carts:
            result.append({
                "customer_id": cart.customer.user_id,
                "items": [book.book_id for book in cart.items]
            })
        return result
    
    def __save_purchases(self, purchases: list[Purchase]):
        #Сериализация покупок
        result = []
        for purchase in purchases:
            result.append({
                "purchase_id": purchase.purchase_id,
                "customer_id": purchase.shop_cart.customer.user_id,
                "purchased_books": [book.book_id for book in purchase.purchased_books],
                "total_amount": purchase.shop_cart.get_sum() if purchase.shop_cart else 0
            })
        return result
    
    def __load_customers(self, customers_data):
        #Десериализация покупателей
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
    
    def __load_authors(self, authors_data):
        #Десериализация авторов
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
    
    def __load_books(self, books_data):
        #Десериализация книг
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
    
    def __load_shopping_carts(self, carts_data, customers, books):
        #Десериализация корзин
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
    
    def __load_purchases(self, purchases_data, customers, books):
        #Десериализация покупок
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

    def create_customer(self, customer):
        """Создание нового покупателя"""
        try:
            customers, authors, books, shopping_carts, purchases = self.load_data()
            customers.append(customer)
            self.save_data(customers, authors, books, shopping_carts, purchases)
            print(f"Покупатель {customer.name} успешно создан")
            return True
        except Exception as e:
            print(f"Ошибка при создании покупателя: {e}")
            return False
        
    def read_customer(self, customer_id):
        """Чтение покупателя по ID"""
        customers, _, _, _, _ = self.load_data()
        for customer in customers:
            if customer.user_id == customer_id:
                return customer
        return None
    
    def delete_customer(self, customer_id):
        try:    
            customers, authors, books, shopping_carts, purchases = self.load_data() #грузим все данные
            original_count = len(customers)
            customers = [c for c in customers if c.user_id != customer_id] #удаляем кастомера по id

            if original_count == len(customers):
                print("Покупатель не найден")
                return False

            shopping_carts = [cart for cart in shopping_carts if cart.customer.user_id != customer_id] #удаляем связанные объекты
            purchases = [p for p in purchases if p.shop_cart.customer.user_id != customer_id]

            self.save_data(customers, authors, books, shopping_carts, purchases)# Сохраняем обновленные данные
            print(f"Покупатель с id {customer_id} успешно удален")
            return True
        except Exception as e:
            print(f"Ошибка при удалении покупателя: {e}")
            return False

    def create_book(self, book):
        """Создание новой книги"""
        try:
            customers, authors, books, shopping_carts, purchases = self.load_data()
            books.append(book)
            self.save_data(customers, authors, books, shopping_carts, purchases)
            print(f"Книга '{book.title}' успешно создана")
            return True
        except Exception as e:
            print(f"Ошибка при создании книги: {e}")
            return False
        
    def read_book(self, book_id):
        """Чтение книги по ID"""
        _, _, books, _, _ = self.load_data()
        for book in books:
            if book.book_id == book_id:
                return book
        return None
    
    def delete_book(self, book_id): #DRY до связи :(
        try:    
            customers, authors, books, shopping_carts, purchases = self.load_data() #грузим все данные
            original_count = len(books)
            books = [b for b in books if b.book_id != book_id] #удаляем книгу по id

            if original_count == len(books):
                print("Книга не найдена")
                return False             

            self.save_data(customers, authors, books, shopping_carts, purchases)# Сохраняем обновленные данные
            print(f"Книга с id {book_id} успешно удалена")
            return True
        except Exception as e:
            print(f"Ошибка при удалении книги: {e}")
            return False
        
    def create_author(self, author):
        try:
            customers, authors, books, shopping_carts, purchases = self.load_data()
            authors.append(author)
            self.save_data(customers, authors, books, shopping_carts, purchases)
            print(f"Автор {author.name} успешно создан")
            return True
        except Exception as e:
            print(f"Ошибка при создании автора: {e}")
            return False
    
    def read_author(self, author_id):
        """Чтение автора по ID"""
        _, authors, _, _, _ = self.load_data()
        for author in authors:
            if author.user_id == author_id:
                return author
        return None

    def delete_author(self, author_id):
        try:
            customers, authors, books, shopping_carts, purchases = self.load_data()#грузим все данные  

            books_id_for_delete = [a.books_id for a in authors if a.user_id == author_id]#сохраняем id книг для удаления 
            # Удаляем автора
            original_count = len(authors)
            authors = [a for a in authors if a.user_id != author_id]
            if len(authors) == original_count:
                print(f"Автор с id {author_id} не найден")
                return False
            
            # Сохраняем обновленные данные
            self.save_data(customers, authors, books, shopping_carts, purchases)
            print(f"Автор с ID {author_id} успешно удален")
            
            #удаляем книги автора
            if books_id_for_delete:
                for books_id in books_id_for_delete:
                    for b in books_id:
                        self.delete_book(b)
            return True
        
        except Exception as e:
            print(f"Ошибка при удалении автора: {e}")
            return False
        
    def delete_purchase(self, purchase_id):
        try:    
            customers, authors, books, shopping_carts, purchases = self.load_data() #грузим все данные
            original_count = len(purchases)
            purchases = [p for p in purchases if p.purchase_id != purchase_id] #удаляем покупку по id

            if original_count == len(purchases):
                print("Покупка не найдена")
                return False             

            self.save_data(customers, authors, books, shopping_carts, purchases)# Сохраняем обновленные данные
            print(f"Покупка с id {purchase_id} успешно удалена")
            return True
        except Exception as e:
            print(f"Ошибка при удалении покупки: {e}")
            return False        

    def clear_all_data(self):
        try:
            data = {
            "bookstore": {
                "castomers": [
                    {}
                ],
                "authors":[
                    {}
                ]
                ,
                "books": [
                    {}
                ],
                "shopping_carts": [
                    {}
                ],
                "purchases": [
                    {}
                ]
                 }
            }
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Данные успешно удалены")
            
        except Exception as e:
            print(f"Ошибка при удалении JSON: {e}")
