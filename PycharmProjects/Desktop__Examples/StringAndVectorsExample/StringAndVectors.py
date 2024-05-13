def Hello_My_Cloud(): return "Hello My Cloud :-)";
print(''); print(Hello_My_Cloud()); print('');print('');

print(f"Assignment 1 - Basic Data Types:"); #ASSIGNMENT 2
print(f"bits are 1 or 0 .... bytes are a stream of 8 bits [00000000]");
print(f"bool is true or false .... Numbers are integers or floating point numbers");
print(f"strings are sets of alphanumeric values .... Lists, Sets, Dictionaries, Tuples");
print(f"BODMAS -> ()Brackets, ^Orders, / // % Division, *Multiplication, +Addition, -Subtraction");
print(f"Division -> [a/b=>floating point number], [a//b=>nearest integer], [a%b=>remainder]")
print(f"function -> def A(a,b,c): ~~~~; ~~~~;");
print(f"print() => will print any kind of variable above ... DONE!"); print('');

print('Assignment 2 - Counting and Strings:'); #ASSIGNMENT 3

print("Here is the Database:")
print("data1 = 'cloudacademy.python.2020';");
print("letter1 = 'a'; word1 ='cloud'; num1 = 2020;")
data1 = 'cloudacademy.python.2020'; letter1 = 'a'; word1 ='cloud'; num1 = '2020'; print('');

#code1 => Count letters, words, and numbers in data1
print(f"code1 => Count letters, words, and numbers in '{data1}'");
print(f"There are {data1.count(letter1)} letter '{letter1}'s");
print(f"There is {data1.count(word1)} word '{word1}'");
print(f"There is {data1.count(num1)} number '{num1}'"); print('');

#code2 => Get character length of string
print(f"code2 => Get character length of '{data1}'")
length1 = len(data1); print(f"The length is {length1} characters long"); print('');

#code3 => Get the highest character in string
print(f"code3 => Get the highest character in '{data1}'")
maximum1 = max(data1); print(f"The highest character is '{maximum1}'"); print('');

#code4 => Get the lowest character in string
print(f"code4 => Get the lowest character in '{data1}'")
minimum1 = min(data1); print(f"The lowest character is '{minimum1}'"); print('');print('');
