#include "stdio.h"
#include "string.h"
#include "stdlib.h"

//Ŀ¼�ṹ 
typedef struct FOLDER{		
	char name[256];					//Ŀ¼��
	struct FOLDER *nextFolder; 		//ͬ����һĿ¼
	struct FOLDER *frontFolder;		//ͬ����һĿ¼
	struct FOLDER *parentFolder;	//��Ŀ¼
	struct FOLDER *firstChildFolder;//��Ŀ¼ 
	struct FILE *firstChildFile;	//���ļ�
	int canRead;					//�Ƿ�ɶ� 
	int canWrite; 					//�Ƿ��д 
}FOLDER, *PFOLDER;
//�ļ����ƿ���Ϣ 
typedef struct FILE{
	char name[256];					//�ļ��� 
	char content[1000];				//�ļ�����		 
	struct FILE *frontFile;			//ͬ��Ŀ¼��һ�ļ�	 
	struct FILE *nextFile;			//ͬ��Ŀ¼��һ�ļ� 
	struct FOLDER *parentFolder;	//��Ŀ¼ 
	int canRead;					//�Ƿ�ɶ� 
	int canWrite;					//�Ƿ��д 
}FILE, *PFILE;

PFOLDER root;						//��Ŀ¼ 
int count = 0;						//���������ʽ 
int flagD = 0;						//ɾ����־

//����ָ��Ŀ¼ 
PFOLDER findCurrentFolder(PFOLDER currentFolder, char name[])
{
	PFOLDER folder;
	if(currentFolder == NULL){
		return NULL;
	}
	if(strcmp(currentFolder->name, name)==0){
		return currentFolder;
	}
	folder = findCurrentFolder(currentFolder->firstChildFolder, name);
	if(folder != NULL)
		return folder;
	folder = findCurrentFolder(currentFolder->nextFolder, name);
	if(folder != NULL)
		return folder;
	return NULL;
}
// ����ָ���ļ�
PFILE findCurrentFile(PFOLDER currentFolder, char name[])
{
	PFILE tempFile;
	if(currentFolder == NULL)
		return NULL;
	//������ǰĿ¼���ļ�
	tempFile = currentFolder->firstChildFile;
	while(tempFile != NULL){
		//�ҵ����ļ�
		if(strcmp(tempFile->name, name) == 0)
			return tempFile;
		//��ǰ�ļ���ƥ�䣬����ҵ�ǰĿ¼����һ���ļ���ֱ����ǰĿ¼���ļ�
		tempFile=tempFile->nextFile;
	}
	//������һĿ¼���Ƿ���ڸ��ļ�
	tempFile=findCurrentFile(currentFolder->firstChildFolder, name);
	if(tempFile != NULL)
		return tempFile;
	//������һĿ¼���Ƿ���ڸ��ļ�
	tempFile=findCurrentFile(currentFolder->nextFolder, name);
	if(tempFile != NULL)
		return tempFile;
	//���Ҳ���
	return NULL;
}

PFOLDER prepareWorkBeforeCreate()
{
	PFOLDER currentFolder = NULL;
	char name[256];
	printf("���뵱ǰĿ¼����:");
	gets(name);
	fflush(stdin);
	currentFolder=findCurrentFolder(root, name);
	if(currentFolder == NULL){
		puts("Ŀ¼�����ڣ�");
		return NULL;
	}
	if(currentFolder->canWrite == 0){
		puts("Ȩ�޲��������贴����");
		return NULL;
	}
	return currentFolder;
}
void createFolder()
{
	PFOLDER currentFolder=prepareWorkBeforeCreate();
	if(currentFolder == NULL){
		return;
	}
	char name[256];
	printf("������Ŀ¼�����ƣ�");
	gets(name);
	fflush(stdin);
	PFOLDER newFolder;
	newFolder = (PFOLDER)malloc(sizeof(FOLDER));
	strcpy(newFolder->name, name);
	newFolder->firstChildFolder=NULL;
	newFolder->firstChildFile=NULL;
	newFolder->nextFolder=NULL;
	newFolder->parentFolder=NULL;
	newFolder->frontFolder=NULL;
	newFolder->canRead=1;
	newFolder->canWrite=1;
	if(currentFolder->firstChildFolder == NULL){
		currentFolder->firstChildFolder=newFolder;
		newFolder->parentFolder=currentFolder;
	}else{
		PFOLDER tempFolder=currentFolder->firstChildFolder;
		PFOLDER lastFolder;
		while(tempFolder != NULL){
			lastFolder=tempFolder;
			if(strcmp(tempFolder->name, newFolder->name) == 0){
				printf("%sĿ¼������ͬ��Ŀ¼��\n", currentFolder->name);
				free(newFolder);
				return ;
			}
			tempFolder=tempFolder->nextFolder;
		}
		lastFolder->nextFolder=newFolder;
		newFolder->frontFolder=lastFolder;
	}
	puts("�����ɹ���");
}

