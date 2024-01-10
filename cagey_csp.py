# =============================
# Student Names: Olivia Radcliffe
# Group ID: 48
# Date: Feb 13, 2022
# =============================
# CISC 352 - W22
# cagey_csp.py
# desc:
#

from cspbase import *
from cagey_csp import *
from propagators import *
from heuristics import *

import itertools

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Cagey puzzle.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows:
+---+---+---+---+
|1,1|1,2|...|1,n|
+---+---+---+---+
|2,1|2,2|...|2,n|
+---+---+---+---+
|...|...|...|...|
+---+---+---+---+
|n,1|n,2|...|n,n|
+---+---+---+---+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''
def row_col_ne(dom, n):
    '''takes a domain of a row/col and generates all satisfying tuples
    where the cells are not equal'''
    return [t for t in itertools.permutations(dom,n)]

def eq_add(vals, eq):
    '''checks if the values given(vals) add to the equal var eq.
    Returns True if it does, False otherwise'''
    # set the inital sum
    sum = 0
    # add every value given in vals
    for v in vals:
        sum += v
        
    return (sum == eq)


def eq_multiply(vals, eq):
    '''checks if the values given multiply to equal the var eq.
    ReturnsTtrue if it does, False otherwise'''
    # set the inital product
    prod = 1
    
    # multiply every value given in vals
    for v in vals:
        prod *= v
        
    return (prod == eq)

def eq_subtract(vals, eq):
    '''checks if the values given (vals) can be subtracted in any
    order to equal the variable eq. Returns True if possible,
    False otherwise'''
    # go through the possible permutations of the values
    for values in itertools.permutations(vals):
        
        # set the first value to be subtracted from
        sub = values[0]
        
        # subtract the rest of the valuues
        for i in range(1, len(values)):
            sub -= values[i]
            
        # check if its equal to the given eq
        if(sub == eq):
            return True
        
    return False

def eq_divide(vals, eq):
    '''checks if the values given (vals) can be divided in any
    order to equal the var eq'''
    # go through the possible permutations of the values
    for values in itertools.permutations(vals):
        
        # set the first value to be the numerator 
        quo = values[0]
        
        # divide the rest of the values
        for i in range(1, len(values)):
            quo //= values[i]
            
        # check if its equal to the given eq
        if(quo == eq):
            return True
        
    return False

def binary_ne_grid(cagey_grid):
    '''A model of a Cagey grid (without cage constraints) built
    using only binary not-equal constraints for both the row and
    column constraints. Grids range in size from 3 × 3 to 9 × 9'''
    # save the grid size
    n = cagey_grid[0][0]
    
    # set the initial row/col index
    r = 0
    
    # set the initial domain
    dom = []

    # add numbers 1-n to the domain
    for r in range(cagey_grid[0][0]):
        dom.append(r+1)

    # create grid of cell variables
    grid = []
    for r in dom:
        rows = []
        for c in dom:
            rows.append(Variable('V{}{}'.format(r, c), dom))
        grid.append(rows)

    # set binary row and col constraints
    cons = []
    
    for r in range(len(grid)-1):
        
        # generate every pair in the row
        var_tuples = itertools.combinations(grid[r], 2)

        # generate the possible different pairs from the domain 
        sat_tuples = row_col_ne(dom, 2)

        # adding a constraint for each row varibale pair
        for pair in var_tuples:
            con = Constraint("R({},{})".format(pair[0], pair[1]),[pair[0], pair[1]])
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        # set initial cell    
        cell = 0
        # go through the next row
        for r2 in range(r, len(grid)-1):
            # add a constraint for each column in the rows 
            for cell in range(len(grid[r])):
                con = Constraint("C({},{})".format(grid[r][cell], grid[r2+1][cell]),[grid[r][cell], grid[r2 + 1][cell]])
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
                
    # create csp
    csp = CSP("{}-Cagey-Grid-Binay_ne".format(n))

    # add variables to csp
    for row in grid:
        for row_vars in row:
            csp.add_var(row_vars)

    # add constraints to csp
    for c in cons:
        csp.add_constraint(c)

    # flatten 2D grid to 1D for return   
    flattened_grid = [val for row in grid for val in row]

    return csp, flattened_grid



