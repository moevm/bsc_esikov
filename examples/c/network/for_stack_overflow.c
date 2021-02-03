#include<stdio.h>
float getDiscountedPrice(float totalPrice, float discountedPercent){
    float percentageOf = (discountedPercent/100)*totalPrice;
    return totalPrice - percentageOf;
}

int main(){
    float totalPrice, discountedPercent, sum;
    printf("Total price of the product? - ");
    scanf("%f", &totalPrice);
    printf("The amount of discount percentage? - ");
    scanf("%f", &discountedPercent);
    sum = getDiscountedPrice(totalPrice,discountedPercent);
    printf("Your discounted price is Rs %f", sum);

}
