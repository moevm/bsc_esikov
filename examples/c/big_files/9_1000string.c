#include <stdio.h>
#include <stdlib.h>
#include "get_name.h"
#include <string.h>
#include "print_str.h"

typedef int type;

typedef struct StackElem{
    type data;
    struct StackElem* pred;
} StackElem;

typedef struct Stack{
    struct StackElem* last;
} Stack;

Stack initStack(){
    Stack stack;
    stack.last = NULL;
    return stack;
}

void push(Stack* pointer, type value){
    StackElem* element = (StackElem*)malloc(sizeof(StackElem));
    element->data = value;
    element->pred = pointer->last;
    pointer->last = element;
}

type pop(Stack* pointer){
    StackElem* temp = pointer->last;
    type result = temp->data;
    pointer->last = pointer->last->pred;
    free(temp);
    return result;
}

type top(Stack* pointer){
    return pointer->last->data;
}

int isEmpty(Stack* pointer){
    if(pointer->last)
        return 1;
    else
        return 0;
}

int count(Stack* pointer){
    int result = 0;
    StackElem* temp = pointer->last;
    while(temp){
        result++;
        temp = temp->pred;
    }
    return result;
}

int help(){
	FILE *FHelp=fopen("help.txt","r");
	if(FHelp==NULL){
		printf("Произошла ошибка, файла с инструкцией был удален\n");
		return 0;
	}
	char simbol;
	printf("\n\n\n\n\n");
	while((simbol=fgetc(FHelp))!=EOF){
		printf("%c",simbol);
	}
	printf("\n\n\n\n\n");
	fclose(FHelp);
	return 1;
}

char* get_name()
{
char* name = (char*)malloc(80*sizeof(char));
int i = 0;
char ch;
while ((ch = getchar()) != '\n')
{
name[i] = ch;
i++;
}
name[i] = '\0';
return name;
}

void print_str(char* str1, char*  str2, int num)
{
puts(strncat(str1, str2, num));
}

int test1()
{
char hello[90] = "Hello, ";
char* result;
result = get_name();
print_str(hello, result, 80);
free(result);
return 0;
}

int diff(int* arr, int len){
return max(arr, len) - min(arr, len);}

int max(int *arr, int len){
        int i, max = arr[0];
        for(i = 1; i < len; ++i){
                if(arr[i] > max)
			max = arr[i];}
return max;}

