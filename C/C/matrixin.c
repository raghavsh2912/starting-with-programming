#include<stdio.h>
#include<conio.h>
int main(){
    int A[100][100],i,j,m,n;
    printf("Enter the number of rows and columns of the matrix: ");
    scanf("%d %d",&m,&n);
    printf("Enter the elements of the matrix: ");
    for(i=0;i<m;i++){
        for(j=0;j<n;j++){
            scanf("%d",&A[i][j]);
        }
    }
    printf("The 2d array is: \n");
    for(i=0;i<m;i++){
        for(j=0;j<n;j++){
            
            printf("%d ",A[i][j]);
        }
        printf("\n");
    }
    getch();
    return 0;
}