import datetime
import random

import sqlalchemy
import sqlalchemy.sql as sql
import sqlalchemy.orm

import tfr_exceptions

# Database info
DB_NAME = 'tfr_db_fields_test'
DB_IP = 'localhost'
DB_PORT = '3306'
DB_USER = 'root'
DB_PASS =''

# The connection string used by the engine to connect to the database
conn_string = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASS, DB_IP, DB_PORT, DB_NAME)

# Create DB engine
engine = sqlalchemy. \
         create_engine(conn_string)

# Create connector to the database

# Create meta that will be used to generate the table objects
meta = sqlalchemy.MetaData()
meta.reflect(bind=engine)


### Generate table objects and appropriate dictionaries
# Programs
tfrregresccc = meta.tables['tfrregresccc']
tfrexpcc     = meta.tables['tfrexpcc']
tfrregrescdd = meta.tables['tfrregrescdd']
tfrrt        = meta.tables['tfrrt']
tfrwt        = meta.tables['tfrwt']
tfrothers    = meta.tables['tfrothers']
tfrsleepers  = meta.tables['tfrsleepers']
tfrt         = meta.tables['tfrt']
tfrupgrade   = meta.tables['tfrupgrade']
tfrupgrade2	 = meta.tables['tfrupgrade2']
tfrupgrade3	 = meta.tables['tfrupgrade3']
tfrupgrade4	 = meta.tables['tfrupgrade4']
tfrccoldies= meta.tables['tfrccoldies']

programs_dict = {'tfrregresccc':tfrregresccc,
                 'tfrexpcc':tfrexpcc,
                 'tfrregrescdd':tfrregrescdd,
                 'tfrrt':tfrrt,
                 'tfrsleepers':tfrsleepers,
                 'tfrothers':tfrothers,
                 'tfrwt':tfrwt,
                 'tfrt':tfrt,
                 'tfrupgrade':tfrupgrade,
				 'tfrupgrade2':tfrupgrade2,
				 'tfrupgrade3':tfrupgrade3,
				 'tfrupgrade4':tfrupgrade4,
				 'tfrccoldies':tfrccoldies}

# Auxiliary tables
tfrcalls     = meta.tables['tfrcalls']
tfrresults   = meta.tables['tfrresults']
tfrprograms  = meta.tables['tfrprograms']
tfroperators = meta.tables['tfroperators']
tfroperatorreport = meta.tables['tfroperatorreport']
tfrcallsreport = meta.tables['tfrcallsreport']

# DEPRECATED
# # Shifts --Not yet used--
# tfrregrescccshift = meta.tables['tfrregrescccshift']
# tfrregrescddshift = meta.tables['tfrregrescddshift']
# tfrexpccshift     = meta.tables['tfrexpccshift']
# tfrrtshift        = meta.tables['tfrrtshift']
# tfrsleepersshift  = meta.tables['tfrsleepersshift']

# Results
tfrothersresults = meta.tables['tfrothersresults']
tfrccresults     = meta.tables['tfrccresults']
tfrddresults     = meta.tables['tfrddresults']
tfrrtresults     = meta.tables['tfrrtresults']
tfrslpresults    = meta.tables['tfrslpresults']
tfrexpresults    = meta.tables['tfrexpresults']
tfrwtresults     = meta.tables['tfrwtresults']
tfrtresults      = meta.tables['tfrtresults']
tfrupgresults    = meta.tables['tfrupgresults']
tfrupg2results   = meta.tables['tfrupg2results']
tfrupg3results   = meta.tables['tfrupg3results']
tfrupg4results   = meta.tables['tfrupg4results']
tfrccoldresults  = meta.tables['tfrccoldresults']

results_dict = {'tfrregresccc':tfrccresults,
                'tfrregrescdd':tfrddresults,
                'tfrrt':tfrrtresults,
                'tfrexpcc':tfrexpresults,
                'tfrsleepers':tfrslpresults,
                'tfrothers':tfrothersresults,
                'tfrwt':tfrwtresults,
                'tfrt':tfrtresults,
                'tfrupgrade':tfrupgresults,
				'tfrupgrade2':tfrupg2results,
				'tfrupgrade3':tfrupg3results,
				'tfrupgrade4':tfrupg4results,
				'tfrccoldies':tfrccoldresults}

# DEPRECATED
# # Scheduled calls
# tfrsleepers_temp_sched  = meta.tables['tfrsleepers_temp_sched']
# tfrrt_temp_sched        = meta.tables['tfrrt_temp_sched']
# tfrexpcc_temp_sched     = meta.tables['tfrexpcc_temp_sched']
# tfrregresccc_temp_sched = meta.tables['tfrregresccc_temp_sched']
# tfrregrescdd_temp_sched = meta.tables['tfrregrescdd_temp_sched']
# tfrothers_temp_sched    = meta.tables['tfrothers_temp_sched']
# tfrwt_temp_sched        = meta.tables['tfrwt_temp_sched']

