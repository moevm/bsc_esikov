struct BitmapInfoHeader{
	unsigned int size;
	unsigned int width;
	unsigned int height;
	unsigned short planes;
	unsigned short bitperpixel;
	unsigned int compression;
	unsigned int imagesize;
	unsigned int xpixelspermeter;
	unsigned int ypixelspermeter;
	unsigned int colorsintable;
	unsigned int colorimprotant;
};

struct Rgb{
	unsigned char b;
	unsigned char g;
	unsigned char r;
};

struct Bmp{
	struct BitmapFileHeader fileheader;
	struct BitmapInfoHeader infoheader;
	struct Rgb** pixelarray;
};

int test8(int argc, char** argv){
	int i, j;
	struct Bmp image;

	FILE* input = fopen(argv[1], "rb");
	if(!input){
		printf("Fail with input file\n");
		return 0;
	}

	fread(&image.fileheader, sizeof(struct BitmapFileHeader), 1, input);
	fread(&image.infoheader, sizeof(struct BitmapInfoHeader), 1, input);
	image.pixelarray = malloc(sizeof(struct Rgb*) * image.infoheader.height);
	for(i = 0; i < image.infoheader.height; i++)
		image.pixelarray[i] = malloc(sizeof(struct Rgb) * image.infoheader.width);

	int pad = (image.infoheader.width * sizeof(struct Rgb)) % 4;
	if(pad)
		pad = 4 - pad;

	fseek(input, image.fileheader.offsettopixelarr, SEEK_SET);

	for(i = 0; i < image.infoheader.height; i++){
		for(j = 0; j < image.infoheader.width; j++)
			fread(&image.pixelarray[i][j], sizeof(struct Rgb), 1, input);
		int buf;
		fread(&buf, sizeof(char), pad, input);
	}

	fclose(input);

        int x0 = atoi(argv[2]);
        int y0 = atoi(argv[3]);
        int x1 = atoi(argv[4]);
        int y1 = atoi(argv[5]);
	if(x0 > image.infoheader.width){
		printf("Fail with x0\n");
		return 0;
	}
	if(x1 > image.infoheader.width){
		printf("Fail with x1\n");
		return 0;
	}
	if(y1 > image.infoheader.height){
		printf("Fail with y0\n");
		return 0;
	}
	if(y0 > image.infoheader.height){
		printf("Fail with y1\n");
		return 0;
	}
	if(y0 - y1 != x1 - x0){
		printf("Not square\n");
		return 0;
	}

	int deltaforx = x0 - y1;
	int deltafory = x0 + y0;

        FILE* output = fopen("otvet.bmp", "wb");
        fwrite(&image.fileheader, sizeof(struct BitmapFileHeader), 1, output);
        fwrite(&image.infoheader, sizeof(struct BitmapInfoHeader), 1, output);

	fseek(output, image.fileheader.offsettopixelarr, SEEK_SET);

        for(i = 0; i < image.infoheader.height; i++){
                for(j = 0; j < image.infoheader.width; j++){
                        if((j >= x0 && i >= y1) && (j <= x1 && i <= y0))
                                fwrite(&image.pixelarray[j-deltaforx][deltafory-i], sizeof(struct Rgb), 1, output);
                        else
                                fwrite(&image.pixelarray[i][j], sizeof(struct Rgb), 1, output);
                }
                int buf = 0;
                fwrite(&buf, sizeof(char), pad, output);
        }

        fclose(output);

	return 0;
}
