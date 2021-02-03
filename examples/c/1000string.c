#include <stdio.h>
#include <stdlib.h>
#include "get_name.h"
#include <string.h>
#include "print_str.h"


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

int test2(){
	int arr[100], i, a;
	char ch;
	printf("Нажмите 0 для поиска максимального числа в массиве\n");
        printf("Нажмите 1 для поиска минимального числа в массиве\n");
        printf("Нажмите 2 для нахождения разности максимального и минимального числа в массиве\n");
        printf("Нажмите 3 для нахождения суммы чисел, стоящих до минимального числа\n");
	scanf("%d", &a);
	printf("Введите массив чисел\n");
	for(i = 0; i != 100; ++i){
		scanf("%d", arr + i);
		if((ch = getchar()) == '\n')
			break;}
	switch(a){
		case 0:{
			printf("%d\n", max(arr, i));
			break;}
		case 1:{
			printf("%d\n", min(arr, i));
			break;}
		case 2:{
			printf("%d\n", diff(arr, i));
			break;}
		case 3:{
			printf("%d\n", sum(arr, i));
			break;}
		default:{
			printf("Данные некорректны\n");
			break;}}
return 0;}

int min(int* arr, int len){
	int i, min = arr[0];
	for(i = 1; i < len; ++i){
		if(arr[i] < min)
			min = arr[i];}
return min;}

int sum(int* arr, int len){
        int i, summa = 0;
        for(i = 0; arr[i] != min(arr, len); ++i)
		summa += arr[i];
return summa;}

int test3(){
        int r = 1, big = 0, snachala = 0, potom = 0, kolsim = 0;
        char simvol;
        char* vrem;
        char* nachpred;
        char* text0 = malloc(100 * sizeof(char));
        char* text = text0;
        while((simvol = getchar()) != '\n'){					//считывание текста
                *(text++) = simvol;
                kolsim++;
                if((kolsim % 100) == 0){					//выделение дополнительной памяти
                    r++;
                    if(!(text0 = realloc(text0, (100 * r) * sizeof(char)))){
		       free(text0);
                       printf("Память кончилась.\n");
                       return -10000;}
		    else text = text0 + kolsim;}}				//перемещение указателя на новое место
        *(++text) = '\0';
        text = text0;
        char* result0 = malloc(kolsim * sizeof(char));
        char* result = result0;
        while(*text == ' ' || *text == '\t')					//удаление пробелов и табуляций перед первым предложением
            text++;
        while(*text != '\0'){							//запись редактируемого текста в новую строку
                *(result++) = *(text++);
                if(*text == '.' || *text == ';' || *text == '?'){		//счётчик предложений
                    snachala++;
                    *(result++) = *(text++);
                    while(*text == ' ' || *text == '\t')			//удаление табуляций перед началом предложений
                        text++;
                    *(result++) = '\n';}}
        *result = '\0';
        result = result0;
        potom = snachala;
        while(*result != '\0'){							//удаление предложений, содержащих больше одной большой буквы
            nachpred = result;
            vrem = nachpred;
            while(*result != '\n' && *result != '\0'){
                if(*result >= 'A' && *result <= 'Z')
                    big++;
                result++;}
            if(big > 1){
                result++;
                potom--;
                while(*result != '\0')
                    *(vrem++) = *(result++);
                *vrem = '\0';
                result = nachpred;}
            else result++;
            big = 0;}
        printf("%s\n", result0);
        printf("Количество предложений до %d и количество предложений после %d", snachala, potom);
        free(text0);
        free(result0);
return 0;}

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stddef.h>

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


int test4(){
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

#define N 100

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

int test7(){
	int flag = 0;
	DIR* dir = opendir("/home/box/tmp");
	if(!dir)
		return 0;
	struct dirent* value = readdir(dir);
        while(value){
                if(value->d_type == DT_DIR && strcmp(value->d_name, "..") != 0 && strcmp(value->d_name, ".") != 0){
                        if(!strcmp(value->d_name, "add"))
                                flag = 1;
                        if(!strcmp(value->d_name, "mul"))
                                flag = 2;
			break;
		}
		value = readdir(dir);
	}
	closedir(dir);
	FILE* file = fopen("/home/box/result.txt", "w");
	long long int result = InDir("/home/box/tmp", flag);
        fprintf(file, "%lld", result);
	fclose(file);
	return 0;
}

#pragma pack(push, 1)
struct BitmapFileHeader{
	unsigned short signature;
	unsigned int filesize;
	unsigned short reserved1;
	unsigned short reserved2;
	unsigned int offsettopixelarr;
};
#pragma pack(pop)

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

int True_Png(char *str){
    char str1[100]="";
    strcat(str1,str);
    char *str2=strtok(str1,".");
    if(str2!=NULL){
        str2=strtok(NULL,".");
    }
    if(str2!=NULL)
    	if(strcmp(str2,"png")==0)
		return 1;
    return 0;
}
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
