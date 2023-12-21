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

quads = []
tempCounter = 0
programName = ""

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
    global state, word, programName
    if state != 'programtk':
        print(str(line)+": program not found at the beginning")
        exit(0)
    word, state = lex()
    name = word
    programName = name
    if state != 'idtk':
        print(str(line)+": program name not found")
        exit(0)

    word, state = lex()
    if state != '{tk':
        print(str(line)+": { not found after program name")
        exit(0)
    word, state = lex()
    block(name)
    if state != '}tk':
        print(str(line)+": } not found at the end of program")
        exit(0)

def block(name):
    global programName
    declarations()
    subprograms()
    
    genquad("begin block", name, "_", "_")
    statements()
    if name == programName:
        genquad("halt", "_", "_", "_")
    genquad("end block", name, "_", "_")

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
        name = word
        if state != 'idtk':
            print(str(line)+": function name not found after function")
            exit(0)
        word, state = lex()
        funcbody(name)
    elif state == 'proceduretk':
        word, state = lex()
        name = word
        if state != 'idtk':
            print(str(line)+": procedure name not found after procedure")
            exit(0)
        word, state = lex()
        funcbody(name)

def funcbody(name):
    global state, word
    formalpars()
    if state != '{tk':
        print(str(line)+": { not found after ) of function or procdure")
        exit(0)
    word, state = lex()
    block(name)
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
        assignmentID = word
        word, state = lex()
        assignment_stat(assignmentID)
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

def assignment_stat(assignmentID):
    global state, word
    if state != ':=tk':
        print(str(line)+": := not found after variable")
        exit(0)
    word, state = lex()
    eplace = expression()
    genquad(":=", eplace, "_", assignmentID)
    
def if_stat():
    global state, word
    if state != '(tk':
        print(str(line)+": ( not found after if")
        exit(0)

    word, state = lex()
    true, false = condition()
    print(true, false)
    if state != ')tk':
        print(str(line)+": ) not found after condition")
        exit(0)

    word, state = lex()
    if state != 'thentk':
        print(str(line)+": then not found after )")
        exit(0)
    word, state = lex()
    
    backpatch(true, nextquad())
    statements()
    
    jumpList = makelist(nextquad())
    genquad("jump", "_", "_", "_")
    backpatch(false, nextquad())    
    elsepart()

    
    backpatch(jumpList, nextquad())
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
    label = nextquad()
    true, false = condition()

    if state != ')tk':
        print(str(line)+": ) not found after condition")
        exit(0)

    backpatch(true, nextquad())
    word, state = lex()
    statements()
    genquad("jump", "_", "_", label)
    backpatch(false, nextquad())

def doublewhile_stat():
    global state, word
    
    flag = newtemp()
    genquad(":=", 0, "_", flag)
    label = nextquad()
    
    if state != '(tk':
        print(str(line)+": ( not found after doublewhile")
        exit(0)

    word, state = lex()
    
    true, false = condition()

    if state != ')tk':
        print(str(line)+": ) not found after condition")
        exit(0)

    word, state = lex()
    
    backpatch(true, nextquad())
    jump1 = makelist(nextquad())
    genquad("=", flag, 2, "_")
    
    statements()
    
    genquad(":=", 1, "_", flag)
    genquad("jump", "_", "_", label)
    
    if state != 'elsetk':
        print(str(line)+": else not found after statements")
        exit(0)

    backpatch(false, nextquad())
    jump2 = makelist(nextquad())
    genquad("=", flag, 1, "_")
    jump1 = merge(jump1, jump2)
    
    word, state = lex()
    statements()
    
    genquad(":=", 2, "_", flag)
    genquad("jump", "_", "_", label)
    
    backpatch(jump1, nextquad())

def loop_stat():
    global state, word, exitList
    
    exitList = emptylist()
    
    label = nextquad()
    statements()
    genquad("jump", "_", "_", label)
    
    backpatch(exitList, nextquad())

def exit_stat():
    global state, word, exitList
    
    exit = makelist(nextquad())
    exitList = merge(exitList, exit)
    genquad("jump", "_", "_", "_")
    return

def forcase_stat():
    global state, word
    
    label = nextquad()
    
    while state == 'whentk':
        word, state = lex()
        if state != '(tk':
            print(str(line)+": ( not found after when")
            exit(0)

        word, state = lex()
        true, false = condition()

        if state != ')tk':
            print(str(line)+": ) not found after condition")
            exit(0)

        word, state = lex()
        if state != ':tk':
            print(str(line)+": : not found after )")
            exit(0)
        word, state = lex()
        backpatch(true, nextquad())
        statements()
        genquad("jump", "_", "_", label)
        backpatch(false, nextquad())

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
    label = nextquad()
    flag = newtemp()
    genquad(":=", 0, "_", flag)
    
    while state == 'whentk':
        word, state = lex()
        if state != '(tk':
            print(str(line)+": ( not found after when")
            exit(0)

        word, state = lex()
        true, false = condition()

        if state != ')tk':
            print(str(line)+": ) not found after condition")
            exit(0)

        word, state = lex()
        if state != ':tk':
            print(str(line)+": : not found after )")
            exit(0)
        word, state = lex()
        
        backpatch(true, nextquad())
        genquad(":=", 1, "_", flag)
        
        statements()
        
        backpatch(false, nextquad())
    genquad("=", 1, flag, label)
    
