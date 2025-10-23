import xml.etree.ElementTree as ET
from userClasses import Customer, Author
from digbook import DigitalBook, ShoppingCart, Purchase

class XMLDataManager:
    def __init__(self, filename="xmldata.xml"):
        self.filename = filename
    
    def save_data(self, customers: list, authors: list, books: list, shopping_carts: list, purchases: list):
        #Сохранение всех данных в XML файл
        try:
            # Создаем корневой элемент
            root = ET.Element("bookstore_system")
            
            # Добавляем все разделы
            self.__save_customers(root, customers)
            self.__save_authors(root, authors)
            self.__save_books(root, books)
            self.__save_shopping_carts(root, shopping_carts)
            self.__save_purchases(root, purchases)
            
            # Создаем дерево и записываем в файл
            tree = ET.ElementTree(root)
            self._pretty_print(root)

            xml_string = ET.tostring(root, encoding='utf-8', method='xml', xml_declaration=True)
        
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(xml_string.decode('utf-8'))
            print(f"Данные успешно сохранены в {self.filename}")
            
        except Exception as e:
            print(f"Ошибка при сохранении XML: {e}")
    
    def load_data(self):
        #Загрузка данных из XML файла
        try:
            tree = ET.parse(self.filename)
            root = tree.getroot()
            
            customers = self.__load_customers(root.find("customers"))
            authors = self.__load_authors(root.find("authors"))
            books_data = root.find("books")
            shopping_carts_data = root.find("shopping_carts")
            purchases_data = root.find("purchases")
            
            books = self.__load_books(books_data)
            shopping_carts = self.__load_shopping_carts(shopping_carts_data, customers, books)
            purchases = self.__load_purchases(purchases_data, customers, books)
            
            print(f"Данные успешно загружены из {self.filename}")
            return customers, authors, books, shopping_carts, purchases
            
        except Exception as e:
            print(f"Ошибка при загрузке XML: {e}")
            return [], [], [], [], []
    
    def __save_customers(self, root, customers):
        #Сохранение покупателей в XML
        customers_elem = ET.SubElement(root, "customers")
        for customer in customers:
            customer_elem = ET.SubElement(customers_elem, "customer")
            
            ET.SubElement(customer_elem, "user_id").text = str(customer.user_id)
            ET.SubElement(customer_elem, "name").text = customer.name
            ET.SubElement(customer_elem, "email").text = customer.email
            ET.SubElement(customer_elem, "balance").text = str(customer.balance)
            
            library_elem = ET.SubElement(customer_elem, "library")
            for book_id in customer.library:
                ET.SubElement(library_elem, "book_id").text = str(book_id)
    
    def __save_authors(self, root, authors):
        #Сохранение авторов в XML
        authors_elem = ET.SubElement(root, "authors")
        for author in authors:
            author_elem = ET.SubElement(authors_elem, "author")
            
            ET.SubElement(author_elem, "user_id").text = str(author.user_id)
            ET.SubElement(author_elem, "name").text = author.name
            ET.SubElement(author_elem, "email").text = author.email
            ET.SubElement(author_elem, "biography").text = author.biography
            ET.SubElement(author_elem, "rating").text = str(author.rating)
            
            social_elem = ET.SubElement(author_elem, "social_media")
            for platform, link in author.social_media.items():
                ET.SubElement(social_elem, platform).text = link
            
            books_elem = ET.SubElement(author_elem, "books_id")
            for book_id in author.books_id:
                ET.SubElement(books_elem, "book_id").text = str(book_id)
    
    def __save_books(self, root, books):
        #Сохранение книг в XML
        books_elem = ET.SubElement(root, "books")
        for book in books:
            book_elem = ET.SubElement(books_elem, "book")
            
            ET.SubElement(book_elem, "book_id").text = str(book.book_id)
            ET.SubElement(book_elem, "title").text = book.title
            ET.SubElement(book_elem, "author_id").text = str(book.author_id)
            ET.SubElement(book_elem, "price").text = str(book.price)
            ET.SubElement(book_elem, "description").text = book.description
            
            tags_elem = ET.SubElement(book_elem, "tags")
            for tag in book.tags:
                ET.SubElement(tags_elem, "tag").text = tag
    
    def __save_shopping_carts(self, root, carts):
        #Сохранение корзин в XML
        carts_elem = ET.SubElement(root, "shopping_carts")
        for cart in carts:
            cart_elem = ET.SubElement(carts_elem, "cart")
            
            ET.SubElement(cart_elem, "customer_id").text = str(cart.customer.user_id)
            
            items_elem = ET.SubElement(cart_elem, "items")
            for book in cart.items:
                ET.SubElement(items_elem, "book_id").text = str(book.book_id)
            
            ET.SubElement(cart_elem, "total_amount").text = str(cart.get_sum())
    
    def __save_purchases(self, root, purchases):
        #Сохранение покупок в XML
        purchases_elem = ET.SubElement(root, "purchases")
        for purchase in purchases:
            purchase_elem = ET.SubElement(purchases_elem, "purchase")
            
            ET.SubElement(purchase_elem, "purchase_id").text = str(purchase.purchase_id)
            ET.SubElement(purchase_elem, "customer_id").text = str(purchase.shop_cart.customer.user_id)
            
            books_elem = ET.SubElement(purchase_elem, "books")
            for book in purchase.purchased_books:
                ET.SubElement(books_elem, "book_id").text = str(book.book_id)
            
            ET.SubElement(purchase_elem, "total_amount").text = str(purchase.shop_cart.get_sum() if purchase.shop_cart else 0)
    
    def __load_customers(self, customers_elem):
        #Загрузка покупателей из XML
        customers = []
        if customers_elem is None:
            return customers
            
        for customer_elem in customers_elem.findall("customer"):
            try:
                user_id = int(customer_elem.find("user_id").text)
                name = customer_elem.find("name").text
                email = customer_elem.find("email").text
                balance = float(customer_elem.find("balance").text)
                
                customer = Customer(user_id, name, email, balance)
                
                library_elem = customer_elem.find("library")
                if library_elem is not None:
                    customer.library = [int(book_id.text) for book_id in library_elem.findall("book_id")]
                
                customers.append(customer)
            except Exception as e:
                print(f"Ошибка при создании покупателя: {e}")
        return customers
    
    def __load_authors(self, authors_elem):
        #Загрузка авторов из XML
        authors = []
        if authors_elem is None:
            return authors
            
        for author_elem in authors_elem.findall("author"):
            try:
                user_id = int(author_elem.find("user_id").text)
                name = author_elem.find("name").text
                email = author_elem.find("email").text
                biography = author_elem.find("biography").text
                rating = float(author_elem.find("rating").text)
                
                social_media = {}
                social_elem = author_elem.find("social_media")
                if social_elem is not None:
                    for elem in social_elem:
                        social_media[elem.tag] = elem.text
                
                books_id = []
                books_elem = author_elem.find("books_id")
                if books_elem is not None:
                    books_id = [int(book_id.text) for book_id in books_elem.findall("book_id")]
                
                author = Author(user_id, name, email, biography, rating, social_media, books_id)
                authors.append(author)
            except Exception as e:
                print(f"Ошибка при создании автора: {e}")
        return authors
    
    def __load_books(self, books_elem):
        #Загрузка книг из XML
        books = []
        if books_elem is None:
            return books
            
        for book_elem in books_elem.findall("book"):
            try:
                book_id = int(book_elem.find("book_id").text)
                title = book_elem.find("title").text
                author_id = int(book_elem.find("author_id").text)
                price = float(book_elem.find("price").text)
                description = book_elem.find("description").text
                
                tags = []
                tags_elem = book_elem.find("tags")
                if tags_elem is not None:
                    tags = [tag.text for tag in tags_elem.findall("tag")]
                
                book = DigitalBook(book_id, title, author_id, price, description, tags)
                books.append(book)
            except Exception as e:
                print(f"Ошибка при создании книги: {e}")
        return books
    
    def __load_shopping_carts(self, carts_elem, customers, books):
        #Загрузка корзин из XML
        shopping_carts = []
        if carts_elem is None:
            return shopping_carts
            
        customer_dict = {customer.user_id: customer for customer in customers}
        book_dict = {book.book_id: book for book in books}
        
        for cart_elem in carts_elem.findall("cart"):
            try:
                customer_id = int(cart_elem.find("customer_id").text)
                customer = customer_dict.get(customer_id)
                
                if customer:
                    cart = ShoppingCart(customer)
                    
                    items_elem = cart_elem.find("items")
                    if items_elem is not None:
                        for book_id_elem in items_elem.findall("book_id"):
                            book_id = int(book_id_elem.text)
                            book = book_dict.get(book_id)
                            if book:
                                cart.items.append(book)
                    
                    shopping_carts.append(cart)
                else:
                    print(f"Покупатель с ID {customer_id} не найден")
            except Exception as e:
                print(f"Ошибка при создании корзины: {e}")
        return shopping_carts
    
    def __load_purchases(self, purchases_elem, customers, books):
        #Загрузка покупок из XML
        purchases = []
        if purchases_elem is None:
            return purchases
            
        customer_dict = {customer.user_id: customer for customer in customers}
        book_dict = {book.book_id: book for book in books}
        
        for purchase_elem in purchases_elem.findall("purchase"):
            try:
                purchase_id = int(purchase_elem.find("purchase_id").text)
                customer_id = int(purchase_elem.find("customer_id").text)
                customer = customer_dict.get(customer_id)
                
                if customer:
                    temp_cart = ShoppingCart(customer)
                    
                    books_elem = purchase_elem.find("books")
                    if books_elem is not None:
                        for book_id_elem in books_elem.findall("book_id"):
                            book_id = int(book_id_elem.text)
                            book = book_dict.get(book_id)
                            if book:
                                temp_cart.items.append(book)
                    
                    purchase = Purchase(purchase_id, temp_cart)
                    purchase.purchased_books = temp_cart.items.copy()
                    purchases.append(purchase)
                else:
                    print(f"Покупатель с ID {customer_id} не найден")
            except Exception as e:
                print(f"Ошибка при создании покупки: {e}")
        return purchases

    
    def create_customer(self, customer):
        #Создание нового покупателя
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
        #Чтение покупателя по ID
        customers, _, _, _, _ = self.load_data()
        for customer in customers:
            if customer.user_id == customer_id:
                return customer
        return None
    
    def delete_customer(self, customer_id):
        #Удаление покупателя по ID
        try:
            customers, authors, books, shopping_carts, purchases = self.load_data()
            original_count = len(customers)
            
            customers = [c for c in customers if c.user_id != customer_id]
            shopping_carts = [cart for cart in shopping_carts if cart.customer.user_id != customer_id]
            purchases = [p for p in purchases if p.shop_cart.customer.user_id != customer_id]
            
            if original_count == len(customers):
                print("Покупатель не найден")
                return False
            
            self.save_data(customers, authors, books, shopping_carts, purchases)
            print(f"Покупатель с ID {customer_id} успешно удален")
            return True
        except Exception as e:
            print(f"Ошибка при удалении покупателя: {e}")
            return False
    
    def create_book(self, book):
        #Создание новой книги
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
        #Чтение книги по ID
        _, _, books, _, _ = self.load_data()
        for book in books:
            if book.book_id == book_id:
                return book
        return None
    
    def delete_book(self, book_id):
        #Удаление книги по ID
        try:
            customers, authors, books, shopping_carts, purchases = self.load_data()
            original_count = len(books)
            
            books = [b for b in books if b.book_id != book_id]
            
            if original_count == len(books):
                print("Книга не найдена")
                return False
            
            self.save_data(customers, authors, books, shopping_carts, purchases)
            print(f"Книга с ID {book_id} успешно удалена")
            return True
        except Exception as e:
            print(f"Ошибка при удалении книги: {e}")
            return False
    
    def create_author(self, author):
        #Создание нового автора
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
        #Чтение автора по ID
        _, authors, _, _, _ = self.load_data()
        for author in authors:
            if author.user_id == author_id:
                return author
        return None
    
    def delete_author(self, author_id):
        #Удаление автора по ID
        try:
            customers, authors, books, shopping_carts, purchases = self.load_data()
            original_count = len(authors)
            
            # Находим книги автора для удаления
            author_to_delete = None
            for author in authors:
                if author.user_id == author_id:
                    author_to_delete = author
                    break
            
            if author_to_delete is None:
                print(f"Автор с ID {author_id} не найден")
                return False
            
            # Удаляем автора
            authors = [a for a in authors if a.user_id != author_id]
            
            # Удаляем книги автора
            if author_to_delete.books_id:
                books = [b for b in books if b.book_id not in author_to_delete.books_id]
            
            self.save_data(customers, authors, books, shopping_carts, purchases)
            print(f"Автор с ID {author_id} и его книги успешно удалены")
            return True
        except Exception as e:
            print(f"Ошибка при удалении автора: {e}")
            return False
    
    def clear_all_data(self):
        #Очистка всех данных
        try:
            root = ET.Element("bookstore_system")
            ET.SubElement(root, "customers")
            ET.SubElement(root, "authors")
            ET.SubElement(root, "books")
            ET.SubElement(root, "shopping_carts")
            ET.SubElement(root, "purchases")
            
            tree = ET.ElementTree(root)
            self._pretty_print(root)
            
            xml_string = ET.tostring(root, encoding='utf-8', method='xml', xml_declaration=True)
        
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(xml_string.decode('utf-8'))
            
            print("Все данные успешно очищены")
        except Exception as e:
            print(f"Ошибка при очистке данных: {e}")
    
    def _pretty_print(self, elem, level=0):     #magic code idk
        """Форматирование XML с отступами"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._pretty_print(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    