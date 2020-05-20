#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //set variable n to prompt size later on
    int n;
    int i;
    int j;
    //do while loop to prompt height of desirable hash blocks
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
    for(i = 0; i < n; i++)
    {
        // left block
        for(j = 0; j < n-1-i; j++)
        {
            printf(" ");
        }
        for(j = 0; j < i + 1; j++)
        {
            printf("#");
        }

        // 2 spaces in the middle
        printf("  ");

        // right block, order swapped
        for(j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