int Inter_Face(VariableFunction * variable,int argc,char **argv){
	int option;
	char *OptString="e:s:c:w:hp";
	int IndexLong=0;
	struct option LongOptFrame[]={
		{"frame",0,NULL,0},
		{"type",1,NULL,0},
		{"width",1,NULL,'w'},
		{"color",1,NULL,'c'},
		{NULL,0,NULL,0}
	};
	struct option LongOptRectangle[]={
		{"rectangle",0,NULL,0},
		{"start",1,NULL,'s'},
		{"color",1,NULL,'c'},
		{"end",1,NULL,'e'},
		{"width",1,NULL,'w'},
		{"poured",0,NULL,'p'},
		{"color_poured",1,NULL,0},
		{NULL,0,NULL,0}
	};
	struct option LongOptTurn[]={
		{"turn",0,NULL,0},
		{"start",1,NULL,'s'},
		{"end",1,NULL,'e'},
		{"angle",1,NULL,0},
		{NULL,0,NULL,0}
	};
	opterr=0;//Устанавливаем свою обработку ошибок
	if(argv[1]==NULL){
		printf("Не выбрана функция для работы с изображением\n");
		return 0;
	}
	if (strcmp("--rectangle",argv[1])==0){
		variable->NumberFunction=1;
		while((option=getopt_long(argc,argv,OptString,LongOptRectangle,&IndexLong))!=-1){
			switch(option){
				case 'w':
					if(sscanf(optarg,"%d",&(variable->WidthLine))==0){
                                                        printf("Ошибка при вводе ширини границ\n");
                                                        return 0;
                                                }
                                        break;
				case 'c':
					 variable->color=optarg;
					 break;
				case 's':
					 if(sscanf(optarg,"%d",&(variable->x1))==0){
                                                        printf("Ошибка при вводе начальных координат\n");
                                                        return 0;
                                                }
                                         if(sscanf(argv[optind],"%d",&(variable->y1))==0){
                                                        printf("Ошибка при вводе начальных координат\n");
                                                        return 0;
                                                }
					break;
				case 'e':
					if(sscanf(optarg,"%d",&(variable->x2))==0){
                                                        printf("Ошибка при вводе конечных координат\n");
                                                        return 0;
                                                }
                                        if(sscanf(argv[optind],"%d",&(variable->y2))==0){
                                                        printf("Ошибка при вводе конечных координат\n");
                                                        return 0;
                                                }
					break;
				case 'p':
					variable->poured=1;
					break;
				case 0:
					if(strcmp("color_poured",LongOptRectangle[IndexLong].name)==0){
						variable->PouredColor=optarg;
					}
					else if(strcmp("rectangle",LongOptRectangle[IndexLong].name)==0);
					else{
						printf("Длинная опция не была найдена\n");
						return 0;
					}
					break;
				case '?':
					printf("Была введена не определенная опция,попробуйте снова\n");
					return 0;
				case ':':
					printf("Был пропущен аргумент\n");
					return 0;
			}
		}
	}
	else if(strcmp("--frame",argv[1])==0){
		variable->NumberFunction=2;
		while((option=getopt_long(argc,argv,OptString,LongOptFrame,&IndexLong))!=-1){
                        switch(option){
				case 'w':
					if(sscanf(optarg,"%d",&(variable->WidthPattern))==0){
                                                        printf("Ошибка при вводе начальных координат\n");
                                                        return 0;
                                                }
					break;
				case 'c':
					variable->ColorPattern=optarg;
					break;
                                case 0:
                                        if(strcmp("type",LongOptFrame[IndexLong].name)==0){
                                                if(sscanf(optarg,"%d",&(variable->TypePattern))==0){
                                                        printf("Ошибка при вводе начальных координат\n");
                                                        return 0;
                                                }
                                        }
					else if(strcmp("frame",LongOptFrame[IndexLong].name)==0);
                                        else{
                                                printf("Длинная опция не была найдена\n");
                                                return 0;
                                        }
					break;
				case '?':
                                        printf("Была введена не определенная опция,попробуйте снова\n");
                                        return 0;
                                case ':':
                                        printf("Был пропущен аргумент\n");
                                        return 0;
                                default:
                                        break;
			}
		}
	}
	else if (strcmp("--turn",argv[1])==0){
                variable->NumberFunction=3;
                while((option=getopt_long(argc,argv,OptString,LongOptTurn,&IndexLong))!=-1){
                        switch(option){
				case 's':
					if(sscanf(optarg,"%d",&(variable->x11))==0){
                                                        printf("Ошибка при вводе начальных координат\n");
                                                        return 0;
                                                }
                                        if(sscanf(argv[optind],"%d",&(variable->y11))==0){
                                                        printf("Ошибка при вводе начальных координат\n");
                                                        return 0;
                                                }
					break;
				case 'e':
					if(sscanf(optarg,"%d",&(variable->x22))==0){
                                                        printf("Ошибка при вводе конечных координат\n");
                                                        return 0;
                                                }
                                        if(sscanf(argv[optind],"%d",&(variable->y22))==0){
                                                        printf("Ошибка при вводе конечных координат\n");
                                                        return 0;
                                                }
					break;
                                case 0:
					if(strcmp("angle",LongOptTurn[IndexLong].name)==0){
                                                if(sscanf(optarg,"%d",&(variable->AngleTurn))==0){
                                                        printf("Ошибка при вводе начальных координат\n");
                                                        return 0;
                                                }
                                        }
					else if(strcmp("turn",LongOptTurn[IndexLong].name)==0);
					else{
                                                printf("Длинная опция не была найдена\n");
                                                return 0;
                                        }
                                        break;
                                case '?':
                                        printf("Была введена не определенная опция,попробуйте снова\n");
                                        return 0;
                                case ':':
                                        printf("Был пропущен аргумент\n");
                                        return 0;
                                default:
                                        break;
                        }
                }
        }
	else if (strcmp("--help",argv[1])==0||strcmp("-h",argv[1])==0){
                variable->NumberFunction=4;
		return 1;
	}
	else if (strcmp("--info",argv[1])==0||strcmp("-h",argv[1])==0){
                variable->NumberFunction=5;
		variable->NameFileIn=argv[argc-1];
		variable->NameFileOut=argv[argc-1];
		return 1;
        }
	else if(strcmp("--cleanF",argv[1])==0){
		variable->NumberFunction=6;
		variable->NameFileIn=argv[argc-1];
		variable->NameFileOut=argv[argc-1];
		return 1;
	}
        else {
		printf("Введена не определенная функция\n");
		return 0;
	}
	argc-=optind;
	argv+=optind;
	while(True_Png(argv[argc-1])==0){
		argc-=1;
	}
	if(True_Png(argv[argc-2])!=0){
		variable->NameFileIn=argv[argc-2];
		variable->NameFileOut=argv[argc-1];
	}
	else{
		variable->NameFileIn=argv[argc-1];
		variable->NameFileOut=argv[argc-1];
	}
	return 1;
}