def return_stat():
    global state, word
    
    eplace = expression()
    genquad("retv", eplace, "_", "_")

def call_stat():
    global state, word

    callName = word
    if state != 'idtk':
        print(str(line)+": procedure name not found after call")
        exit(0)

    word, state = lex()
    actualpars()
    
    genquad("call", callName, "_", "_")


def print_stat():
    global state, word

    if state != '(tk':
        print(str(line)+": ( not found after print")
        exit(0)

    word, state = lex()
    eplace = expression()
    genquad("out", eplace, "_", "_")
    
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
    
    genquad("inp", word, "_", "_")
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
        eplace = expression()
        genquad("par", eplace, "CV", "_")
    else:
        word, state = lex()
        if state != 'idtk':
            print(str(line)+": parameter name expected")
            exit(0)
        
        genquad("par", word, "REF", "_")
        word, state = lex()

def condition():
    global state, word
    
    bt1true, bt1false = boolterm()
    while state == 'ortk':
        backpatch(bt1false, nextquad())
        
        word, state = lex()
        bt2true, bt2false = boolterm()
        
        bt1true = merge(bt1true, bt2true)
        bt1false = bt2false
    return bt1true, bt1false

def boolterm():
    global state, word
    
    bf1true, bf1false = boolfactor()
    while state == 'andtk':
        
        backpatch(bf1true, nextquad())
        word, state = lex()
        bf2true, bf2false = boolfactor()
        
        bf1true = bf2true
        bf1false = merge(bf1false, bf2false)
        
    return bf1true, bf1false

def boolfactor():
    global state, word
    true = [] 
    false = []
    if state == 'nottk':
        word, state = lex()
        if state != '[tk':
            print(str(line)+": [ not found after not")
            exit(0)
        word, state = lex()
        true, false = condition()
        true, false = false, true
        
        if state != ']tk':
            print(str(line)+": ] not found after condition")
            exit(0)
        word, state = lex()
    elif state == '[tk':
        word, state = lex()
        true, false = condition()
        if state != ']tk':
            print(str(line)+": ] not found after condition")
            exit(0)
        word, state = lex()
    else:
        e1place = expression()
        r = word
        relational_oper()
        e2place = expression()
        
        true = makelist(nextquad())
        genquad(r, e1place, e2place, "_")
        
        false = makelist(nextquad())
        genquad("jump", "_", "_", "_")
    return true, false
        
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
    
    t1place = term()

    while state == '+tk' or state == '-tk':
        state1 = state
        word, state = lex()
        t2place = term()
        
        w = newtemp()
        if state1 == '+tk':
            genquad("+", t1place, t2place, w)
        else:
            genquad("-", t1place, t2place, w)
        t1place = w
        
    return t1place

def term():
    global state, word
    f1place = factor()

    while state == '*tk' or state == '/tk':
        state1 = state
        word, state = lex()
        f2place = factor()
        
        w = newtemp()
        if state1 == '*tk':
            genquad("*", f1place, f2place, w)
        else:
            genquad("/", f1place, f2place, w)
        f1place = w
    
    return f1place

def factor():
    global state, word
    if state != 'constanttk' and state != 'idtk' and state != '(tk':
        print(str(line)+": constant, id or ( not found for expression")
        exit(0)
    if state == 'constanttk':
        place = word
        word, state = lex()
    elif state == '(tk':
        word, state = lex()
        place = expression()
        if state != ')tk':
            print(str(line)+": ) not found after expression")
            exit(0)
        word, state = lex()
    else:
        place = word
        word, state = lex()
        place = idtail(place)
    return place

def idtail(place):
    global state, word
    
    if state == '(tk':
        actualpars()
        ret = newtemp()
        genquad("par", ret, "RET", "_")
        genquad("call", place, "_", "_")
        return ret
    return word


def nextquad():
    global quads
    
    return len(quads)

def newtemp():
    global tempCounter
    
    tempCounter = tempCounter + 1
    return "T_" + str(tempCounter)

def genquad(op, x, y, z):
    global quads
    
    quads = quads + [[nextquad(), op, x, y, z]]

def emptylist():
    return []

def makelist(x):
    return [x]

def merge(list1, list2):
    return list1 + list2

def backpatch(list1, z):
    global quads
    
    for i in range(len(list1)):
        label = list1[i]
        quads[label][4] = z
    
def printQuads():
    global quads
    name = sys.argv[1]
    name = name[0: len(name) - 3] + "int"
   
    outfile = open(name, "w")
    
    for i in range(len(quads)):
        print(quads[i])
        line = str(quads[i][0])
        for j in range(1,5):
            line = line + ", "+ str(quads[i][j])
        line = line + "\n"
        outfile.write(line)
        
    outfile.close()


word, state = lex()
program()
printQuads()
