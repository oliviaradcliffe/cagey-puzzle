# =============================
# Student Names: Olivia Radcliffe
# Group ID: 48
# Date: Feb 13, 2022
# =============================
# CISC 352 - W22
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

'''
def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    '''A propagator function that propagates according to the
    FC algorithm that check constraints that have exactly one
    uninstantiated variable in their scope, and prune appropriately.
    If newVar is None, forward check all constraints. Otherwise only
    check constraints containing newVar.'''

    # set initial pruned list
    pruned = []

    # check if newVar is given if so, set queue to constraints containing
    # the varibale otherwise, set queue to all constraints 
    if newVar:
        queue = csp.get_cons_with_var(newVar)
    else:
        queue = csp.get_all_cons()

    # go through each constraint in the queue
    for c in queue:
        
        # only check constraints with only one uninstantiated variable
        if c.get_n_unasgn() == 1:
            
            #save the unassigned variable
            un_var = c.get_unasgn_vars()[0]
            
            #save all variables in the constraint
            vars = c.get_scope()
            
            #go through unassigned variables current domain
            for val in un_var.cur_domain():
                
                # create list for scope variables values
                vals = []
            
                # go through variables in scope
                for var in vars:
                    
                    if var.is_assigned():
                        # add the assigned values to vals
                        vals.append(var.get_assigned_value())
                    else:
                        # add the current value in un_vars domain
                        vals.append(val)

                # check if possible value satisfies constraints and not already pruned 
                if (not c.check(vals)) and ((un_var.cur_domain(), val) not in pruned):
                        # remove the value that violates the constraint
                        un_var.prune_value(val)
                        pruned.append((un_var, val))
                    
                # check un_vars current domain, if empty return false as a deadend has been reached
                if len(un_var.cur_domain()) == 0:
                    return False, pruned
                
    return True, pruned
                
'''

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    
    # set initial pruned list
    pruned = []

    # check if variable is given if so, set queue to constraints
    # containing newVar otherwise, set queue to all constraints.
    if newVar:
        queue = csp.get_cons_with_var(newVar)
        
    else:
        queue = csp.get_all_cons()

    
    while len(queue) > 0:
        
        # remove and save constraint from queue
        c = queue.pop()
        
        # go through each variable in constraint scope
        for var in c.get_scope():
            
            # go through varibales current domain
            for val in var.cur_domain():
                
                # check if possible values satisfies constraints
                if (not c.has_support(var, val)) and ((var, val) not in pruned):
                    
                    #remove the value that violates the constraint
                    var.prune_value(val)
                    pruned.append((var, val))
                    
                    #if the variable's current domain is empty, clear queue and
                    #return false as a deadend has been reached
                    if len(var.cur_domain()) == 0:
                        queue.clear()
                        return False, pruned
                    
                    else:
                        #add group of constraints that are involved with the variable to the queue
                        for vcon in csp.get_cons_with_var(var):
                            if vcon not in queue:
                                queue.append(vcon)
                                
    return True, pruned
