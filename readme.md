Веб-приложение предназначено для работы с каталогом товаров. 
Приложение реализовано на языке Python и фреймворке FastAPI.
Приложение позволяет:
- просматривать текущий каталог товаров;
- удалять товары из каталога;
- добавлять товары в каталог.
 
Установка приложения (MS Windows)
---------------------------------
В среде IDE PyCharm следует клонировать проект из ссылки в GitHub:

[https://github.com/nan0gr1d/dplm_2/](https://github.com/nan0gr1d/dplm_2/)

Установить фреймворк FastAPI и нужные библиотеки:

>> pip install fastapi uvicorn pydantic aiofiles


Запуск приложения
-----------------
Для запуска приложения в среде PyCharm следует в терминале 
перейти в каталог проекта: 

>> cd [имя_проекта]

И запустить локальный сервер:

>> uvicorn main:app 

Сервер после запуска укажет URL для вызова приложения в браузере,
обычно вот этот:  

http://127.0.0.1:8000 


Примеры работы приложения
-------------------------
_Главная страница_

<img src="fast_main.jpg">


_Каталог товаров_

<img src="fast_catalog.jpg">


_Форма добавления товара_

<img src="fast_add_product.jpg">