# DEPRECATED
# scheduled_dict = {'tfrregresccc':tfrregresccc_temp_sched,
#                   'tfrregrescdd':tfrregrescdd_temp_sched,
#                   'tfrrt':tfrrt_temp_sched,
#                   'tfrexpcc':tfrexpcc_temp_sched,
#                   'tfrsleepers':tfrsleepers_temp_sched,
#                   'tfrothers':tfrothers_temp_sched,
#                   'tfrwt':tfrwt_temp_sched}

# DEPRECATED
# shift_calls = {'tfrregresccc':tfrregrescccshift,
#                'tfrregrescdd':tfrregrescddshift,
#                'tfrrt':tfrrtshift,
#                'tfrexpcc':tfrexpccshift,
#                'tfrsleepers':tfrsleepersshift}

tfrscheduledcalls = meta.tables['tfrscheduledcalls']
tfrcontactchanges = meta.tables['tfrcontactchanges']
tfrfinancechanges = meta.tables['tfrfinancechanges']
tfranswers        = meta.tables['tfranswers']

# Interactions
tfrddinteractions     = meta.tables['tfrddinteractions']
tfrccinteractions     = meta.tables['tfrccinteractions']
tfrslpinteractions    = meta.tables['tfrslpinteractions']
tfrrtinteractions     = meta.tables['tfrrtinteractions']
tfrexpinteractions    = meta.tables['tfrexpinteractions']
tfrothersinteractions = meta.tables['tfrothersinteractions']
tfrwtinteractions     = meta.tables['tfrwtinteractions']
tfrtinteractions      = meta.tables['tfrtinteractions']
tfrupginteractions    = meta.tables['tfrupginteractions']
tfrupg2interactions   = meta.tables['tfrupg2interactions']
tfrupg3interactions   = meta.tables['tfrupg3interactions']
tfrupg4interactions   = meta.tables['tfrupg4interactions']
tfrccoldinteractions  = meta.tables['tfrccoldinteractions']

interactions_dict = {'tfrregresccc':tfrccinteractions,
                     'tfrexpcc':tfrexpinteractions,
                     'tfrsleepers':tfrslpinteractions,
                     'tfrregrescdd':tfrddinteractions,
                     'tfrrt':tfrrtinteractions,
                     'tfrothers':tfrothersinteractions,
                     'tfrwt':tfrwtinteractions,
                     'tfrt':tfrtinteractions,
                     'tfrupgrade':tfrupginteractions,
					 'tfrupgrade2':tfrupg2interactions,
					 'tfrupgrade3':tfrupg3interactions,
					 'tfrupgrade4':tfrupg3interactions,
					 'tfrccoldies':tfrccoldinteractions}

def operator_dict():
    """Return operator/password dictionary."""
    conn = engine.connect()
    s = sql.select([tfroperators.c.operator_id, tfroperators.c.password])
    result = conn.execute(s)
    conn.close()
    return {operator_id:password for operator_id, password in result}

def check_if_program_is_dead(program_name):
    """Check if a program is dead."""
    conn = engine.connect()
    program = programs_dict[program_name]
    s = sql.select([program]). \
        where(program.c.has_result=='0')
    proxy = conn.execute(s)
    conn.close()
    if proxy.rowcount==0:
        return True
    else:
        return False

def deactivate_dead_programs():
    """Deactivate any program that is dead."""
    conn = engine.connect()
    s = sql.select([tfrprograms.c.name])
    for row in conn.execute(s):
        if check_if_program_is_dead(row[0]):
            stmt = tfrprograms.update(). \
                   where(tfrprograms.c.name == row[0]). \
                   values(active=0)
            conn.execute(stmt)                        
    conn.close()
        
def active_program_list():
    """Return all active program names as a list."""
    conn = engine.connect()
    deactivate_dead_programs()
    s = sql.select([tfrprograms]). \
        where(tfrprograms.c.active == 1)
    result = conn.execute(s)
    conn.close()
    return [row[tfrprograms.c.name] for row in result]


### ACTIVe PROGRAMS AND OPERATOR/PASSWORD DICTIONARY
active_programs = active_program_list()
op_pass_dict    = operator_dict()

LOOKUP_ID = 'LookupID'

def supporters_proxy(program_name):
    """Return the support proxy."""
    conn = engine.connect()
    program = programs_dict[program_name]
    s = sql.select([program]). \
        where(sql.and_(program.c.has_result=='0', program.c.has_schedule=='0'))
    result = conn.execute(s)
    conn.close()
    return result
    
def create_proxies():
    """Create proxies for every active program.
    
    Proxies are mapped to their corresponding program_name
    via a dictionary.
    """
    proxies = {program_name:supporters_proxy(program_name) \
               for program_name in active_programs}
    return proxies

active_proxies = create_proxies() 


def refresh_proxy(program_name):
    """Refresh the appropriate active proxy."""
    active_proxies[program_name] = supporters_proxy(program_name)
    
###QUERY FOR SHIFT CALLS
# s = sql.select([tfrexpcc]).\
#     select_from(
#     tfrexpcc.outerjoin(tfrexpccshift, tfrexpcc.c.LookupID==tfrexpccshift.c.supporter_id)). \
#     where(tfrexpccshift.c.call_id==None)

