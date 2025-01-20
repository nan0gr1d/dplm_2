from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

# Настраиваем Jinja2 для загрузки шаблонов из папки templates
templates = Jinja2Templates(directory="templates")

class Product(BaseModel):
    """
    Модель описания таблицы каталога товаров.
    """
    id: int
    title: str
    description: str
    price: int


# Список товаров для эмуляции таблицы БД
products = []


#  Для отладки -- не пустой каталог товаров
prod1 = Product(id=1, title='Product 1', description='Descr First', price=100)
prod2 = Product(id=2, title='Product 2', description='Descr Second', price=200)
products.append(prod1)
products.append(prod2)


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)


# Отображение
@app.get("/")
async def homepage(request: Request) -> HTMLResponse:
    """
    Функция отображения главной (домашней) страницы приложения
    :param request: - параметры запроса
    :return: - возвращает (отображает) главную страницу приложения, формируемую
            из шаблона home.html
    """
    return templates.TemplateResponse("home.html", {"request": request})


@app.get('/catalog/')
async def get_all_products(request: Request) -> HTMLResponse:
    """
    Функция отображения каталога товаров
    :param request: - параметры запроса
    :return: - возвращает страницу каталога товаров, формируемую
            из шаблона catalog.html
    """
    return templates.TemplateResponse("catalog.html", {"request": request, "products": products})


@app.get("/show_form_add_product/", response_class=HTMLResponse)
async def show_form_add_product(request: Request):
    """
    Функция отображает форму добавления товара в каталог
    :param request: - параметры запроса
    :return: - возвращает форму добавления товара в каталог, формируемую из шаблона add_product.html
    """
    return templates.TemplateResponse("add_product.html", {"request": request})


@app.post("/add_product/")
async def add_product(request: Request, title: str = Form(), description: str = Form(), price: str = Form()):
    """
    Функция обработки данных из формы добавления товара
    :param request: - параметры запроса
    :param title:  - название товара
    :param description:  - описание товара
    :param price:  - цена товара
    :return: - возвращает форму добавления товара с сообщением о добавлении товара ИЛИ
                с сообщением об ошибке, если данные в форму введены некорректно.
    """
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


@app.get('/delete_product/{product_id}')
async def delete_product(request: Request, product_id: int) -> HTMLResponse:
    """
    Функция удаление товара из каталога по идентификатору
    :param request: - параметры запроса
    :param product_id: - идентификатор товара
    :return: - возвращает текущий каталог товара через шаблон catalog.html с отображением сообщения:
                - товар удален из каталога (Product [itle] id=[id] deleted.)
                ИЛИ
                - товар с указанным идентификатором в каталоге не найден (Product id=[id] not found!)
    """
    product_index = await find_product_id(product_id)
    if product_index < 0:
        message = f"Product id={product_id} not found!"
    else:
        product = products.pop(product_index)
        message = f'Product {product.title} (id={product.id}) deleted.'
    return templates.TemplateResponse("catalog.html", {"request": request, "products": products, "message": message})