void createFile()
{
	PFOLDER currentFolder=prepareWorkBeforeCreate();
	if(currentFolder == NULL){
		return ;
	}
	char name[256];
	printf("���������ļ����ƣ�");
	gets(name);
	fflush(stdin);
	PFILE newFile;
	newFile=(PFILE)malloc(sizeof(FILE));
	strcpy(newFile->name, name);
	printf("�Ƿ������ļ����ݣ�:");
	char ans = getchar();
	fflush(stdin);
	if(ans == 'y' || ans == 'Y'){
		printf("�����ļ����ݣ�");
		gets(newFile->content);
	}else{
		strcpy(newFile->content, "");
	}
	fflush(stdin);
	newFile->nextFile=NULL;
	newFile->frontFile=NULL;
	newFile->parentFolder=NULL;
	newFile->canRead=1;
	newFile->canWrite=1;
	if(currentFolder->firstChildFile==NULL){
		currentFolder->firstChildFile=newFile;
		newFile->parentFolder=currentFolder;
	}else{
		PFILE tempFile=currentFolder->firstChildFile;
		PFILE lastFile;
		while(tempFile!=NULL){
			lastFile=tempFile;
			if(strcmp(tempFile->name, newFile->name) == 0){
				printf("%sĿ¼���Ѿ���ͬ���ļ���\n", currentFolder->name);
				free(newFile);
				return;
			}
			tempFile=tempFile->nextFile;
		}
		lastFile->nextFile=newFile;
		newFile->frontFile=lastFile;
	}
	puts("�����ɹ���");
}

void inputName(char name[])
{
	printf("�������ƣ�");
	gets(name);
	fflush(stdin);
}
//ɾ����Ŀ¼����������
void deleteAllChild(PFOLDER currentFolder)
{
	PFILE tempFile, dFile;
	if(currentFolder==NULL)
		return ;
	if(flagD)
		deleteAllChild(currentFolder->nextFolder);
	flagD=1;
	deleteAllChild(currentFolder->firstChildFolder);
	tempFile=currentFolder->firstChildFile;
	while(tempFile!=NULL){
		dFile=tempFile;
		tempFile=tempFile->nextFile;
		free(dFile);
	}
	free(currentFolder);
}

void deleteFolder()
{
	char name[256];
	inputName(name);
	if(strcmp(name, "root") == 0){
		puts("��Ŀ¼��׼ɾ����");
		return;
	}
	PFOLDER currentFolder=findCurrentFolder(root, name);
	if(currentFolder==NULL){
		printf("��Ŀ¼�����ڣ�");
		return;
	}
	if(currentFolder->canWrite==0){
		printf("Ȩ�޲������޷�ɾ����");
		return;
	}
	if(currentFolder->frontFolder==NULL){
		currentFolder->parentFolder->firstChildFolder=currentFolder->nextFolder;
		if(currentFolder->nextFolder!=NULL){
			currentFolder->nextFolder->frontFolder=NULL;
		}
	}else{
		currentFolder->frontFolder->nextFolder=currentFolder->nextFolder;
	}
	deleteAllChild(currentFolder);
	puts("ɾ���ɹ���");
}
//ɾ���ļ�
void deleteFile()
{
	char name[256];
	inputName(name);
	PFILE currentFile=findCurrentFile(root, name);
	if(currentFile==NULL){
		printf("�ļ������ڣ�");
		return;
	}
	if(currentFile->frontFile==NULL){
		currentFile->parentFolder->firstChildFile=currentFile->nextFile;
		if(currentFile->nextFile!=NULL){
			currentFile->nextFile->frontFile=NULL;
		}
	}else{
		currentFile->frontFile->nextFile=currentFile->nextFile;
	}
	free(currentFile);
	puts("ɾ���ɹ���");
}
void displayFile(PFOLDER currentFolder)
{
	PFILE tempFile;
	if(currentFolder != NULL && currentFolder->canRead)
	{
		for(int i=0;i<count;i++){
			printf(" ");
		}
		printf("|-");
		printf(currentFolder->name);
		int length=15-count*2-strlen(currentFolder->name);
		for(i=0;i<length;i++){
			printf(" ");
		}
		if(count==0)
			printf("	canRead		canWrite\n");
		else
			printf("<dir>	%d		%d\n", currentFolder->canRead,currentFolder->canWrite);
	}else if(currentFolder==NULL){
		count--;
		return;
	}
	count++;
	tempFile=currentFolder->firstChildFile;
	while(tempFile!=NULL){
		if(tempFile!=NULL){
			for(int i =0;i<count;i++){
				printf(" ");
			}
			printf("|-");
			printf(tempFile->name);
			int length=20-count*2-strlen(tempFile->name);
			for(i=0;i<length;i++)
				printf(" ");
			if(count==0)
				printf("	canRead		canWrite\n");
			else
				printf("	%d		%d\n", tempFile->canRead, tempFile->canWrite);
		}
		tempFile=tempFile->nextFile;
	}
	displayFile(currentFolder->firstChildFolder);
	displayFile(currentFolder->nextFolder);
}
//չʾ�ļ�����
void showFileContent()
{
	PFILE currentFile=NULL;
	char name[256];
	printf("�������ļ�����");
	gets(name);
	fflush(stdin);
	currentFile=findCurrentFile(root, name);
	if(currentFile==NULL){
		puts("�ļ������ڣ�");
		return ;
	}
	if(!currentFile->canRead){
		puts("Ȩ�޲������޷���ȡ��");
		return ;
	}
	printf("�ļ����ݣ�%s\n", currentFile->content);
	printf("�ļ����ȣ�%d\n", strlen(currentFile->content));
}
 