## active proxies dictionary
    
def supporter_list(program_name):
    """Return the supporter list."""
    supp_list = []
    proxy = active_proxies[program_name]
    for result in proxy:
        supp_list.append(result.items())
    return supp_list

def create_supporter_lists():
    supp_lists = {program_name:supporter_list(program_name) \
                  for program_name in active_programs}
    return supp_lists

programs_list_dict = create_supporter_lists()

### Temporarily out of order
#def create_supporter_list_length():
#    length_of_lists = {program_name:len(sup_list) \
#                       for program_name, sup_list in programs_list_dict.it#eritems()}
#    return length_of_lists

def create_supporter_list_length():
    proxies = create_proxies()
    length_of_lists = {program_name:proxy.rowcount \
                       for program_name, proxy in proxies.iteritems()}
    return length_of_lists


remaining_supp_dict = create_supporter_list_length()

def remaining_supporters(operator_id):
    """Return the remaining supporters for each active program.
    
    Dictionary form.
    """
    
    return create_supporter_list_length()

def refresh_supporter_list(program_name):
    programs_list_dict[program_name] = supporter_list(program_name)

### Provide supporter
# 
#   Used by the agent to provide
#   the operator with a  supporter to call.

def provide_supporter(operator_id, program_name):
    """Provide operator with a supporter to call.
    
    The supporter to be called is chosen randomly by 
    the appropriate program list. The supporter provided
    is then popped from the list.
    """
    prog_list = programs_list_dict[program_name]
    length = len(prog_list)
    if length > 0:
        rand_range = length - 1
    else:
        rand_range = 0
    index = random.randint(0, rand_range)
    if prog_list:
        return prog_list.pop(index)
    else:
        if check_if_program_is_dead(program_name):
            return '2'
        else:
            refresh_proxy(program_name)
            refresh_supporter_list(program_name)
            return '1'
    
# DEPRECATED
# def provide_supporter(operator_id, program_name):
#     """ Provide supporter to the requesting operator.

#     Program is defined by the choice of the operator.
#     Returns a list containing key-value tuples based on the 
#     database representation of the supporter.
#     """
#     #if check_next_scheduled_call() == True:
#     #    return next_scheduled_call_supporter()
#     #else:
#     proxy =  active_proxies[program_name]
#     return proxy.fetchone().items()
    
#  
### PROVIDE CALLS
# 
#

def get_calls(operator_id, supporter_id, program_name):
    """Get the calls made to given supporter.

    The calls are returned as a list in ascending
    call number.
    """
    conn = engine.connect()
    s = sql.select([tfrcalls.c.call_number, tfrcalls.c.operator_username,
                    tfrcalls.c.call_datetime, tfrcalls.c.comments]). \
        where(sql.and_ \
              (tfrcalls.c.supporter_id==supporter_id, 
               tfrcalls.c.program==program_name)). \
        order_by(tfrcalls.c.call_number)

    result = conn.execute(s)
    conn.close()
    call_list = [row for row in result.fetchall()]
    return call_list


### OPERATOR/LOGIN MANAGEMENT ###
def activate_operator(operator_id):
    """Activate operator in the operators table."""
    conn = engine.connect()
    stmt = tfroperators.update(). \
           where(tfroperators.c.operator_id == operator_id). \
           values(active=1)
    conn.execute(stmt)
    conn.close()
        

def deactivate_operator(operator_id):
    """Activate operator in the operators table."""
    conn = engine.connect()
    stmt = tfroperators.update(). \
           where(tfroperators.c.operator_id == operator_id). \
           values(active=0)
    conn.execute(stmt)
    conn.close()

def get_operator_activity(operator_id):
    """Return the active field of the given operator."""
    conn = engine.connect()
    s = sql.select([tfroperators.c.active]). \
        where(tfroperators.c.operator_id == operator_id)
    result = conn.execute(s)
    conn.close()
    try:
        active = result.fetchone()[0]
        return active
    except TypeError:
        print "This operator_id is invalid"

def check_operator_active(operator_id):
    """Check if given operator is active."""
    if get_operator_activity(operator_id):
        return True
    else:
        return False

def activate_being_called(operator_id, supporter_id, program_name):
    """Activate (switch to 1) the is_being_called entry of a supporter"""
    conn = engine.connect()
    program = programs_dict[program_name]
    stmt = program.update(). \
           where(program.c.LookupID==supporter_id). \
           values(is_being_called="1")
    conn.execute(stmt)
    conn.close()
    
def deactivate_being_called(operator_id, supporter_id, program_name):
    """Deactivate (switch to 0) the is_being_called entry of a supporter"""
    conn = engine.connect()
    program = programs_dict[program_name]
    stmt = program.update(). \
           where(program.c.LookupID==supporter_id). \
           values(is_being_called="0")
    conn.execute(stmt)
    conn.close()


