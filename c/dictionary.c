// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table representing each letter of the alphabet
const unsigned int N = 26;

// Hash table
node *table[N];

//total number of words counted
int total = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    return false;
}

// Hashes word to a number
//use n buckets(26) each for one letter a-z
unsigned int hash(const char *word)
{
    int bucket = (int) tolower(word[0]) - 97;
    return bucket;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open & read dict file
    FILE *file = fopen(dictionary, "r");

    //init temp space for holding the word
    char *strWord = malloc(LENGHT);
    if (word == NULL){ return false; }

    //while not reaching end of file
    while (fscanf(file, "%s", strWord) != EOF)
    {
        //allocate memory for a node in which I insert the word
        node *n = malloc(sizeof(node));
        if (n == NULL){ return false; }

        //copy the word into allocated node space
        strcpy(n->word, strWord);
        //count the word
        total ++;


    }


    return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    //returning value of total words counted while loading()
    return total;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    return false;
}
