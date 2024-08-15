#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int row = 0; row < height; row++)
    {
        for (int space = 0; space < height - row - 1; space++)
        {
            printf(" ");
        }
        for (int hash = 0; hash <= row; hash++)
        {
            printf("#");
        }
        for (int mid = 0; mid < 2; mid++)
        {
            printf(" ");
        }
        for (int hashes = 0; hashes <= row; hashes++)
        {
            printf("#");
        }
        printf("\n");
    }
}
