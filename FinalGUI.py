import tkinter
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from automata.fa.dfa import DFA
from main import *

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

root = Tk()
root.title("Design of Compilers")
root.minsize(800, 600)

header = Label(text="Enter a Regular Expression")
header.pack(pady=10)

userInput = Entry()
userInput.pack()

def openDFA():
  newWindow = Toplevel()
  newWindow.title("DFA")
  img = ImageTk.PhotoImage(Image.open("Assets/DFA.png"))
  label = Label(newWindow, image=img)
  label.pack()
  newWindow.mainloop()

def openParse():
    G = parse(tokenlisterForParsing(userInput.get()))
    # G = parse(tokenlisterForParsing("! x || y"))
    pos = graphviz_layout(G, prog="dot")
    nx.draw_networkx_nodes(G, pos, node_size=0)
    nx.draw_networkx_edges(G, pos, G.edges(), edge_color="black")
    nx.draw_networkx_labels(G, pos)
    plt.show()


def openSyntax():
    G = nx.DiGraph()
    x = toTree(userInput.get())
    DrawSyntaxTree(x, G)
    pos = graphviz_layout(G, prog="dot")
    nx.draw_networkx_nodes(G, pos, node_size=0)
    nx.draw_networkx_edges(G, pos, G.edges(), edge_color="black")
    nx.draw_networkx_labels(G, pos)
    plt.show()



def sen():
    global canvas

    canvas = Canvas(root)

    expResult = Label(canvas, text=" ".join(expressionchecker(userInput.get())))
    expResult.pack(pady=10)

    stringToken = Label(canvas, text=" ".join(tokenlister(userInput.get())))
    stringToken.pack()

    userInputLabel = Label(canvas, text=" ".join(tokenlister2(userInput.get())))
    userInputLabel.pack()

    dfa = DFA(
        states={'q1', 'q2', 'q3', 'q4', 'Dead'},
        input_symbols={"ID", "Number", "Operator", "Comparator", "Unknown Token"},
        transitions={
            'q1': {"ID": 'q2', "Number": 'q2', "Operator": 'Dead', "Comparator": 'Dead', "Unknown Token": 'Dead'},
            'q2': {"ID": 'Dead', "Number": 'Dead', "Operator": 'q3', "Comparator": 'q3', "Unknown Token": 'Dead'},
            'q3': {"ID": 'q4', "Number": 'q4', "Operator": 'Dead', "Comparator": 'Dead', "Unknown Token": 'Dead'},
            'q4': {"ID": 'Dead', "Number": 'Dead', "Operator": 'q1', "Comparator": 'Dead', "Unknown Token": 'Dead'},
            # 'q5': { "ID": 'q2', "Number" : 'q2', "Comparator" : 'Dead', "Operator" : 'Dead' }
            # 'q6': {"ID": 'q4', "Number" : 'q4', "Comparator" : 'Dead', "Operator" : 'Dead' }
            'Dead': {"ID": 'Dead', "Number": 'Dead', "Operator": 'Dead', "Comparator": 'Dead', "Unknown Token": 'Dead'},
        },
        initial_state='q1',
        final_states={'q1', 'q2', 'q4', 'q3', 'Dead'}
    )
    for i in dfa.read_input_stepwise(tokenlister(userInput.get())):
        dfaResult=Label(canvas, text=i)
        dfaResult.pack(pady=10)
    switch()
    canvas.pack()
        
def reset():
  canvas.destroy()


enterBtn = Button(text="Enter",command=sen)
enterBtn.pack(pady=5)

showDFA = Button(root, text="Show DFA", command=openDFA)
showDFA.pack(pady=5)

resetBtn = Button(text="Reset", command=reset)
resetBtn.pack(pady=5)

#Switch

def switch():
    showSyntax["state"]=DISABLED
    showParse["state"]=DISABLED

    if expressionchecker(userInput.get())=="Accepted":
        showSyntax["state"] = NORMAL
        showParse["state"] = NORMAL


button_frame = tkinter.Frame(root)
button_frame.pack()

showParse = Button(button_frame, text="Show Parse Tree", command=openParse)
showParse.grid(row=0, column=0, pady=5)

showSyntax = Button(button_frame, text="Show Syntax Tree", command=openSyntax)
showSyntax.grid(row=0, column=1, pady=5)

switch()

# if __name__=="__main__":
#     G = parse(tokenlisterForParsing("! x || y"))
#     pos = graphviz_layout(G, prog="dot")
#     nx.draw_networkx_nodes(G, pos, node_size=0)
#     nx.draw_networkx_edges(G, pos, G.edges(), edge_color="black")
#     nx.draw_networkx_labels(G, pos)
#     plt.show()

mainloop()


