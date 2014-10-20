import SocketServer
import threading
import pickle
import socket
import datetime
import time

import op_exceptions
import tfr_aux


### Request message codes
### Message codes:
### RQ_SUPP   -- Request Supporter
### RQ_USUPP  -- Request uncalled supporter
### RQ_PROG_L -- Request active program list
### RQ_SC_CALL-- Request scheduled call
### RQ_CALLS  -- Request calls made to supporter

RQ_SUPP     = 101  # done
RQ_USUPP    = 102
RQ_PROG_L   = 103  # done
# RQ_SC_CALL  = 104  # deprecated
RQ_CALLS    = 105  # done
RQ_USERNAME = 106  # done
RQ_SCH_CALL_LIST = 107 # done
RQ_SUP_BY_ID = 108
RQ_SCH_BY_ID = 109
RQ_REM_SUP   = 110

### Status message codes:
### ST_LOGIN  -- Login user
### ST_LOGOUT -- Logout user
### ST_PROG   -- Choose Program
### ST_INTERACTIONS -- Get program interactions

ST_LOGIN  = 201  # done
ST_LOGOUT = 202
ST_PROG   = 203  # done
ST_INTERACTIONS = 204 # done
### Update message codes

UPD_CALL      = 301 
UPD_SCH_CALL  = 302 # done
UPD_PERS_INFO = 303 # done
UPD_FNC_INFO  = 304 # done
UPD_INT       = 305 # done
UPD_ANSWER    = 306 # done
UPD_SHIFT     = 307
UPD_CALLS_MADE= 308
UPD_ACT_CALLED= 309
UPD_DE_CALLED = 310

### Agent address.
SERVER_IP = '192.168.30.19'
PORT      = 8888

### Number of previous supporters
NU_OF_PREVIOUS = 6

# programs = {'regresccc':'tfrregresccc',
#             'expcc':'tfrexpcc',
#             'regrescdd':'tfrregrescdd',
#             'rt':'tfrrt',
#             'sleepers':'tfrsleepers'}

def picklify(message):
    """Pickle dumps the given message."""
    return pickle.dumps(message)

def unpicklify(message):
    """Pickle loads the given message."""
    return pickle.loads(message)

def client(message):
    start = time.clock()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))
    try:
        msg = picklify(message)
        sock.sendall(msg)
        response = sock.recv(8192)
        sock.close()
        print time.clock() - start
        return unpicklify(response)
    finally:
        sock.close()

def get_active_programs_list(operator_id):
    """Auxiliary function that returns the active programs list."""
    message = (operator_id, RQ_PROG_L, None)
    return client(message)

def get_remaining_supporters(operator_id):
    """Auxiliary function that returns the remaining supporters list."""
    message = (operator_id, RQ_REM_SUP, None)
    return client(message)