def nary_ad_grid(cagey_grid):
    '''A model of a Cagey grid (without cage constraints) built using only n-ary all-different
    constraints for both the row and column constraints.'''
    # save the grid size
    n = cagey_grid[0][0]
    
    # set the initial row/col index
    r = 0
    
    # set the initial domain
    dom = []

    #add numbers 1-n to the domain
    for r in range(cagey_grid[0][0]):
        dom.append(r+1)

    # create grid of cell variables
    grid = []
    for r in dom:
        rows = []
        for c in dom:
            rows.append(Variable('V{}{}'.format(r, c), dom))
        grid.append(rows)
            

    # set initial constraint list
    cons = []

    # set n-ary row constraints
    for r in range(len(grid)):
        sat_tuples = row_col_ne(dom, n)
        con = Constraint("R{}".format(r+1),grid[r])
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # set n-ary col constraints
    for c in range(len(grid)):
        
        # set initial col
        col = []
        
        # create column from rows
        for r in range(len(grid)):
            col.append(grid[r][c])

        # add clolumn constraint
        con = Constraint("C{}".format(c+1),col)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)          

    # create csp
    csp = CSP("{}-Cagey-Grid-n-ary".format(n))

    # add variables to csp
    for row in grid:
        for row_vars in row:
            csp.add_var(row_vars)

    # add constraints to csp
    for c in cons:
        csp.add_constraint(c)

    # flatten 2D grid to 1D for return
    flattened_grid = [val for row in grid for val in row]
        
    return csp, flattened_grid


def cagey_csp_model(cagey_grid):
    '''A model built using your choice of (1) binary binary not-equal,
    constraints for the grid, together with (3)
    cage constraints. That is, you will choose one of the previous two grid
    models and expand it to include cage constraints.'''
    # save the grid size
    n = cagey_grid[0][0]
    
    # set the initial row/col index
    r = 0
    
    # set the initial domain
    dom = []

    #adding numbers 1-n to the domain
    for r in range(cagey_grid[0][0]):
        dom.append(r+1)

    #creating grid of cell variables
    grid = []
    for r in dom:
        rows = []
        for c in dom:
            rows.append(Variable('V{}{}'.format(r, c), dom))
        grid.append(rows)
        
    # set initial constraint list
    cons = []

    # create cage constraints
    for cage in cagey_grid[0][1]:
        
        # set initial scope of the cage
        scope = []
        # add varibales to scope
        for var in cage[1]:
            r = var[0] - 1
            c = var[1] - 1 
            scope.append(grid[r][c])
            
        # create constraint on the cage
        con = Constraint("(Cage{})".format(scope),scope)

        # save scope variable domains
        varDoms = []
        for v in scope:
            varDoms.append(v.domain())

        # set initial satisfying value list
        sat_tuples = []

        # deal with 1 varibale cages 
        if len(scope) == 1:
            sat_tuples.append([cage[0]])

        # create sat_tuples depending on equation character    
        for t in itertools.product(*varDoms):
            if cage[-1] == '+':
                if eq_add(t, cage[0]):
                    sat_tuples.append(t)
            elif cage[-1] == '*':
                if eq_multiply(t, cage[0]):
                    sat_tuples.append(t)
            elif cage[-1] == '-':
                if eq_subtract(t, cage[0]):
                    sat_tuples.append(t)
            elif cage[-1] == '/':
                if eq_divide(t, cage[0]):
                    sat_tuples.append(t)
            elif cage[-1] == '?':
                if eq_add(t, cage[0]) or eq_multiply(t, cage[0]) or eq_divide(t, cage[0]) or eq_subtract(t, cage[0]):
                    sat_tuples.append(t)
                   
        # add satisfying tuples to cage constraint            
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
        

    for r in range(len(grid)-1):
        
        # generate every pair in the row
        var_tuples = itertools.combinations(grid[r], 2)

        # generate the possible different pairs from the domain 
        sat_tuples = row_col_ne(dom, 2)

        # adding a constraint for each row varibale pair
        for pair in var_tuples:
            con = Constraint("R({},{})".format(pair[0], pair[1]),[pair[0], pair[1]])
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        # set initial cell    
        cell = 0
        # go through the next row
        for r2 in range(r, len(grid)-1):
            # add a constraint for each column in the rows 
            for cell in range(len(grid[r])):
                con = Constraint("C({},{})".format(grid[r][cell], grid[r2+1][cell]),[grid[r][cell], grid[r2 + 1][cell]])
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    # create csp
    csp = CSP("{}-Cagey-CSP-model".format(n))

    # add variables to csp
    for row in grid:
        for row_vars in row:
            csp.add_var(row_vars)

    # add constraints to csp
    for c in cons:
        csp.add_constraint(c)

    # flatten 2D grid to 1D for return
    flattened_grid = [val for row in grid for val in row]
        
    return csp, flattened_grid

