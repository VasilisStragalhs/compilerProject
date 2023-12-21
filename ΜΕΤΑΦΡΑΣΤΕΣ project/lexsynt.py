#Mpalatsoukas Nikolaos A.M. 3037 Username: cse53037
#Stragalis Vasileios A.M. 2909 Username: cse42909

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
word = ""
state = 0

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
        if word in ['program', 'declare','if', 'else', 'while', 'doublewhile', 'loop', 'exit', 'forcase', 'incase', 'when', 'default', 'not', 'and', 'or', 'function', 'procedure', 'call', 'return', 'in', 'inout', 'input', 'print', 'then']:
            state = word +"tk"
    return word, state

def program():
    global state, word
    if state != 'programtk':
        print(str(line)+": program not found at the beginning")
        exit(0)
    word, state = lex()
    if state != 'idtk':
        print(str(line)+": program name not found")
        exit(0)

    word, state = lex()
    if state != '{tk':
        print(str(line)+": { not found after program name")
        exit(0)
    word, state = lex()
    block()
    if state != '}tk':
        print(str(line)+": } not found at the end of program")
        exit(0)

def block():
    declarations()
    subprograms()

    statements()


def declarations():
    global state, word
    while state == 'declaretk':
        word, state = lex()
        varlist()
        if state != ';tk':
            print(str(line)+": ; not found at the end of declarations")
            exit(0)
        word, state = lex()

def varlist():
    global state, word
    if state == 'idtk':
        word, state = lex()
        while state == ',tk':
            word, state = lex()
            if state != 'idtk':
                print(str(line)+": variable name not found after ,")
                exit(0)
            word, state = lex()

def subprograms():
    global state, word
    while state == 'functiontk' or state == 'proceduretk':
        subprogram()

def subprogram():
    global state, word
    if state == 'functiontk':
        word, state = lex()
        if state != 'idtk':
            print(str(line)+": function name not found after function")
            exit(0)
        word, state = lex()
        funcbody()
    elif state == 'proceduretk':
        word, state = lex()
        if state != 'idtk':
            print(str(line)+": procedure name not found after procedure")
            exit(0)
        word, state = lex()
        funcbody()

def funcbody():
    global state, word
    formalpars()
    if state != '{tk':
        print(str(line)+": { not found after ) of function or procdure")
        exit(0)
    word, state = lex()
    block()
    if state != '}tk':
        print(str(line)+": } not found at the end of function or procdure")
        exit(0)
    word, state = lex()

def formalpars():
    global state, word
    if state != '(tk':
        print(str(line)+": ( not found after function or procdure name")
        exit(0)
    word, state = lex()
    formalparlist()

    if state != ')tk':
        print(str(line)+": ) not found after function or procdure parameters")
        exit(0)
    word, state = lex()

def formalparlist():

    global state, word

    if state == 'intk' or state == 'inouttk':
        formalparitem()
        while state == ',tk':
            word, state = lex()
            formalparitem()

def formalparitem():
    global state, word
    if state != 'intk' and state != 'inouttk':
        print(str(line)+": in or inout expected for parameters declaration")
        exit(0)

    word, state = lex()
    if state != 'idtk':
        print(str(line)+": parameter name expected")
        exit(0)
    word, state = lex()

def statements():
    global state, word

    if state == '{tk':
        word, state = lex()
        statement()
        while state == ';tk':
            word, state = lex()
            statement()
        if state != '}tk':
            print(str(line)+": } not found at end of statements")
            exit(0)
        word, state = lex()
    else:
        statement()
def statement():
    global state, word

    if state == 'idtk':
        word, state = lex()
        assignment_stat()
    elif state == 'iftk':
        word, state = lex()
        if_stat()
    elif state == 'whiletk':
        word, state = lex()
        while_stat()
    elif state == 'doublewhiletk':
        word, state = lex()
        doublewhile_stat()
    elif state == 'looptk':
        word, state = lex()
        loop_stat()
    elif state == 'exittk':
        word, state = lex()
        exit_stat()
    elif state == 'forcasetk':
        word, state = lex()
        forcase_stat()
    elif state == 'incasetk':
        word, state = lex()
        incase_stat()
    elif state == 'calltk':
        word, state = lex()
        call_stat()
    elif state == 'returntk':
        word, state = lex()
        return_stat()
    elif state == 'inputtk':
        word, state = lex()
        input_stat()
    elif state == 'printtk':
        word, state = lex()
        print_stat()
    else:
        print(word, state)
        print(str(line)+": not valid statement")
        exit(0)

def assignment_stat():
    global state, word
    if state != ':=tk':
        print(str(line)+": := not found after variable")
        exit(0)
    word, state = lex()
    expression()

def if_stat():
    global state, word
    if state != '(tk':
        print(str(line)+": ( not found after if")
        exit(0)

    word, state = lex()
    condition()

    if state != ')tk':
        print(str(line)+": ) not found after condition")
        exit(0)

    word, state = lex()
    if state != 'thentk':
        print(str(line)+": then not found after )")
        exit(0)
    word, state = lex()
    statements()
    elsepart()

def elsepart():
    global state, word
    if state == 'elsetk':
        word, state = lex()
        statements()

def while_stat():
    global state, word
    if state != '(tk':
        print(str(line)+": ( not found after while")
        exit(0)

    word, state = lex()
    condition()

    if state != ')tk':
        print(str(line)+": ) not found after condition")
        exit(0)

    word, state = lex()
    statements()

