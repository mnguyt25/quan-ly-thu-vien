import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.books import get_all_books
books = get_all_books()
for b in books:
    print(b)

