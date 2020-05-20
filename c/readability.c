#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int letterCounter(string text);
int wordCounter(string text);
int sentenceCounter(string text);

int main(void)
{

    string text = get_string("Text: ");


    int charCount = letterCounter(text);
    int wordCount = wordCounter(text);
    int sentenceCount = sentenceCounter(text);

    // average number of letters per 100 words
    float averageL = (100 * (float)charCount / wordCount);

    // average number of sentences per 100 words
    float averageS = (100 * (float)sentenceCount / wordCount);
    
    //C-L index
    float grade = round(0.0588 * averageL - 0.296 * averageS - 15.8);
    
    //Print correct grade
    if (grade < 1) 
    {
            printf("Before Grade 1\n");
    }
    else if (grade >= 16) 
    {
            printf("Grade 16+\n");
    }
    else 
    {
            printf("Grade %.0f\n", grade);
    }

}

int letterCounter(string text)
{

    int charCount = 0;

    for (int i = 0; text[i]; i++)
    {

        //check if char is lower or upper case
        if (isalpha(text[i]))
        {
            charCount++;
        }
    }

    return charCount;

}

int wordCounter(string text)
{

    int wordCount = 1;


    for (int i = 0; text[i] != '\0'; i++) 
    {

        //check for spaces between chars
        if (isspace(text[i]))
        {
            
            wordCount++;
            
        } 
    }

    return wordCount;
}

int sentenceCounter(string text)
{


    int sentenceCount = 0;


    for (int i = 0; text[i]; i++) 
    {

        //check for char .?! between chars
        if ((text[i]) == ('.') || (text[i]) == ('?') || (text[i]) == ('!'))
        {
            sentenceCount ++ ;
        }
    }

    return sentenceCount;
}
