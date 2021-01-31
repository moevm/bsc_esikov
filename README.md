# bsc_esikov

## Запуск

Переименовать файл `.env.example` в `.env` и внести в него свои данные, согласно представленному шаблону.

Для запуска необходимо в качестве параметров передать путь до проверяемого файла .c:
```
python3 main.py -f ../program.c
```

Если необходимо осуществить поиск в конкретной директории, то нужно передать соответствующий путь с помощью параметра ``-d``:
```
python3 main.py -f ../program.c -d ../search_dir
```

Один или оба параметра могут быть url к github файлам и репозиториям:
```
python3 main.py -f https://github.com/owner/repo/blob/master/src/file.c -d https://github.com/owner/repo
```

## Параметры

### Обязательные

* Путь до проверяемого файла в файловой системе или на github: `-f` или `--file`

### Необязательные

* Путь до директории или репозитория, где осуществляется поиск: `-d` или `--data`. По умолчанию поиск осуществляется в репозиториях по названиям функций в файле с помощью [search code](https://searchcode.com/).
* Предельное значение допустимого сходства программ в процентах — при его превышении программа будет считаться заимствованной: `-l` или `--limit`. По умолчанию — 60%.

## Пример работы

Воспроизвести результат можно с помощью команды:
```
python3 main.py -f ./examples/c/search.c -d ./examples/c/collection -l 10
```

Исходный файл:
```
#include <stdio.h>
#include "search.h"

int updateCriticalNumber(int value)
{
    if (value == 0)
    {
        return value + 64;
    }
    if (value == -10)
    {
        return 10;
    }
    if (value == 10)
    {
        return func(value);
    }
}
```

### Результат

#### rename.c:

Сходство 100%.

Схожие фрагменты:
```
int changeValue(int number)
{
    if (number == 0) {
        return number + 64;
    }
    if (number == -10) {
        return 10;
    }
    if (number == 10) {
        return func(number);
    }
}
```

#### switch.c:

Сходство 100%.

Схожие фрагменты:
```
int updateCriticalNumber(int value)
{
    switch (value)
    {
        case 0:
        {
            return value + 64;
            break;
        }
        case -10:
        {
            return 10;
            break;
        }
        case 10:
        {
            return func(value);
            break;
        }
    }
}
```

#### max_change.c:

Сходство 80%.

Схожие фрагменты:
```
long myFunc(long x)
{
    //double value = 0.456;
    // if
    if (x == 0)
    {
        return x + 64;
                                }
    if (x == -10)

                            return 10;
        if (x == 10)
                    {
            // return
            return func(x);
            }
```

#### other_func.c:

Сходство 43%.

Схожие фрагменты:
```
if (a > b)
        return a;
    else
        return 
```

## Тестирование

Все тесты расположены в папке ``tests``. Для выполнения конкретного теста можно использовать команду:
```
python3 -m unittest tests/test_tokenizer.py
```

Для выполнения всех тестов используется скрипт:
```
python3 test_runner.py
```
