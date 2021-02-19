# print('hello from python')
f=open("guru99.txt", "a+")
for i in range(2):
     f.write("Appended line %d\r\n" % (i+1))