### OPERATOR LOGIN FUNCTION
#
#   This is the function that will be used by the agent to login 
#   an operator.
def operator_login(operator_id, password):
    """Login operator.
    
    Check if operator_id is correct, pass is correct and finally 
    login user(activate and return true.
    """
    # check if user is already logged in
    
    if operator_id in op_pass_dict:
        if (op_pass_dict[operator_id] == password):
            # If operator/password is in op_pass dictionary,
            # activate operator and return true
            activate_operator(operator_id)
            return True
        else:
            # if password is not correct
            raise tfr_exceptions.PasswordLoginError('Password not correct')
    else:
        # if operator_id is incorrect
        raise tfr_exceptions.IDLoginError('Operator_id not correct')

def operator_logout(operator_id):
    """Log out the given user."""
    if check_operator_active(operator_id):
        deactivate_operator(operator_id)
    else:
        raise tfr_exceptions.LoginError('Operator is not logged in.')

### HANDLE CALLS ###

def check_number_of_calls(lookup_id, program):
    """Check how many calls to this supporter have been made."""
    conn = engine.connect()
    # query by lookup_id and program, order by descending order of calls made
    s = sql.select([tfrcalls]). \
        where(sql.and_ \
              (tfrcalls.c.supporter_id == lookup_id,
               tfrcalls.c.program == program)).\
        order_by(tfrcalls.c.call_number.desc())
    
    call = conn.execute(s).fetchone()
    conn.close()
    # if None is returned by the proxy, no entry exists and so
    # no calls have been made
    if call is None:
        return 0
    else:
        # descending order means the first entry is the last call made.
        return call[tfrcalls.c.call_number]

### Add a new call to the tfrcalls table
#   
#   

def get_operator_username(operator_id):
    """Get operator name by operator's id."""
    conn = engine.connect()
    s = sql.select([tfroperators.c.username]). \
        where(tfroperators.c.operator_id==operator_id)
    result = conn.execute(s)
    conn.close()
    name = result.fetchone()
    return name[0]

def add_call(operator_id, lookup_id, program, comment):
    """Submit call.
    
    Increment if the supporter has already been called.
    Number of calls equals one if supporter has not already
    been contacted.

    """
    conn = engine.connect()
    number_of_calls = check_number_of_calls(lookup_id, program)
    if number_of_calls == 0:
        actual_program = programs_dict[program]
        stmt = actual_program.update(). \
               where(actual_program.c.LookupID==lookup_id).\
               values(is_mam="0")
        conn.execute(stmt)

    just_now = datetime.datetime.now()
    operator_username = get_operator_username(operator_id)
    ins = tfrcalls.insert(). \
          values(operator_username=operator_username, call_number=(number_of_calls+1),
                 program=program, call_datetime=just_now, comments=comment,
                 supporter_id=lookup_id)
    conn.execute(ins)
    conn.close()
    
    ### Deprecated after use of new supporter entries
    # shift_program = shift_calls[program]
    # ins = shift_program.insert(). \
    #       values(supporter_id=lookup_id)
    # conn.execute(ins)

### SCHEDULED CALLS
#
#   Handling scheduled calls

### DEPRECATED
# def add_scheduled_call(operator_id, datetime, supporter_id,
#                        comments, program_name):
#     """Add scheduled call."""
#     ins = tfrscheduledcalls.insert(). \
#           values(operator_id=operator_id, program=program_name,
#                  supporter_id=supporter_id, operator_comments = comments,
#                  datetime=datetime)
#     conn.execute(ins)
#     supporter = (cut_supporter_from_program(operator_id, supporter_id,
#                                            program_name))
#     table = scheduled_dict[program_name]
#     ins = table.insert().values(supporter)
#     conn.execute(ins)

### New version, making use of new supporter fields
def add_scheduled_call(operator_id, sch_datetime, supporter_id,
                       comments, program_name):
    """Add scheduled call."""
    conn = engine.connect()
    ins = tfrscheduledcalls.insert(). \
          values(operator_id=operator_id, program=program_name,
                 supporter_id=supporter_id, operator_comments = comments,
                 datetime=sch_datetime)
    conn.execute(ins)
    program = programs_dict[program_name]
    stmt = program.update(). \
           where(program.c.LookupID == supporter_id). \
           values(has_schedule="1")
    conn.execute(stmt)
    formatted_date = sch_datetime.strftime("%d/%m, %H:%M")
    call_comment = 'TA->' + formatted_date + comments
    add_call(operator_id, supporter_id, program_name, call_comment)
    conn.close()
    

def ordered_scheduled_list(operator_id):
    """Get the ordered scheduled calls list."""
    conn = engine.connect()
    s = sql.select([tfrscheduledcalls]). \
        order_by(tfrscheduledcalls.c.datetime)
    result = conn.execute(s)
    conn.close()
    sch_calls = []
    for row in result:
        sch_calls.append(row.items())
    return sch_calls
    
def some_scheduled_calls(number_of_calls):
    """Return the first number_of_calls scheduled calls as a list."""
    ordered = ordered_scheduled_list()
    return ordered[:number_of_calls]    

def first_scheduled_call():
    """Return the next (chronologically ordered) call."""
    return some_scheduled_calls(1)[0]

