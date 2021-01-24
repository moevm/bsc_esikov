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
