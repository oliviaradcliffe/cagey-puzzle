# =============================
# Student Names: Olivia Radcliffe
# Group ID: 48
# Date: Feb 13, 2022
# =============================
# CISC 352 - W22
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic -
    A variable ordering heuristic that chooses the next variable
    to be assigned according to the Degree heuristic (DH). ord dh
    returns the variable that is involved in the largest number of
    constraints involving other unassigned variables.'''
    # getting all variables
    vars = csp.get_all_unasgn_vars()
    
    largest = vars[0]
    # setting inital max number of constraints
    max = 0

    # check each variable for the highest degree
    for var in vars:
        
        cons = []
        #look at the constraints that include var
        for c in csp.get_cons_with_var(var):
            #check if the constraint includes other unassigned variables
            
            if c.get_n_unasgn() > 1:
                # adding constraint with unassigned variables to cons
                cons.append(c)
                
        # chech if the variables list of constaints with unassigned variables
        # is larger than the current max
        if len(cons) > max:
            # set the new max
            max = len(cons)
            # set the new varibale with the highest degree
            largest = var
            
    return largest

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic -
    A variable ordering heuristic that chooses the next variable to be
    assigned according to the Minimum- Remaining-Value (MRV) heuristic.
    ord mrv returns the variable with the most constrained current domain
    (i.e., the variable with the fewest legal values remaining).'''
    # get all variables
    vars = csp.get_all_unasgn_vars()
    
    # set inital min number of legal values remaining
    min = 100
    
    # check each variable for the MRV
    for var in vars:
        
        # check if the variable has less remaining values than the current min
        if len(var.cur_domain()) < min:
            # set the new min
            min = len(var.cur_domain())
            # set the new MRV variable
            best = var
            
    return best
