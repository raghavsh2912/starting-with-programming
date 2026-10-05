A=[71,38,42,65]
i=0
for i in range(0,len(A),+1):
    if A[i]<40:
        print("Fail in subject scoring marks less than 40",A[i])
    else:
        print("pass in subject scoring marks greater than 40",A[i])

    b= int(A[i]/5)
    c= 5*(b+1)-A[i]

    if c<=3:
        A[i]=5*(b+1)

    else:
        A[i]=A[i]

print("Final marks after rounding off",A)