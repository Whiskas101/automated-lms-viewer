#include<stdio.h>
#include<conio.h>
void main()
{
    clrscr();
    int i, j, n, temp, counter, number[100];
    counter=0;
    clrscr();
    printf("Enter how many numbers you want to sort: ");
    scanf("%d",&n);
    for(i=0; i<n; i++)
    {
        printf("Enter %d elements: ",n);
        for(i=0; i<n; i++) 
        {
            scanf("%d",&number[i]);
        }
        for(i=1; i<n; i++)
         {
            temp=number[i];
            j=i-1;
            counter++;
            while((temp<number[j])&&(j>=0)) {
                number[j+1]=number[j];
                j=j-1;
                counter++;
            }
            number[j+1]=temp;
        }
        printf("Order of Sorted elements: ");
        for(i=0; i<n; i++) {
            printf(" %d",number[i]);
            counter++;
        }
        printf("\n complexity is =%d",counter);
        getch();
    }
}