import SocketServer
import threading
import datetime
import pickle
import sys

import tfr_data
import tfr_exceptions

IP   = '192.168.30.19'
PORT = 8888 


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    """Bla.

    """
    ### Request message codes
    ### Message codes:
    ### RQ_SUPP     -- Request Supporter
    ### RQ_USUPP    -- Request uncalled supporter
    ### RQ_PROG_L   -- Request active program list
    ### RQ_SC_CALL  -- Request scheduled call
    ### RQ_USERNAME -- Request operator's nickname
    ### RQ_SCH_CALL_LIST -- Request scheduled call list
    ### RQ_SUP_BY_ID -- Request supporter based on id
    ### RQ_SCH_BY_ID -- Request scheduled supporter based on id

    RQ_SUPP    = 101
    RQ_USUPP   = 102
    RQ_PROG_L  = 103
#    RQ_SC_CALL = 104 # deprecated
    RQ_CALLS   = 105
    RQ_USERNAME= 106
    RQ_SCH_CALL_LIST = 107
    RQ_SUP_BY_ID = 108
    RQ_SCH_BY_ID = 109
    RQ_REM_SUP = 110

    ### Status message codes
    ### ST_LOGIN  -- Login User
    ### ST_LOGOUT -- Logout
    ### ST_PROG   -- Choose Program
    
    ST_LOGIN        = 201
    ST_LOGOUT       = 202
    ST_PROG         = 203
    ST_INTERACTIONS = 204

    ### Update message codes
    UPD_CALL      = 301
    UPD_SCH_CALL  = 302    
    UPD_PERS_INFO = 303
    UPD_FNC_INFO  = 304
    UPD_INT       = 305
    UPD_ANSWER    = 306
    UPD_SHIFTS    = 307
    UPD_CALLS_MADE= 308
    UPD_ACT_CALLED= 309
    UPD_DE_CALLED = 310

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        cur_thread = threading.current_thread()
        print "{}: {}".format(cur_thread.name, self.data)
        unp_data = pickle.loads(self.data)
        reply = self.handle_message(unp_data)
        msg = pickle.dumps(reply)
        print sys.getsizeof(msg)
        self.request.sendall(msg)
    ### Handling requests.
    def supporter_to_operator(self, operator_id, program_name):
        """Provide a supporter to the operator."""
        return tfr_data.provide_supporter(operator_id, program_name)

    def get_supporter_calls(self, operator_id, feedback):
        """Get calls made to supporter."""
        supporter_id, program_name = feedback
        return tfr_data.get_calls(operator_id, supporter_id, program_name)
        
    def uncalled_supporter_to_operator(self, operator_id):
        """Provide an uncalled supporter to the operator."""
        pass
    
    def active_program_list(self, operator_id):
        """Return the active program list."""
        return tfr_data.active_programs

    def get_operator_username(self, operator_id):
        """Return the operator's username."""
        return tfr_data.get_operator_username(operator_id)

    def get_scheduled_call_list(self, operator_id):
        """Return the scheduled calls list."""
        return tfr_data.ordered_scheduled_list(operator_id)

    def supporter_by_id(self, operator_id, data):
        supporter_id, program = data
        return tfr_data.get_supporter_by_id(supporter_id, program)
    
    def scheduled_by_id(self, operator_id, data):
        call_id = data
        return tfr_data.get_scheduled_supporter_by_call_id(operator_id, call_id)
        
    def get_remaining_supporters(self, operator_id):
        return tfr_data.remaining_supporters(operator_id)

    ### Handling status.
    def login(self, operator_id, password):
        """Handle login."""
        try:
            return tfr_data.operator_login(operator_id, password)
        except tfr_exceptions.IDLoginError as e:
            return '1'
        except tfr_exceptions.PasswordLoginError as e:
            return '2'

    def logout(self, operator_id):
        """Handle logout."""
        tfr_data.operator_logout(operator_id)

    def operator_program(self, operator_id, program_name):
        """Declare the program choice for the operator."""
        tfr_data.choose_program(operator_id, program_name)
        
    def get_interactions(self, operator_id, program_name):
        """Retrieve possible interactions for given program."""
        return tfr_data.program_interactions(program_name)

    ### Handling updates.
    def update_call(self, operator_id, data):
        """Update a call."""
        supporter_id, program_name, call_comment = data
        tfr_data.add_call(operator_id, supporter_id,
                             program_name, call_comment)

    def update_scheduled_call(self, operator_id, data):
        """Update a scheduled_call."""
        datetime, supporter_id, comments, program_name = data
        tfr_data.add_scheduled_call(operator_id, datetime, supporter_id,
                                    comments, program_name)        

    def update_personal_info(self, operator_id, feedback):
        """Update personal info.
        
        The update is made using the tuple that is provided by the operator.
        The tuple should contain the supporter_id, the program name
        and the data concerning the changes to be recorded.
        """
        supporter_id, program_name, data = feedback
        tfr_data.submit_personal_changes(operator_id, supporter_id, 
                                         program_name, data)
        tfr_data.update_personal(operator_id, supporter_id,
                                 program_name, data)

    def update_financial_info(self, operator_id, feedback):
        """Update financial info.
        
        The update is made using the tuple that is given by the 
        operator. The tuple should contain the supporter_id the program name 
        and the data concerning the changes to be recorded.
        """
        supporter_id, program_name, data = feedback
        tfr_data.submit_financial_changes(operator_id, supporter_id, 
                                          program_name, data)

    def update_interaction(self, operator_id, feedback):
        """Update interaction.
        
        The update is made using the tuple given by the operator.
        The tuple should contain the supporter_id, the program name 
        and the data concerning the changes to be recorded."""
        supporter_id, program_name, data = feedback
        tfr_data.commit_interaction(operator_id, supporter_id, 
                                    program_name, data)

    def update_answer(self, operator_id, feedback):
        """Update answer."""
        supporter_id, program_name, data = feedback
        tfr_data.commit_answer(operator_id, supporter_id,
                                    program_name, data)
        
    def update_shift(self, operator_id, feedback):
        data = feedback
        tfr_data.report_shift(operator_id, data)

    def update_calls_made(self, operator_id, feedback):
        data = feedback 
        tfr_data.report_calls_made(operator_id, data)
    
    def update_being_called_activate(self, operator_id, feedback):
        supporter_id, program_name = feedback
        tfr_data.activate_being_called(operator_id, supporter_id, program_name)

    def update_being_called_deactivate(self, operator_id, feedback):
        supporter_id, program_name = feedback
        tfr_data.deactivate_being_called(operator_id, supporter_id, program_name)

    ### Parsing messages
    def handle_message(self, message):
        operator_id = message[0]
        msg_number = message[1]
        data = message[2]
        if msg_number in range(100,200):
            return self.handle_request(operator_id, msg_number, data)
        elif msg_number in range(200,300):
            return self.handle_status(operator_id, msg_number, data)
        elif msg_number in range(300,400):
            return self.handle_update(operator_id, msg_number, data)

    def handle_request(self, operator_id, msg_number, feedback):
        """Handle request message.
        
        All requests provide supporter_id information.
        An additional data argument is provided for each function.
        
        data for each function:
        RQ_SUPP - supporter_to_operator -- program_name needed
        RQ_PROG_L - active_program_list -- no data needed
        RQ_SC_CALL - scheduled_call_to_operator -- call_id required
        RQ_CALLS - get_supporter_calls -- supporter_id required
        """
        if msg_number == self.RQ_SUPP:
            return self.supporter_to_operator(operator_id, feedback)
        elif msg_number == self.RQ_USUPP:
            return "Not yet implemented"
        elif msg_number == self.RQ_PROG_L:
            return self.active_program_list(operator_id)
