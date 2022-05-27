import matplotlib.pyplot as plt
import networkx as nx
import re

NonTerm = ["exp", "exp'", "term", "term'", "factor", "factor'", "comop", "operand"]
Terminal = ["!", "ID", "||", "&&", "<", ">", "=", "#", "$"]
numbers = "0123456789"
operators = "|&"
comparator = "=><!"
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

ParsingTable ={
    ("Exp", '!'): "Term ExpD",
    ("Exp", 'ID'): "Term ExpD",
    ("ExpD", '||'): "|| Term ExpD",
    ("ExpD", '$'): "#",
    ("Term", "!"): "Factor TermD",
    ("Term", "ID"): "Factor TermD",
    ("TermD", "||"): "#",
    ("TermD", "&&"): "&& Factor TermD",
    ("TermD", "$"): "#",
    ("Factor", "ID"): "Operand FactorD",
    ("Factor", "!"): "Operand FactorD",
    ("FactorD", "||"): "#",
    ("FactorD", "&&"): "#",
    ("FactorD", "<"): "Comparator Operand FactorD",
    ("FactorD", ">"): "Comparator Operand FactorD",
    ("FactorD", "="): "Comparator Operand FactorD",
    ("FactorD", "$"): "#",
    ("Comparator", "<"): "<",
    ("Comparator", ">"): ">",
    ("Comparator", "="): "=",
    ("Operand", "!"): "! Operand",
    ("Operand", "ID"): "ID"
}


def evenchecker(number):
    if number%2 ==0:
        return True
    else:
        return False

def IdentifierChecker(word):
    if word[0] == "!":
        if len(word) < 2:
            return False 
        if word[1] in numbers:
            return False
        for i in range(1, len(word)):
            if word[i] not in letters and word[i] not in numbers:
                return False

    if word[0] == "!":
        for i in range(1, len(word)):
            if((word[i] not in letters) and (word[i] not in numbers)):
                return False

    if word[0] not in letters and word[0] != "!":
        return False

    return True

def numchecker(word):
    if word[0] == "!":
        for i in range(1, len(word)):
            if word[i] not in numbers:
                return False

    if word[0] == "!":
        for i in range(1, len(word)):
            if((word[i] not in numbers)):
                return False

    if word not in numbers and word[0] != "!":
        return False            
    return True

def operatorchecker(word):
    if word[0] not in operators:
        return False

    if len(word) == 2:
        if word == "||" or word == "&&":
            return True

    return False

def comparatorchecker(word):
    if word[0] not in comparator:
        return False

    if len(word) > 2:
        return False

    if len(word) == 2:
        if word == "<=":
            return True
        elif word == ">=":
            return True
        elif word == "!=":
            return True
        elif word == "==":
            return True
        else:
            return False
    return True


def expressionchecker(sentence):
    splited_sentence = sentence.split()
    compCounter = 0

    for i in splited_sentence:
        if(comparatorchecker(i)):
            compCounter += 1

        elif(operatorchecker(i)):
            if compCounter == 1:
                compCounter -= 1

    if evenchecker(len(splited_sentence)):
        return "Not accepted"
    for i in range(0, len(splited_sentence), 2):
        if((numchecker(splited_sentence[i])!=True) and (IdentifierChecker(splited_sentence[i])!=True) and (comparatorchecker(splited_sentence[i])!=True)):
            return "Not accepted"
    for i in range(1, len(splited_sentence), 2):
        if(operatorchecker(splited_sentence[i]) != True) and (comparatorchecker(splited_sentence[i]) != True):
            return "Not accepted"
    if compCounter > 1:
        return "Not accepted"
    return "Accepted"

def tokenlister(sentence):
    mylist = []
    compCounter = 0

    splited_sentence = sentence.split()
    for i in splited_sentence:
        if(IdentifierChecker(i)):
            mylist.append("ID")
        elif(numchecker(i)):
            mylist.append("Number")
        elif(comparatorchecker(i) and compCounter < 1):
            mylist.append("Comparator")
            compCounter += 1
        elif(operatorchecker(i)):
            if compCounter == 1:
                compCounter -= 1
            mylist.append("Operator")
        else:
            mylist.append("Unknown Token")

    return mylist

def tokenlister2(sentence):
    return sentence.split()


##########################################################
######################## Parsing #########################
##########################################################

def tokenlisterForParsing(sentence):
    mylist = []
    x = 0
    j =0
    splited_sentence = sentence.split(" ")
    for i in splited_sentence:
        if (IdentifierChecker(i)):
            mylist.append((splited_sentence[j], "ID"))
            j+=1
        elif (numchecker(i)):
            mylist.append((splited_sentence[j], "Number"))
            j+=1

        elif (operatorchecker(i)):
            if x == 1:
                x -= 1
            mylist.append((splited_sentence[j], "Operator"))
            j+=1

        elif (comparatorchecker(i) and x < 1):
            mylist.append((splited_sentence[j], "Comparator"))
            x += 1
            j+=1

        else:
            mylist.append("Unknown Token")
    return mylist

