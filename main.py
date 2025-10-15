from digbook import DigitalBook, ShoppingCart, Purchase
from userClasses import Castomer, Author
from exeptions import *

cast = Castomer(214, 'tolyz', 'mr.kul.06@mail.ru', 500)
testauth = Author(565, 'king', 'mr.sdpgiu@mail.ru', 'я пишу книги', 4.5, {'inst': 'ссылка'}, [])
book = DigitalBook(100, 'IT', testauth, 400, 'страшно очень очень', [])

shopcart_cast = ShoppingCart(cast)
shopcart_cast.add_book(book)


purch = Purchase(155, shopcart_cast)
purch.payment()

