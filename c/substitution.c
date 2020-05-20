#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


int main(int argc, string argv[])
{

    //make sure user provides the key and length of the key is correct
    if (argc != 2 || strlen(argv[1]) != 26)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    //create new chars array to store letters 
    char alphabet[26];
    //create new chars array for storing the key
    char key[26];


    for (int i = 0; i < 26; i++)
    {
        //transform all letters to capital letters for convenience when checking conditions
        key[i] = toupper(argv[1][i]);
                    
        // if true: assign new letter to the alphabet
        if (key[i] >= 65 && key[i] <= 90)
        {
            alphabet[i] = 65 + i - key[i];
        }
        //if not alpha character program must throw error message
        else 
        {
            printf("Key must contain letters only.\n");
            return 1;
        }
                   
        // Iterate to check for duplicates
        for (int j = 0; j < i; j++)
        {
            if (key[i] == key[j])
            {
                printf("Key cannot contain duplicates\n");
                return 1;
            }
        }
    }


    //if above conditions checked and false, prompt user to input plaintext
    string plainInput = get_string("plaintext: ");

    int input_len = strlen(plainInput);

    for (int i = 0; i < input_len; i++)
    {
        //encode the input with the alphabet character from created above array
        //where needed apply lower chars
        if (plainInput[i] >= 65 && plainInput[i] <= 90)
        {
            plainInput[i] = plainInput[i] - alphabet[plainInput[i] - 65];
            printf("ciphertext: %c\n", plainInput[i]);
        }
        else if (plainInput[i] >= 97 && plainInput[i] <= 122)
        {
            plainInput[i] = plainInput[i] - alphabet[plainInput[i] - 97];
        }
    }

    // print out ciphered message
    printf("ciphertext: %s\n", plainInput);
    return 0;
}


