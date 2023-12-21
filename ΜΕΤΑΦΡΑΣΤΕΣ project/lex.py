import sys
Trans_Diagram = [
    [0, 0, 0, 1, 2, '+tk', '-tk', '*tk', 6, 3, 4, '=tk', ';tk', ',tk', 5, '(tk', ')tk', '[tk', ']tk', '{tk', '}tk', 'eoftk', 'errortk' ],
    ['idtk', 'idtk', 'idtk', 1, 1, 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk', 'idtk'],
    ['constanttk', 'constanttk', 'constanttk', 'constanttk', 2, 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk', 'constanttk'],
    ['<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<>tk', '<=tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk', '<tk'],
    ['>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>=tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk', '>tk'],
    [':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':=tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk', ':tk'],
    ['/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', 9, 7, '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk', '/tk'],
    [7, 7, 0, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 'error1tk', 7],
    [7, 7, 0, 7, 7, 7, 7, 'error2tk', 'error2tk', 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 'error1tk', 7],
    [9, 9, 9, 9, 9, 9, 9, 10, 11, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 'error1tk', 9],
    [9, 9, 9, 9, 9, 9, 9, 10, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 'error1tk', 9],
    [9, 9, 0, 9, 9, 9, 9, 'error2tk', 'error2tk', 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 'error1tk', 9]
    ]

infile = open(sys.argv[1])
line = 1
def lex():
    global line
    state = 0
    word = ""

    while state in range(12):
        ch = infile.read(1)

        col = 22
        if ch == ' ':
            col = 0
        elif ch == '\t':
            col = 1
        elif ch == '\n':
            col = 2
            line = line + 1
        elif ch.isalpha():
            col = 3
        elif ch.isdigit():
            col = 4
        elif ch == '+':
            col = 5
        elif ch == '-':
            col = 6
        elif ch == '*':
            col = 7
        elif ch == '/':
            col = 8
        elif ch == '<':
            col = 9
        elif ch == '>':
            col = 10
        elif ch == '=':
            col = 11
        elif ch == ';':
            col = 12
        elif ch == ',':
            col = 13
        elif ch == ':':
            col = 14
        elif ch == '(':
            col = 15
        elif ch == ')':
            col = 16
        elif ch == '[':
            col = 17
        elif ch == ']':
            col = 18
        elif ch == '{':
            col = 19
        elif ch == '}':
            col = 20
        elif ch == '':
            col = 21
        state = Trans_Diagram[state][col]

        word = word + ch
        if state == 0:
            word = ""

    if state in ['idtk', 'constanttk', '<tk', '>tk', ':tk', '/tk']:
        word = word[:-1]
        infile.seek(infile.tell()-1)
        if ch == '\n':
            line = line - 1

    if state == 'error1tk':
        print(str(line)+": EOF before end of comments\n")
        exit(0)
    if state == 'error2tk':
        print(str(line)+": comments begin inside comments\n")
        exit(0)
    if state == 'errortk':
        print(str(line)+": unrecognized character\n")
        exit(0)

    if state == 'idtk':
        if word in ['program', 'declare','if', 'else', 'while', 'doublewhile', 'loop', 'exit', 'forcase', 'incase', 'when', 'default', 'not', 'and', 'or', 'function', 'procdure', 'call', 'return', 'in', 'inout', 'input', 'print']:
            state = word +"tk"
    return word, state

for i in range(len(Trans_Diagram)):
    print(len(Trans_Diagram[i]))


word, state = lex()
print(word, state)

while state != 'eoftk':
  word, state = lex()
  print(word, state)
