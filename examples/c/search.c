#include <stdio.h>
#include "search.h"

int updateCriticalNumber(int value)
{
    if (value == 0)
    {
        int temp = 20;
        value = func(temp) + 45 - 21;
        return value;
    }
    if (value == -10)
    {
        return 10;
    }
    if (value == 10)
    {
        return func(value);
    }
    else
    {
        return value + 64;
    }
}
