# bsc_esikov

## Запуск

Переименовать файл `.env.example` в `.env` и внести в него свои данные, согласно представленному шаблону.

Запуск осуществляется с помощью команды
```
python3 main.py -c ../program.c
```

Или с помощью *docker*
```
docker-compose build --no-cache  
docker-compose up
```

## Параметры

### Обязательные

* **Check path** — путь до файла или директории на [github](https://github.com/)
* **Language** — проверяемый язык программирования

### Необязательные

* **Search path** — путь до файла, директории или репозитория на [github](https://github.com/). Если не указать, то поиск будет осуществляться в репозиториях на [github](https://github.com/) и на [stackoverflow](https://stackoverflow.com/) по названиям функций в файле с помощью [search code](https://searchcode.com/), [github search](https://docs.github.com/en/rest/reference/search#search-code), [stack exchange](https://api.stackexchange.com/docs/advanced-search)
* **Limit** — предельное значение допустимого сходства программ в процентах — при его превышении программа будет считаться заимствованной. По умолчанию **60%**
* **Branches to search** — осуществлять ли поиск только на главной ветке репозитория или на всех ветках

## Тестирование

Все тесты расположены в папке ``tests``. Для выполнения конкретного теста можно использовать команду:
```
python3 -m unittest tests/test_tokenizer.py
```

Для выполнения всех тестов используется скрипт:
```
python3 test_runner.py
```

Для выполнения тестов на скорость работы используется скрипт:
```
python3 time_test_runner.py
```

## Описание

Более подробно прочитать про принцип работы можно [на wiki](https://github.com/moevm/bsc_esikov/wiki)