#include "PngC.h"
//===================================================================================================

int true_png_sign(PNG_SIGNATURE sign){
        int i;
        char png[8]={(char)137,(char)80,(char)78,(char)71,(char)13,(char)10,(char)26,(char)10};
        for(i=0;i<8;i++)
                if(png[i]!=sign.signature[i])
                        break;
        if(i==8)
                return 1;
        else
                return 0;
}

int **Minor(int **matrix, int size, int row, int colm)
{
	int i = 0, j = 0, offsetrow = 0, offsetcolm=0;
	int **matrixM = (int**)malloc((size - 1) * sizeof(int*));
	for (i = 0; i < (size - 1); i++)
		matrixM[i] = (int*)malloc((size - 1) * sizeof(int));
	for (i = 0; i < size - 1; i++)
	{
		if (i == row)
			offsetrow = 1;
		offsetcolm = 0;
		for (j = 0; j < size - 1; j++)
		{
			if (j == colm)
				offsetcolm = 1;
			matrixM[i][j] = matrix[i + offsetrow][j + offsetcolm];
		}
	}
	return matrixM;
}

int determiant(int **matrix, int size)
{
	int det = 0, degree = 1, i = 0;
	if (size == 1)
		return matrix[0][0];
	if (size == 2)
		return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
	int **buf;
	for (i = 0; i < size; i++)
	{
		buf = Minor(matrix, size, 0, i);
		det = det + (degree*matrix[0][i] * determiant(buf, size - 1));
		degree = -degree;
	}
	free(buf);
	return det;
}

typedef struct matrix
{
	int row;
	int colm;
	int **matr;
} matrix;


void print_matrix(void **matr, int matrow, int matcolm, char *filename, int size_of_element);
int **matrix_transponition(int **matr, int matArow, int matAcolm);
int **mult_2_matr(int matrow1, int matcolm1, int **mat1, int matrow2, int matcolm2, int **mat2);
void matrix_multiplication(matrix*array, int number);
int **Minor(int **matrix, int size, int row, int colm);
int determiant(int **matrix, int size);
void inverse_matrix(matrix structure, int number);

while (newtext != NULL)
				{
					arr[i] = newtext;
					i++;
					if (i + 1 == size_of_arr)
					{
						size_of_arr += M;
						arr = (char**)realloc(arr, (size_of_arr) * sizeof(char *));
					}
					newtext = strtok(NULL, " ");
				}

typedef struct MusicalComposition{ // Описание структуры MusicalComposition
    char* name;
    char* author;
    int year;
    struct MusicalComposition* next;
    struct MusicalComposition* pred;} MusicalComposition;

MusicalComposition* createMusicalComposition(char* name, char* author, int year){ // Создание структуры MusicalComposition
    MusicalComposition* adres = (MusicalComposition*)malloc(sizeof(MusicalComposition));
    adres->name = name;
    adres->author = author;
    adres->year = year;
    return adres;}
// Функции для работы со списком MusicalComposition

MusicalComposition* createMusicalCompositionList(char** array_names, char** array_authors, int* array_years, int n){
    int i = 0;
    MusicalComposition* head;
    MusicalComposition* temp;
    for(; i < n; i++){
        if(i == 0){										//создание головы списка
            head = createMusicalComposition(array_names[i], array_authors[i], array_years[i]);
            head->pred = NULL;
            temp = head;
            i++;}
        temp->next = createMusicalComposition(array_names[i], array_authors[i], array_years[i]);
        temp->next->next = NULL;
        temp->next->pred = temp;
        temp = temp->next;}
    return head;}

void push(MusicalComposition* head, MusicalComposition* element){
    while(head){
        if(head->next == NULL)									//нахождение последнего элемента списка
            break;
        head = head->next;}
    head->next = element;
    element->next = NULL;
    element->pred = head;}