def doublewhile_stat():
    global state, word
    if state != '(tk':
        print(str(line)+": ( not found after doublewhile")
        exit(0)

    word, state = lex()
    condition()

    if state != ')tk':
        print(str(line)+": ) not found after condition")
        exit(0)

    word, state = lex()
    statements()

    if state != 'elsetk':
        print(str(line)+": else not found after statements")
        exit(0)

    word, state = lex()
    statements()

def loop_stat():
    global state, word
    statements()

def exit_stat():
    global state, word
    return

def forcase_stat():
    global state, word
    while state == 'whentk':
        word, state = lex()
        if state != '(tk':
            print(str(line)+": ( not found after when")
            exit(0)

        word, state = lex()
        condition()

        if state != ')tk':
            print(str(line)+": ) not found after condition")
            exit(0)

        word, state = lex()
        if state != ':tk':
            print(str(line)+": : not found after )")
            exit(0)
        word, state = lex()
        statements()

    if state != 'defaulttk':
        print(str(line)+": default not found in forcase")
        exit(0)

    word, state = lex()
    if state != ':tk':
        print(str(line)+": : not found after )")
        exit(0)
    word, state = lex()
    statements()



def incase_stat():
    global state, word
    while state == 'whentk':
        word, state = lex()
        if state != '(tk':
            print(str(line)+": ( not found after when")
            exit(0)

        word, state = lex()
        condition()

        if state != ')tk':
            print(str(line)+": ) not found after condition")
            exit(0)

        word, state = lex()
        if state != ':tk':
            print(str(line)+": : not found after )")
            exit(0)
        word, state = lex()
        statements()

def return_stat():
    global state, word
    expression()

def call_stat():
    global state, word

    if state != 'idtk':
        print(str(line)+": procedure name not found after call")
        exit(0)

    word, state = lex()
    actualpars()


def print_stat():
    global state, word

    if state != '(tk':
        print(str(line)+": ( not found after print")
        exit(0)

    word, state = lex()
    expression()
    if state != ')tk':
        print(str(line)+": ) not found after expression")
        exit(0)
    word, state = lex()

def input_stat():
    global state, word

    if state != '(tk':
        print(str(line)+": ( not found after input")
        exit(0)

    word, state = lex()
    if state != 'idtk':
        print(str(line)+": variable name not found for input")
        exit(0)
    word, state = lex()
    if state != ')tk':
        print(str(line)+": ) not found after variable name")
        exit(0)
    word, state = lex()

def actualpars():
    global state, word
    if state != '(tk':
        print(str(line)+": ( not found after function or procdure name")
        exit(0)
    word, state = lex()
    actualparlist()

    if state != ')tk':
        print(str(line)+": ) not found after function or procdure parameters")
        exit(0)
    word, state = lex()

def actualparlist():

    global state, word

    if state == 'intk' or state == 'inouttk':
        actualparitem()
        while state == ',tk':
            word, state = lex()
            actualparitem()

def actualparitem():
    global state, word
    if state != 'intk' and state != 'inouttk':
        print(str(line)+": in or inout expected for parameters declaration")
        exit(0)
    if state == 'intk':
        word, state = lex()
        expression()
    else:
        word, state = lex()
        if state != 'idtk':
            print(str(line)+": parameter name expected")
            exit(0)
        word, state = lex()

def condition():
    global state, word
    boolterm()
    while state == 'ortk':
        word, state = lex()
        boolterm()
def boolterm():
    global state, word
    boolfactor()
    while state == 'andtk':
        word, state = lex()
        boolfactor()
def boolfactor():
    global state, word
    if state == 'nottk':
        word, state = lex()
        if state != '[tk':
            print(str(line)+": [ not found after not")
            exit(0)
        word, state = lex()
        condition()
        if state != ']tk':
            print(str(line)+": ] not found after condition")
            exit(0)
        word, state = lex()
    elif state == '[tk':
        word, state = lex()
        condition()
        if state != ']tk':
            print(str(line)+": ] not found after condition")
            exit(0)
        word, state = lex()
    else:
        expression()
        relational_oper()
        expression()

def relational_oper():
    global state, word
    if state != '=tk' and state != '<=tk' and state != '>=tk' and state != '<tk' and state != '>tk' and state != '<>tk':
        print(str(line)+": relational operator not found after expression")
        exit(0)
    word, state = lex()

def expression():
    global state, word
    if state == '+tk' or state == '-tk':
        word, state = lex()
    term()

    while state == '+tk' or state == '-tk':
        word, state = lex()
        term()

def term():
    global state, word
    factor()

    while state == '*tk' or state == '/tk':
        word, state = lex()
        factor()

def factor():
    global state, word
    if state != 'constanttk' and state != 'idtk' and state != '(tk':
        print(str(line)+": constant, id or ( not found for expression")
        exit(0)
    if state == 'constanttk':
        word, state = lex()
    elif state == '(tk':
        word, state = lex()
        expression()
        if state != ')tk':
            print(str(line)+": ) not found after expression")
            exit(0)
        word, state = lex()
    else:
        word, state = lex()
        idtail()

def idtail():
    global state, word
    if state == '(tk':
        actualpars()

word, state = lex()
program()
