# bsc_esikov

## Запуск

Для работы необходимо в качестве параметров передать путь до проверяемого файла .c и путь до директории, в которой осуществляется поиск:
```
python3 main.py -f ../program.c -d ../search_dir
```

## Параметры

### Обязательные

* Путь до проверяемого файла `-f` или `--file`
* Путь до директории, в которой осуществляется поиск `-d` или `--dir`

### Необязательные

* Предельное значение допустимого сходства программ — при его превышении программа будет считаться заимствованной `-l` или `--limit`

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