void removeEl(MusicalComposition* head, char* name_for_remove){
    while(head){
        if(!(strcmp(name_for_remove, head->name))){
            if(head->next == NULL){								//удаление элемента, если он последний
                head->pred->next = NULL;
                return;}
            head->next->pred = head->pred;
            head->pred->next = head->next;
            return;}
        head = head->next;}}

int count(MusicalComposition* head){
    int i = 0;
    while(head){
        i++;
        head = head->next;}
    return i;}

void print_names(MusicalComposition* head){
    while(head){
        printf("%s\n", head->name);
        head = head->next;}}

//====================================================================================================

int read_png_file(PNG_FILE* image, const char* name_file){
        FILE *file=fopen(name_file,"rb");
        if(!file){
                printf("Файл не был найден,попробуйте еще раз\n");
                return 0;
        }

        PNG_SIGNATURE signature;
        fread(&signature,sizeof(PNG_SIGNATURE),1,file);
        if(!(true_png_sign(signature))){
                printf("Файла не явялется png формата\n");
                fclose(file);
                return 0;
        }

        image->png_ptr=png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);//Выделение и Инициализация структуры png_ptr
        if(!image->png_ptr){
                printf("Выделение структуры png_ptr не удалось\n");
                fclose(file);
                return 0;
        }
        image->info_ptr=png_create_info_struct(image->png_ptr);//Выделение и Инициализация структуры info_ptr
        if(!image->info_ptr){
                printf("Выделение структуры info_ptr не удалось\n");
                fclose(file);
                return 0;
        }

        if(setjmp(png_jmpbuf(image->png_ptr))){
                printf("Произошла ошибка\n");
                png_destroy_write_struct(&(image->png_ptr),&(image->info_ptr));
                fclose(file);
                return 0;
        }

        png_init_io(image->png_ptr,file);
        png_set_sig_bytes(image->png_ptr,8);
        png_read_info(image->png_ptr,image->info_ptr);
        image->width = png_get_image_width(image->png_ptr, image->info_ptr);
        image->height = png_get_image_height(image->png_ptr, image->info_ptr);
        image->color_type = png_get_color_type(image->png_ptr, image->info_ptr);
        image->bit_depth = png_get_bit_depth(image->png_ptr, image->info_ptr);
        image->number_of_passes = png_set_interlace_handling(image->png_ptr);//тип переплетения

         if (png_get_color_type(image->png_ptr, image->info_ptr) != PNG_COLOR_TYPE_RGBA){
                png_set_add_alpha(image->png_ptr,0xff,PNG_FILLER_AFTER);
         }
        png_read_update_info(image->png_ptr, image->info_ptr);

        image->width = png_get_image_width(image->png_ptr, image->info_ptr);
        image->height = png_get_image_height(image->png_ptr, image->info_ptr);
        image->color_type = png_get_color_type(image->png_ptr, image->info_ptr);
        image->bit_depth = png_get_bit_depth(image->png_ptr, image->info_ptr);
        image->number_of_passes = png_set_interlace_handling(image->png_ptr);//тип переплетения
	//image->height+=300;
        image->row_pointers=(png_bytep*)malloc(sizeof(png_bytep)*(image->height));
        int y;
        for(y=0;y<(image->height);y++)
                image->row_pointers[y]=(png_byte*)malloc(png_get_rowbytes(image->png_ptr,image->info_ptr));
        png_read_image(image->png_ptr,image->row_pointers);

        fclose(file);
	return 1;
}

