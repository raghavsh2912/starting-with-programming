#include<stdio.h>
#include<conio.h>

int main()
{
    int arr[100],n,i,m,index=0;
printf("Enter the number of elements in the array:");
scanf("%d",&n);

for(i=0;i<n;i++)
{
    printf("Enter element %d:",i+1);
    scanf("%d",&arr[i]);
}

printf("Enter the index of the element to be deleted:");
scanf("%d",&m);

if(m<0 || m>=n)
{
    printf("Invalid index");
}
else
{
    for(i=m;i<n-1;i++)
    {
        arr[i]=arr[i+1];
    }
    n--;
    printf("Array after deletion:\n");
    for(i=0;i<n;i++)
    {
        printf("%d ",arr[i]);
    }
}}