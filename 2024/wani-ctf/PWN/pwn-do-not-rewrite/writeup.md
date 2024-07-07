Debug using gdb and we can see that the canary is overwritten by the 4th ingredient in the second and third specifically in this code:

```c
    printf("Enter the calories per gram for %s: ", ingredients[i].name);
    scanf("%lf", &ingredients[i].calories_per_gram);

    printf("Enter the amount in grams for %s: ", ingredients[i].name);
    scanf("%lf", &ingredients[i].amount_in_grams);
```


`%lf` doesnt read bytes but floats. So we can ignore the second and third input so it doesnt replace the canary on the 4th ingredients