#include "PngC.h"
#include <math.h>
//Функции для первого типо рамки(прямой кохи)=====================================================
void KOH(PNG_FILE* image,int x1,int y1,int x2,int y2,int width,int k,int i,int R,int G,int B){
	int x3,y3;
	int x4,y4;
	int x5,y5;
	x3=round((x2-x1)/3+x1);
	y3=round((y2-y1)/3+y1);
	x4=round(x1+2*(x2-x1)/3);
	y4=round(y1+2*(y2-y1)/3);
	double L = sqrt(pow((x1 - x2),2) + pow((y1 - y2),2));
        // высота нового равностороннего треугольника
        double h = L /(2 * sqrt(3));
        // углы между линией и осью ОХ
        double sina = (y2 - y1)/L;
        double cosa = (x2 - x1)/L;

        // вершина галочки
	 int deltaX3_X4=0;
	 int deltaX5=0;

         x5 = round((x2 + x1)/2 + h*i * sina);
         y5 = round((y2 + y1)/2 - h*i * cosa);
	//Дли решения проблемы с преведением типов
	write_line(image,x1,y1,x2,y2,width,255,255,255,0);
	write_line(image,x1,y1,x3,y3,width,R,G,B,0);
	write_line(image,x4,y4,x2,y2,width,R,G,B,0);
	//отрисовка треугольника
	write_line(image,x3,y3,x5,y5,width,R,G,B,0);
	write_line(image,x5,y5,x4,y4,width,R,G,B,0);
	k--;
	if(k>0){
		KOH(image,x1,y1,x3,y3,width,k,i,R,G,B);
		KOH(image,x3,y3,x5,y5,width,k,i,R,G,B);
		KOH(image,x5,y5,x4,y4,width,k,i,R,G,B);
		KOH(image,x4,y4,x2,y2,width,k,i,R,G,B);
	}


}
int koh_proportion_write(PNG_FILE*image,int x1,int y1,int x2,int y2,int width,int i,int k,int R,int G,int B){
	int x3,x4;
        int y3,y4;
	int x5,y5;
        x3=round(x1+(x2-x1)/3);
        y3=round(y1+(y2-y1)/3);
        x4=round(x1+2*(x2-x1)/3);
        y4=round(y1+2*(y2-y1)/3);
	double L = sqrt(pow((x1 - x3),2) + pow((y1 - y3),2));
        // высота нового равностороннего треугольника
        double h = L /(2 * sqrt(3));
        // углы между линией и осью ОХ
        double sina = (y3 - y1)/L;
        double cosa = (x3 - x1)/L;

        // вершина галочки
         x5 = round((x3 + x1)/2 + h * i * sina);
         y5 = round((y3 + y1)/2 - h * i * cosa);

        write_line(image,x1,y1,x3,y3,width,R,G,B,0);
        KOH(image,x1,y1,x3,y3,width,k,i,R,G,B);
        write_line(image,x3,y3,x4,y4,width,R,G,B,0);
        KOH(image,x3,y3,x4,y4,width,k,i,R,G,B);
        write_line(image,x4,y4,x2,y2,width,R,G,B,0);
        KOH(image,x4,y4,x2,y2,width,k,i,R,G,B);
	if(x1==x2)
		return x5;
	else if(y1==y2)
		return y5;
	else
		return 0;

}
#define V3_OFFSET_VALUE 54

#pragma pack(push, 2)
typedef struct tagBITMAPFILEHEADER {
    uint16_t bfType;
    uint32_t bfSize;
    uint16_t bfReserved1;
    uint16_t bfReserved2;
    uint32_t bfOffBits;
} BITMAPFILEHEADER;
#pragma pack(pop)

typedef struct tagBITMAPINFOHEADER {
    uint32_t biSize;
    uint32_t biWidth;
    uint32_t biHeight;
    uint16_t biPlanes;
    uint16_t biBitCount;
    uint32_t biCompression;
    uint32_t biSizeImage;
    uint32_t biXPelsPerMeter;
    uint32_t biYPelsPerMeter;
    uint32_t biClrUsed;
    uint32_t biClrImportant;
} BITMAPINFOHEADER;

//Структура с пикселями
typedef struct tagRGBTRIPLE {
    uint8_t rgbBlue;
    uint8_t rgbGreen;
    uint8_t rgbRed;
} RGBTRIPLE;
//Сам файл
typedef struct tagBMPFile {
    RGBTRIPLE** image;
    BITMAPFILEHEADER* file_header;
    const char* file_name;
    BITMAPINFOHEADER* info;
} BMPFile;
//Функция для чтения .bmp файла
BMPFile* open_bmp(char* file_name){
    FILE* fp;
    BMPFile* bmp_file;

    fp = fopen(file_name, "rb");

    if (fp == NULL){
        printf("Error");
        return 0;
    }
    //Выделение памяти для BITMAPFILEHEADER структуры
    bmp_file = (BMPFile*)malloc(sizeof(BMPFile));
    BITMAPFILEHEADER* bfh = (BITMAPFILEHEADER*)malloc(sizeof(BITMAPFILEHEADER));
    fread(bfh, sizeof(*bfh), 1, fp);
    bmp_file->file_header = bfh;

    BITMAPINFOHEADER* bih = (BITMAPINFOHEADER*)malloc(sizeof(BITMAPINFOHEADER));
    fread(bih, sizeof(*bih), 1, fp);

    bmp_file->info = bih;

    unsigned int height = bmp_file->info->biHeight;
    unsigned int width = bmp_file->info->biWidth;

    RGBTRIPLE** picture = (RGBTRIPLE**)calloc(height, sizeof(RGBTRIPLE*));
    for(unsigned i = 0; i < height; i++){
        picture[i] = (RGBTRIPLE*)calloc(width, sizeof(RGBTRIPLE));
    }

    for(unsigned i = 0; i < height; i++){
        fread(picture[i], sizeof(RGBTRIPLE), width, fp);
        fseek(fp, (width)%4, SEEK_CUR);
    }

    fclose(fp);
    bmp_file->image = picture;
    bmp_file->file_name = file_name;


    return bmp_file;
}

