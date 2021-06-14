import typing as t
from app.models.base import db
from app.models import Course, Lecture, Task, User
from app.models.user import UserRole


LECTURES: t.List[t.Tuple[str, str, int]] = [
    ("Python. Первая Лекция",
     "https://yadi.sk/d/iYW00FQx84r60Q/Python.%20%D0%9F%D0%B5%D1%80%D0%B2%D0%B0%D1%8F%20%D0%9B%D0%B5%D0%BA%D1%86%D0%B8%D1%8F%20%E2%80%93%20%D0%98%D0%BB%D0%B0%D1%80%D0%B8%D1%8F%20%D0%91%D0%B5%D0%BB%D0%BE%D0%B2%D0%B0%20%D0%BE%D1%82%2017.09.19.mp4?w=1",
     1),
    ("Python и инструменты",
     "https://yadi.sk/d/iYW00FQx84r60Q/Python%20%D0%B8%20%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B%20%E2%80%93%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%20%D0%BE%D1%82%2017.09.19.mp4?w=1",
     1),
    ("Структуры данных",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A1%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%8B%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85%20%E2%80%93%20%D0%91%D0%B5%D0%BB%D0%BE%D0%B2%D0%B0%20%D0%98%D0%BB%D0%B0%D1%80%D0%B8%D1%8F%20%D0%BE%D1%82%2024.09..mp4?w=1",
     1),
    ("Экспертная сессия",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%AD%D0%BA%D1%81%D0%BF%D0%B5%D1%80%D1%82%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B5%D1%81%D1%81%D0%B8%D1%8F%20%D0%BE%D1%82%2024.09..mp4?w=1",
     1),
    ("Функции, строки, байтовые строки, потоки ввода-вывода",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%B8%2C%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B8%2C%20%D0%B1%D0%B0%D0%B8%CC%86%D1%82%D0%BE%D0%B2%D1%8B%D0%B5%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B8%2C%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BA%D0%B8%20%D0%B2%D0%B2%D0%BE%D0%B4%D0%B0-%D0%B2%D1%8B%D0%B2%D0%BE%D0%B4%D0%B0%20%E2%80%93%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%20%D0%BE%D1%82%2001.10.19.mp4?w=1",
     1),
    ("Разбор задач",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%93%C2%A0%D0%98%D0%BB%D0%B0%D1%80%D0%B8%D1%8F%20%D0%91%D0%B5%D0%BB%D0%BE%D0%B2%D0%B0%20%D0%BE%D1%82%2001.10.19.mp4?w=1",
     1),
    ("Неймспейсы, замыкания, декораторы, модули",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%9D%D0%B5%D0%B8%CC%86%D0%BC%D1%81%D0%BF%D0%B5%D0%B8%CC%86%D1%81%D1%8B%2C%20%D0%B7%D0%B0%D0%BC%D1%8B%D0%BA%D0%B0%D0%BD%D0%B8%D1%8F%2C%20%D0%B4%D0%B5%D0%BA%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D1%8B%2C%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D0%B8%20%E2%80%93%20%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B8%CC%86%20%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B5%D0%B2%20%D0%BE%D1%82%2008.10.19.mp4?w=1",
     1),
    ("Введение в bytecode",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B2%20bytecode%20%E2%80%93%20%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B8%CC%86%20%D0%A1%D1%82%D1%8B%D1%86%D0%B5%D0%BD%D0%BA%D0%BE%20%D0%BE%D1%82%2008.10.19.mp4?w=1",
     1),
    ("Разбор задач",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%93%20%D0%98%D0%BB%D0%B0%D1%80%D0%B8%D1%8F%20%D0%91%D0%B5%D0%BB%D0%BE%D0%B2%D0%B0%20%D0%BE%D1%82%2008.10.19.mp4?w=1",
     1),
    ("Numpy, pandas",
     "https://yadi.sk/d/iYW00FQx84r60Q/Numpy%2C%20pandas%20%E2%80%93%20%D0%9A%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%20%D0%9B%D1%83%D0%BD%D0%B5%D0%B2%20%D0%BE%D1%82%2015.10.19.mp4?w=1",
     1),
    ("Python - модули, пакеты и система импорта",
     "https://yadi.sk/d/iYW00FQx84r60Q/Python%20-%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D0%B8%2C%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D1%8B%20%D0%B8%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%20%D0%B8%D0%BC%D0%BF%D0%BE%D1%80%D1%82%D0%B0%20%E2%80%93%20%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B8%CC%86%20%D0%A1%D1%82%D1%8B%D1%86%D0%B5%D0%BD%D0%BA%D0%BE%20%D0%BE%D1%82%2015.10.19.mp4?w=1",
     1),
    ("Разбор задач",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%93%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%20%D0%BE%D1%82%2015.10.19.mp4?w=1",
     1),
    ("Python- классы",
     "https://yadi.sk/d/iYW00FQx84r60Q/Python-%20%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B%20%E2%80%93%20%D0%98%D0%BB%D0%B0%D1%80%D0%B8%D1%8F%20%D0%91%D0%B5%D0%BB%D0%BE%D0%B2%D0%B0%20%D0%BE%D1%82%2022.10.19.mp4?w=1",
     1),
    ("Python-типы",
     "https://yadi.sk/d/iYW00FQx84r60Q/Python-%20%D1%82%D0%B8%D0%BF%D1%8B%20%E2%80%93%20%D0%98%D0%BB%D0%B0%D1%80%D0%B8%D1%8F%20%D0%91%D0%B5%D0%BB%D0%BE%D0%B2%D0%B0%20%D0%BE%D1%82%2022.10.19.mp4?w=1",
     1),
    ("Исключения, менеджеры контекста",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%98%D1%81%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F%2C%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D1%8B%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%B0%20%E2%80%93%20%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B8%CC%86%20%D0%A1%D1%82%D1%8B%D1%86%D0%B5%D0%BD%D0%BA%D0%BE%20%D0%BE%D1%82%2029.10.19.mp4?w=1",
     1),
    ("Тестирование, логгирование, setup.py",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A2%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20%D0%BB%D0%BE%D0%B3%D0%B3%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20setup.py%20%E2%80%93%20%D0%9D%D0%B8%D0%BA%D0%B8%D1%82%D0%B0%20%D0%9F%D1%83%D1%82%D0%B8%D0%BD%D1%86%D0%B5%D0%B2%20%D0%BE%D1%82%2029.10.19.mp4?w=1",
     1),
    ("Разбор задач",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%93%20%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B8%CC%86%20%D0%A1%D1%82%D1%8B%D1%86%D0%B5%D0%BD%D0%BA%D0%BE%20%D0%BE%D1%82%2029.10.19.mp4?w=1",
     1),
    ("Часть 1 Итераторы и генераторы",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A7%D0%B0%D1%81%D1%82%D1%8C%201%20%D0%98%D1%82%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%D1%8B%20%D0%B8%20%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%D1%8B%20%E2%80%93%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%20%D0%BE%D1%82%2005.11.19.mp4?w=1",
     1),
    ("Часть 2 Итераторы и генераторы",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A7%D0%B0%D1%81%D1%82%D1%8C%202%20%D0%98%D1%82%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%D1%8B%20%D0%B8%20%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%D1%8B%20%E2%80%93%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%20%D0%BE%D1%82%2005.11.19.mp4?w=1",
     1),
    ("Разбор задач",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%93%C2%A0%D0%9A%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%20%D0%9B%D1%83%D0%BD%D0%B5%D0%B2%20%D0%BE%D1%82%2005.11.19.mp4?w=1",
     1),
    ("часть 1 Про MapReduce",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D1%87%D0%B0%D1%81%D1%82%D1%8C%201%20%D0%9F%D1%80%D0%BE%20MapReduce.%20%D0%9E%D1%82%D0%BA%D1%80%D1%8B%D1%82%D0%B0%D1%8F%20%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D1%8F%20%E2%80%93%20%D0%9C%D0%B0%D0%BA%D1%81%D0%B8%D0%BC%20%D0%90%D1%85%D0%BC%D0%B5%D0%B4%D0%BE%D0%B2%20%D0%BE%D1%82%2012.11.19.mp4?w=1",
     1),
    ("часть 2 Про MapReduce",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D1%87%D0%B0%D1%81%D1%82%D1%8C%202%20%D0%9F%D1%80%D0%BE%20MapReduce.%20%D0%9E%D1%82%D0%BA%D1%80%D1%8B%D1%82%D0%B0%D1%8F%20%D0%BB%D0%B5%D0%BA%D1%86%D0%B8%D1%8F%20%E2%80%93%20%D0%9C%D0%B0%D0%BA%D1%81%D0%B8%D0%BC%20%D0%90%D1%85%D0%BC%D0%B5%D0%B4%D0%BE%D0%B2%20%D0%BE%D1%82%2012.11.19.mp4?w=1",
     1),
    ("Web, HTTP, API",
     "https://yadi.sk/d/iYW00FQx84r60Q/Web%2C%20HTTP%2C%20API%20%E2%80%93%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%20%D0%BE%D1%82%2019.11.19.mp4?w=1",
     1),
    ("Визуализация данных на python",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%92%D0%B8%D0%B7%D1%83%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85%20%D0%BD%D0%B0%20python%20%E2%80%93%20%D0%9C%D0%B0%D1%80%D0%B8%D1%8F%20%D0%9C%D0%B0%D0%BD%D1%81%D1%83%D1%80%D0%BE%D0%B2%D0%B0%20%D0%BE%D1%82%2019.11.19.mp4?w=1",
     1),
    ("как писать прикладное API",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%BA%D0%B0%D0%BA%20%D0%BF%D0%B8%D1%81%D0%B0%D1%82%D1%8C%20%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%BE%D0%B5%20API%20-%20%D0%9A%D0%B0%D0%BC%D0%B8%D0%BB%D1%8C%20%D0%A2%D0%B0%D0%BB%D0%B8%D0%BF%D0%BE%D0%B2%2026-11-2019.mp4?w=1",
     1),
    ("subprocess, threading, multiprocessing",
     "https://yadi.sk/d/iYW00FQx84r60Q/subprocess%2C%20threading%2C%20multiprocessing%20-%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%2026-11-2019.mp4?w=1",
     1),
    ("Простые паттерны проектирования, метаклассы, дескрипторы",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%9F%D1%80%D0%BE%D1%81%D1%82%D1%8B%D0%B5%20%D0%BF%D0%B0%D1%82%D1%82%D0%B5%D1%80%D0%BD%D1%8B%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%2C%20%D0%BC%D0%B5%D1%82%D0%B0%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B%2C%20%D0%B4%D0%B5%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D1%80%D1%8B%20%E2%80%93%20%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB%20%D0%9C%D0%B0%D0%BA%D1%81%D0%B8%D0%BC%D0%BE%D0%B2%20%D0%BE%D1%82%2003.12.19.mp4?w=1",
     1),
    ("Десятиминутка про домашки",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%94%D0%B5%D1%81%D1%8F%D1%82%D0%B8%D0%BC%D0%B8%D0%BD%D1%83%D1%82%D0%BA%D0%B0%20%D0%BF%D1%80%D0%BE%20%D0%B4%D0%BE%D0%BC%D0%B0%D1%88%D0%BA%D0%B8%20%E2%80%93%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%20%D0%BE%D1%82%2003.12.19.mp4?w=1",
     1),
    ("Обзор библиотеки Tensorflow",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%9E%D0%B1%D0%B7%D0%BE%D1%80%20%D0%B1%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA%D0%B8%20Tensorflow%20%E2%80%93%20%D0%A4%D0%B8%D0%BB%D0%B8%D0%BF%D0%BF%20%D0%A1%D0%B8%D0%BD%D0%B8%D1%86%D0%B8%D0%BD%20%D0%BE%D1%82%2003.12.19.mp4?w=1",
     1),
    ("Корутины, async-await, asyncio",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%9A%D0%BE%D1%80%D1%83%D1%82%D0%B8%D0%BD%D1%8B%2C%20async-await%2C%20asyncio%20%E2%80%93%20%D0%92%D0%B0%D0%B4%D0%B8%D0%BC%20%D0%9C%D0%B0%D0%B7%D0%B0%D0%B5%D0%B2%20%D0%BE%D1%82%2010.12.19.mp4?w=1",
     1),
    ("Bindings & Extensions",
     "https://yadi.sk/d/iYW00FQx84r60Q/Bindings%20%26%20Extensions%20%E2%80%93%20%D0%9C%D0%B8%D1%80%D0%BE%D0%BD%20%D0%9B%D0%B5%D0%B2%D0%BA%D0%BE%D0%B2%20%D0%BE%D1%82%2010.12.19.mp4?w=1",
     1),
    ("Разбор задач",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%93%20%D0%9C%D0%B0%D0%BA%D1%81%D0%B8%D0%BC%20%D0%90%D1%85%D0%BC%D0%B5%D0%B4%D0%BE%D0%B2%20%D0%BE%D1%82%2017.12.19.mp4?w=1",
     1),
    ("Оптимизация по времени, памяти. Сериализация",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%9E%D0%BF%D1%82%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BF%D0%BE%20%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B8%2C%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D0%B8.%20%D0%A1%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%E2%80%93%20%D0%9A%D0%B0%D0%BC%D0%B8%D0%BB%D1%8C%20%D0%A2%D0%B0%D0%BB%D0%B8%D0%BF%D0%BE%D0%B2%20%D0%BE%D1%82%2017.12.19.mp4?w=1",
     1),
    ("Как мы прод ускоряли",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%9A%D0%B0%D0%BA%20%D0%BC%D1%8B%20%D0%BF%D1%80%D0%BE%D0%B4%20%D1%83%D1%81%D0%BA%D0%BE%D1%80%D1%8F%D0%BB%D0%B8%20%E2%80%93%20%D0%98%D0%BB%D1%8C%D1%8F%20%D0%98%D1%80%D1%85%D0%B8%D0%BD%20%D0%BE%D1%82%2017.12.19.mp4?w=1",
     1),
    ("Разбор задач",
     "https://yadi.sk/d/iYW00FQx84r60Q/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%93%20%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB%20%D0%9C%D0%B0%D0%BA%D1%81%D0%B8%D0%BC%D0%BE%D0%B2%20%D0%BE%D1%82%2017.12.19.mp4?w=1",
     1),
    ("c++ video 1", "https://youtu.be/FGTcj6kSzGA", 2)]