def parse(tokens):
    stack = []
    stack.append(("$", None))
    tokens.append(["$", "Terminate"])
    stack.append(("Exp", None))
    flag = 0
    g = nx.DiGraph()
    i = 0
    while len(stack) > 0:
        top, parent = stack[len(stack) - 1]
        myName = str(i) + " " + top
        if top != '$':
            g.add_node(str(i) + " " + top)
        if parent is not None:
            g.add_edge(parent, str(i) + " " + top)
        i += 1
        In = tokens[0]
        if top == In[0] or top == In[1]:
            tokens.pop(0)
            stack.pop(-1)
        elif (top, In[0]) in ParsingTable:
            print(top + " => " + ParsingTable[(top, In[0])])
            val = ParsingTable[(top, In[0])]
            if val != '#':
                val = val.split()
                val.reverse()
                stack.pop()
                for element in val:
                    stack.append((element, myName))
            else:
                stack.pop()

        elif (top, In[1]) in ParsingTable:
            print(top + " => " + ParsingTable[(top, In[1])])
            val = ParsingTable[(top,In[1])]
            if val != '#':
                val = val.split()
                val.reverse()
                stack.pop()
                for element in val:
                    stack.append((element, myName))
            else:
                stack.pop()
        else:
            flag = 1
            break

    if flag == 0:
        print("String accepted!")
    else:
        print("String not accepted!")
    return g


##########################################################
######################## Syntax #########################
##########################################################


# def toTree(infixStr):
#     # divide string into tokens, and reverse so I can get them in order with pop()
#     # tokens = re.split(r' *([\|\>=\<\=\&/]) *', infixStr)
#     tokens = re.split(r"\s+", infixStr)
#     tokens = [t for t in reversed(tokens) if t != '']
#     # print(tokens)
#     precs = {'||':0 , '&&':1, '>':2, '<':2, '=':2, "!":3}
#
#     #convert infix expression tokens to a tree, processing only
#     #operators above a given precedence
#
#     def toTree2(tokens, minprec):
#         node = tokens.pop()
#         while len(tokens)>0:
#             prec = precs[tokens[-1]]
#             print(tokens[-1])
#
#             if prec<minprec:
#                 break
#             op=tokens.pop()
#
#             # get the argument on the operator's right
#             # this will go to the end, or stop at an operator
#             # with precedence <= prec
#             arg2 = toTree2(tokens,prec+1)
#             node = (op, node, arg2)
#         return node
#
#     return toTree2(tokens,0)


def toTree(infixStr):
    tokens = re.split(r"\s+", infixStr)
    tokens = [t for t in reversed(tokens) if t != '']
    precs = {'||': 0, '&&': 1, '>': 2,">=":2,"<=": 2, '<': 2, '=': 2, "!": 3}
    def toTree2(tokens, minprec):
        node = tokens.pop()
        while len(tokens) > 0:
            prec = precs[tokens[-1]]
            # print(tokens[-1])
            if prec < minprec:
                break
            op = tokens.pop()
            arg2 = toTree2(tokens, prec + 1)
            node = (op, node, arg2)
        return node

    return toTree2(tokens, 0)

nodeCount = 0
def DrawSyntaxTree(tokenList, g):
    global nodeCount
    # nodeCount=0
    print(tokenList)
    tokenList = list(tokenList)
    isBaseCase = True
    for element in tokenList:
        if isinstance(element, tuple):
            isBaseCase = False
    if isBaseCase:
        g.add_node(str(nodeCount) + "." + tokenList[0])
        g.add_node(str(nodeCount+1) + "." +tokenList[1])
        g.add_node(str(nodeCount+2) + "." +tokenList[2])
        g.add_edge(str(nodeCount) + "." + tokenList[0], str(nodeCount+1) + "." +tokenList[1])
        g.add_edge(str(nodeCount) + "." + tokenList[0], str(nodeCount+2) + "." +tokenList[2])
        nodeCount += 3
        return str(nodeCount - 3) + "." + tokenList[0]
    else:
        for i in range(len(tokenList)):
            element = tokenList[i]
            if isinstance(element, tuple):
                tokenList[i] = DrawSyntaxTree(element, g)
        g.add_node(str(nodeCount) + "." + tokenList[0])
        g.add_node(tokenList[1])
        g.add_node(tokenList[2])
        g.add_edge(str(nodeCount) + "." + tokenList[0], tokenList[1])
        g.add_edge(str(nodeCount) + "." + tokenList[0], tokenList[2])
        nodeCount += 1
        print(tokenList)
        return str(nodeCount- 1) + "." + tokenList[0]

