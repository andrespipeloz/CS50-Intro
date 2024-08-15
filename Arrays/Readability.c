#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    //Number of letters
    int letters = count_letters(text);

    //Number of Words
    int words = count_words(text);

    //Number of sentences
    int sentences = count_sentences(text);

    //Coleman-Liau index
    float L = ((float) letters / (float) words) * 100;
    float S = ((float) sentences / (float) words) * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;
    int inde = round(index);

    if (inde < 1)
    {
        printf("Before Grade 1\n");
    }
    if (1 < inde && inde < 16)
    {
        printf("Grade %i\n", inde);
    }
    if (inde >= 16)
    {
        printf("Grade 16+\n");
    }
}

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    words = words + 1;
    return words;
}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == 33)
        {
            sentences++;
        }
        else if (text[i] == 46)
        {
            sentences++;
        }
        else if (text[i] == 63)
        {
            sentences++;
        }
    }
    return sentences;
}
