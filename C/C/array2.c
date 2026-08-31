#include<stdio.h>
#include<conio.h>

int main()
{
    int arr[100],i,n;
    printf("Enter the number of elements required in the array: ");
    scanf("%d",&n);

    for(i=0;i<n;i++)
    {
        printf("enter the elements of the array: ");
        scanf("%d",&arr[i]);

    }
    for (i=0;i<n;i=i+2)
    {
        printf("The elements of the array are: %d\n",arr[i]);
    }
    return 0;
}