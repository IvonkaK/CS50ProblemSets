
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long long int card_number = get_long("Please provide your credit card number: ");

    int sum = 0;
    int length;
    int first = 0;
    int second = 0;

    //1. Check if a card number provided is valid - using Luhn's algo

        for (length = 0; card_number; card_number /= 10, length++)
        {
            int digit = card_number % 10;
            second = first;
            first = digit;

            if (length % 2) 
            {
                digit += digit;
                if (digit > 9) 
                {
                digit -= 9;
                }
            }
        sum += digit;
    }

    //2. If number is valid (sum last digit == 0), determine if the card provided is either Visa, Master        or Amex.
    //2.5 If the card provided is neither of them throw "Invalid\n"

    sum %= 10;

    char *bank = "INVALID\n";
    if (sum == 0) {
        switch(first) {
            case 3:
                if (length == 15 && (second == 4 || second == 7)) {
                    bank = "AMEX\n";
                }
                break;
            case 4:
                if (length == 13 || length == 16) {
                    bank = "VISA\n";
                }
                break;
            case 5:
                if (length == 16 && second > 0 && second < 6) {
                    bank = "MASTERCARD\n";
                }
                break;
        }
    }
    printf("%s",bank);
}


 

