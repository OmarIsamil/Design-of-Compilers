from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from automata.fa.dfa import DFA

numbers = "0123456789"
operators = "|&"
comparator = "=><!"
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def evenchecker(number):
    if number%2 ==0:
        return True
    else:
        return False

def IdChecker2(word):
    if IdentifierChecker(word):
        return str(word)

def IdentifierChecker(word):

    if len(word) >= 2:
        for i in word:
            if word[0] == "!" + i:
                return True

    if word[0] not in letters:
        return False
    for i in word:
        if((i not in letters) and (i not in numbers)):
            return False
    return True


def operatorchecker(word):
    if len(word) > 2:
        return False
    if word[0] not in operators:
        return False
    return True



def comparatorchecker(word):
    if word[0] not in comparator:
        return False


    if len(word) > 2:
        return False

    # if word[0] == "!":
    #     return True

    if len(word)==1:
        if(word[0]== "<" or ">" or "="):
            return True

    if len(word)==2:
        if word == "<=":
            return True
        elif word == ">=":
            return True
        elif word == "!=":
            return True
        else:
            return False

    return True



def numchecker(word):

    if len(word) >= 2:
        for i in numbers:
            if word == "!" + i:
                return True

    if (word.count(".") > 1):
        return False
    if((word[0]==".") or (word[len(word)-1]==".")):
        return False
    for i in word:
        if((i not in numbers) and i!="."):
            return False

    if len(word) >= 2:
        for i in numbers:
            if word == "!" + i:
                return True
    return True


def expressionchecker(sentence):
    splited_sentence=sentence.split()
    if evenchecker(len(splited_sentence)):
        return "Not accepted"
    for i in range(0, len(splited_sentence), 2):
        if((numchecker(splited_sentence[i])!=True) and (IdentifierChecker(splited_sentence[i])!=True)and (comparatorchecker(splited_sentence[i])!=True)):
            return "Not accepted"
    for i in range(1, len(splited_sentence), 2):
        if(operatorchecker(splited_sentence[i])!=True) and (comparatorchecker(splited_sentence[i])!=True):
            return "Not accepted"
    return "Accepted"

label=Label


def tokenlister(sentence):

    # if expressionchecker(sentence) == "Not accepted":
    #     return "Not a valid expression"
    mylist=[]
    x=0

    splited_sentence = sentence.split()
    for i in splited_sentence:
        if(IdentifierChecker(i)):
            mylist.append("ID")
        elif(numchecker(i)):
            mylist.append("Number")
        elif(operatorchecker(i)):
            if x == 1:
                x-=1
            mylist.append("Operator")
        elif(comparatorchecker(i) and x<1):
            mylist.append("Comparator")
            x+=1
        else:
            mylist.append("Unknown Token")

    return mylist

def tokenlister2(sentence):
    return sentence.split()


main = Tk()
main.title("Design of Compilers")
main.minsize(626, 417)

number1Label = Label(text="Enter a Regular Expression")
number1Label.pack(pady=10)

number1Entry = Entry()
number1Entry.pack(pady=10)

def sen():
    num1=number1Entry.get()
    firstLabel = Label(text=" ".join(expressionchecker(num1)))
    firstLabel.pack(pady=20)

    resultLabel = Label(text=" ".join(tokenlister(num1)))
    resultLabel.pack()
    resultLabel2 = Label(text=" ".join(tokenlister2(num1)))
    resultLabel2.pack()
    dfa = DFA(
        states={'q1', 'q2', 'q3', 'q4', 'Dead'},
        input_symbols={"ID", "Number", "Operator", "Comparator", "Unknown Token"},
        transitions={
            'q1': {"ID": 'q2', "Number": 'q2', "Operator": 'Dead', "Comparator": 'Dead', "Unknown Token": 'Dead'},
            'q2': {"ID": 'Dead', "Number": 'Dead', "Operator": 'Dead', "Comparator": 'q3', "Unknown Token": 'Dead'},
            'q3': {"ID": 'q4', "Number": 'q4', "Operator": 'Dead', "Comparator": 'Dead', "Unknown Token": 'Dead'},
            'q4': {"ID": 'Dead', "Number": 'Dead', "Operator": 'q1', "Comparator": 'Dead', "Unknown Token": 'Dead'},
            # 'q5': { "ID": 'q2', "Number" : 'q2', "Comparator" : 'Dead', "Operator" : 'Dead' }
            # 'q6': {"ID": 'q4', "Number" : 'q4', "Comparator" : 'Dead', "Operator" : 'Dead' }
            'Dead': {"ID": 'Dead', "Number": 'Dead', "Operator": 'Dead', "Comparator": 'Dead', "Unknown Token": 'Dead'},
        },
        initial_state='q1',
        final_states={'q2', 'q4', 'Dead'}
    )
    for i in dfa.read_input_stepwise(tokenlister(number1Entry.get())):
        label=Label(text=i)
        label.pack(pady=(0, 10))


but=Button(text="Enter",command=sen)
but.pack(pady=5)



def openNewWindow():

        newWindow = Toplevel(main)

        newWindow.title("DFA")

        newWindow.geometry("1600x1600")

        Label(newWindow).pack()

        frame = Frame(newWindow, width=1000, height=1000)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5)

        # Create an object of tkinter ImageTk
        img = ImageTk.PhotoImage(Image.open("Assets/DFA.png"))


        # Create a Label Widget to display the text or Image
        label = Label(frame, image=img)
        label.pack()
        newWindow.mainloop()

btn = Button(main, text="Show DFA", command=openNewWindow)
btn.pack(pady=15)

label = Label(main)
label.pack(pady=5)

main.mainloop()







