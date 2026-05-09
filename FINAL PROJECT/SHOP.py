from typing import List, Set, Optional
from dataclasses import dataclass
import uuid



@dataclass(frozen=True)
class Product:
    """
    Класс данных для товара.
    Использование dataclass обеспечивает чистоту кода и автоматическую реализацию методов __init__ и __repr__.
    frozen=True делает объект неизменяемым, что является хорошей практикой в проектировании.
    """
    id: str
    name: str
    price: float
    category: str

    def __str__(self) -> str:
        return f"[{self.category}] {self.name} - {self.price:,.2f} KZT"




class Store:
    """
    Класс управления магазином.
    Инкапсулирует логику хранения товаров и фильтрации.
    """

    def __init__(self):
        # Используем список для хранения объектов Product (согласно плану проекта)
        self.__products: List[Product] = []
        # Используем множество (Set) для быстрого получения списка уникальных категорий
        self.__categories: Set[str] = set()

    def add_product(self, name: str, price: float, category: str) -> None:
        """
        Метод добавления товара с валидацией данных.
        """
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")

        new_product = Product(
            id=str(uuid.uuid4())[:8],  # Генерация короткого ID
            name=name,
            price=price,
            category=category
        )
        self.__products.append(new_product)
        self.__categories.add(category.lower())

    def get_all_products(self) -> List[Product]:
        """Возвращает копию списка всех товаров."""
        return self.__products.copy()

    def find_by_name(self, search_term: str) -> List[Product]:
        """Поиск товаров по частичному совпадению имени."""
        return [p for p in self.__products if search_term.lower() in p.name.lower()]

    def filter_by_category(self, category: str) -> List[Product]:
        """Фильтрация товаров по категории."""
        return [p for p in self.__products if p.category.lower() == category.lower()]

    def get_categories(self) -> List[str]:
        """Возвращает отсортированный список всех категорий."""
        return sorted(list(self.__categories))




def initialize_demo_store():
    store = Store()


    items = [
        ("MacBook Air M2", 650000.00, "Электроника"),
        ("iPhone 15 Pro", 580000.00, "Электроника"),
        ("Python для профессионалов", 12500.00, "Книги"),
        ("Механическая клавиатура", 45000.00, "Аксессуары"),
        ("Монитор 4K", 180000.00, "Электроника")
    ]

    for name, price, cat in items:
        store.add_product(name, price, cat)

    return store


if __name__ == "__main__":
    print("=== Система Online Store: Недели 1-2 успешно запущены ===\n")


    my_store = initialize_demo_store()


    print("--- Полный ассортимент магазина ---")
    for prod in my_store.get_all_products():
        print(prod)


    target_cat = "Электроника"
    print(f"\n--- Фильтр по категории: {target_cat} ---")
    electronics = my_store.filter_by_category(target_cat)
    for item in electronics:
        print(f"Найдено: {item.name}")


    print(f"\nУникальные категории в базе: {', '.join(my_store.get_categories())}")