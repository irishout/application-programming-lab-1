from digbook import DigitalBook, ShoppingCart, Purchase
from userClasses import Author, Customer
from exeptions import *
from forjson import JSONDataManager


cast = Customer(878, 'vas', 'mr.kul.06@mail.ru', 500) 

testauth = Author(565, 'king', 'mr.sdpgiu@mail.ru', 'я пишу книги', 4.5, {'inst': 'ссылка'}, [])
book = DigitalBook(100, 'IT', testauth.user_id, 400, 'страшно очень очень', [])

shopcart_cast = ShoppingCart(cast)
shopcart_cast.add_book(book)
purch = Purchase(155, shopcart_cast)

#jsonManager1 = JSONDataManager()
#jsonManager1.save_data([cast],[testauth],[book],[shopcart_cast], [purch])

jsonManager2 = JSONDataManager("testjson.json")
jsonManager2.delete_purchase(5001)



