def logincheck(email,psw):
    lines = open("info.txt").read().split('\n')
    for i in lines:
        print(i)
        if email in i:
            k=0
            temppsw=''
            while i[k] != ' ':
                k=k+1
            k=k+3
            while k < len(i):
                temppsw=temppsw+i[k]
                k=k+1
            if temppsw == psw:
                check='Access granted'
                break
            else:
                check="Access denied"
                break        
        else:
            check="Access denied"
    return(check)
               