COURSES = ['python', 'c++']

TASKS = [
    # LECTURE 1
    {
        "name": "Hello world",
        "code": "hello_world",
        "text": "<p>Напишите фцнкцию которая возвращает текст \"Hello World\"</p><p>Загрузите файл содержащий функцию <code>def hello_world():</code></p>",
        "lecture_index": 0
    },
    {
        "name": "Common types",
        "code": "common_types",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Common types 2",
        "code": "common_types_2",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Bin tricky",
        "code": "bin_tricky",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Middle value of triple",
        "code": "middle_value_of_triple",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Fizz buzz",
        "code": "fizz_buzz",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Iterate me",
        "code": "iterate_me",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Reverse List",
        "code": "reverse_list",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Make assert",
        "code": "make_assert",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Merge list",
        "code": "merge_list",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Filter list by list",
        "code": "filter_list_by_list",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Bin basic",
        "code": "bin_basic",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Bin peak",
        "code": "bin_peak",
        "text": "",
        "lecture_index": 0
    },
    {
        "name": "Bin min",
        "code": "bin_min",
        "text": "",
        "lecture_index": 0
    },

    # LECTURE 2
    {
        "name": "Banner search system",
        "code": "banner_search_system",
        "text": "",
        "lecture_index": 1
    },
    {
        "name": "Alphabet",
        "code": "alphabet",
        "text": "",
        "lecture_index": 1
    },
    {
        "name": "Rt join",
        "code": "rt_join",
        "text": "",
        "lecture_index": 1
    },
    {
        "name": "Reverse dict",
        "code": "reverse_dict",
        "text": "",
        "lecture_index": 1
    },
    {
        "name": "Min to drop",
        "code": "min_to_drop",
        "text": "",
        "lecture_index": 1
    },
    {
        "name": "Comprehensions",
        "code": "comprehensions",
        "text": "",
        "lecture_index": 1
    },
    {
        "name": "Traverse dictionary",
        "code": "traverse_dictionary",
        "text": "",
        "lecture_index": 1
    },
    {
        "name": "Merge list 2",
        "code": "merge_list_2",
        "text": "",
        "lecture_index": 1
    },
    #     # LECTURE 3
    #     'tail': start_time + timedelta(weeks=6),
    #     'git_blob': start_time + timedelta(weeks=6),
    #     'git_log': start_time + timedelta(weeks=6),
    #     'caesar_cipher': start_time + timedelta(weeks=6),
    #     'count_util': start_time + timedelta(weeks=6),
    #     'merge_list_3': start_time + timedelta(weeks=6),
    #     'normalize_path': start_time + timedelta(weeks=6),
    #     'input_': start_time + timedelta(weeks=6),
    #     # PRE HW 1
    #     'arg_binding': start_time + timedelta(weeks=8),
    #     'codeops': start_time + timedelta(weeks=8),
    #     'byteme': start_time + timedelta(weeks=8),
    #     # HW 1
    #     'vm': start_time + timedelta(weeks=10),
    #     # LECTURE 4
    #     'calc': start_time + timedelta(weeks=12),
    #     'profiler': start_time + timedelta(weeks=12),
    #     'lru_cache': start_time + timedelta(weeks=12),
    #     # LECTURE 5
    #     'numpy_basic': start_time + timedelta(weeks=14),
    #     'replace_nans': start_time + timedelta(weeks=14),
    #     'nonzero_product': start_time + timedelta(weeks=14),
    #     'nearest_value': start_time + timedelta(weeks=14),
    #     'max_element': start_time + timedelta(weeks=14),
    #     'add_zeros': start_time + timedelta(weeks=14),
    #     'vander': start_time + timedelta(weeks=14),
    #     # LECTURE 6
    #     'life_game': start_time + timedelta(weeks=16),
    #     'list_twist': start_time + timedelta(weeks=16),
    #     'game_has_no_name': start_time + timedelta(weeks=16),
    #     'typy': start_time + timedelta(weeks=16),
    #     'typy_generic': start_time + timedelta(weeks=16),
    #     'typy_protocol': start_time + timedelta(weeks=16),
    #     # LECTURE 7
    #     'context_manager': start_time + timedelta(weeks=18),
    #     'broken_module': start_time + timedelta(weeks=18),
    #     'banner_engine': start_time + timedelta(weeks=18),
    #     # LECTURE 8
    #     'warm_it': start_time + timedelta(weeks=20),
    #     'flat_it': start_time + timedelta(weeks=20),
    #     'range': start_time + timedelta(weeks=1),
    #     'pyos': start_time + timedelta(weeks=1),
    #     # PRE HW 2
    #     'diesel_power': start_time + timedelta(weeks=1),
    #     # HW 2
    #     'compgraph': start_time + timedelta(weeks=1),
    #     # LECTURE 10-10.5
    #     'visualization': start_time + timedelta(weeks=1),
    #     'translation_chains': start_time + timedelta(weeks=1),
    #     'wiki_distance': start_time + timedelta(weeks=1),
    #     # LECTURE 11
    #     'property_converter': start_time + timedelta(weeks=1),
    #     'temperature': start_time + timedelta(weeks=1),
    #     # HW 3
    #     'cinemabot': start_time + timedelta(weeks=1),
    #     # LECTURE 12
    #     'animals': start_time + timedelta(weeks=1),
    #     # LECTURE 13
    #     'fbs_parser': start_time + timedelta(weeks=1),
    #     'sync_vs_async': start_time + timedelta(weeks=1),
    #     'async_proxy': start_time + timedelta(weeks=1),
]


