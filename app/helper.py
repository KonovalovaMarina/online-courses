import typing as t
from datetime import datetime

from app.deadlines import python_course
from app.models.base import db
from app.models import Course, Lecture, Mark, Module, Task, User
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
    {"name": "Hello world", "code": "hello_world", "text": "<p>Напишите функцию которая возвращает текст \"Hello World\"</p><p>Загрузите файл содержащий функцию <code>def hello_world():</code></p>", "lecture_index": 0},
    {"name": "Hello universe", "code": "hello_universe", "text": "<p>Напишите функцию которая возвращает текст \"Hello Universe\"</p><p>Загрузите файл содержащий функцию <code>def hello_universe():</code></p>", "lecture_index": 0}
]


def init_marks(user_id: int):
    # за все практики при регистрации пользователя ему выставляются оценки 0
    modules = db.session.query(Module).all()
    for module in modules:
        mark = Mark(user_id=user_id, module_id=module.id, mark=0)
        db.session.add(mark)
        db.session.commit()


def init_courses():
    for name_course in COURSES:
        course = Course(name=name_course)
        db.session.add(course)
    db.session.commit()


def init_modules(deadline_list: t.List[t.Dict[str, datetime]]):
    course_id = 1
    for course in deadline_list:
        for module_name, deadline in course.items():
            record = Module(name=module_name, course_id=course_id, deadline=deadline)
            db.session.add(record)
        db.session.commit()
        course_id += 1


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


def add_modules(course_id: int, list_modules: t.Dict[str, datetime]):
    for module_name, deadline in list_modules:
        module = db.session.query(Module).filter(
            Module.course_id == course_id,
            Module.name == module_name
        ).first()
        if not module:
            record = Module(name=module_name, course_id=course_id, deadline=deadline)
            db.session.add(record)
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


def create_student():
    admin = User(login='student', password="123", role=UserRole.student)
    db.session.add(admin)
    db.session.commit()


def init_database():
    init_courses()
    init_modules([python_course])
    init_lectures()
    init_tasks()
    create_admin()
    create_student()
