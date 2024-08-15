#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over the rows
    for (int i = 0; i < height; i++)
    {
        // Loop over each Pixel
        for (int j = 0; j < width; j++)
        {
            // Take average of R, G, B
            int aver =
                ((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0 + 0.5);

            // Update pixels value
            image[i][j].rgbtRed = aver;
            image[i][j].rgbtGreen = aver;
            image[i][j].rgbtBlue = aver;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    // Loop over the rows
    for (int i = 0; i < height; i++)
    {
        // Loop over each Pixel
        for (int j = 0; j < width; j++)
        {
            // Compute Sepia Values

            int sepiared = image[i][j].rgbtRed * 0.393 + image[i][j].rgbtGreen * 0.769 +
                           image[i][j].rgbtBlue * 0.189 + 0.5;
            if (sepiared >= 255)
            {
                sepiared = 255;
            }

            int sepiagreen = image[i][j].rgbtRed * 0.349 + image[i][j].rgbtGreen * 0.686 +
                             image[i][j].rgbtBlue * 0.168 + 0.5;
            if (sepiagreen >= 255)
            {
                sepiagreen = 255;
            }

            int sepiablue = image[i][j].rgbtRed * 0.272 + image[i][j].rgbtGreen * 0.534 +
                            image[i][j].rgbtBlue * 0.131 + 0.5;
            if (sepiablue >= 255)
            {
                sepiablue = 255;
            }

            // Update pixels with sepia value
            image[i][j].rgbtRed = sepiared;
            image[i][j].rgbtGreen = sepiagreen;
            image[i][j].rgbtBlue = sepiablue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    typedef struct
    {
        int r;
        int g;
        int b;
    } swap;

    // Array for swapping
    swap swaping[height][width];
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        // Loop over each pixels
        for (int j = 0; j < width; j++)
        {
            // Swap pixels
            swaping[i][j].r = image[i][j].rgbtRed;
            swaping[i][j].g = image[i][j].rgbtGreen;
            swaping[i][j].b = image[i][j].rgbtBlue;
        }
        // Change each pixel with swap value
        for (int j = 0; j < width; j++)
        {
            image[i][width - j - 1].rgbtRed = swaping[i][j].r;
            image[i][width - j - 1].rgbtGreen = swaping[i][j].g;
            image[i][width - j - 1].rgbtBlue = swaping[i][j].b;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
     RGBTRIPLE copy[height][width];
    int rows[] = {-1, -1, -1, 0, 0, 0, 1, 1, 1};
    int colums[] = {-1, 0, 1, -1, 0, 1, -1, 0, 1};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float counter = 0.00;
            int sumr = 0;
            int sumg = 0;
            int sumb = 0;
            for (int k = 0; k < 9; k++)
            {
                if (i + rows[k] < height && i + rows[k] >= 0 && j + colums[k] < width &&
                    j + colums[k] >= 0)
                {
                    sumr = image[i + rows[k]][j + colums[k]].rgbtRed + sumr;
                    sumg = image[i + rows[k]][j + colums[k]].rgbtGreen + sumg;
                    sumb = image[i + rows[k]][j + colums[k]].rgbtBlue + sumb;
                    counter++;
                }
            }
            copy[i][j].rgbtRed = round(sumr / counter);
            copy[i][j].rgbtGreen = round(sumg / counter);
            copy[i][j].rgbtBlue = round(sumb / counter);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
    }
    return;
}