def get_scheduled_call_by_id(operator_id, call_id):
    """Return the scheduled call corresponding to the call_id."""
    conn = engine.connect()
    s = sql.select([tfrscheduledcalls]). \
        where(tfrscheduledcalls.c.scheduled_id==call_id)
    result = conn.execute(s)
    sch_call = result.fetchone() 
    conn.close()
    if sch_call == None:
        return False
    else:
        return sch_call
    

def get_scheduled_supp_by_id(lookup_id, program):
    conn = engine.connect()
    s = sql.select([program]). \
        where(program.c.LookupID == lookup_id)
    result = conn.execute(s)
    conn.close()
    return result.fetchone().items()

def del_scheduled_call_by_id(operator_id, call_id):
    """Delete the scheduled call corresponding to the call_id."""
    conn = engine.connect()
    s = tfrscheduledcalls.delete(). \
        where(tfrscheduledcalls.c.scheduled_id==call_id)
    conn.execute(s)
    conn.close()

# Deprecated
def fetch_supporter_from_sched(operator_id, supporter_id, program_name):
    """Fetch supporter from scheduled table."""
    conn = engine.connect()
    program = scheduled_dict[program_name]
    s = sql.select([program]). \
        where(program.c.LookupID==supporter_id)
    result = conn.execute(s)
    conn.close()
    return result.fetchone()

# Deprecated
def insert_into_program_table(operator_id, supporter, program_name):
    """Insert into table of program_name the supporter_id."""
    conn = engine.connect()
    program = programs_dict[program_name]
    ins = program.insert().values(supporter)
    conn.execute(ins)
    conn.close()
    
# Deprecated
def move_supporter_from_sched_to_program(operator_id, supporter_id,
                                         program_name):
    """Move supporter from scheduled table to program."""
    conn = engine.connect()
    supporter = tuple(fetch_supporter_from_sched(operator_id, supporter_id, 
                                                 program_name))
    insert_into_program_table(operator_id, supporter, program_name)
    program = scheduled_dict[program_name]
    ins = program.delete(). \
        where (program.c.LookupID==supporter_id)
    conn.execute(ins)
    conn.close()
    
#   GET SCHEDULED SUPPORTER BY CALL ID.
#   Used by tfr_agent, this function provides the supporter that corresponds 
#   to the scheduled call, whose id is given as a function argument.

# def get_scheduled_supporter_by_call_id(operator_id, call_id):
#     """Return the supporter based on the scheduled call's id."""
#     scheduled = get_scheduled_call_by_id(operator_id, call_id)
#     lookup_id = scheduled['supporter_id']
#     program_name = scheduled['program']
#     comment = scheduled['operator_comments']
#     program = scheduled_dict[program_name]
#     supporter = get_scheduled_supp_by_id(lookup_id, program)
#     del_scheduled_call_by_id(operator_id, call_id)
#     move_supporter_from_sched_to_program(operator_id, lookup_id,
#                                          program_name)
#     return supporter, comment, program_name

### Updated version, using the new supporter fields.
def get_scheduled_supporter_by_call_id(operator_id, call_id):
    """Return the supporter based on the scheduled call's id."""
    conn = engine.connect()
    scheduled = get_scheduled_call_by_id(operator_id, call_id)
    if scheduled == False:
        conn.close()
        return "1"
    else:
        lookup_id = scheduled['supporter_id']
        program_name = scheduled['program']
        comment = scheduled['operator_comments']
        program = programs_dict[program_name]
        supporter = get_scheduled_supp_by_id(lookup_id, program)
        stmt = program.update(). \
               where(program.c.LookupID==lookup_id). \
               values(has_schedule="0")
        conn.execute(stmt)
        conn.close()
        del_scheduled_call_by_id(operator_id, call_id)
        return supporter, comment, program_name

def get_supporter_by_id(lookup_id, program_name):
    """Return the supported based on lookup_id."""
    conn = engine.connect()
    try:
        program = programs_dict[program_name]
        s = sql.select([program]). \
            where(program.c.LookupID == lookup_id)
        supporter = conn.execute(s).fetchone()
        conn.close()
        if supporter is None:
            return '2'
        else:
            if supporter['is_being_called']=='0':
                return supporter.items()
            else:
                return '3'
    except KeyError:
        conn.close()
        return '1'
    
def refresh_scheduled_calls():
    """Refresh the schedule calls table.

    All entries that have surpassed the day limit 
    are deleted.
    """
    conn = engine.connect()
    right_now = datetime.datetime.now()
    margin = datetime.timedelta(hours=24)
    s = tfrscheduledcalls.delete(). \
        where(tfrscheduledcalls.c.datetime < right_now - margin)
    conn.execute(s)
    conn.close()

def check_next_scheduled_call():
    """Check if it's time for the next scheduled call.
    
    If the scheduled time of the next scheduled call 
    is 9 minutes prior and up to 2 minutes later from 
    current time the function returns True, otherwise False.
    """
    call = first_scheduled_call()
    scheduled_time = call['datetime'] 
    right_now = datetime.datetime.now()
    margin_lower = datetime.timedelta(minutes=9)
    margin_upper = datetime.timedelta(minutes=2)
    if (scheduled_time < right_now + margin_upper) \
       and (scheduled_time > right_now - margin_lower):
        return True
    else:
        return False

