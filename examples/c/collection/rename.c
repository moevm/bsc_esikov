#include <stdio.h>
#include "rename.h"

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
