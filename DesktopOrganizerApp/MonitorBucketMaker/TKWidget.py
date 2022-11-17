from tkinter import *


class BucketWidget(object):
    """ TAKES CONTENTS OF BASE TXT FILE WITHOUT NEWLINE CHARACTERS
    SHOULD NOT MODIFY THE TEXT, JUST RETURN THE BASE STYLE TXT :: [["item1,item2,item3,item4"]]
    """
    def clear(self):
        self.classInp.delete(0, END)
        self.nameInp.delete(0, END)
        self.dueInp.delete(0, END)
        self.noteInp.delete(0, END)

    def add(self):
        task = [param.get() for param in self.params]
        task = ",".join(task)
        self.lines.append(task)
        self.clear()

    def remove(self):
        pass

    # THE TITTLE
    def __init__(self, lines):
        self.lines = lines  # list of str::lines joined by commas
        self.main = Tk()
        self.main.title('Monitor Bucket Editor')
        self.main.geometry('400x600')
        Label(self.main, text="Class:").grid(row=1)
        Label(self.main, text="Assignment (title):").grid(row=2)
        Label(self.main, text="Due Date (d/m):").grid(row=3)
        Label(self.main, text="Note:").grid(row=4)
        Label(self.main, text="Output:").grid(row=5)

        self.classInp = Entry(self.main)
        self.nameInp = Entry(self.main)  # name of assignment
        self.dueInp = Entry(self.main)  # due date
        self.noteInp = Entry(self.main)

        self.params = [self.classInp, self.nameInp, self.dueInp, self.noteInp]
        for i in range(len(self.params)):
            self.params[i].grid(row=i+1, column=1)
        # RESPONSE !!
        self.out = Entry(self.main)
        # THE BUTTONS
        Button(self.main, text='Add', command=self.add).grid(row=0, column=0, sticky=W, )
        Button(self.main, text='Remove', command=self.remove).grid(row=0, column=1, sticky=W)
        Button(self.main, text='Clear', command=self.clear).grid(row=0, column=2, sticky=W)
        # QUIT
        Button(self.main, text='Quit', command=self.main.destroy).grid(row=5, column=2, sticky=W)
        mainloop()