void print_triangle(BMPFile* file, FILE* ptrFile,int x0, int y0, int x1, int y1){
    int x_start = x0;
    int x_finish = x1 - (x1-x0)/2;
    int y_start = y1 ;
    int y_finish = y0 - (y0-y1)/2;
    //Треугольник заполняется черными пикселями
    int  k = y_finish;
    for(int i = x_start;i < x_finish; i++){
        for(int j=y_start;j<y_finish ;j++){
            if(j<k){
                (file->image[i]+j)->rgbBlue = 0;
                (file->image[i]+j)->rgbRed = 0;
                (file->image[i]+j)->rgbGreen = 0;
            }
        }
        k--;
    }

    fwrite(file->file_header, 1, sizeof(BITMAPFILEHEADER), ptrFile);
    fwrite(file->info, 1, sizeof(BITMAPINFOHEADER), ptrFile);

    for(unsigned i = 0; i < file->info->biHeight; i++){
        fwrite(file->image[i], sizeof(RGBTRIPLE), file->info->biWidth, ptrFile);
        fwrite("0", 1, (file->info->biWidth)%4, ptrFile);
    }
}

int main(int argc, char **argv){
    char input_file[100];
    int x0, y0, x1, y1;
    strcpy(input_file, argv[1]);
    x0 = atoi(argv[2]);
    y0 = atoi(argv[3]);
    x1 = atoi(argv[4]);
    y1 = atoi(argv[5]);
    printf("%s %d %d %d %d\n", input_file,x0,y0,x1,y1);
    if(!fopen(input_file, "rb")){
        printf("Fail with input_file\n");
        return 0;
    }
    if(x1-x0 != y0-y1){
        printf("Wrong input\n");
        return 0;
    }
    BMPFile* file = open_bmp(input_file);
    FILE* editedFile = fopen ( "image.bmp" , "wb" );
    print_triangle(file,editedFile, x0,y0,x1,y1);
    fclose(editedFile);
    return 0;
}

#include "PngC.h"
int write_rectangle(PNG_FILE* image,int x1,int y1,int x2,int y2,int width_line,char* color,int poured,char*poured_color){
	int x,y;
        int R=0,G=0,B=0;//цветы границ
        int R1=0,G1=0,B1=0;//цвет залития
   	choise_color(color,&R,&G,&B);
	if(poured==1){
		choise_color(poured_color,&R1,&G1,&B1);
	}

//=ПРОВЕРКА НА КОРРЕКТНОСТЬ ВВЕДЕННЫХ ДАННЫХ=========================================
	if(x1<0||x1>image->width||x2<0||x2>image->width){
		printf("Вышли за границы ширины картинки\n");
		return 0;
	}
	if(y1<0||y1>image->height||y2<0||y2>image->height){
                printf("Вышли за границы высоты картинки\n");
                return 0;
        }
	if(x1>=x2||y1>=y2){
		printf("Не верно введены коориднаты прямоугольника\n");
		return 0;
	}

        if(width_line<=0||width_line>50){
                printf("Ширина линии вышла за рамки возможных(максимальная ширина %d и минимальная ширина %d ), проверьте введенные данные\n",50,0);
                return 0;
        }

        if(poured>1||poured<0){
                printf("Не определен тип залития\n");
                return 0;
        }
        if((width_line>=(x2-x1))||(width_line>=(y2-y1))){
                printf("Ширина границы больше,чем ширина или длина прямоугольника,проветьте введенные данные\n");
                return 0;
        }
//====================================================================================
	x1=x1+1;
	x2=x2-1;
	y2=y2-1;
	write_line(image,x1+width_line/2,y1+width_line/2,x2-width_line/2,y1+width_line/2,width_line,R,G,B,0);
	write_line(image,x1+width_line/2,y1+width_line/2,x1+width_line/2,y2-width_line/2,width_line,R,G,B,0);
	write_line(image,x2-width_line/2,y1+width_line/2,x2-width_line/2,y2-width_line/2,width_line,R,G,B,0);
	write_line(image,x1+width_line/2,y2-width_line/2,x2-width_line/2,y2-width_line/2,width_line,R,G,B,0);
	draw_point(image,x2-width_line/2,y2-width_line/2,width_line,R,G,B);
	if(poured==1){
                for(x=x1+width_line;x<=x2-width_line;x++)
                       for(y=y1+width_line;y<=y2-width_line;y++)
				draw_point(image,x,y,1,R1,G1,B1);
        }
        return 1;
}