void changeFileContent()
{
	PFILE currentFile=NULL;
	char name[256];
	printf("�����ļ�����");
	gets(name);
	fflush(stdin);
	currentFile=findCurrentFile(root, name);
	if(currentFile==NULL){
		puts("�ļ������ڣ�");
		return;
	}
	if(!currentFile->canWrite)
	{
		puts("Ȩ�޲��㣬�����޸ģ�");
		return ;
	}
	printf("�����ļ����ݣ�");
	gets(currentFile->content);
	fflush(stdin);
	puts("���ĳɹ���");
}

void changeAllChildPermission(PFOLDER currentFolder, int canRead, int canWrite)
{
	PFILE tempFile;
	if(currentFolder!=NULL)
	{
		currentFolder->canRead=canRead;
		currentFolder->canWrite=canWrite;
	}else if(currentFolder==NULL)
		return;
	tempFile = currentFolder->firstChildFile;
	while(tempFile!=NULL){
		tempFile->canRead=canRead;
		tempFile->canWrite=canWrite;
		tempFile = tempFile->nextFile;
	}
	changeAllChildPermission(currentFolder->firstChildFolder, canRead, canWrite);
	if(currentFolder->firstChildFolder!=NULL)
		changeAllChildPermission(currentFolder->firstChildFolder->nextFolder, canRead, canWrite);

}

void changeFolderPermission()
{
	char name[256];
	inputName(name);
	if(strcmp(name, "root") == 0){
		puts("��Ŀ¼���������Ȩ�ޣ�");
		return;
	}
	PFOLDER currentFolder=NULL;
	currentFolder=findCurrentFolder(root, name);
	if(currentFolder==NULL){
		puts("Ŀ¼�����ڣ�");
		return ;
	}
	printf("����Ŀ¼Ȩ�ޣ��� д��->�� 0 1��");
	scanf("%d%d", &currentFolder->canRead, &currentFolder->canWrite);
	fflush(stdin);
	changeAllChildPermission(currentFolder, currentFolder->canRead, currentFolder->canWrite);
	puts("Ȩ���޸ĳɹ���");
}