def next_scheduled_call_supporter():
    """Get the supporter that corresponds to the next scheduled call."""
    call = first_scheduled_call()
    lookup_id = call['supporter_id']
    program = call['program']
    return get_supporter_by_id(lookup_id, program)

### CHOOSING PROGRAM
# 
#   This function is used by the agent
#   to allow operators to choose programs 

def choose_program(operator_id, program_name):
    """Choose program."""
    conn = engine.connect()
    if program_name in active_programs:
        stmt = tfroperators.update(). \
               where(tfroperators.c.operator_id == operator_id). \
               values(program=program_name)
        conn.execute(stmt)
        conn.close()
        return True
    else:
        conn.close()
        raise tfr_exceptions.UserInputError('Given program is not active.')
        

def change_program():
    """Change the chosen program."""
    pass

### PROGRAM INTERACTIONS

def program_interactions(program_name):
    """Return a list of the program's possible interactions."""
    conn = engine.connect()
    interactions = interactions_dict[program_name]
    s = sql.select([interactions.c.Subcategory]). \
        order_by(interactions.c.Subcategory)
    result = conn.execute(s)
    conn.close()
    return [inter[0] for inter in result.fetchall()]


### RESULT ENTRY ###
# 
# Result is a tuple that will be passed on as a value in the 
# insert statement to the tfrresults table.
# Several entries are formed in the data space and dont require operator input.
# The rest are given via a tuple by the operator. 

def program_name_by_operator(operator_id):
    """Return the program that the operator has chosen."""
    conn = engine.connect()
    s = sql.select([tfroperators.c.program]). \
        where(tfroperators.c.operator_id==operator_id)
    result = conn.execute(s)
    conn.close()
    return result.fetchone()[0]

def find_constituent_name(lookup_id, program_name):
    """Return the constituent's name based on his lookup_id."""
    # find the correct table/program.
    conn = engine.connect()
    program = programs_dict[program_name]
    s = sql.select([program.c.FirstName, program.c.Surname]). \
        where(program.c.LookupID==lookup_id)
    result = conn.execute(s)
    conn.close()
    name = result.fetchone()
    # form the constituent's fullname and return it
    return name[0] + ' ' + name[1]
    
def create_program_summary(program_name):
    """Create the correct summary.

    Find the actual program's name querying the db.
    """
    conn = engine.connect()
    s = sql.select([tfrprograms.c.actual_name]). \
        where(tfrprograms.c.name==program_name)
    actual_name = conn.execute(s).fetchone()[0]
    conn.close()
    return "TFR Response: " + actual_name
   
def interaction_status():
    """Return the 'Completed' status."""
    return "Completed"

def get_contact_method():
    """Return the proper contact method."""
    return "Outbound Phone Call"

def program_category(program_name):
    """Return the appropriate program category"""
    conn = engine.connect()
    s = sql.select([tfrprograms.c.category]). \
        where(tfrprograms.c.name==program_name)
    result = conn.execute(s)
    conn.close()
    return result.fetchone()[0]

def program_actual_date(program_name):
    """Return the appropriate program actual_date."""
    conn = engine.connect()
    s = sql.select([tfrprograms.c.actual_date]). \
        where(tfrprograms.c.name==program_name)
    result = conn.execute(s)
    conn.close()
    return result.fetchone()[0]

def format_expected_date():
    today = datetime.date.today()
    today_string = str(today.day) + "/" + str(today.month) + \
                   "/" + str(today.year)
    return today_string

def check_lookup_id_exists(lookup_id, program_name):
    """Check if the lookup_id exists in the given program."""
    conn = engine.connect()
    program = programs_dict[program_name]
    s = sql.select([program]). \
        where(program.c.LookupID==lookup_id)
    result = conn.execute(s)
    if result.fetchone() is None:
        scheduled = scheduled_dict[program_name]
        s = sql.select([scheduled]). \
            where(scheduled.c.LookupID==lookup_id)
        result2 = conn.execute(s)
        if result2.fetchone() is None:
            conn.close()
            return False
        else:
            conn.close()
            return True
    else:
        conn.close()
        return True

### FEEDBACK DATA.
#   The feedback of the operator, concerning the interaction,
#   comes in the form of a tuple. The FDB_ constants denounce 
#   in what position we can find the values required. This is 
#   is used by the operator to form his own interaction
#   feedback.


FDB_SUB_CATEGORY = 0
FDB_COMMENT      = 1
FDB_INC_DECR     = 2
FDB_NEW_FREQ     = 3
FDB_ONE_OFF      = 4

