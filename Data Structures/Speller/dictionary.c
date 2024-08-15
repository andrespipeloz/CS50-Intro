// Implements a dictionary's functionality

#include <cs50.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * 45;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // Hash the word to obtain its hash value
    unsigned int hash_value = hash(word);

    // Search the hash table at the location specified by the word’s hash value
    for (node *cursor = table[hash_value]; cursor != NULL; cursor = cursor->next)
    {
        // Return true if the word is found
        char *prueba = cursor->word;
        if (strcasecmp(prueba, word) == 0)
        {
            return true;
        }
    }
    // Return false if no word is found
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int length = strlen(word);
    int hash = (toupper(word[0]) - 'A') * (length + 1) - 1;
    if (hash > N)
    {
        hash = hash % N;
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO

    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        printf("Could not open dictionary in r \n");
        return false;
    }

    char *word = malloc(LENGTH + 1);
    if (word == NULL)
    {
        printf("Could not malloc for word \n");
        return false;
    }

    // Set all table ptr to NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Read each word in the file

    while (fscanf(source, "%s", word) != EOF)
    {
        // Create space for a new hash table node
        node *new_word = malloc(sizeof(node));
        if (new_word == NULL)
        {
            printf("Could not malloc for new_word \n");
            return false;
        }

        // Copy the word into the new node
        strcpy(new_word->word, word);
        new_word->next = NULL;

        // Hash the word to obtain its hash value
        unsigned int hash_value = hash(new_word->word);

        // Insert the new node into the hash table (using the index specified by its hash value)
        new_word->next = table[hash_value];
        table[hash_value] = new_word;
    }

    // Close the dictionary file
    fclose(source);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    int counter = 0;
    for (int i = 0; i < N; i++)
    {
        for (node *ptr = table[i]; ptr != NULL; ptr = ptr->next)
        {
            if (sizeof(ptr->word) == sizeof(char *) || strlen((char *) ptr->word) != 0)
            {
                counter++;
            }
        }
    }

    if (counter == 0)
    {
        return 0;
    }
    else
    {
        return counter;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    node *tmp = NULL;
    node *ptr = NULL;
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            tmp = cursor;
            ptr = cursor->next;
            free(tmp);
            cursor = ptr;
        }
    }
    return true;
}
