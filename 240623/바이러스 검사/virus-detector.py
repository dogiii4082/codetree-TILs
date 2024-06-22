n = int(input())
CUST = list(map(int, input().split()))
LDR, MBR = map(int, input().split())


ans = 0
for cust in CUST:
    if cust <= LDR:
        ans += 1
        continue
    else:
        cust -= LDR
        ans += 1
        if cust % MBR == 0:
            ans += cust // MBR
        else:
            ans += cust // MBR + 1
print(ans)