def interaction_form(operator_id, supporter_id, program_name, feedback):
    """Create the interaction form
    
    Use the FDB_ constants to obtain the operation feedback.
    Check if the constituent_lookup_id is correct
    If not raise an exception. Otherwise, continue
    to creating the interaction_form.
    
    """
    ### Feedback from the operator.
    constituent_lookup_id = supporter_id

    # Check for lookup_id's existence
    if not check_lookup_id_exists(constituent_lookup_id, program_name):
        raise tfr_exceptions.InteractionLoginError("Wrong Lookup_id")
 
    subcategory      = feedback[FDB_SUB_CATEGORY]
    comment          = feedback[FDB_COMMENT]
    incr_decr_amount = feedback[FDB_INC_DECR]
    new_frequency    = feedback[FDB_NEW_FREQ]
    one_off_donation = feedback[FDB_ONE_OFF]
    
    
    ### Feedback created in data_space.
    constituent_name = find_constituent_name(constituent_lookup_id, 
                                             program_name)
    owner            = operator_id
    summary          = create_program_summary(program_name)
    status           = interaction_status()
    contact_method   = get_contact_method()
    category         = program_category(program_name)
    expected_date    = format_expected_date()
    actual_date      = program_actual_date(program_name)
    number_of_calls  = str(int(check_number_of_calls(constituent_lookup_id, 
                                            program_name)) + 1)
    return (constituent_lookup_id,
            constituent_name,
            summary,
            status,
            contact_method,
            category,
            subcategory,
            expected_date,
            actual_date,
            comment,
            incr_decr_amount,
            new_frequency,
            one_off_donation,
            number_of_calls,
            owner)

### COMMIT INTERACTION
#
#   Used by the agent to commit 
#   an interaction.

def commit_interaction(operator_id, supporter_id, program_name, feedback):
    """Commit interaction."""
    conn = engine.connect()
    program = programs_dict[program_name]
    stmt = program.update(). \
           where(program.c.LookupID==supporter_id). \
           values(has_result="1")
    conn.execute(stmt)
    form = interaction_form(operator_id, supporter_id, program_name, feedback)
    ins = tfrresults.insert().values(form)
    conn.execute(ins)
    conn.close()

### PERSONAL AND ADDRESS INFO
# Positioning of fields in personal_info tuple coming from an operator.

CON_PHONE1  = 0
CON_PHONE2  = 1
CON_PHONE3  = 2
CON_EMAIL   = 3
CON_ADDRESS = 4
CON_CITY    = 5
CON_POSTAL  = 6
CON_NAME    = 7
CON_SURNAME = 8
CON_COMMENT = 9

def personal_changes_form(operator_id, supporter_id, program_name, data):
    """Create the personal changes form
    
    Use the CON_ constants to obtain the operator feedback.
    Check if the constituent_lookup_id is correct
    If not raise an exception. Otherwise, continue
    to creating the personal_changes_form and return it.
    
    """
    
    # USER DEFINED CHANGES
    phone1  = data[CON_PHONE1]
    phone2  = data[CON_PHONE2]
    phone3  = data[CON_PHONE3]
    email   = data[CON_EMAIL]    
    address = data[CON_ADDRESS]
    city    = data[CON_CITY]
    postal  = data[CON_POSTAL]
    name    = data[CON_NAME]
    surname = data[CON_SURNAME]
    comment = data[CON_COMMENT]

    if not check_lookup_id_exists(supporter_id, program_name):
        raise tfr_exceptions.ContactInfoIDError("Wrong Lookup_id")

    # defined in data space
    date_added = datetime.datetime.now()

    return (None,
            operator_id,
            supporter_id,
            program_name,
            date_added,
            phone1,
            phone2,
            phone3,
            email,
            address,
            city,
            postal,
            name,
            surname,
            comment)


def submit_personal_changes(operator_id, supporter_id, program_name, data):
    conn = engine.connect()
    form = personal_changes_form(operator_id, supporter_id,
                                 program_name, data)
    ins = tfrcontactchanges.insert().values(form)
    conn.execute(ins)
    conn.close()
    
### FINANCIAL CHANGES
FNC_AMOUNT    = 0
FNC_FREQUENCY = 1
FNC_CARD_TYPE = 2
FNC_EXPIRE    = 3
FNC_CARD_NUM  = 4
FNC_CARD_CVV  = 5
FNC_BANK      = 6
FNC_IBAN      = 7
FNC_COMMENT   = 8

def finance_changes_form(operator_id, supporter_id, program_name, data):
    amount      = data[FNC_AMOUNT]
    frequency   = data[FNC_FREQUENCY]
    card_type   = data[FNC_CARD_TYPE]
    expire      = data[FNC_EXPIRE]
    card_number = data[FNC_CARD_NUM]
    card_cvv    = data[FNC_CARD_CVV]
    bank        = data[FNC_BANK]
    iban        = data[FNC_IBAN]
    comment     = data[FNC_COMMENT]
    
    # defined in data space
    date_added  = datetime.datetime.now()

    if not check_lookup_id_exists(supporter_id, program_name):
        raise tfr_exceptions.FinancialUpdateIDError("Wrong Lookup_id")
    
    return (None,
            operator_id,
            supporter_id,
            program_name,
            date_added,
            amount,
            frequency,
            card_type,
            expire,
            card_number,
            card_cvv,
            bank,
            iban,
            comment)

def submit_financial_changes(operator_id, supporter_id, program_name, data):
    conn = engine.connect()
    form = finance_changes_form(operator_id, supporter_id, 
                                program_name, data)
    ins = tfrfinancechanges.insert().values(form)
    conn.execute(ins)
    conn.close()

        