void changeFilePermission()
{
	char name[256];
	inputName(name);
	PFILE currentFile=NULL;
	currentFile=findCurrentFile(root, name);
	if(currentFile==NULL){
		puts("�ļ������ڣ�");
		return ;
	}
	printf("�����ļ�Ȩ�ޣ��� д��->�� 0 1��");
	scanf("%d%d", &currentFile->canRead, &currentFile->canWrite);
	fflush(stdin);
	puts("Ȩ���޸ĳɹ���");
}
//�ж����������ļ��Ƿ�����
int fileNameIsDuplication(PFILE currentFile, char name[])
{
	PFILE tempFile = currentFile->frontFile;
	while(tempFile!=NULL){
		if(strcmp(tempFile->name, name)==0){
			printf("�ļ�������");
			return 1;
		}
		tempFile = tempFile->frontFile;
	}
	tempFile = currentFile->nextFile;
	while(tempFile!=NULL){
			if(strcmp(tempFile->name, name)==0){
			printf("�ļ�������");
			return 1;
		}
		tempFile = tempFile->nextFile;
	}
	return 0;
}
//�ж�Ŀ¼�������Ƿ�����
int folderNameIsDuplication(PFOLDER currentFolder, char name[])
{
	PFOLDER tempFolder = currentFolder->frontFolder;
	while(tempFolder!=NULL){
		if(strcmp(tempFolder->name, name)==0){
			printf("Ŀ¼������");
			return 1;
		}
		tempFolder = tempFolder->frontFolder;
	}
	tempFolder = currentFolder->nextFolder;
	while(tempFolder!=NULL){
		if(strcmp(tempFolder->name, name)==0){
			printf("Ŀ¼������");
			return 1;
		}
		tempFolder = tempFolder->nextFolder;
	}
	return 0;
}

void renameFolder()
{
	char name[256];
	inputName(name);
	if(strcmp("root", name)==0){
		puts("��Ŀ¼�޷���������");
		return ;
	}
	PFOLDER currentFolder = findCurrentFolder(root, name);
	if(currentFolder==NULL){
		puts("Ŀ¼�����ڣ�");
		return;
	}
	printf("���������ƣ�");
	gets(name);
	fflush(stdin);
	if(folderNameIsDuplication(currentFolder, name))
		return ;
	strcpy(currentFolder->name, name);
	puts("�������ɹ���");
}

void renameFile()
{
	char name[256];
	inputName(name);
	PFILE currentFile=findCurrentFile(root, name);
	if(currentFile==NULL){
		puts("�ļ������ڣ�");
		return;
	}
	printf("���������ƣ�");
	gets(name);
	fflush(stdin);
	if(fileNameIsDuplication(currentFile, name))
		return;
	strcpy(currentFile->name, name);
	puts("�������ɹ���");
}

void menu()
{
	char choice[256];
	printf("\t*********************************************************\n");
	printf("\t*		mkdir:		����Ŀ¼		*\n");
	printf("\t*		rmdir:		ɾ��Ŀ¼		*\n");
	printf("\t*		rnamedir:	������Ŀ¼		*\n");
	printf("\t*		chdir:		����Ŀ¼Ȩ��		*\n");
	printf("\t*		touch:		�����ļ�		*\n");
	printf("\t*		rmfile:		ɾ���ļ�		*\n");
	printf("\t*		rnamefile:	�������ļ�		*\n");
	printf("\t*		less:		��ʾ�ļ�����		*\n");
	printf("\t*		vi:		�����ļ�����		*\n");
	printf("\t*		chmod:		�����ļ�Ȩ��		*\n");
	printf("\t*		exit:		�˳�			*\n");
	printf("\t*********************************************************\n");
	count = 0;
	printf("\n��Ŀ¼�ṹ��\n");
	displayFile(root);
	while(1){
		printf("\n---------------------------------------------------\n");
		printf("������������");
		gets(choice);
		fflush(stdin);
		if(strcmp(choice, "mkdir")==0){
			createFolder();
		}else if(strcmp(choice, "rmdir")==0){
			deleteFolder();
		}else if(strcmp(choice, "rnamedir")==0){
			renameFolder();
		}else if(strcmp(choice, "chdir")==0){
			changeFolderPermission();
		}else if(strcmp(choice, "touch")==0){
			createFile();
		}else if(strcmp(choice, "rmfile")==0){
			deleteFile();
		}else if(strcmp(choice, "rnamefile")==0){
			renameFile();
		}else if(strcmp(choice, "less")==0){
			showFileContent();
		}else if(strcmp(choice, "vi")==0){
			changeFileContent();
		}else if(strcmp(choice, "chmod")==0){
			changeFilePermission();
		}else if(strcmp(choice, "exit")==0){
			exit(0);
		}
		count = 0;
		printf("\n��Ŀ¼�ṹ��\n");
		displayFile(root);
	}
}

void initRootFolder()
{
	root=(PFOLDER)malloc(sizeof(FOLDER));
	root->frontFolder=NULL;
	root->nextFolder=NULL;
	root->parentFolder=NULL;
	root->firstChildFolder=NULL;
	root->firstChildFile=NULL;
	root->canRead=1;
	root->canWrite=1;
	strcpy(root->name, "root");
}

int main() {
	initRootFolder();
	menu();
	return 0;
}