void print_matrix(void **matr, int matrow, int matcolm, char*filename, int size_of_element)
{
	FILE *myfile;
	myfile = fopen(filename, "a");
	if (myfile != NULL)
	{
		int i=0,j = 0;
		for (i = 0; i < matrow; i++)
		{
			for (j = 0; j < matcolm; j++)
			{
				if (size_of_element == 4)
					fprintf(myfile, "%3d ", ((int**)matr)[i][j]);
				else if (size_of_element == 8)
					fprintf(myfile, "%5g ", ((double**)matr)[i][j]);
			}
			fprintf(myfile, "\n");
		}
		fprintf(myfile, "\n");
		fclose(myfile);
	}
	else
		printf("File can not be opened\n");
}


int  **matrix_transponition(int **matr, int matrow, int matcolm)
{
	int i, j;
	int **matT = (int **)malloc(matcolm * sizeof(int*));
	for (i = 0; i < matcolm; i++)
		matT[i] = (int*)malloc(matrow * sizeof(int));
	for(i=0; i<matcolm; i++)
		for (j = 0; j < matrow; j++)
		{
			matT[i][j] = matr[j][i];
		}
	return matT;
}


int **mult_2_matr(int matrow1, int matcolm1, int **mat1, int matrow2, int matcolm2, int **mat2)
{
	int k = 0, n = 0, j = 0, t = 0, i = 0;
	int **res = (int**)malloc(matrow1 * sizeof(int*));
	for (i = 0; i < matrow1; i++)
		res[i] = (int*)malloc(matcolm2 * sizeof(int));
	for (i = 0; i < matrow1; i++)
	{
		for (j = 0; j < matcolm2; j++)
		{
			res[i][j] = 0;
			for (k = 0; k < matcolm1; k++)
				res[i][j] += mat1[i][k] * mat2[k][j];
		}
	}
	return res;
}

MusicalComposition* del_year(MusicalComposition* head){
    MusicalComposition* head_return = head;
    while(head){
        if(head->year % 4 == 0){
            if(head->pred == NULL){
                head->next->pred = NULL;
                head = head->next;
                head_return = head;
                continue;}
            if(head->next == NULL){
                head->pred->next = NULL;
                break;}
            head->next->pred = head->pred;
            head->pred->next = head->next;}
        head = head->next;}
    return head_return;}

int test5(){
    int length;
    scanf("%d\n", &length);

    char** names = (char**)malloc(sizeof(char*)*length);
    char** authors = (char**)malloc(sizeof(char*)*length);
    int* years = (int*)malloc(sizeof(int)*length);

    for (int i=0;i<length;i++)
    {
        char name[80];
        char author[80];

        fgets(name, 80, stdin);
        fgets(author, 80, stdin);
        fscanf(stdin, "%d\n", &years[i]);

        (*strstr(name,"\n"))=0;
        (*strstr(author,"\n"))=0;

        names[i] = (char*)malloc(sizeof(char*) * (strlen(name)+1));
        authors[i] = (char*)malloc(sizeof(char*) * (strlen(author)+1));

        strcpy(names[i], name);
        strcpy(authors[i], author);

    }
    MusicalComposition* head = createMusicalCompositionList(names, authors, years, length);
    char name_for_push[80];
    char author_for_push[80];
    int year_for_push;

    char name_for_remove[80];

    fgets(name_for_push, 80, stdin);
    fgets(author_for_push, 80, stdin);
    fscanf(stdin, "%d\n", &year_for_push);
    (*strstr(name_for_push,"\n"))=0;
    (*strstr(author_for_push,"\n"))=0;

    MusicalComposition* element_for_push = createMusicalComposition(name_for_push, author_for_push, year_for_push);

    fgets(name_for_remove, 80, stdin);
    (*strstr(name_for_remove,"\n"))=0;

    printf("%s %s %d\n", head->name, head->author, head->year);
    int k = count(head);

    printf("%d\n", k);
    push(head, element_for_push);

    k = count(head);
    printf("%d\n", k);

    removeEl(head, name_for_remove);
    head = del_year(head);
    print_names(head);

    k = count(head);
    printf("%d\n", k);

    for (int i=0;i<length;i++){
        free(names[i]);
        free(authors[i]);
    }
    free(names);
    free(authors);
    free(years);

    return 0;

}