def init_courses():
    for name_course in COURSES:
        course = Course(name=name_course)
        db.session.add(course)
    db.session.commit()


def init_lectures():
    for name, ref, course_id in LECTURES:
        lecture = Lecture(name=name, ref=ref, course_id=course_id)
        db.session.add(lecture)
    db.session.commit()


def init_tasks():
    for data in TASKS:
        lecture = LECTURES[data.pop('lecture_index')]
        lecture = Lecture.query.filter_by(name=lecture[0]).one()
        task = Task(lecture_id=lecture.id, **data)
        db.session.add(task)
    db.session.commit()


# сделать проверки на существование


def add_course(name_course):
    course = db.session.query(Course).filter(Course.name == name_course).first()
    if not course:
        new_course = Course(name=name_course)
        db.session.add(new_course)
        db.session.commit()


def add_lectures(list_lectures):
    for name, ref, course_id in list_lectures:
        lecture = db.session.query(Lecture).filter(Lecture.course_id == course_id).filter(Lecture.name == name).first()
        if not lecture:
            new_lecture = Lecture(name=name, ref=ref, course_id=course_id)
            db.session.add(new_lecture)
            db.session.commit()


def create_admin():
    admin = User(login='admin', password="123", role=UserRole.admin)
    db.session.add(admin)
    db.session.commit()


def create_student(login):
    admin = User(login=login, password="123", role=UserRole.student)
    db.session.add(admin)
    db.session.commit()


def init_database():
    init_courses()
    init_lectures()
    init_tasks()
    create_admin()
    create_student('student')
    create_student('student_1')
