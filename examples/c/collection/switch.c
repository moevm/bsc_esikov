#include <stdio.h>
#include "switch.h"

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
