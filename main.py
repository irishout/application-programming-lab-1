from digbook import DigitalBook, ShoppingCart, Purchase
from userClasses import Author, Customer
from exeptions import *
from forjson import JSONDataManager
from forxml import XMLDataManager
import json


# with open("testjson.json", 'r', encoding='utf-8') as f:
#     data = json.load(f)

#print(data['bookstore']['customers'][0])


cast = Customer(1, 'vas', 'mr.kul.06@mail.ru', 1) 

testauth = Author(565, 'king', 'mr.sdpgiu@mail.ru', 'я пишу книги', 4.5, {'inst': 'ссылка'}, [])
book = DigitalBook(105, 'IT', testauth.user_id, 400, 'страшно очень очень', [])

shopcart_cast = ShoppingCart(cast)
shopcart_cast.add_book(book)
purch = Purchase(155, shopcart_cast)

# jsonManager1 = JSONDataManager()
# jsonManager1.save_data([cast],[testauth],[book],[shopcart_cast], [purch])

#jsonManager2 = JSONDataManager("testjson.json")
#jsonManager2.create_author(author)

# xmlmanager = XMLDataManager()
# xmlmanager.save_data([cast],[testauth],[book],[shopcart_cast], [purch])



