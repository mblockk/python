#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MyCupboard

@author: michaelblock
"""

from tkinter import *
import string
import re
import os

class kit_item:

    def __init__(self, quantity, quantype, name):
        self.name = name
        self.quantity = quantity
        self.quantype = quantype


    def __str__(self):
        return 'item: {}, quantity: {} {}'.format(\
                self.name, self.quantity, self.quantype)

    def __repr__(self):
        return self.__str__()
        
    def add(self, amt):
        self.quantity += amt
        return self.quantity
        
    def use(self, amt):
        self.quantity -= amt
        return self.quantity


    
class myCupboard: 
    def __init__(self, items):
        self.cupboard = {}
        self.oddtypes = ['box', 'pack', 'can', 'jar', 'packet', 'shaker', 'jug',\
                         'bottle', 'case', 'cloves', 'stick', 'slice', 'slices',\
                         '', ' ', 'n\a', 'n/a', 'tbsp', 'teaspoons', 'tablespoons',\
                         'tbsps', 'tablespoon', 'teaspoon', 'spoon', 'dollop', 'ladle',\
                         'pinch', 'tsp', 'tsps', 'dash', 'package']
        self.rdb = recipedb(self.oddtypes)
        self.idb = instructiondb()
        self.cupboardFile = open("./runfiles/cupboard.txt", "a+")
        self.cupboardFile.seek(0)
        self.similartypes = getSimilarTypes()

        for line in self.cupboardFile:
                self.addInitial(line)
        
    def addInitial(self, item):
        i = item.lower().replace(',', ' ')
        theitem = i.split()
        name = theitem[-1]
        if len(theitem) < 2:
            name = stripPlural(name)
            quantity = 'n/a'
            quantype = ''
        elif len(theitem) ==2:
            quantity = theitem[0]
            name = theitem[1]
            quantype = ''
        else:
            quan, t, name = theitem
            name = stripPlural(name)
            quantity, quantype = convert(quan, t, self.oddtypes)
        new_item = kit_item(quantity, quantype, name)        
        self.cupboard[new_item.name] = new_item        
    
    def addItem(self, item):
        noQuantity = False
        if not item:
            return "please enter an item"
    
        theitem = item.lower().split()
        name = theitem[-1]
        if len(theitem) > 3:
            return "invalid entry"
        if len(theitem) == 2:
            try:
                itemname = float(theitem[0])
            except ValueError:
                print("Not a float")
            if type(itemname) == float:
                
                name = stripPlural(name)
                quantity = theitem[0]
                quantype = ' '
        elif len(theitem) == 1:               
                name = stripPlural(name)
                quantity = 'n/a'
                quantype = ''
                noQuantity = True
        else:
            quan, t, name = theitem
            name = stripPlural(name)
            quantity, quantype = convert(quan, t, self.oddtypes)        
        new_item = kit_item(quantity, quantype, name)
        self.cupboardFile.write("{}, {} {}\n".format(quantity, quantype, name))
        self.cupboardFile.flush()
        os.fsync(self.cupboardFile.fileno())        
        self.cupboard[new_item.name] = new_item
        if noQuantity:
            return "added: [{}] without quantity".format(name)
        else:
            return "added: [{}]".format(item) 
        
            
    def canMake(self):
        canmake = {}
        cupboard = self.cupboard
        rbd = self.rdb
        idb = self.idb
        ingredients = []
        swappeditems = {}
        
        for k,v in self.rdb.items():
            swappeditems[k] = {}
            
            canMake = True
            trySwap = True
            for i in v:
                replacements = []
                swapoptions = []
                if canMake == False:
                    continue
                recipe = k
                recipelist = v
                rq, rt, recname = i                        
                recquan, rectype = convert(rq, rt, thekit.oddtypes)
                recitem = kit_item(recquan, rectype, recname)
                
                for p, j in self.similartypes.items():
                    if i[-1] in j:
                        swapoptions = j
                        
                for option in swapoptions:
                    if option in cupboard.keys():
                        replacements.append(option)
                
                if i[-1] in cupboard.keys():
                    recipe = k
                    recipelist = v
                    rq, rt, recname = i                        
                    recquan, rectype = convert(rq, rt, thekit.oddtypes)
                    recitem = kit_item(recquan, rectype, recname)
                    ingredient = self.cupboard.get(recname)
                    quantype = ingredient.quantype                   
                    quantity = ingredient.quantity
                    if quantype == recitem.quantype and quantity >= recitem.quantity:
                        canMake = True
                    elif (a in self.oddtypes for a in [quantity, quantype, recquan, rectype]):
                        canMake = True
                    else:
                        canMake = False
                        break
                                        
                elif replacements:
                    trySwap = True
                    for r in replacements:
                        ingredient = self.cupboard.get(r)
                        quantype = ingredient.quantype                   
                        quantity = ingredient.quantity
                        if quantype == recitem.quantype and quantity >= recitem.quantity:                            
                            canMake = True
                        elif (a in self.oddtypes for a in [quantity, quantype, recquan, rectype]):                            
                            canMake = True
                        else:
                            replacements.remove(r)                    
                            
                    if replacements:
                        swappeditems[k][i[-1]] = replacements
                        canMake = True
                        
                    else:
                        canMake = False
                        
                
                elif not i[-1] in cupboard.keys() and not replacements:
                    canMake = False
                                                   
            if canMake == True:
                canmake[recipe] = [recipelist, idb.get(recipe), swappeditems]
            
        return canmake
    
    def deleteitem(self, item):
        toDelete = item
        dlist = toDelete.split()
        ditem = dlist[1]
        item = re.sub(r'([^\s\w\/-]|_)+', '', ditem)
        if item in self.cupboard:
            del self.cupboard[item]
            self.cupboardFile.seek(0)
            cbcopy = self.cupboardFile.readlines()
            os.remove('./runfiles/cupboard.txt')
            self.cupboardFile = open("./runfiles/cupboard.txt", "a+")
            for line in cbcopy:
                arr = line.split()
                if item not in arr:
                    self.cupboardFile.write(line)
                
    
def convert(quantity, quantype, oddtypes):
    if quantype in oddtypes or quantity in oddtypes:
        return(quantity, quantype)
        
    else:
        qt = "ounces"
        quantity = float(quantity)
        if quantype == "oz" or quantype == "ozs":
            q = quantity*1        
        elif quantype == "lb" or quantype == "lbs":
            q = quantity*16
        elif quantype == "pound" or quantype == "pounds":
            q = quantity*16 
        elif quantype == "cup" or quantype == "cups":
            q = quantity*8
        elif quantype == "pint" or quantype == "pints":
            q = quantity*16
        elif quantype == "quart" or quantype == "quarts":
            q = quantity*32
        elif quantype == "liter" or quantype == "liters":
            q = quantity * 33.8
        elif quantype == "gallon" or quantype == "gallons":
            q = quantity * 128          
        else:
            q = quantity
            qt = quantype
        
        return (q, qt)
             
def pretty(d, indent=0):
    for key, value in d.items():
        for v in value.items():
            print(v)
            
def stripPlural(name):
    if name[-1] == 's':
        name = name[:-1]
        return name
    else:
        return name
            
def findRecipes(kit):
    return kit.canMake()
            
def recipedb(oddtypes): 
    recipes = {}
    recipename = 0
    with open('./runfiles/recipes.txt', 'r') as recipe_data:
        for line in recipe_data.readlines():
            l = line.strip('\n').rstrip()
            line = l.lower()
            if line.startswith('*'):
                if not recipename == 0:
                    recipes[recipename] = ingredients
                
                name = re.sub(r'([^\s\w\/]|_)+', '', line)
                recipename = name
                ingredients = []
            else:
                step = re.sub(r'([^\s\w\/-[.]]|_)+', '', line)
                items = step.split()
                if len(items) == 3:
                    ingredient = items[-1]
                    ingredient = stripPlural(ingredient)
                    quantity, quantype = convert(items[0], items[1], oddtypes)
                    ingredients.append([quantity, quantype, ingredient])
                elif len(items) == 2:
                    ingredient = items[-1]
                    ingredient = stripPlural(ingredient)
                    quantity = items[1]
                    if type(quantity) == str:
                        quantype = 'n/a'                       
                    else:
                        quantity = 'n/a'
                        quantype = 'n/a'
                        
                    ingredients.append([quantity, quantype, ingredient])
                elif len(items) == 1:                
                    ingredient = items[0]
                    ingredient = stripPlural(ingredient)
                    quantity = 'n/a'
                    quantype = 'n/a'
                    ingredients.append([quantity, quantype, ingredient])
                else:
                    break
                
    recipe_data.close()
    return recipes
    
def instructiondb():
    instructions = {}
    with open('./runfiles/recipeinstructions.txt', 'r') as instruction_data:
        for line in instruction_data.readlines():
            l = line.strip('\n').rstrip()
            line = l.lower()
            if line.startswith('*'):
                name = re.sub(r'([^\s\w\/]|_)+', '', line)
                recipename = name
                steps = []
            else:
                instruction = re.sub(r'([^\s\w+[.]\/\|_)+', '', line)
                steps.append(instruction)

            instructions[recipename] = steps
              
    instruction_data.close()              
    return instructions
        
def getSimilarTypes():
    similartypes = {}
    with open('./runfiles/similartypes.txt', 'r') as similarfile:
        for line in similarfile.readlines():
            l = line.strip('\n').rstrip()
            line = l.lower()
            if line.startswith('*'):
                name = re.sub(r'([^\s\w\/]|_)+', '', line)
                types = []
            else:
                t = re.sub(r'([^\s\w+[.]\/\|_)+', '', line)
                types.append(t)    
            similartypes[name] = types
    
    similarfile.close()
    return similartypes
                       

class GUI():
    def __init__(self, window, thekit):
        self.master = window
        rows = 0
        self.allitems = 0
        while rows < 50:
            self.master.rowconfigure(rows, weight=1)
            self.master.columnconfigure(rows,weight=1)
            rows += 1
        self.thekit = thekit
        self.master.title("My Cupboard")
        w = 620
        h = 800
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        wd = (screenwidth/2) - (w/2)
        ht = (screenheight/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, wd, ht))       
        self.x = wd
        self.y = ht        

        lbl = Label(window, text="Welcome to MyCupboard", font= 'Helvetica 18 bold')
        lbl.grid(column=1, row=0)
        self.welcomemsg = "Find recipes to cook with food you already have! \n"
        self.padspace = "   "
        welcome = Label(window, text = self.welcomemsg)
        welcome.grid(column=1, row = 1)
        pad = Label(window, text = self.padspace)
        pad.grid(column=0, row = 10)

        self.addbar = Entry(self.master, width=40, borderwidth=0.5)
        self.addbar.grid(column=1, row=4)
        
        self.scroller1 = Scrollbar(self.master)
        self.cbquery = Listbox(self.master, yscrollcommand=self.scroller1.set, width = 40)
        self.scroller1.config(command=self.cbquery.yview)
        self.scroller2 = Scrollbar(self.master)
        self.recquery = Listbox(self.master, yscrollcommand=self.scroller2.set, height = 22, width = 40)
        self.scroller1.config(command=self.recquery.yview)

        def popcb():
            if self.thekit.cupboard.values():
                for key, value in self.thekit.cupboard.items():
                    self.cbquery.insert(END, value)                
            else:                
                self.cbquery.insert(END, "Nothing in here. Add something!")
                
            self.allitems = self.cbquery.get(0, 'end')

        def poprec():
                
            rec = findRecipes(self.thekit)
            idx = 1
            stepnum = 1
            if rec:
                self.recquery.insert(END, "You can make: \n")
                for key, value in rec.items():
                    swap = False
                    ingredients = []
                    
                    item = str(key)
                    i = value[0]
                    for x in i:
                        ing = []
                        for k in x:
                            if not k == '' and not k == ' ' and not k == 'n/a' and not k == 'n\a':
                                ing.append(k)
                        ingredients.append((ing))
                    
                    steps = value[1]
                    s = value[2]
                    swapcheck = s.get(item)

                    if swapcheck:
                        swap = True
                    if swap:
                        self.recquery.insert(END, "({}): {} ** ".format(idx, item))
                    else:
                        self.recquery.insert(END, "({}): {}".format(idx, item))
                    self.recquery.insert(END, " ")
                    self.recquery.insert(END, "   Ingredients needed: ")
                    for i in range(0, len(ingredients)):
                        self.recquery.insert(END, "   {}".format(ingredients[i]))
                    if swap:
                        self.recquery.insert(END, " ")
                        self.recquery.insert(END, "** some items missing")
                        self.recquery.insert(END, "possible replacements shown below:")
                        self.recquery.insert(END, " ")
                        for k,v in swapcheck.items():
                            if not k == "":
                                self.recquery.insert(END, "replace {} with {}".format(k, v))
                                                        
                    self.recquery.insert(END, " ")
                    self.recquery.insert(END, "   Steps: ")
                    for i in range(0, len(steps)):
                        self.recquery.insert(END, "   {}.  {}".format(stepnum, steps[i]))
                        stepnum += 1
                    self.recquery.insert(END, "-----------------------".format(value))
                    idx += 1
                    stepnum = 1
            else:
                self.recquery.insert(END, "No recipes yet.\n ")
                self.recquery.insert(END, "Try adding something to your cupboard...")
            
            self.numrecipes = idx-1
            
        def remove():
            selections = self.cbquery.curselection()
            if selections:
                self.addconfirm.delete('0', 'end')
                self.addconfirm.insert(END, "deleted {}".format(self.allitems[selections[0]]))
                thekit.deleteitem(self.allitems[selections[0]])
            else:
                self.addconfirm.delete('0', 'end')
                self.addconfirm.insert(END, "select an item to delete")
            
        def helpPopUp():
            helpwindow = Tk()
            helpwindow.config(background = "gray")
            helpwindow.geometry("+%d+%d" % (self.x+650,
                          self.y+20))
            #helpwindow.geometry('350x620')
            helpwindow.wm_title("How to use MyCupboard:")
            with open('./runfiles/helpmsg.txt', "r") as helpfile:
                msg = helpfile.read()
            helpfile.close()
            helpmsg = Label(helpwindow, text=msg, background = "white smoke")
            helpmsg.grid(column=0, row = 0)
            okay = Button(helpwindow, text= "Okay", command = helpwindow.destroy)
            okay.grid(column=0, row = 2)
            helpwindow.mainloop()
            
        
        self.addconfirm = Listbox(self.master, width = 40, height=1, background = "white smoke")
        self.addbutton = Button(self.master, text=" Add to MyCupboard ", command= lambda:\
                                [self.cbquery.delete('0', 'end'), self.addconfirm.delete('0', 'end'),\
                                 self.addconfirm.insert(END, thekit.addItem(self.addbar.get())),\
                                 self.addbar.delete('0','end'), popcb()])
        self.viewbutton = Button(self.master, text = " View MyCupboard ", command = lambda: \
                                 [self.cbquery.delete('0', 'end'), popcb(), self.addconfirm.delete('0','end')])
        self.searchbutton = Button(self.master, text=" Search for recipes ", command = lambda: \
                                   [self.recquery.delete('0', 'end'), poprec(), self.addconfirm.delete('0','end'),\
                                   self.addconfirm.insert(END, "found: {} recipe(s) for you".format(self.numrecipes))])
        self.clearview = Button(self.master, text=" Clear \n window ", command = lambda: \
                                [self.cbquery.delete('0', 'end'), self.addconfirm.delete('0','end')])
        self.clearrec = Button(self.master, text=" Clear \n window ", command = lambda: 
                               [self.recquery.delete('0', 'end'), self.addconfirm.delete('0','end')])
        self.deleteitem = Button(self.master, text = " Delete item ", command = lambda: 
                                 [remove(), self.cbquery.delete(self.cbquery.curselection()),\
                                 self.recquery.delete('0', 'end')])
        self.deletecupboard = Button(self.master, text = " Empty Cupboard ", command = lambda:\
                                     [thekit.cupboardFile.truncate(0), thekit.cupboard.clear(),\
                                      self.addbar.delete('0','end'), self.addconfirm.delete('0','end'),\
                                      self.cbquery.delete('0', 'end'), self.recquery.delete('0', 'end')])
        
        self.quit = Button(self.master, text = " Quit ", command = lambda: [exit(0), self.master.destroy()])
        self.helpbutton = Button(self.master, text = " Help ", command = lambda: helpPopUp())
        self.helpbutton.config(height = 2, width =6)
        
        self.quit.grid(column = 3, row = 0)
        self.helpbutton.grid(column = 2, row = 1)
        self.addbutton.grid(column=2, row = 4)
        self.viewbutton.grid(column=1, row=8)
        self.clearview.grid(column=3, row=10)
        self.searchbutton.grid(column=2, row=17)
        self.clearrec.grid(column=3, row=17)
        self.deleteitem.grid(column = 2, row = 10)
        self.deletecupboard.grid(column = 1, row = 11)

        self.addconfirm.grid(column=1, row=7)
        self.cbquery.grid(column=1, row=10)
        self.recquery.grid(column=1, row=17) 

        self.addbar.focus()
        self.numrecipes = 0
        popcb()

class main():
        inititem = kit_item('void', 0, 'void')
        global thekit
        thekit = myCupboard(inititem)

        window = Tk()
        items = []
        app = GUI(window, thekit)
        window.mainloop()