int test6(){
    char text[N], operator;
    char* tokin[N];
    int i = 0, chislo;
    type first, two;
    Stack stack = initStack();

    fgets(text, N, stdin);
    tokin[i] = strtok(text, " ");
    while(tokin[i]){
        chislo = atoi(tokin[i]);
        if(chislo){
            push(&stack, chislo);
        }
        else{
            if(count(&stack) > 1){
                operator = *tokin[i];
                switch((int)operator){
                    case 43:{
                        first = pop(&stack);
                        two = pop(&stack);
                        push(&stack, two + first);
                        break;
                    }
                    case 45:{
                        first = pop(&stack);
                        two = pop(&stack);
                        push(&stack, two - first);
                        break;
                    }
                    case 42:{
                        first = pop(&stack);
                        two = pop(&stack);
                        push(&stack, two * first);
                        break;
                    }
                    case 47:{
                        first = pop(&stack);
                        two = pop(&stack);
                        push(&stack, two / first);
                        break;
                    }
                    default:{
                        printf("error\n");
                        return 0;
                    }
                }
            }
            else{
                printf("error\n");
                return 0;
            }
        }
        tokin[++i] = strtok(NULL, " ");
    }
    if(count(&stack) == 1)
        printf("%d\n", pop(&stack));
    else
        printf("error\n");
	return 0;
}

int IsName(char* name){
	char* regexp = "^.*\\.txt$";
	regex_t comp;
	if(regcomp(&comp, regexp, REG_EXTENDED))
		return 0;
	return regexec(&comp, name, 0, NULL, 0) == 0;
}

long long int InFile(char* name, int flag){
	FILE* file = fopen(name, "r");
	if(!file)
		return 0;
	long long int key, result = 0;
	if(flag == 1)
		while(fscanf(file, "%lld", &key) != EOF)
			result += key;
	if(flag == 2){
		result++;
		while(fscanf(file, "%lld", &key) != EOF)
			result *= key;
	}
	fclose(file);
	return result;
}

long long int InDir(char* startdir, int key){
	int flag;
	long long int result = 0, temp1 = 0, temp2 = 0;
	DIR* dir = opendir(startdir);
	if(!dir)
		return 0;
	char nextdir[256];
	strcpy(nextdir, startdir);
	struct dirent* value = readdir(dir);
	if(key == 2){
		result++;
		temp1++;
		temp2++;
	}
	while(value){
		if(value->d_type == DT_DIR && strcmp(value->d_name, "..") != 0 && strcmp(value->d_name, ".") != 0){
        		if(!strcmp(value->d_name, "add"))
                		flag = 1;
        		if(!strcmp(value->d_name, "mul"))
                		flag = 2;
			int len = strlen(nextdir);
			strcat(nextdir, "/");
			strcat(nextdir, value->d_name);
			temp1 = InDir(nextdir, flag);
			nextdir[len] = '\0';
		}
		if(value->d_type == DT_REG && IsName(value->d_name)){
			int len = strlen(nextdir);
			strcat(nextdir, "/");
			strcat(nextdir, value->d_name);
			temp2 = InFile(nextdir, key);
			nextdir[len] = '\0';
		}
		if(key == 1){
			result += temp1;
			result += temp2;
			temp1 = 0;
			temp2 = 0;
		}
		if(key == 2){
			result *= temp1;
			result *= temp2;
			temp1 = 1;
			temp2 = 1;
		}
		value = readdir(dir);
	}
	closedir(dir);
	return result;
}

#define N 100
