#include<stdio.h>
#include<conio.h>

int main() 
{
    int arr[100],i,n,m,index=0;

    printf("Enter the number of elements required in the array: ");
    scanf("%d",&n);

    for (i=0;i<n;i++)
    {
        printf("Enter the element %d: ",i+1);
        scanf("%d",&arr[i]);
    }

    printf("Enter the elemnt to be searched:");
    scanf("%d",&m);

    for (i=0;i<n;i++)
    {
        if (arr[i]==m)
        {
            index=i;
            break;
        }
    }

    if (index < n)
    {
        printf("Element found at index: %d\n", index);
    }
    else
    {
        printf("Element not found in the array.\n");
    }

    return 0;
}