### SUBMIT ANSWERS
#
#
ANS_ANSWER  = 0
ANS_COMMENT = 1 

def answer_form(operator_id, supporter_id, program_name, data):
    answer   = data[ANS_ANSWER]
    comments = data[ANS_COMMENT]

    date_added = datetime.datetime.now()

    if not check_lookup_id_exists(supporter_id, program_name):
        raise tfr_exceptions.FinancialUpdateIDError("Wrong Lookup_id")

    return (None,
            supporter_id,
            operator_id,
            program_name,
            date_added,
            answer,
            comments)

def commit_answer(operator_id, supporter_id, program_name, data):
    conn = engine.connect()
    form = answer_form(operator_id, supporter_id,
                       program_name, data)
    ins = tfranswers.insert().values(form)
    conn.execute(ins)
    set_supporter_result(operator_id, supporter_id, program_name, data)
    call_comment = "OK - " + data[ANS_ANSWER] + ' - ' + data[ANS_COMMENT]
    add_call(operator_id, supporter_id, program_name, call_comment)
    conn.close()

def fetch_supporter(operator_id, supporter_id, program_name):
    """Fetch supporter"""
    conn = engine.connect()
    program = programs_dict[program_name]
    s = sql.select([program]). \
        where(program.c.LookupID==supporter_id)
    result = conn.execute(s)
    conn.close()
    return result.fetchone()

def get_supporter_from_program(operator_id, supporter_id, program_name):
    """Remove supporter from the appropriate program and return him."""
    program = programs_dict[program_name]
    supporter = tuple(fetch_supporter(operator_id, supporter_id, program_name))
    return supporter

###


def set_supporter_result(operator_id, supporter_id, program_name, data):
    conn = engine.connect()
    result = data[ANS_ANSWER]
#    comment = data[ANS_COMMENT]
    # Date that the transaction has been recorded
    date_recorded = datetime.date.today()
    supporter = get_supporter_from_program(operator_id, supporter_id, 
                                           program_name)
    extra = (program_name, operator_id, result, date_recorded)
    result_table = results_dict[program_name]
    form = supporter + extra
    ins = result_table.insert().values(form)
    conn.execute(ins)
    conn.close()

def get_program_actual_name(program_name):
    conn = engine.connect()
    s = sql.select([tfrprograms.c.actual_name]). \
        where(tfrprograms.c.name==program_name)
    actual_name = conn.execute(s).fetchone()[0]
    conn.close()
    return actual_name

def report_hours(operator_id, program_name, hours, minutes,
                 start_time, end_time, device, no_of_calls):
    conn = engine.connect()
    date = datetime.date.today()
    actual_name = get_program_actual_name(program_name)
    username = get_operator_username(operator_id)
    form = (None, operator_id, username, hours, minutes, actual_name,
            date, start_time, end_time, device, no_of_calls)
    ins = tfroperatorreport.insert().values(form)
    conn.execute(ins)
    conn.close()
                      
def report_shift(operator_id, data):
    reported_hours = data
    print reported_hours
    for program, hours, minutes, start_time, end_time, device, no_of_calls in reported_hours:
        report_hours(operator_id, program, hours, minutes, 
                     start_time, end_time, device, no_of_calls)
        
def report_calls_made(operator_id, data):
    conn = engine.connect()
    calls_made = data
    date = datetime.date.today()
    form = (None, operator_id, date, calls_made)
    ins = tfrcallsreport.insert().values(form)
    conn.execute(ins)
    conn.close()

def update_personal(operator_id, supporter_id, program_name, data):
    phone1  = data[CON_PHONE1]
    phone2  = data[CON_PHONE2]
    phone3  = data[CON_PHONE3]
    email   = data[CON_EMAIL]    
    address = data[CON_ADDRESS]
    city    = data[CON_CITY]
    postal  = data[CON_POSTAL]
    name    = data[CON_NAME]
    surname = data[CON_SURNAME]
    comment = data[CON_COMMENT]
    
    program = programs_dict[program_name]
    if phone1 != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(Phone1=phone1)
        conn.execute(stmt)
        conn.close()
    if phone2 != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(Phone2=phone2)
        conn.execute(stmt)
        conn.close()
    if phone3 != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(Phone3=phone3)
        conn.execute(stmt)
        conn.close()
    if email != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(EmailAddress=email)
        conn.execute(stmt)
        conn.close()
    if address != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(Address=address)
        conn.execute(stmt)
        conn.close()
    if city != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(City=city)
        conn.execute(stmt)
        conn.close()
    if postal != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(Postal=postal)
        conn.execute(stmt)
        conn.close()
    if name != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(FirstName=name)
        conn.execute(stmt)
        conn.close()
    if surname != '':
        conn = engine.connect()
        stmt = program.update(). \
               where(program.c.LookupID==supporter_id). \
               values(Surname=surname)
        conn.execute(stmt)
        conn.close()
        
              
        

    
    
    

    

    
    
