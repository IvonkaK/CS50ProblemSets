#include <stdio.h>
#include <stdlib.h>

//program to recover jpeg from memory card
int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //open memory card
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        return 1;
    }

    //create buffer to allocate jpeg
    unsigned char *buffer = malloc(512);
    int count = 0;

    FILE *img;
    //pattern for filename is 7 char long - ###.jpeg
    char filename[7];

    //read the 'file'
    while (fread(buffer, 512, 1, file))
    {
        //look for jpeg pattern in the open file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //close the file previously writing to
            if (count > 0)
            {
                fclose(img);
            }

            //create filename
            sprintf(filename, "%03i.jpg", count);

            //open new img file
            img = fopen(filename, "w");

            //is file created?
            if (img == NULL)
            {
                //if not close the main file free memory and return 1
                fclose(file);
                free(buffer);
                return 1;
            }

            count ++;
        }

        //if already found jpg img keep writing to buffer next 512 bytes
        if (count > 0)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    //close files and free memory on buffer
    fclose(img);
    fclose(file);
    free(buffer);
    return 0;
}
