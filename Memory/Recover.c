#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int blocksize = 512;
int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *rawfile = fopen(argv[1], "r");
    if (rawfile == NULL)
    {
        printf("Could not open");
        return 1;
    }

    // Initialize variables
    uint8_t buffer[blocksize];
    bool found = false;
    int counter = 0;
    char filename[8];
    FILE *imgptr = NULL;

    // While there is still data left to read from the memory card
    while (fread(buffer, 1, blocksize, rawfile) == 512)
    {
        // Look for beginning of the JPEG - IF start of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            found = true;
        }

        if (found == true)
        {
            if (counter == 0)
            {
                sprintf(filename, "%03i.jpg", counter);
                imgptr = fopen(filename, "w");
                fwrite(buffer, 1, blocksize, imgptr);
                found = false;
                counter++;
            }
            else
            {
                fclose(imgptr);
                sprintf(filename, "%03i.jpg", counter);
                imgptr = fopen(filename, "w");
                fwrite(buffer, 1, blocksize, imgptr);
                found = false;
                counter++;
            }
        }
        else if (counter != 0)
        {
            fwrite(buffer, 1, blocksize, imgptr);
        }
    }
    fclose(imgptr);
    fclose(rawfile);
}
