#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            float grayscale = round((image[j][i].rgbtBlue + image[j][i].rgbtGreen + image[j][i].rgbtRed) / 3.000);
            image[j][i].rgbtBlue = grayscale;
            image[j][i].rgbtGreen = grayscale;
            image[j][i].rgbtRed = grayscale;
        }
    }
    return;
}

//set limit to 255 for RGB sum
int rgbLimit(int rgb)
{
    if (rgb > 255)
    {
        rgb = 255;
    }

    return rgb;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            int sepiaBlue = rgbLimit(round(0.272 * image[j][i].rgbtRed + 0.534 * image[j][i].rgbtGreen + 0.131 * image[j][i].rgbtBlue));
            int sepiaGreen = rgbLimit(round(0.349 * image[j][i].rgbtRed + 0.686 * image[j][i].rgbtGreen + 0.168 * image[j][i].rgbtBlue));
            int sepiaRed = rgbLimit(round(0.393 * image[j][i].rgbtRed + 0.769 * image[j][i].rgbtGreen + 0.189 * image[j][i].rgbtBlue));

            image[j][i].rgbtBlue = sepiaBlue;
            image[j][i].rgbtGreen = sepiaGreen;
            image[j][i].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            //swap each column - j of pixels to the half width
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //make a copy of anew image to work with
    RGBTRIPLE newImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            newImage[i][j] = image[i][j];
        }
    }


    for (int i = 0, red, green, blue, counter; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //assign values to black colour
            red = green = blue = counter = 0;
            
            // add the center pixel
            if (i >= 0 && j >= 0)
            {
                red += newImage[i][j].rgbtRed;
                green += newImage[i][j].rgbtGreen;
                blue += newImage[i][j].rgbtBlue;
                counter++;
            }
            // add below pixel
            if (i >= 0 && j - 1 >= 0)
            {
                red += newImage[i][j - 1].rgbtRed;
                green += newImage[i][j - 1].rgbtGreen;
                blue += newImage[i][j - 1].rgbtBlue;
                counter++;
            }
            // add right pixel
            if ((i >= 0 && j + 1 >= 0) && (i >= 0 && j + 1 < width))
            {
                red += newImage[i][j + 1].rgbtRed;
                green += newImage[i][j + 1].rgbtGreen;
                blue += newImage[i][j + 1].rgbtBlue;
                counter++;
            }
            // add left pixel
            if (i - 1 >= 0 && j >= 0)
            {
                red += newImage[i - 1][j].rgbtRed;
                green += newImage[i - 1][j].rgbtGreen;
                blue += newImage[i - 1][j].rgbtBlue;
                counter++;
            }
            // add left below pixel
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                red += newImage[i - 1][j - 1].rgbtRed;
                green += newImage[i - 1][j - 1].rgbtGreen;
                blue += newImage[i - 1][j - 1].rgbtBlue;
                counter++;
            }
            // add left upper pixel
            if ((i - 1 >= 0 && j + 1 >= 0) && (i - 1 >= 0 && j + 1 < width))
            {
                red += newImage[i - 1][j + 1].rgbtRed;
                green += newImage[i - 1][j + 1].rgbtGreen;
                blue += newImage[i - 1][j + 1].rgbtBlue;
                counter++;
            }
            // add upper pixel
            if ((i + 1 >= 0 && j >= 0) && (i + 1 < height && j >= 0))
            {
                red += newImage[i + 1][j].rgbtRed;
                green += newImage[i + 1][j].rgbtGreen;
                blue += newImage[i + 1][j].rgbtBlue;
                counter++;
            }
            // add below right pixel
            if ((i + 1 >= 0 && j - 1 >= 0) && (i + 1 < height && j - 1 >= 0))
            {
                red += newImage[i + 1][j - 1].rgbtRed;
                green += newImage[i + 1][j - 1].rgbtGreen;
                blue += newImage[i + 1][j - 1].rgbtBlue;
                counter++;
            }
            // add upper right pixel
            if ((i + 1 >= 0 && j + 1 >= 0) && (i + 1 < height && j + 1 < width))
            {
                red += newImage[i + 1][j + 1].rgbtRed;
                green += newImage[i + 1][j + 1].rgbtGreen;
                blue += newImage[i + 1][j + 1].rgbtBlue;
                counter++;
            }

            image[i][j].rgbtRed = round(red / (counter * 1.0));
            image[i][j].rgbtGreen = round(green / (counter * 1.0));
            image[i][j].rgbtBlue = round(blue / (counter * 1.0));
        }
    }
}