#deprecated        elif msg_number == self.RQ_SC_CALL:
#            return self.scheduled_call_to_operator(operator_id, feedback)
        elif msg_number == self.RQ_CALLS:
            return self.get_supporter_calls(operator_id, feedback)
        elif msg_number == self.RQ_USERNAME:
            return self.get_operator_username(operator_id)
        elif msg_number == self.RQ_SCH_CALL_LIST:
            return self.get_scheduled_call_list(operator_id)
        elif msg_number == self.RQ_SUP_BY_ID:
            return self.supporter_by_id(operator_id, feedback)
        elif msg_number == self.RQ_SCH_BY_ID:
            return self.scheduled_by_id(operator_id, feedback)
        elif msg_number == self.RQ_REM_SUP:
            return self.get_remaining_supporters(operator_id)

    def handle_status(self, operator_id, msg_number, feedback):
        """Handle status messages. """
        if msg_number == self.ST_LOGIN:
            return self.login(operator_id, feedback)
        elif msg_number == self.ST_LOGOUT:
            return self.logout(operator_id)
        elif msg_number == self.ST_PROG:
            return self.operator_program(operator_id, feedback)
        elif msg_number == self.ST_INTERACTIONS:
            return self.get_interactions(operator_id, feedback)
        
    def handle_update(self, operator_id, msg_number, feedback):
        """Blah. """
        if msg_number == self.UPD_CALL:
            return self.update_call(operator_id, feedback)
        elif msg_number == self.UPD_SCH_CALL:
            return self.update_scheduled_call(operator_id, feedback)
        elif msg_number == self.UPD_PERS_INFO:
            return self.update_personal_info(operator_id, feedback)
        elif msg_number == self.UPD_FNC_INFO:
            return self.update_financial_info(operator_id, feedback)
        elif msg_number == self.UPD_INT:
            return self.update_interaction(operator_id, feedback)
        elif msg_number == self.UPD_ANSWER:
            return self.update_answer(operator_id, feedback)
        elif msg_number == self.UPD_SHIFTS:
            return self.update_shift(operator_id, feedback)
        elif msg_number == self.UPD_CALLS_MADE:
            return self.update_calls_made(operator_id, feedback)
        elif msg_number == self.UPD_ACT_CALLED:
            return self.update_being_called_activate(operator_id, feedback)
        elif msg_number == self.UPD_DE_CALLED:
            return self.update_being_called_deactivate(operator_id, feedback)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

# class TFRAgent(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
#     """Bla Bla.

#     """

#     def __init__(self, server_address, RequestHandlerClass):
#         """Constructor. """
#         SocketServer.TCPServer. \
#         __init__(self, server_address, RequestHandlerClass)
        
    
if __name__ == '__main__':  
        address = (IP, PORT)
        agent = ThreadedTCPServer(address, ThreadedTCPRequestHandler)
#        agent.serve_forever()
        server_thread = threading.Thread(target=agent.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        

