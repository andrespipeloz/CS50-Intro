#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string digito);
char rotate(char p, int n);

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }

    // Make sure every character in argv[1] is a digit

    bool digit = only_digits(argv[1]);
    if (digit == false)
    {
        return 1;
    }

    // Convert argv[1] from a `string` to an `int`
    int number = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("Plaintext: ");

    // Rotate the character if it's a letter
    int length = strlen(plaintext);
    char cyphertext[length + 1];

    for (int i = 0; i < length; i++)
    {
        cyphertext[i] = rotate(plaintext[i], number);
    }
    cyphertext[length] = '\0';
    printf("ciphertext: %s\n", cyphertext);
    return 0;
}

bool only_digits(string digito)
{
    bool valfal = true;
    for (int i = 0, length = strlen(digito); i < length; i++)
    {
        if (!isdigit(digito[i]))
        {
            valfal = false;
        }
    }

    if (!valfal)
    {
        printf("Usage: ./caesar key \n");
        return valfal;
    }

    return valfal;
}

char rotate(char p, int n)
{
    // Convert ASCII to alpha Index
    char pa, cy, c;
    if (islower(p))
    {
        pa = p - 'a';
        c = (pa + n) % 26;
        cy = c + 'a';
    }

    else if (isupper(p))
    {
        pa = p - 'A';
        c = (pa + n) % 26;
        cy = c + 'A';
    }
    else
    {
        return p;
    }
    return cy;
}