class TFROperator(object):
    def __init__(self):
        # Active supporter is the supporter that is up for interaction
        self.active_supporter = None
        # Active supporter_id is the lookup id og the active supporter
        self.active_supporter_id = None
        # Call list is the calls that have already been made to the supporter.
        self.call_list = None
        # Active program
        self.active_program = None
        # mum defines whether the operator is reachning for
        # called or non-called supporters. mum == true
        # means non-called supporters.
        self.mum = False
        # The program that the operator is calling
        self.chosen_program = None
        # True if user logged in, false when not.
        self.logged = False
        self.pr_interactions = None
        self.operator_nickname = None
        self.scheduled_call_list = None
        self.scheduled_call_comment = None
        self.interaction_committed = False
        self.postponed_calls = []
        self.no_of_postponed = 0
        self.no_of_calls = 0
        self.previous_supporters = tfr_aux.FixedlenList(NU_OF_PREVIOUS)
        self.previous_programs = tfr_aux.FixedlenList(NU_OF_PREVIOUS)
        self.previous_index = 0
        self.in_previous = False
        self.aux_supporter = None
        self.aux_program = None
        
    def __find_value_by_field(self, searched_field):
        """Find any value of the active supporter appropriate field."""
        for field, value in self.active_supporter:
            if field == searched_field:
                return value
                
    def login(self, operator_id, password):
        """Login operator."""
        request = ST_LOGIN
        data = password
        message = (operator_id, request, data)
        reply = client(message)
        if reply == True:
            self.operator_id = operator_id
            self.logged = True
            # Populate active_programs list                
            self.active_programs = get_active_programs_list(self.operator_id)
            self.remaining_sups = get_remaining_supporters(self.operator_id)
            self.operator_username = self.get_operator_username()
            self.set_scheduled_call_list()
        elif reply == '1':
            raise op_exceptions.IDError('ID is incorrect')
        elif reply == '2':
            raise op_exceptions.PWDError('Password is incorrect')

    def refresh_remaining_sups(self):
        """Refresh the remaining supporters dictionary."""
        self.remaining_sups = get_remaining_supporters(self.operator_id)

    def update_supporter_details(self):
        """Update all necessary details whenever a new supporter is provided."""
        self.set_program_interactions()
        self.get_supporter_call_list()
        self.set_supporter_id()
        self.interaction_committed = False
        self.in_previous = False
        self.activate_being_called(self.active_supporter_id,
                                       self.active_program)

    def previous_check(self):
        """The previous supporter procedure required for each new supporter"""
        if self.active_supporter is not None:
            if self.in_previous == False:
                self.previous_supporters.append(self.active_supporter)
                self.previous_programs.append(self.active_program)
                #print (len(self.previous_supporters) - 1)
                self.previous_index = len(self.previous_supporters) - 1
            else:
                self.previous_supporters.append(self.aux_supporter)
                self.previous_programs.append(self.active_program)
                self.previous_index = len(self.previous_supporters) - 1
                
    
    def de_being_called(self):
        """Deactivate the supporter before getting a new one."""
        if self.active_supporter is not None:
            self.deactivate_being_called(self.active_supporter_id,
                                         self.active_program)

    def get_operator_username(self):
        """Get the operator's username."""
        request = RQ_USERNAME
        data = None
        message = (self.operator_id, request, data)
        return client(message)

    def set_supporter_id(self):
        """Get the lookup id of the active supporter."""
        self.active_supporter_id = self.__find_value_by_field('LookupID')

    def get_supporter_call_list(self):
        """Get the call list of the active supporter.
        
        This method is called whenever the active_supporter variable 
        is updated. With the supporter update we get the call list
        updated as well.
        """
        request = RQ_CALLS
        # looking for the supporter's lookupid in the active_supporter
        data = self.__find_value_by_field('LookupID')
        message = (self.operator_id, request, data)
        self.call_list = client(message)
        
    def choose_program(self, program_name):
        """Choose operator's working program.
        
        The choice is registered both at database side, as
        well as in the operator space via the class variable.
        """
        if program_name in self.active_programs:
            request = ST_PROG
            data = program_name
            message = (self.operator_id, request, data)
            # Update the db for the program choice
            client(message)
            # Update the object for the program choice
            self.chosen_program = program_name
            self.active_program = self.chosen_program
            self.set_program_interactions()
        else:
            raise op_exceptions.ProgramError("Incorrect program name")

    def set_program_interactions(self):
        """Get interactions for given program."""
        request = ST_INTERACTIONS
        data = self.active_program
        message = (self.operator_id, request, data)
        self.pr_interactions = client(message)
        
    def get_next_active_supporter(self):
        """Get next active supporter.
        
        Simply ask the server to send the next not necessarilly not 
        called supporter. It comes in the format of tuples of key
        value pairs.
        """
        self.previous_check()
        self.de_being_called()
        request = RQ_SUPP
        data = self.chosen_program
        message = (self.operator_id, request, data)
        reply = client(message)
        if reply == '1':
            raise op_exceptions.NoMoreSupportersError('All supporters have been called./n Check the time of last call.')
        if reply == '2':
            raise op_exceptions.NoMoreSupportersError("Program is closed./n There are no active supporters left.")
    
        else:
            self.active_supporter = reply
            self.active_program = self.chosen_program
            self.update_supporter_details()

    def previous_supporter(self):
        """Get previous supporter from the previous_supporters list."""
        if self.previous_index > -1:
            if self.in_previous == False:
                self.aux_supporter = self.active_supporter
                self.aux_program = self.active_program
            print 'previous index: {}'.format(self.previous_index)
            self.active_supporter = self.previous_supporters[self.previous_index]
            self.active_program = self.previous_programs[self.previous_index]
            self.set_program_interactions()
            self.get_supporter_call_list()
            self.set_supporter_id()
            self.interaction_committed = False
            self.previous_index = self.previous_index - 1
            self.in_previous = True
        else:
            raise op_exceptions.NoPreviousSupporter('Cannot go further back')

    def get_supporter_by_id(self, lookup_id, program):
        """Get supporter by id.
        
        Ask the server to get the supporter
        based on the lookup_id provided.
        """
        self.previous_check()
        self.de_being_called()
        request = RQ_SUP_BY_ID
        # Change program name to appropriate program description
        data = lookup_id, program
        message = (self.operator_id, request, data)
        reply = client(message)
        if reply == '1':
            raise op_exceptions.ProgramError('Program choice is wrong')
        elif reply =='2':
            raise op_exceptions.SupporterIDError('Supporter ID does not exist')
        elif reply=='3':
            raise op_exceptions.IsBeingCalledError('Supporter is being called')
        else:
            self.active_supporter = reply
            self.get_supporter_call_list()
            self.active_program = program
            self.update_supporter_details()

    def get_scheduled_call(self, call_id):
        """Choose a specific scheduled to call.

        Instead of waiting for the next scheduled call,
        pick one manually.
        """
        self.previous_check()
        self.de_being_called()
        request = RQ_SCH_BY_ID
        data = call_id
        message = (self.operator_id, request, data)
        reply = client(message)
        if reply == "1":
            raise op_exceptions.ScheduledCallError('Scheduled call no longer exists.')
        else:
             supporter, comment, program = reply       
             self.active_supporter = supporter
             self.get_supporter_call_list()
             self.active_program = program
             self.scheduled_call_comment = comment
             self.update_supporter_details()

    def set_scheduled_call_list(self):
        """Set the scheduled call list."""
        request = RQ_SCH_CALL_LIST
        data = None
        message = (self.operator_id, request, data)
        self.scheduled_call_list = client(message)

    
    ### COMMITS
    def __form_call_data(self, personal_info, finance_info, interaction):
        """Just form a tuple containing the data needed for a call commit."""
        return (personal_info, finance_info, interaction)
    
    def scheduled_call(self, supporter_id, datetime, comments, program_name):
        """Commit a scheduled call."""
        request = UPD_SCH_CALL
        data =  datetime, supporter_id, comments, program_name
        message = (self.operator_id, request, data)
        client(message)
    
    def commit_call(self, supporter_id, program_name, call_comment):
        """Commit a regular call.
        """
        request = UPD_CALL
        data = supporter_id, program_name, call_comment
        message = (self.operator_id, request, data)
        client(message)

    def commit_answer(self, supporter_id, program_name, data):
        """Commit answer."""
        request = UPD_ANSWER
        feedback = supporter_id, program_name, data
        message = (self.operator_id, request, feedback)
        client(message)
        
    def commit_interaction(self, supporter_id, program_name, data):
        """Commit interaction.

        Data comes from the supporter_form.
        program_name is decided on the spot.
        """
        request = UPD_INT
        feedback = supporter_id, program_name, data
        message = (self.operator_id, request, feedback)
        client(message)
        self.interaction_committed = True

    def commit_financial_changes(self, supporter_id, program_name, data):
        """Commit financial changes.
        
        Data comes from the supporter_form.
        program_name is decided on the spot.
        """
        request = UPD_FNC_INFO
        feedback = supporter_id, program_name, data
        message = (self.operator_id, request, feedback)
        client(message)
        self.change_financial_to_supporter(data)

    def commit_personal_changes(self, supporter_id, program_name, data):
        """Commit personal changes.
        
        Data comes from the supporter_form.
        program_name is decided on the spot.
        """
        request = UPD_PERS_INFO
        feedback = supporter_id, program_name, data
        message = (self.operator_id, request, feedback)
        client(message)
        self.change_personal_to_supporter(data)
        

    def update_shift(self, data):
        """Report shift hours of the operator.
        
        At the end of his/her shift the operator reports 
        how many hours and what programs he/she has worked.
        """
        request = UPD_SHIFT
        feedback = data
        message = (self.operator_id, request, feedback)
        client(message)

    def update_calls_made(self):
        """Report shift calls of the operator.

        At the end of his/her shift, the operator repots how 
        many calls he has made.
        """
        request = UPD_CALLS_MADE
        feedback = self.no_of_calls
        message = (self.operator_id, request, feedback)
        client(message)

    def add_postponed_call(self, comment):
        """Add active supporter to postponed_calls."""
        time_called = datetime.datetime.now().time()
        entry = (self.no_of_postponed, 
                 time_called,
                 self.active_program,
                 self.active_supporter,
                 comment)
        self.postponed_calls.append(entry)
        self.no_of_postponed += 1

    def get_postponed_call(self, psp_id):
        """Get the appropriate supporter for the given index."""
        self.previous_check()
        self.de_being_called()
        entry = self._return_postponed_by_index(psp_id)
        self.active_program = entry[2]
        self.active_supporter = entry[3]
        self.update_supporter_details()

    def _return_postponed_by_index(self, psp_id):
        for idx,entry in enumerate(self.postponed_calls):
            if entry[0] == psp_id:
                searched = entry
                pop_idx = idx
        self.postponed_calls.pop(pop_idx)
        return searched
        
    def activate_being_called(self, supporter_id, program_name):
        """Activate being called entry for given supporter."""
        request=UPD_ACT_CALLED
        data = supporter_id, program_name
        message = (self.operator_id, request, data)
        client(message)

    def deactivate_being_called(self, supporter_id, program_name):
        """Deactivate being_called entry for given supporter."""
        request = UPD_DE_CALLED
        data = supporter_id, program_name
        message = (self.operator_id, request, data)
        client(message)

    def supporter_has_result(self):
        for field, value in self.active_supporter:
            if field=='has_result':
                if value==u'0':
                    return False
                else:
                    return True
        raise ValueError('The supporter does not have a has_result value')

    def activate_has_result(self):
        """Change the active supporter's has_result entry.
    
        When commiting an interaction, change the has_result entry
        of the active_supporter to 1.
        """
        # find the index of active supporter tuple list
        # where has_result is the first element of the tuple
        index = [x for x,y in enumerate(self.active_supporter) \
                 if y[0]=='has_result'][0]
        # change the entry to '1'
        self.active_supporter[index] = (u'has_result', u'1')
    
    def __create_contact_changes_dict(self, data):
        fields = ['Phone1',
                  'Phone2',
                  'Phone3',
                  'EmailAddress',
                  'Address',
                  'City',
                  'Postal',
                  'FirstName',
                  'Surname']
        return dict(zip(fields, data))
        
    def find_index(self, field):
        index = [x for x,y in enumerate(self.active_supporter) \
                 if y[0]==field][0]
        return index

    def change_personal_to_supporter(self, data):
        """Change personal details to local(client) supporter."""
        comment_index = len(data) - 1
        # convert to list in order to remove the comment 
        # from the changes list
        data_list = list(data)
        del data_list[comment_index]
        changes = self.__create_contact_changes_dict(data_list)
        for field, change in changes.iteritems():
            if change != '':
                index = self.find_index(field)
                self.active_supporter[index] = (field, change)
    
    def __create_finance_changes_dict(self, data):
        fields = ['RecurringGiftAmount',
                  'RecurringGiftFrequency',
                  'CardType',
                  'ExpireDate',
                  'CreditCardNumber',
                  'CVV',
                  'Bank',
                  'IBAN']
        return dict(zip(fields, data))
    
    def change_financial_to_supporter(self, data):
        """Change financial details to local(client)supporter."""
        comment_index = len(data) - 1
        # convert to list in order to remove the comment 
        # from the changes list
        data_list = list(data)
        del data_list[comment_index]
        changes = self.__create_finance_changes_dict(data_list)
        for field, change in changes.iteritems():
            if change != '':
                index = self.find_index(field)
                self.active_supporter[index] = (field, change)
 
    
