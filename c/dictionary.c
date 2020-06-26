// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH];
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
    //set the cursor which will become the pointer to elements of our linked list
    node *cursor = table[hash(word)];

    //look for the word and return true if found
    if (strcasecmp(cursor->word, word) == 0)
    {
        return true;
    }

    //while not reaching the end of linked list
    while (cursor->next != NULL)
    {
        //take cursor and move to the next node of the linked list
        cursor = cursor->next;

        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
    }
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
    char *strWord = malloc(LENGTH);
    if (strWord == NULL)
    {
        return false;
    }

    //while not reaching end of file
    while (fscanf(file, "%s", strWord) != EOF)
    {
        //allocate memory for a node in which I insert the word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        //copy the word into allocated node space
        strcpy(n->word, strWord);
        //count the words
        total++;

        //next has to point to the beginning of the list
        n->next = table[hash(strWord)];

        //list has to point at n (n is the head of the list)
        table[hash(strWord)] = n;

    }

    //close the file and free the memory for strWord
    fclose(file);
    free(strWord);

    return true;
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
    //set the cursor which will become the pointer to elements of our linked list
    node *cursor;
    //temp pointer
    node *temp;

    //iterate every bucket in the table
    for (int i = 0; i < N; i++)
    {
        //if the current bucket of the table is empty go to the next one
        if (table[i] == NULL)
        {
            continue;
        }

        //set cursor to current linked list and temp value to cursor so they would both point to the same node of the linked list
        cursor = table[i];
        temp = cursor;

        //while not reaching end of linked list free allocated memory for each node
        while (cursor->next != NULL)
        {
            cursor = cursor->next;
            free(temp);
            temp = cursor;
        }

        free(cursor);
    }
    return true;
}
