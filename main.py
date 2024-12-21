from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

# Настраиваем Jinja2 для загрузки шаблонов из папки templates
templates = Jinja2Templates(directory="templates")

class Product(BaseModel):
    id: int
    title: str
    description: str
    price: int


# Список товаров для эмуляции таблицы БД
products = []

"""
### Для отладки -- не пустой каталог товаров
prod1 = Product(id=1, title='prod1', description='descr 1', price=100)
prod2 = Product(id=2, title='prod 2', description='descr 2', price=400)
products.append(prod1)
products.append(prod2)
"""

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)


# Отображение главной 9домашней) страницы приложения
@app.get("/")
async def homepage(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("home.html", {"request": request})


# Отображение каталога товаров
@app.get('/catalog/')
async def get_all_products(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("catalog.html", {"request": request, "products": products})


# Вывод формы добавления товара в каталог
@app.get("/show_form_add_product/", response_class=HTMLResponse)
async def show_form_add_product(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

# Обработка данных из формы добавления товаров
@app.post("/add_product/")
async def add_product(request: Request, title: str = Form(), description: str = Form(), price: str = Form()):
    # Для повторной выдачи значений в форме при ошибках
    entered = Product(id=0, title=title, description=description, price=0)
    product_price = price
    # Проверка - число ли в поле цены?
    try:
        price = float(price)
    except ValueError:
        message = "Product price must be positive number!"
        return templates.TemplateResponse("add_product.html", {"request": request, "message": message,
                                                               "product": entered, "product_price": product_price})

    # Проверка - на положительность цены товара
    if price <= 0:
        message = "Product price must be positive number!"
        return templates.TemplateResponse("add_product.html", {"request": request, "message": message,
                                                               "product": entered, "product_price": product_price})
    # Проверка на уникальность названия товара
    if products:
        for product in products:
            if product.title == title:
                message = f"Product {title} already in catalog!"
                return templates.TemplateResponse("add_product.html", {"request": request, "message": message,
                                                                       "product": entered,
                                                                       "product_price": product_price})
    # генерация id для нового товара в каталоге
    new_product_id = max([int(product.id) for product in products], default=0) + 1
    product = Product(id=new_product_id, title=title, description=description, price=price)
    products.append(product)
    message = f"Product {title} added."
    return templates.TemplateResponse("add_product.html", {"request": request, "message": message})


async def find_product_id(product_id: int) -> int:
    """
    Функция проверки и нахождения идентификатора товара в каталоге.
    Нужна для операций удаления и обновления товара по идентификатору.
    :param product_id: Идентификатор товара
    :return: число - индекс товара в каталоге, если товар найден.
            Возвращает -1, если товар не найден.-
    """
    for product_index, product in enumerate(products):
        if product.id == product_id:
            return product_index
    return -1


# Удаление товара из каталога по идентификатору
@app.get('/delete_product/{product_id}')
async def delete_product(request: Request, product_id: int) -> HTMLResponse:
    product_index = await find_product_id(product_id)
    if product_index < 0:
        message = f"Product id={product_id} not found!"
    else:
        product = products.pop(product_index)
        message = f'Product {product.title} (id={product.id}) deleted.'
    return templates.TemplateResponse("catalog.html", {"request": request, "products": products, "message": message})
