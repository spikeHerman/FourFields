

import datetime
from socket import error as socket_error

import Tkinter as tk
import ttk
import tkFont
import tkMessageBox


import tfr_operator as op
import op_exceptions

# Color at Contact info frames
CONTACT_INFO_COLOR='#C9C8C9'
# Color at Finace info frames
FINANCE_INFO_COLOR='#CADADA'
# Color at calls frame
CALLS_COLOR = '#DDD4BC'
# Color at scheduled frames
SCHEDULED_COLOR = '#DDD4BC'
# Color at changed entries
HIGHLIGHT_COLOR = '#ADEDB8'

def no_connection(func):
    def check_connection_and_proceed(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except socket_error as serr:
            tkMessageBox.showerror('Connection',
                                   'Connection to server is impossible,contact admin')
    return check_connection_and_proceed

def get_value_of_supporter(supporter, given_key):
    """Take the key and find the value in a supporter tuple.
    """
    for key, value in supporter:
        if given_key == key:
            return value
    return "N/A"

def check_entry_length(max_length, entry):
    """Check if given entry's character length is less than maximum."""
    if entry is not None:
        if len(entry) <= max_length:
            return True
        else:
            return False
    else:
        return True

class TFRSupporterForm(tk.Canvas):
    def __init__(self, operator, master=None):
        tk.Canvas.__init__(self, master)
        self.operator = operator
        self.grid()
        self.create_widgets()
        self.create_checkbuttons_list()
#        self.fill_form()
    
    def create_widgets(self):
        self.contact_form = TFRContactForm(self)
        self.contact_form.grid(row=0, column=0, sticky="ewns")

        self.address_form = TFRAddressForm(self)
        self.address_form.grid(row=0, column=1, sticky="ewns")
        
        self.program_info = TFRProgramInfoForm(self)
        self.program_info.grid(row=3, column=2, sticky="ewns")
        
        #len(self.operator.call_list)
        self.max_number_of_calls = 6
        self.calls = TFRCallsForm(self, self.max_number_of_calls)
        self.calls.grid(row=1, column=0, rowspan=2, columnspan=2, sticky="ewns")
        
        self.interactions_list_size = 6
        self.interactions = TFRInteractions(self,
                                            height=self.interactions_list_size)
        self.interactions.grid(row=3, column=0, columnspan=2,
                               rowspan=2, sticky="ewns")

        self.supporter_id = TFRSupporterIDForm(self)
        self.supporter_id.grid(row=2, column=2, sticky="ewns")
   
        self.supporter_name = TFRSupporterNameForm(self)
        self.supporter_name.grid(row=0, column=2, sticky="ewns")

        self.supporter_info_form = TFRSupporterInfoForm(self)
        self.supporter_info_form.grid(row=1, column=2, sticky="ewns")
        
        self.account_info = TFRAccountInfoForm(self)
        self.account_info.grid(row=5, columnspan=3, sticky="ew")

        self.failed_transactions = TFRFailedTransactions(self)
        self.failed_transactions.grid(row=6, column=2, sticky=tk.NW)
        
        self.successfull_transactions = TFRSuccessfullTransactions(self)
        self.successfull_transactions.grid(row=7, column=2, sticky='nsew')

        self.last_interactions = TFRLastInteractions(self)
        self.last_interactions.grid(row=6, column=0, 
                                    columnspan=2 , sticky='nsew')

        self.once_off = TFRLastOnceOff(self)
        self.once_off.grid(row=7, column=0,
                           columnspan=2, sticky='nsew')
    
    def check_supporter_exists(self):
        if self.operator.active_supporter is not None:
            return True
        else: 
            return False
    
    def create_checkbuttons_list(self):
        """Create a list of all the checkbuttons in the Supporter Form.
    
        The list contains tuples consisting of checkbutton, corresponding 
        IntVar variable and the corresponding Entry.
        Order is very important, since in order to finance and personal
        changes, the tuple that is sent to the tfr_agent is formed by going
        through this list.
        So when adding information to the personal and finance changes one
        should be extra careful to have the correct correspondence between 
        the placement of the added info here and in the tfr_data space.
        """
        self.CBFinanceList = [(self.account_info.amount_check,
                               self.account_info.amount_check_var,
                               self.account_info.amount_var,
                               self.account_info.amount_entry),

                              (self.account_info.frequency_check,
                               self.account_info.frequency_check_var,
                               self.account_info.frequency_var,
                               self.account_info.frequency_entry),

                              (self.account_info.card_type_check,
                               self.account_info.card_type_check_var,
                               self.account_info.card_type_var,
                               self.account_info.card_type_entry),

                              (self.account_info.expire_check,
                               self.account_info.expire_check_var,
                               self.account_info.expire_var,
                               self.account_info.expire_entry),

                              (self.account_info.card_number_check,
                               self.account_info.card_number_check_var,
                               self.account_info.card_number_var,
                               self.account_info.card_number_entry),

                              (self.account_info.cvv_check,
                               self.account_info.cvv_check_var,
                               self.account_info.cvv_var,
                               self.account_info.cvv_entry),

                              (self.account_info.bank_check,
                               self.account_info.bank_check_var,
                               self.account_info.bank_var,
                               self.account_info.bank_entry),

                              (self.account_info.iban_check,
                               self.account_info.iban_check_var,
                               self.account_info.iban_var,
                               self.account_info.iban_entry)]
                              
        self.CBPersonalList = [(self.contact_form.phone1_check, 
                                self.contact_form.phone1_check_var,
                                self.contact_form.phone_var1,
                                self.contact_form.phone_number_entry1),
                            
                               (self.contact_form.phone2_check,
                                self.contact_form.phone2_check_var,
                                self.contact_form.phone_var2,
                                self.contact_form.phone_number_entry2),
                       
                               (self.contact_form.phone3_check,
                                self.contact_form.phone3_check_var,
                                self.contact_form.phone_var3,
                                self.contact_form.phone_number_entry3),
                       
                               (self.contact_form.email_check,
                                self.contact_form.email_check_var,
                                self.contact_form.email_var,
                                self.contact_form.email_entry),
                    
                               (self.address_form.address_check,
                                self.address_form.address_check_var,
                                self.address_form.address_var,
                                self.address_form.address_line_entry),
                       
                               (self.address_form.city_check,
                                self.address_form.city_check_var,
                                self.address_form.city_var,
                                self.address_form.city_entry),
                               
                               (self.address_form.postal_check,
                                self.address_form.postal_check_var,
                                self.address_form.postal_var,
                                self.address_form.postal_entry),
                               
                               (self.supporter_name.name_check,
                                self.supporter_name.name_check_var,
                                self.supporter_name.name_var,
                                self.supporter_name.supporter_name_entry),

                               (self.supporter_name.surname_check,
                                self.supporter_name.surname_check_var,
                                self.supporter_name.surname_var,
                                self.supporter_name.supporter_surname_entry)]
    
    def __check_comment_length(self, comment):
        max_comment_length = 250
        if len(comment) > max_comment_length:
            return False
        else:
            return True
    
    def highlight_changes(self, checkbuttons_list):
        """Checks a checkbutton_lsit and highlight any changes."""
        for cb, check_var, entry_var, entry in checkbuttons_list:
            if check_var.get() == 1:
                entry.configure(background=HIGHLIGHT_COLOR)

    def __check_for_changes(self, checkbuttons_list):
        """Check a checkbutton_list and return the corresponding entries.
    
        Returns a tuple of all the entries in a checkbuttons_list
        that their corresponding checkbox is checked.
        The order in which the tuple is formed is determined by the 
        checkbuttons_list.
        """
        valid = False
        entries = []
        for checkbutton, check_var, entry_var, entry in checkbuttons_list:
            if check_var.get() == 1:
                entries.append(entry_var.get())
            elif check_var.get() == 0:
                entries.append('')
        return entries
        
    def __check_changes_list(self, changes_list):
        """Check a change list if it is full of None elements."""
        got_changes = False
        for entry in changes_list:
            if entry != '':
                got_changes = True
        return got_changes
            
    def get_finance_changes(self):
        """Get all finance changes."""
        changes = self.__check_for_changes(self.CBFinanceList)
        fnc_comment = self.account_info.fnc_comment_txt.get("0.0", tk.END+"-1c")
        if fnc_comment != '':
            changes.append(fnc_comment)
            return tuple(changes)
        elif self.__check_changes_list(changes):
            changes.append('')
            return tuple(changes)
        else:
            return None
        
    def get_personal_changes(self):
        """Get all personal changes."""
        changes = self.__check_for_changes(self.CBPersonalList)
        prsn_comment = self.supporter_info_form.prsn_comment_txt. \
                       get("0.0", tk.END+"-1c")
        if prsn_comment != '':
            changes.append(prsn_comment)
            return tuple(changes)
        elif self.__check_changes_list(changes):
            changes.append('')
            return tuple(changes)
        else:
            return None

    ### Needs FIXING   
    # def check_dd_onspot(self):
    #     """Check if requirements of DD on spot are met.
        
    #     Requirements are met if IBAN is given."""
    #     answer = self.check_and_get_result()
    #     print answer
    #     print "22 - TFR DD on spot"
    #     # CBFinanceList[7] is the Iban checkbutton in the interface.
    #     ch, check_var, entr_var, entr = self.CBFinanceList[7]
    #     print check_var.get()
    #     if answer=="22 - TFR DD on Spot":
    #         if check_var.get()==0:
    #             #Return false if no Iban number has been given
    #             return False
    #     return True
                
            
    def check_and_get_result(self):
        """Get the result chosen by the operator."""
        if self.interactions.interactions_list.curselection():
            selection = int(self.interactions. \
                            interactions_list.curselection()[0])
            return self.interactions.interactions_list.get(selection)
        else:
            return None
            
    def make_answer(self):
        """Commit the answer based on the result."""
        temp = self.interactions.inter_comments_txt.get("0.0", tk.END)
        if temp == '':
            comment = None
        else:
            comment = temp
        if self.check_and_get_result() is not None:
            self.operator. \
                commit_answer(self.operator.active_supporter_id,
                              self.operator.chosen_program,
                              (self.check_and_get_result(),comment))
            # Get current selection, in order to change its background color.
            selection = int(self.interactions.interactions_list.curselection()[0])
            # Clear selection of interactions listbox
            list_size = self.interactions.interactions_list.size()
            self.interactions.interactions_list.selection_clear(0, list_size)
            # Change color to the previously selected element
            self.interactions.interactions_list.itemconfig(selection, bg=HIGHLIGHT_COLOR)
        
    def commit_interaction(self):
        """Commit the interaction based on the result."""
        if self.check_and_get_result() is not None:
            self.operator. \
                commit_interaction(self.operator.active_supporter_id,
                                   self.operator.chosen_program,
                                   (self.check_and_get_result(),'','','',''))
    
    def make_personal_changes(self):
        """Complete personal changes."""
        changes = self.get_personal_changes()
        if changes is not None:
            self.operator. \
                commit_personal_changes(self.operator.active_supporter_id,
                                        self.operator.chosen_program,
                                        changes)
            self.highlight_changes(self.CBPersonalList)
        
    def make_finance_changes(self):
        """Complete finance changes."""
        changes = self.get_finance_changes()
        if changes is not None:
            self.operator. \
                commit_financial_changes(self.operator.active_supporter_id,
                                         self.operator.chosen_program,
                                         changes)
            self.highlight_changes(self.CBFinanceList)
    
    

    def __is_entry_list_invalid(self, entry_list):
        max_entry_length = 66
        for entry in entry_list:
            if not check_entry_length(max_entry_length, entry):
                return entry
        return False

    def do_all_finance_changes(self):
        """Do all financial related commits."""
        self.make_finance_changes()
        self.commit_interaction()
        self.make_answer()
    
    @no_connection
    def submit_button(self):
        """Submit button for finance and personal changes."""
        #if self.operator.interaction_committed:
        #    tkMessageBox.showwarning('Commit answer',
        #                             'You have already committed a change for this supporter')
        if self.check_supporter_exists():
            if self.check_and_get_result() is None and \
               self.get_finance_changes() is None:
                tkMessageBox.showwarning('No changes made.',
                                         'There are no changes to be commited.')
            else:
                finc_entries = self.__check_for_changes(self.CBFinanceList)
                fnc_invalid = self.__is_entry_list_invalid(finc_entries)
                if fnc_invalid:
                    tkMessageBox.showerror('Commit changes', 
                                           'Entries %s are too long.\nMax number of characters is 65' % (fnc_invalid))
                else:
                    if tkMessageBox.askokcancel('Commit changes', 
                                                'About to commit changes.Proceed?'):
                        #"-1c" is required because tkinter adds a newline at the end of the comment
                        fnc_comment = self.account_info.fnc_comment_txt. \
                                      get("0.0", tk.END+"-1c")
                        ans_comment = self.interactions.inter_comments_txt. \
                                      get("0.0", tk.END+"-1c")
                        if self.__check_comment_length(fnc_comment) and \
                           self.__check_comment_length(ans_comment):
                            if self.check_and_get_result() is not None:
                                if self.operator.supporter_has_result():
                                    tkMessageBox.showerror('Commit changes',
                                                           "This supporter has already an interaction commited. \
                                                           You can only commit financial changes.")
                                else:
                                    #if self.check_dd_onspot():
                                    self.do_all_finance_changes()
                                    self.operator.activate_has_result()
                                    #else:
                                    #    tkMessageBox.showerror('Commit changes',
                                    #                           'IBAN or Credit card is required to commit an On Spot Answer.')
                            else:
                                self.do_all_finance_changes()
                        else:
                            tkMessageBox.showerror('Commit changes',
                                                   'Comment length is too long, max length is 250 characters')
        else:
            tkMessageBox.showerror('Commit changes',
                                   'There is no active supporter, no data to submit.')

    @no_connection
    def commit_contact_button(self):
        if self.check_supporter_exists():
            if self.get_personal_changes() is None:
                tkMessageBox.showwarning('No changes made.',
                                         'No changes to be commited.')
            else:
                prsn_entries = self.__check_for_changes(self.CBPersonalList)
                prsn_invalid = self.__is_entry_list_invalid(prsn_entries)
                if prsn_invalid:
                    tkMessageBox.showerror('Commit changes',
                                           'Entries %s and %s are too long.\nMax number of characters is 65' % (fnc_invalid, prsn_invalid))
                else:
                    if tkMessageBox.askyesno('Commit changes',
                                             'About to commit.Proceed?'):
                        prsn_comment = self.supporter_info_form.prsn_comment_txt. \
                                       get("0.0", tk.END+"-1c")
                        if self.__check_comment_length(prsn_comment):
                            self.make_personal_changes()
                        else:
                            tk.MessageBox.showerror('Commit changes',
                                                'Comment length is too long, max length is 250 characters')
        else:
            tkMessageBox.showerror('Commit changes',
                                   'There is no active supporter, no data to submit.')
                    
    def get_call_comment(self):
        """Get the call comment,input by the operator."""
        no_of_calls = len(self.operator.call_list)
        if no_of_calls < 6:
            return self.calls.call_entries[no_of_calls][3].get()
        else:
            return self.calls.call_entries[5][3].get()

    @no_connection
    def commit_call(self):
        """Commit a call."""
        if self.check_supporter_exists():
            comment = self.get_call_comment()
            max_comment_length = 250
            if len(comment) <= max_comment_length:
                self.operator.commit_call(self.operator.active_supporter_id,
                                          self.operator.chosen_program,
                                          comment)
                self.calls.commit_call_button.configure(state=tk.DISABLED)
                tkMessageBox.showinfo('Commit call',
                                      'Call commited!')
            else:
                tkMessageBox.showerror('Commit call',
                                       'Comment length is too long,\n max length is 250 characters')
        else:
            tkMessageBox.showerror('Commit call',
                                   'There is no active supporter, no data to submit.')

    def __get_input_date_text(self):
        try:
            day = int(self.calls.day_entry.get())
            month = int(self.calls.month_entry.get())
            year = int(self.calls.year_entry.get())
            hour = int(self.calls.hour_entry.get())
            minutes = int(self.calls.minutes_entry.get())
            return (day, month, year, hour, minutes)
        except ValueError as e:
            return False


    def get_scheduled_date(self):
        """Get the scheduled date inputted by the user."""
        date = self.__get_input_date_text()
        if date:
            day, month, year, hour, minutes = date
            return datetime.datetime(year, month, day, hour, minutes)
        else:
            return False

    @no_connection            
    def commit_scheduled_call(self):
        """Commit a scheduled call."""
        if self.check_supporter_exists():
            try:
                date = self.get_scheduled_date()
                comment = self.calls.sch_comments_entry.get('0.0', tk.END)
                if date:
                    if self.__check_comment_length(comment):
                        self.operator.scheduled_call(self.operator.active_supporter_id,
                                                     date, comment,
                                                     self.operator.chosen_program)
                        # Disable the button since commit was successful
                        self.calls.scheduled_button.configure(state=tk.DISABLED)
                        self.master.refresh_sch_list()
                        tkMessageBox.showinfo('Scheduled call', 
                                              'Scheduled call committed')
                    else:
                        tkMessageBox.showerror('Scheduled call',
                                               'Comment too long, max length is 250')
                else:
                    tkMessageBox.showerror('Scheculed call',
                                               'Wrong input date')
            except ValueError as e:
                tkMessageBox.showerror('Scheduled call', e)
        else:
            tkMessageBox.showerror('Commit changes',
                                   'There is no active supporter, no data to submit.')


    
    def postpone_call(self):
        comment = self.calls.psp_comment_entry.get()
        if self.check_supporter_exists():
            if len(comment) == 0: 
                tkMessageBox.showwarning('Postponing a call',
                                         'You have not entered any comment.')
            else:
                self.operator.add_postponed_call(comment)
                self.master.refresh_postponed_list()
                tkMessageBox.showinfo('Postponing a call',
                                      'Call has been postponed.')
        else:
            tkMessageBox.showerror('Commit changes',
                                   'There is no active supporter, no data to submit.')

    
    def fill_form(self):
        self.fill_contact_form()
        self.fill_address_form()
        self.fill_program_info()
        self.fill_calls()
        self.fill_supporter_id()
        self.fill_supporter_name()
        self.fill_supporter_info()
        self.fill_account_info()
        self.fill_failed_transactions()
        self.fill_interactions()
        self.fill_successfull_transactions()
        self.fill_last_interactions()
        self.fill_onceoff()

    def clear_form(self):
        self.clear_calls()
        self.clear_contact_form()
        self.clear_address_form()
        self.clear_program_info()
        self.clear_supporter_id()
        self.clear_supporter_name()
        self.clear_supporter_info()
        self.clear_account_info()
        self.clear_failed_transactions()
        self.clear_interactions()
        self.clear_checkbuttons()
        self.clear_comments()
        self.clear_scheduled_call()
        self.clear_successfull_transactions()
        self.clear_last_interactions()
        self.clear_onceoff()
        self.clear_disabled_buttons()
        self.clear_postponed()
        self.clear_highlights()

    def clear_postponed(self):
        self.calls.psp_comment_entry.delete(0, tk.END)

    def clear_disabled_buttons(self):
        self.interactions.interactions_button.configure(state=tk.NORMAL)
        self.calls.commit_call_button.configure(state=tk.NORMAL)
        self.calls.scheduled_button.configure(state=tk.NORMAL)


    def clear_scheduled_call(self):
        self.calls.day_entry.delete(0, tk.END)
        self.calls.month_entry.delete(0, tk.END)
        self.calls.year_entry.delete(0, tk.END)
        self.calls.hour_entry.delete(0, tk.END)
        self.calls.minutes_entry.delete(0, tk.END)

    def clear_comments(self):
        self.interactions.inter_comments_txt.delete("0.0", tk.END)
        self.account_info.fnc_comment_txt.delete("0.0", tk.END)
        self.supporter_info_form.prsn_comment_txt.delete("0.0", tk.END)
        self.calls.sch_comments_entry.delete("0.0", tk.END)

    def clear_checkbuttons(self):
        """ Toggle all checkbuttons to unmarked."""
        # Personal info checkbuttons
        for checkbutton, check_var, entry_var, entry in self.CBPersonalList:
            if check_var.get() == 1:
                checkbutton.toggle()
        # Finance Checkbuttons
        for checkbutton, check_var, entry_var, entry in self.CBFinanceList:
            if check_var.get() == 1:
                checkbutton.toggle()
            
    def clear_highlights(self):
        """Turn off all highlighted entries."""
        for cb, cv, ev, entry in self.CBPersonalList:
            entry.configure(background='white')
        for cb, cv, ev, entry in self.CBFinanceList:
            entry.configure(background='white')

    def fill_interactions(self):
        for interaction in self.operator.pr_interactions:
            self.interactions.interactions_list.insert(tk.END, interaction)

    def clear_interactions(self):
        self.interactions.interactions_list.delete(0, tk.END)
        # number_of_interactions = len(self.operator.pr_interactions)
        # self.interactions.interactions_list.delete(0, number_of_interactions)
        
    def clear_calls(self):
        rows = range(6)
        columns = range(0,4)
        for row in rows:
            for column in columns:
                self.calls.call_entries[row][column]. \
                    delete(0, tk.END)
    
    def get_last_call(self):
        no_of_calls = len(self.operator.call_list)
        if no_of_calls != 0:
            return int(self.operator.call_list[no_of_calls-1][0])
        else:
            last_call = 0
            return last_call

    def fill_calls(self):
        no_of_calls = len(self.operator.call_list)
        row_number = 5
        column_number = 4
        
        # Handle the case where calls made are less than 6.
        # print them all and keep space for the extra call,
        # who is about to be committed.
        if no_of_calls < 6:
            for row in range(no_of_calls):
                for column in range(column_number):
                    self.calls.call_entries[row][column]. \
                        insert(0, self.operator.call_list[row][column])
            row_number = no_of_calls 
        # If calls made are 6 or more, then the last 5 should be printed
        # keeping a spot for the call about to be committed.
        else:
            starting_call = no_of_calls - 5
            for row in range(row_number):
                for column in range(column_number):
                    self.calls.call_entries[row][column]. \
                        insert(0,self.operator.call_list[starting_call][column])
                starting_call += 1

        # print the last call about to be committed.
        last_call = self.get_last_call()
        self.calls.call_entries[row_number][0].insert(0, last_call+1)
        self.calls.call_entries[row_number][1].insert(0, self.operator.operator_username)
        self.calls.call_entries[row_number][2].insert(0, datetime.datetime.now())

    def clear_supporter_info(self):
        self.supporter_info_form.supp_dob_entry.delete(0, tk.END)
        self.supporter_info_form.registration_entry.delete(0, tk.END)
        self.supporter_info_form.proffession_entry.delete(0, tk.END)

    def fill_supporter_info(self):
        dob = get_value_of_supporter(self.operator.active_supporter, 
                                     'BirthDate')
        self.supporter_info_form.supp_dob_entry.insert(0, dob)
        
        registration = get_value_of_supporter(self.operator.active_supporter, 
                                              'RecurringGiftStartDate')
        self.supporter_info_form.registration_entry.insert(0, registration)

        proffession = get_value_of_supporter(self.operator.active_supporter, 
                                             'Profession')
        self.supporter_info_form.proffession_entry.insert(0, proffession)

    def clear_address_form(self):
        self.address_form.address_line_entry.configure(state=tk.NORMAL)
        self.address_form.address_line_entry.delete(0, tk.END)
        self.address_form.city_entry.configure(state=tk.NORMAL)
        self.address_form.city_entry.delete(0, tk.END)
        self.address_form.postal_entry.configure(state=tk.NORMAL)
        self.address_form.postal_entry.delete(0, tk.END)


    def fill_address_form(self):
        address_line = get_value_of_supporter(self.operator.active_supporter,
                                              'Address')
        self.address_form.address_line_entry.insert(0, address_line)
        self.address_form.address_line_entry.configure(state='readonly')

        city = get_value_of_supporter(self.operator.active_supporter,
                                      'City')
        self.address_form.city_entry.insert(0, city)
        self.address_form.city_entry.configure(state='readonly')

        postal = get_value_of_supporter(self.operator.active_supporter,
                                        'Postal')
        self.address_form.postal_entry.insert(0, postal)
        self.address_form.postal_entry.configure(state='readonly')

    def clear_contact_form(self):
        self.contact_form.phone_number_entry1.configure(state=tk.NORMAL)
        self.contact_form.phone_number_entry1.delete(0, tk.END)
        self.contact_form.phone_number_entry2.configure(state=tk.NORMAL)
        self.contact_form.phone_number_entry2.delete(0, tk.END)
        self.contact_form.phone_number_entry3.configure(state=tk.NORMAL)
        self.contact_form.phone_number_entry3.delete(0, tk.END)
        self.contact_form.email_entry.configure(state=tk.NORMAL)
        self.contact_form.email_entry.delete(0, tk.END)
        

    def fill_contact_form(self):
        phone1 = get_value_of_supporter(self.operator.active_supporter, 
                                        'Phone1')
        self.contact_form.phone_number_entry1.insert(0, phone1)
        self.contact_form.phone_number_entry1.configure(state='readonly')

        phone2 = get_value_of_supporter(self.operator.active_supporter,
                                        'Phone2')
        self.contact_form.phone_number_entry2.insert(0, phone2)
        self.contact_form.phone_number_entry2.configure(state='readonly')

        phone3 = get_value_of_supporter(self.operator.active_supporter,
                                        'Phone3')
        self.contact_form.phone_number_entry3.insert(0, phone3)
        self.contact_form.phone_number_entry3.configure(state='readonly')

        email = get_value_of_supporter(self.operator.active_supporter,
                                       'EmailAddress')
        self.contact_form.email_entry.insert(0, email)
        self.contact_form.email_entry.configure(state='readonly')

    def clear_supporter_id(self):
        self.supporter_id.universe_id_entry.delete(0,tk.END)
        
    def fill_supporter_id(self):
        lookup = get_value_of_supporter(self.operator.active_supporter,
                                        'LookupID')
        self.supporter_id.universe_id_entry.insert(0,lookup)
        
    def clear_supporter_name(self):
        self.supporter_name.supporter_name_entry.configure(state=tk.NORMAL)
        self.supporter_name.supporter_name_entry.delete(0, tk.END)
        self.supporter_name.supporter_surname_entry.configure(state=tk.NORMAL)
        self.supporter_name.supporter_surname_entry.delete(0, tk.END)

    def fill_supporter_name(self):
        first_name = get_value_of_supporter(self.operator.active_supporter,
                                            'FirstName')
        last_name = get_value_of_supporter(self.operator.active_supporter,
                                           'Surname')        
        self.supporter_name.supporter_name_entry.insert(0, first_name)
        self.supporter_name.supporter_name_entry.configure(state='readonly')
        self.supporter_name.supporter_surname_entry.insert(0, last_name)
        self.supporter_name.supporter_surname_entry.configure(state='readonly')

    def clear_program_info(self):
        self.program_info.page_entry.delete(0, tk.END)
        self.program_info.appeal_entry.delete(0, tk.END)
        self.program_info.finder_entry.delete(0, tk.END)
        self.program_info.source_entry.delete(0, tk.END)
        
    def fill_program_info(self):
        page = get_value_of_supporter(self.operator.active_supporter,
                                      'Page')
        self.program_info.page_entry.insert(0, page)
        
        appeal = get_value_of_supporter(self.operator.active_supporter,
                                        'ProgramName')
        self.program_info.appeal_entry.insert(0, appeal)
        ### ---NOT CHANGED BY JIM----
        finder = get_value_of_supporter(self.operator.active_supporter,
                                        'FinderNumber')
        self.program_info.finder_entry.insert(0, finder)
        ### ---NOT CHANGED BY JIM-----
        source = get_value_of_supporter(self.operator.active_supporter,
                                        'SourceCode')
        self.program_info.source_entry.insert(0, source)
        
    def clear_account_info(self):
        ## Ammount entry
        self.account_info.amount_entry.configure(state=tk.NORMAL)
        self.account_info.amount_entry.delete(0, tk.END)
        
        ## Frequency entry
        self.account_info.frequency_entry.configure(state=tk.NORMAL)
        self.account_info.frequency_entry.delete(0, tk.END)

        ## Commence entry
        self.account_info.commence_entry.configure(state=tk.NORMAL)
        self.account_info.commence_entry.delete(0, tk.END)
    
        ### Card type entry
        self.account_info.card_type_entry.configure(state=tk.NORMAL)
        self.account_info.card_type_entry.delete(0, tk.END)
        
        ### Expire date entry 
        self.account_info.expire_entry.configure(state=tk.NORMAL)
        self.account_info.expire_entry.delete(0, tk.END)
        
        ### Card Number entry
        self.account_info.card_number_entry.configure(state=tk.NORMAL)
        self.account_info.card_number_entry.delete(0, tk.END)

        ### CVV entry
        self.account_info.cvv_entry.configure(state=tk.NORMAL)
        self.account_info.cvv_entry.delete(0, tk.END)
                                                   
        ### bank entry
        self.account_info.bank_entry.configure(state=tk.NORMAL)
        self.account_info.bank_entry.delete(0, tk.END)

        ### IBAN entry
        self.account_info.iban_entry.configure(state=tk.NORMAL)
        self.account_info.iban_entry.delete(0, tk.END)

    def fill_account_info(self):
        ## Ammount entry
        amount = get_value_of_supporter(self.operator.active_supporter,
                                        'RecurringGiftAmount')
        self.account_info.amount_entry.insert(0, amount)
        self.account_info.amount_entry.configure(state='readonly')

        ## Frequency entry
        frequency = get_value_of_supporter(self.operator.active_supporter,
                                          'RecurringGiftFrequency')
        self.account_info.frequency_entry.insert(0, frequency)
        self.account_info.frequency_entry.configure(state='readonly')

        ### Commence date entry
        startdate = get_value_of_supporter(self.operator.active_supporter,
                                           'RecurringGiftStartDate')
        self.account_info.commence_entry.insert(0,startdate)
        self.account_info.commence_entry.configure(state='readonly')

        ### Card Type entry
        card_type = get_value_of_supporter(self.operator.active_supporter,
                                           'CardType')
        self.account_info.card_type_entry.insert(0, card_type)
        self.account_info.card_type_entry.configure(state='readonly')


        ### Expire date entry
        expire_date = get_value_of_supporter(self.operator.active_supporter,
                                             'ExpireDate')
        self.account_info.expire_entry.insert(0, expire_date)
        self.account_info.expire_entry.configure(state='readonly')
        
        ### Card Number
        card_number = get_value_of_supporter(self.operator.active_supporter,
                                             'CreditCardNumber')
        self.account_info.card_number_entry.insert(0, card_number)
        self.account_info.card_number_entry.configure(state='readonly')

        ### Credit Card CVV
        cvv_number = get_value_of_supporter(self.operator.active_supporter,
                                            'CVV')
        self.account_info.cvv_entry.insert(0, cvv_number)
        self.account_info.cvv_entry.configure(state='readonly')

        ### Bank
        bank = get_value_of_supporter(self.operator.active_supporter,
                                      'Bank')
        self.account_info.bank_entry.insert(0, bank)
        self.account_info.bank_entry.configure(state='readonly')
        
        ### IBAN
        iban = get_value_of_supporter(self.operator.active_supporter,
                                      'IBAN')
        self.account_info.iban_entry.insert(0, iban)
        self.account_info.iban_entry.configure(state='readonly')

    def clear_last_interactions(self):
        self.last_interactions.date1_entry.delete(0, tk.END)
        self.last_interactions.date2_entry.delete(0, tk.END)
        self.last_interactions.date3_entry.delete(0, tk.END)
        self.last_interactions.interaction1_entry.delete(0, tk.END)
        self.last_interactions.interaction2_entry.delete(0, tk.END)
        self.last_interactions.interaction3_entry.delete(0, tk.END)

    def fill_last_interactions(self):
        date1 = get_value_of_supporter(self.operator.active_supporter,
                                       'InteractionDate1')
        self.last_interactions.date1_entry.insert(0, date1)
        date2 = get_value_of_supporter(self.operator.active_supporter,
                                       'InteractionDate2')
        self.last_interactions.date2_entry.insert(0, date2)
        date3 = get_value_of_supporter(self.operator.active_supporter,
                                       'InteractionDate3')
        self.last_interactions.date3_entry.insert(0, date3)
        
        interaction1 = get_value_of_supporter(self.operator.active_supporter,
                                              'InteractionSubcategory1')
        self.last_interactions.interaction1_entry.insert(0, interaction1)
        interaction2 = get_value_of_supporter(self.operator.active_supporter,
                                              'InteractionSubcategory2')
        self.last_interactions.interaction2_entry.insert(0, interaction2)
        interaction3 = get_value_of_supporter(self.operator.active_supporter,
                                              'InteractionSubcategory3')
        self.last_interactions.interaction3_entry.insert(0, interaction3)
                               
    def clear_successfull_transactions(self):
        self.successfull_transactions.date1_entry.delete(0, tk.END)
        self.successfull_transactions.date2_entry.delete(0, tk.END)
        self.successfull_transactions.date3_entry.delete(0, tk.END)
        self.successfull_transactions.method1_entry.delete(0, tk.END)
        self.successfull_transactions.method2_entry.delete(0, tk.END)
        self.successfull_transactions.method3_entry.delete(0, tk.END)
        self.successfull_transactions.ammount1_entry.delete(0, tk.END)
        self.successfull_transactions.ammount2_entry.delete(0, tk.END)
        self.successfull_transactions.ammount3_entry.delete(0, tk.END)

    def fill_successfull_transactions(self):
        date1 = get_value_of_supporter(self.operator.active_supporter,
                                       'SuccessDate1')
        self.successfull_transactions.date1_entry.insert(0, date1)
        
        date2 = get_value_of_supporter(self.operator.active_supporter,
                                       'SuccessDate2')
        self.successfull_transactions.date2_entry.insert(0, date2)

        date3 = get_value_of_supporter(self.operator.active_supporter,
                                       'SuccesDate3')
        self.successfull_transactions.date3_entry.insert(0, date3)

        method1 = get_value_of_supporter(self.operator.active_supporter,
                                         'SuccessPaymentMethod1')
        self.successfull_transactions.method1_entry.insert(0, method1)

        method2 = get_value_of_supporter(self.operator.active_supporter,
                                         'SuccessPaymentMethod2')
        
        self.successfull_transactions.method2_entry.insert(0, method2)
        
        method3 = get_value_of_supporter(self.operator.active_supporter,
                                         'SuccessPaymentMethod3')
        
        self.successfull_transactions.method3_entry.insert(0, method3)

        amount1 = get_value_of_supporter(self.operator.active_supporter,
                                         'SuccessAmount1')
        self.successfull_transactions.ammount1_entry.insert(0, amount1)

        amount2 = get_value_of_supporter(self.operator.active_supporter,
                                         'SuccessAmount2')
        self.successfull_transactions.ammount2_entry.insert(0, amount2)

        amount3 = get_value_of_supporter(self.operator.active_supporter,
                                         'SuccessAmount3')
        self.successfull_transactions.ammount3_entry.insert(0, amount3)


    def clear_failed_transactions(self):
        self.failed_transactions.date1_entry.delete(0, tk.END)
        self.failed_transactions.date2_entry.delete(0, tk.END)
        self.failed_transactions.date3_entry.delete(0, tk.END)
        self.failed_transactions.why_failed1_entry.delete(0, tk.END)
        self.failed_transactions.why_failed2_entry.delete(0, tk.END)
        self.failed_transactions.why_failed3_entry.delete(0, tk.END)
    
    def fill_failed_transactions(self):
        date1 = get_value_of_supporter(self.operator.active_supporter,
                                       'AttemptDate1')
        self.failed_transactions.date1_entry.insert(0, date1)

        date2 = get_value_of_supporter(self.operator.active_supporter,
                                       'AttemptDate2')
        self.failed_transactions.date2_entry.insert(0, date2)

        date3 = get_value_of_supporter(self.operator.active_supporter,
                                       'AttemptDate3')
        self.failed_transactions.date3_entry.insert(0, date3)

        fail_reason = get_value_of_supporter(self.operator.active_supporter,
                                             'Rejection1')
        self.failed_transactions.why_failed1_entry.insert(0, fail_reason)

        fail_reason2 = get_value_of_supporter(self.operator.active_supporter,
                                              'Rejection2')
        self.failed_transactions.why_failed2_entry.insert(0, fail_reason2)
        
        fail_reason3 = get_value_of_supporter(self.operator.active_supporter,
                                              'Rejection3')
        self.failed_transactions.why_failed3_entry.insert(0, fail_reason3)
    
    def clear_onceoff(self):
        """Not yet implemented"""
        self.once_off.date_entry.delete(0, tk.END)
        self.once_off.method_entry.delete(0, tk.END)
        self.once_off.amount_entry.delete(0, tk.END)

    def fill_onceoff(self):
        """Not applicable right now"""
        date = get_value_of_supporter(self.operator.active_supporter,
                                      'OnceOffDate')
        self.once_off.date_entry.insert(0, date)
        method = get_value_of_supporter(self.operator.active_supporter,
                                        'OnceOffPaymentMethod')
        self.once_off.method_entry.insert(0, method)
        amount = get_value_of_supporter(self.operator.active_supporter,
                                        'OnceOffAmount')
        self.once_off.amount_entry.insert(0, amount)

def activate(widget):
    if widget.cget('state') == 'readonly':
        widget.configure(state=tk.NORMAL)
    else:
        widget.configure(state='readonly')
        
class TFRContactForm(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, background=CONTACT_INFO_COLOR)
        self.BOLD   = tkFont.Font(family='Times', weight='bold')
        self.NORMAL = tkFont.Font(family='Times')

        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        self.phone_number_lbl = tk.Label(self, text="Phone Numbers",
                                         padx=15,
                                         font=self.BOLD,
                                         background=CONTACT_INFO_COLOR)
        self.phone_number_lbl.grid(row=0, column=0)
        
        ### PHONE NUMBER TEXT VARIABLES
        self.phone_var1 = tk.StringVar()
        self.phone_var2 = tk.StringVar()
        self.phone_var3 = tk.StringVar()

        ### PHONE NUMBER ENTRIES
        self.phone_number_entry1 = tk.Entry(self, bd=2, width=26,
                                            textvariable=self.phone_var1,
                                            readonlybackground='white')
        self.phone_number_entry2 = tk.Entry(self, bd=2, width=26,
                                            textvariable=self.phone_var2,
                                            readonlybackground='white')
        self.phone_number_entry3 = tk.Entry(self, bd=2, width=26,
                                            textvariable=self.phone_var3,
                                            readonlybackground='white')
        self.phone_number_entry1.grid(row=2, column=0)
        self.phone_number_entry2.grid(row=3, column=0)
        self.phone_number_entry3.grid(row=4, column=0)
        
        ### PHONE NUMBER CHECKBUTTONS
        self.phone1_check_var = tk.IntVar()
        self.phone1_check = tk.Checkbutton(self, 
                                           variable=self.phone1_check_var,
                                           command=lambda: activate(self.phone_number_entry1),
                                           background=CONTACT_INFO_COLOR)
        self.phone1_check.grid(row=2,column=1)

        self.phone2_check_var = tk.IntVar()
        self.phone2_check = tk.Checkbutton(self, 
                                           variable=self.phone2_check_var,
                                           command=lambda: activate(self.phone_number_entry2),
                                           background=CONTACT_INFO_COLOR)
        self.phone2_check.grid(row=3,column=1)

        self.phone3_check_var = tk.IntVar()
        self.phone3_check = tk.Checkbutton(self, 
                                           variable=self.phone3_check_var,
                                           command=lambda: activate(self.phone_number_entry3),
                                           background=CONTACT_INFO_COLOR)
        self.phone3_check.grid(row=4,column=1)

        ### EMAIL ENTRIES AND LABELS AND SUCH
        self.email_lbl = tk.Label(self, text="Email Address",
                                  padx=16,
                                  font=self.BOLD,
                                  background=CONTACT_INFO_COLOR)
        self.email_lbl.grid(row=5, column=0)
        
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self, bd=2, width=26,
                                    textvariable=self.email_var,
                                    readonlybackground='white')
        self.email_entry.grid(row=6, column=0)
        self.email_check_var = tk.IntVar()
        self.email_check = tk.Checkbutton(self, 
                                          variable=self.email_check_var,
                                          command=lambda: activate(self.email_entry),
                                          background=CONTACT_INFO_COLOR)
        self.email_check.grid(row=6,column=1)

    
class TFRAddressForm(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, background=CONTACT_INFO_COLOR)
        self.BOLD   = tkFont.Font(family='Times', weight='bold')

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        ### Address Line
        self.address_var = tk.StringVar()
        self.address_line_lbl = tk.Label(self, text="Address",
                                         font=self.BOLD,
                                         background=CONTACT_INFO_COLOR)
        self.address_line_lbl.grid(row=0, column=0)
        self.address_line_entry = tk.Entry(self, bd=2,  width=33,
                                           textvariable=self.address_var,
                                           readonlybackground='white')
        self.address_line_entry.grid(row=1, column=0)
        self.address_check_var = tk.IntVar()
        self.address_check = tk.Checkbutton(self,
                                            variable=self.address_check_var,
                                            command=lambda: activate(self.address_line_entry),
                                            background=CONTACT_INFO_COLOR)
        self.address_check.grid(row=1, column=1)
        
        ### City
        self.city_var = tk.StringVar()
        self.city_lbl = tk.Label(self, text="City",
                                 font=self.BOLD,
                                 background=CONTACT_INFO_COLOR)
        self.city_lbl.grid(row=2, column=0)
        self.city_entry = tk.Entry(self, bd=2, width=33,
                                   textvariable=self.city_var,
                                   readonlybackground='white')
        self.city_entry.grid(row=3, column=0)
        self.city_check_var = tk.IntVar()
        self.city_check = tk.Checkbutton(self,
                                         variable=self.city_check_var,
                                         command=lambda: activate(self.city_entry),
                                         background=CONTACT_INFO_COLOR)
        self.city_check.grid(row=3, column=1)

        
        ### Postal Code
        self.postal_var = tk.StringVar()
        self.postal_lbl = tk.Label(self, text="Postal",
                                   font=self.BOLD,
                                   background=CONTACT_INFO_COLOR)
        self.postal_lbl.grid(row=4, column=0)
        self.postal_entry = tk.Entry(self, bd=2, width=11,
                                     textvariable=self.postal_var,
                                     readonlybackground='white')
        self.postal_entry.grid(row=5, column=0)
        self.postal_check_var = tk.IntVar()
        self.postal_check = tk.Checkbutton(self,
                                           variable=self.postal_check_var,
                                           command=lambda: activate(self.postal_entry),
                                           background=CONTACT_INFO_COLOR)
        self.postal_check.grid(row=5, column=1)



class TFRInteractions(tk.LabelFrame):
    def __init__(self, master=None, height=6):
        """TFRInteractions init method."""
        tk.LabelFrame.__init__(self, master, text="Interactions",
                               background=FINANCE_INFO_COLOR)
        self.BOLD = tkFont.Font(family='Times', weight='bold')
        self.height = height
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        """Create the interaction widgets."""
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL,
                                    background=FINANCE_INFO_COLOR)
        self.yScroll.grid(row=0, column=1, sticky="ns")
        
        self.interactions_list = tk.Listbox(self, height=self.height,
                                            yscrollcommand=self.yScroll.set,
                                            width=33,
                                            exportselection=0)
        self.interactions_list.grid(row=0, column=0)
        self.yScroll['command'] = self.interactions_list.yview
        self.clear_list_button = tk.Button(self, text="Clear List",
                                           command=self.clear_list,
                                           background=FINANCE_INFO_COLOR)
        self.clear_list_button.grid(row=1, column=0, sticky='we')
        
        ### The Commit Changes button.
        self.interactions_button_frame = tk.Frame(self, padx=6,
                                                  background=FINANCE_INFO_COLOR)
        self.interactions_button_frame.grid(row=1, column=2)
        
        self.interactions_button = tk.Button(self.interactions_button_frame,
                                             text="Commit Finance Changes",
                                             command=self.master.submit_button,
                                             background=FINANCE_INFO_COLOR)
        self.interactions_button.grid(row=0, column=0)
        
        ### The interaction comments
        self.interactions_comments_frame = tk.LabelFrame(self, 
                                                         text="Comments",
                                                         padx=6,
                                                         background=FINANCE_INFO_COLOR)
        self.interactions_comments_frame.grid(row=0, column=2)
        self.inter_comments_txt = tk.Text(self.interactions_comments_frame,
                                          width=16, height=4)
        self.inter_comments_txt.grid(row=0, column=0)
        
    def clear_list(self):
        """Clear the interactions list selection."""
        list_size = self.interactions_list.size()
        self.interactions_list.selection_clear(0, list_size)
        
class TFRCallsForm(tk.LabelFrame):
    def __init__(self, master=None, number_of_calls=0):
        tk.LabelFrame.__init__(self, master, background=CALLS_COLOR)
        self.BOLD   = tkFont.Font(family='Times', weight='bold')
        self.NORMAL = tkFont.Font(family='Times')

        self.number_of_calls = number_of_calls
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Call labels
        self.number_lbl = tk.Label(self, text="##", padx = 15,
                                   background=CALLS_COLOR)
        self.number_lbl.grid(row=0, column = 0)

        self.operator_lbl = tk.Label(self, text="Operator", padx=15,
                                     font=self.BOLD,
                                     background=CALLS_COLOR)
        self.operator_lbl.grid(row=0, column=1)

        self.datetime_lbl = tk.Label(self, text="Date/Time", padx=15,
                                     font=self.BOLD,
                                     highlightthickness = 3,
                                     highlightbackground = 'black',
                                     background=CALLS_COLOR)
        self.datetime_lbl.grid(row=0, column=2)

        self.comment_lbl = tk.Label(self, text="Comment", padx=15,
                                    font=self.BOLD,
                                    background=CALLS_COLOR)
        self.comment_lbl.grid(row=0, column=3)
        # Create call rows
        self.call_entries = []
        rows = range(1,self.number_of_calls+1)
        columns = range(0,4)
        for row in rows:
            current_row = []
            for column in columns:
                if column == 0:
                    call_entry = tk.Entry(self, width=3)
                if column == 1:
                    call_entry = tk.Entry(self, width=10)
                if column == 2:
                    call_entry = tk.Entry(self, width=15)
                if column == 3:
                    call_entry = tk.Entry(self, width=25)
                call_entry.grid(row=row, column=column)
                current_row.append(call_entry)
            self.call_entries.append(current_row)
            
        self.commit_call_button_frame = tk.Frame(self, padx=6, pady=6,
                                                 background=CALLS_COLOR)
        self.commit_call_button_frame.grid(row=7, column=3, sticky='e')
        self.commit_call_button = tk.Button(self.commit_call_button_frame,
                                            text="Commit call",
                                            command=self.master.commit_call,
                                            background=CALLS_COLOR)
        self.commit_call_button.grid()
        
        ### Create scheduled calls constructor
        self.scheduled_call_frame = tk.LabelFrame(self, text='Scheduled Calls',
                                                  background=SCHEDULED_COLOR)
        self.scheduled_call_frame.grid(row=8, column=0, columnspan=4,
                                       sticky='nsew')
        
        ### Create the date entries
        # day
        self.day_label = tk.Label(self.scheduled_call_frame, text='Day',
                                  background=SCHEDULED_COLOR)
        self.day_label.grid(row=0, column=0)
        self.day_entry = tk.Entry(self.scheduled_call_frame, width=2)
        self.day_entry.grid(row=1, column=0)
        self.dash1 = tk.Label(self.scheduled_call_frame, text='-',
                              background=SCHEDULED_COLOR)
        self.dash1.grid(row=1, column=1)
        # month
        self.month_label = tk.Label(self.scheduled_call_frame, text='Month',
                                    background=SCHEDULED_COLOR)
        self.month_label.grid(row=0, column=2)
        self.month_entry = tk.Entry(self.scheduled_call_frame, width=2)
        self.month_entry.grid(row=1, column=2)
        self.dash2 = tk.Label(self.scheduled_call_frame, text='-',
                              background=SCHEDULED_COLOR)
        self.dash2.grid(row=1, column=3)
        # year
        self.year_label = tk.Label(self.scheduled_call_frame, text='Year',
                                   background=SCHEDULED_COLOR)
        self.year_label.grid(row=0, column=4)
        self.year_entry = tk.Entry(self.scheduled_call_frame, width=4)
        self.year_entry.grid(row=1, column=4)
        # date/hour separator
        self.date_separator = tk.Label(self.scheduled_call_frame, text='----',
                                       background=SCHEDULED_COLOR)
        self.date_separator.grid(row=1, column=5)
        ### Create the time entries
        # hour
        self.hour_label = tk.Label(self.scheduled_call_frame, text='Hour',
                                   background=SCHEDULED_COLOR)
        self.hour_label.grid(row=0, column=6)
        self.hour_entry = tk.Entry(self.scheduled_call_frame, width=2)
        self.hour_entry.grid(row=1, column=6)
        self.hour_colon = tk.Label(self.scheduled_call_frame, text=':',
                                   background=SCHEDULED_COLOR)
        self.hour_colon.grid(row=1, column=7)
        # minutes
        self.minutes_label = tk.Label(self.scheduled_call_frame, text='Min',
                                      background=SCHEDULED_COLOR)
        self.minutes_label.grid(row=0, column=8)
        self.minutes_entry = tk.Entry(self.scheduled_call_frame, width=2)
        self.minutes_entry.grid(row=1, column=8)
        # scheduled_call_comments
        self.sch_comments_label = tk.Label(self.scheduled_call_frame, 
                                           text='Comments',
                                           background=SCHEDULED_COLOR)
        self.sch_comments_label.grid(row=0, column=9)
        self.sch_comments_entry = tk.Text(self.scheduled_call_frame,
                                           width=18, height=2)
        self.sch_comments_entry.grid(row=1, column=9)
        # scheduled_call_button
        self.sch_button_frame = tk.Frame(self.scheduled_call_frame,
                                         padx=6, pady=6,
                                         background=SCHEDULED_COLOR)
        self.sch_button_frame.grid(row=0, column=10, rowspan=2, sticky='e')
        self.scheduled_button = tk.Button(self.sch_button_frame,
                                          text='Commit date',
                                          command=self.master.commit_scheduled_call,
                                          background=SCHEDULED_COLOR)
        self.scheduled_button.grid()
        
        ### Postponed Calls frame
        self.postponed_frame = tk.Frame(self, 
                                        background=CALLS_COLOR)
        self.postponed_frame.grid(row=7, columnspan=3, sticky='nsew')
        self.psp_comment_entry = tk.Entry(self.postponed_frame,
                                          width=16)
        self.psp_comment_entry.grid(row=0, column=0)
        self.psp_button_frame = tk.Frame(self.postponed_frame,
                                         padx=6,
                                         pady=6,
                                         background=CALLS_COLOR)
        self.psp_button_frame.grid(row=0, column=1)
        self.psp_button = tk.Button(self.psp_button_frame,
                                    text='Postpone a call',
                                    command=self.master.postpone_call,
                                    background=CALLS_COLOR)
        self.psp_button.grid()

        
class TFRNotesForm(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, text="Notes")
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.textnote = tk.Text(self, width=48, height=9)
        self.textnote.grid(row=0, column=0)

class TFRProgramInfoForm(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master)
        self.BOLD   = tkFont.Font(family='Times', weight='bold')
        self.NORMAL = tkFont.Font(family='Times')
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.date_lbl = tk.Label(self)
        self.date_lbl.grid(row=0, column=0)
        
        self.page_lbl = tk.Label(self, text="Page:", font=self.BOLD)
        self.page_lbl.grid(row=1, column=0)

        self.page_entry = tk.Entry(self, width=33)
        self.page_entry.grid(row=1, column=1)

        self.appeal_lbl = tk.Label(self, text="Appeal Mailing:", font=self.BOLD)
        self.appeal_lbl.grid(row=2, column=0)

        self.appeal_entry = tk.Entry(self, width=33,
                                     background='white')
        self.appeal_entry.grid(row=2, column=1)
    
        self.finder_lbl = tk.Label(self, text="Finder Number:", font=self.BOLD)
        self.finder_lbl.grid(row=3, column=0)

        self.finder_entry = tk.Entry(self, width=33)        
        self.finder_entry.grid(row=3, column=1)

        self.source_lbl = tk.Label(self, text="Source Code:", font=self.BOLD)
        self.source_lbl.grid(row=4, column=0)
        
        self.source_entry = tk.Entry(self, width=33)
        self.source_entry.grid(row=4, column=1)


class TFRSupporterIDForm(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master)
        self.BOLD   = tkFont.Font(family='Times', weight='bold')
        self.NORMAL = tkFont.Font(family='Times')
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.supporter_id_lbl = tk.Label(self, text="Supporter id",
                                         font=self.BOLD,
                                         pady=6)
        self.supporter_id_lbl.grid(row=0, column=0, columnspan=2)
        
        # Universe ID
        self.universe_id_lbl = tk.Label(self, text="Universe:", font=self.BOLD)
        self.universe_id_lbl.grid(row=1, column=0)
        self.universe_id_entry = tk.Entry(self)
        self.universe_id_entry.grid(row=1, column=1)
        
        # Friends ID
        self.friends_id_lbl = tk.Label(self, text="Friends:", font=self.BOLD)
        self.friends_id_lbl.grid(row=2, column=0)
        self.friends_id_entry = tk.Entry(self)
        self.friends_id_entry.grid(row=2, column=1)
        
class TFRSupporterNameForm(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, background=CONTACT_INFO_COLOR)
        self.BOLD   = tkFont.Font(family='Times', weight='bold')
        self.NORMAL = tkFont.Font(family='Times')
        self.NAMEFONT = tkFont.Font(family='Times', weight='bold', size=16)
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        # Name
        self.name_var = tk.StringVar()
        self.supporter_name_lbl = tk.Label(self, text="Name:", 
                                           font=self.BOLD,
                                           background=CONTACT_INFO_COLOR)
                                           
                                           
        self.supporter_name_lbl.grid(row=0, column=0)
        self.supporter_name_entry = tk.Entry(self, font=self.NAMEFONT,
                                             textvariable=self.name_var,
                                             readonlybackground='white')
        self.supporter_name_entry.grid(row=1, column=0)
        self.name_check_var = tk.IntVar()
        self.name_check = tk.Checkbutton(self,
                                         variable=self.name_check_var,
                                         background=CONTACT_INFO_COLOR,
                                         command=lambda: activate(self.supporter_name_entry))
        self.name_check.grid(row=1, column=1)

        # Surname
        self.surname_var = tk.StringVar()
        self.supporter_surname_lbl = tk.Label(self,
                                              text="Surname:",
                                              font=self.BOLD,
                                              background=CONTACT_INFO_COLOR)
        self.supporter_surname_lbl.grid(row=2, column=0)
        self.supporter_surname_entry = tk.Entry(self, font=self.NAMEFONT,
                                                textvariable=self.surname_var,
                                                readonlybackground='white')
        self.supporter_surname_entry.grid(row=3, column=0)
        self.surname_check_var = tk.IntVar()
        self.surname_check = tk.Checkbutton(self,
                                            variable=self.surname_check_var,
                                            background=CONTACT_INFO_COLOR,
                                            command=lambda: activate(self.supporter_surname_entry))
        self.surname_check.grid(row=3, column=1)

        # Commit contact changes button
        self.contact_button_frame = tk.Frame(self, padx=6, pady=6,
                                             background=CONTACT_INFO_COLOR)
        self.contact_button_frame.grid(row=4, column=0, columnspan=2)
        
        self.contact_button = tk.Button(self.contact_button_frame,
                                        background=CONTACT_INFO_COLOR,
                                        text='Commit contact changes',
                                        command=self.master.commit_contact_button)
        self.contact_button.grid()

    def activate(self, widget):
        if widget.cget('state') == 'readonly':
            widget.configure(state=tk.NORMAL)
        else:
            widget.configure(state='readonly')
        
class TFRSupporterInfoForm(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master,
                               background=CONTACT_INFO_COLOR)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # supporter date of birth
        self.supp_dob_lbl = tk.Label(self, text="Date of Birth:",
                                     background=CONTACT_INFO_COLOR)
        self.supp_dob_lbl.grid(row=2, column=0)            
        self.supp_dob_entry = tk.Entry(self)
        self.supp_dob_entry.grid(row=2, column=1)
        
        # supporter signing date
        self.registration_lbl = tk.Label(self, text="Registration:",
                                         background=CONTACT_INFO_COLOR)
        self.registration_lbl.grid(row=3, column=0)
        self.registration_entry = tk.Entry(self)
        self.registration_entry.grid(row=3, column=1)
        
        # supporter profession
        self.proffession_lbl = tk.Label(self, text="Proffession",
                                        background=CONTACT_INFO_COLOR)
        self.proffession_lbl.grid(row=4, column=0)
        self.proffession_entry= tk.Entry(self)
        self.proffession_entry.grid(row=4, column=1)

        # Contact Comments
        self.personal_comment_frame = tk.LabelFrame(self, 
                                                    text='Personal Comment',
                                                    background=CONTACT_INFO_COLOR)
        self.personal_comment_frame.grid(row=0, column=0, columnspan=2,
                                          rowspan=2, sticky='nsew')
        self.prsn_comment_txt = tk.Text(self.personal_comment_frame,
                                     height=3, width=32)
        self.prsn_comment_txt.grid(row=0, column=0, sticky='nsew')


class TFRAccountInfoForm(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, background=FINANCE_INFO_COLOR)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # support amount
        self.amount_var = tk.StringVar()
        self.amount_lbl = tk.Label(self, text="Amount:",
                                   background=FINANCE_INFO_COLOR)
        self.amount_lbl.grid(row=0, column=0)
        self.amount_entry = tk.Entry(self,
                                     textvariable=self.amount_var,
                                     readonlybackground='white')
        self.amount_entry.grid(row=0, column=1)
        self.amount_check_var = tk.IntVar()
        self.amount_check = tk.Checkbutton(self, bd=2,
                                           variable=self.amount_check_var,
                                           command=lambda: activate(self.amount_entry),
                                           background=FINANCE_INFO_COLOR)
        self.amount_check.grid(row=0, column=2)

        # support frequency
        self.frequency_var = tk.StringVar()
        self.frequency_lbl = tk.Label(self, text="Frequency:",
                                      background=FINANCE_INFO_COLOR)
        self.frequency_lbl.grid(row=0, column=3)
        self.frequency_entry = tk.Entry(self,
                                        textvariable=self.frequency_var,
                                        readonlybackground='white')
        self.frequency_entry.grid(row=0, column=4)
        self.frequency_check_var = tk.IntVar()
        self.frequency_check = tk.Checkbutton(self, bd=2, 
                                              variable=self.frequency_check_var,
                                              command=lambda: activate(self.frequency_entry),
                                              background=FINANCE_INFO_COLOR)
        self.frequency_check.grid(row=0,column=5)

        # commence date
        self.commence_lbl = tk.Label(self, text="Commence date:",
                                     background=FINANCE_INFO_COLOR)
        self.commence_lbl.grid(row=0, column=6)
        self.commence_entry = tk.Entry(self)                                   
        self.commence_entry.grid(row=0, column=7)

        # card type
        self.card_type_var = tk.StringVar()
        self.card_type_lbl = tk.Label(self, text="Card type:",
                                      background=FINANCE_INFO_COLOR)
        self.card_type_lbl.grid(row=1, column=0)
        self.card_type_entry = tk.Entry(self,
                                        textvariable=self.card_type_var,
                                        readonlybackground='white')
        self.card_type_entry.grid(row=1, column=1)
        self.card_type_check_var = tk.IntVar()
        self.card_type_check = tk.Checkbutton(self, bd=2,
                                              variable=self.card_type_check_var,
                                              command=lambda: activate(self.card_type_entry),
                                              background=FINANCE_INFO_COLOR)
        self.card_type_check.grid(row=1, column=2)

        # card expiration date
        self.expire_var = tk.StringVar()
        self.expire_lbl = tk.Label(self, text="Expire date:",
                                   background=FINANCE_INFO_COLOR)
        self.expire_lbl.grid(row=1, column=3)
        self.expire_entry = tk.Entry(self,
                                     textvariable=self.expire_var,
                                     readonlybackground='white')
        self.expire_entry.grid(row=1, column=4)
        self.expire_check_var = tk.IntVar()
        self.expire_check = tk.Checkbutton(self, bd=2,
                                           variable=self.expire_check_var,
                                           command=lambda: activate(self.expire_entry),
                                           background=FINANCE_INFO_COLOR)
        self.expire_check.grid(row=1, column=5)

        # card Number
        self.card_number_var = tk.StringVar()
        self.card_number_lbl = tk.Label(self, text="Card Number:",
                                        background=FINANCE_INFO_COLOR)
        self.card_number_lbl.grid(row=2, column=0)
        self.card_number_entry = tk.Entry(self,
                                          textvariable=self.card_number_var,
                                          readonlybackground='white')
        self.card_number_entry.grid(row=2, column=1)
        self.card_number_check_var = tk.IntVar()
        self.card_number_check = tk.Checkbutton(self, bd=2,
                                                variable=self.card_number_check_var,
                                                command=lambda: activate(self.card_number_entry),
                                                background=FINANCE_INFO_COLOR)
        self.card_number_check.grid(row=2, column=2)

        # CVV
        self.cvv_var = tk.StringVar()
        self.cvv_lbl = tk.Label(self, text="CVV:",
                                background=FINANCE_INFO_COLOR)
        self.cvv_lbl.grid(row=2, column=3)
        self.cvv_entry = tk.Entry(self,
                                  textvariable=self.cvv_var,
                                  readonlybackground='white')
        self.cvv_entry.grid(row=2, column=4)
        self.cvv_check_var = tk.IntVar()
        self.cvv_check = tk.Checkbutton(self, bd=2,
                                        variable=self.cvv_check_var,
                                        command=lambda: activate(self.cvv_entry),
                                        background=FINANCE_INFO_COLOR)
        self.cvv_check.grid(row=2, column=5)
                        
        # Bank
        self.bank_var = tk.StringVar()
        self.bank_lbl = tk.Label(self, text="Bank:",
                                 background=FINANCE_INFO_COLOR)
        self.bank_lbl.grid(row=3, column=0)
        self.bank_entry = tk.Entry(self,
                                   textvariable=self.bank_var,
                                   readonlybackground='white')
        self.bank_entry.grid(row=3, column=1)
        self.bank_check_var = tk.IntVar()
        self.bank_check = tk.Checkbutton(self, bd=2,
                                         variable=self.bank_check_var,
                                         command=lambda: activate(self.bank_entry),
                                         background=FINANCE_INFO_COLOR)
        self.bank_check.grid(row=3, column=2)

        # IBAN 
        self.iban_var = tk.StringVar()
        self.iban_lbl = tk.Label(self, text="IBAN:",
                                 background=FINANCE_INFO_COLOR)
        self.iban_lbl.grid(row=3, column=3)
        self.iban_entry = tk.Entry(self,
                                   textvariable=self.iban_var,
                                   readonlybackground='white')
        self.iban_entry.grid(row=3, column=4)
        self.iban_check_var = tk.IntVar()
        self.iban_check = tk.Checkbutton(self, bd=2,
                                         command=lambda: activate(self.iban_entry),
                                         variable=self.iban_check_var,
                                         background=FINANCE_INFO_COLOR)
        self.iban_check.grid(row=3, column=5)

        # Finance comments
        self.fnc_comment_frame = tk.LabelFrame(self, text="Finance Comments",
                                               background=FINANCE_INFO_COLOR)
        self.fnc_comment_frame.grid(row=1, column=6, rowspan=2, columnspan=2,
                                    sticky='nswe')
        self.fnc_comment_txt = tk.Text(self.fnc_comment_frame,
                                       height=2, width=32)
        self.fnc_comment_txt.grid(row=0,column=0, sticky='nsew')

class TFRFailedTransactions(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, 
                               text="Last three failed transactions")
        self.BOLD   = tkFont.Font(family='Times', weight='bold')

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.date1_entry = tk.Entry(self)
        self.date2_entry = tk.Entry(self)
        self.date3_entry = tk.Entry(self)

        self.date1_entry.grid(row=0, column=0)
        self.date2_entry.grid(row=1, column=0)
        self.date3_entry.grid(row=2, column=0)

        self.why_failed1_entry = tk.Entry(self)
        self.why_failed2_entry = tk.Entry(self)
        self.why_failed3_entry = tk.Entry(self)
        
        self.why_failed1_entry.grid(row=0, column=1)
        self.why_failed2_entry.grid(row=1, column=1)
        self.why_failed3_entry.grid(row=2, column=1)

class TFRSuccessfullTransactions(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, 
                               text="Last three successful transactions")
        self.BOLD   = tkFont.Font(family='Times', weight='bold')
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.date1_entry = tk.Entry(self, width=10)
        self.date2_entry = tk.Entry(self, width=10)
        self.date3_entry = tk.Entry(self, width=10)

        self.date1_entry.grid(row=0, column=0)
        self.date2_entry.grid(row=1, column=0)
        self.date3_entry.grid(row=2, column=0)

        self.method1_entry = tk.Entry(self)
        self.method2_entry = tk.Entry(self)
        self.method3_entry = tk.Entry(self)
        
        self.method1_entry.grid(row=0, column=1)
        self.method2_entry.grid(row=1, column=1)
        self.method3_entry.grid(row=2, column=1)

        self.ammount1_entry = tk.Entry(self, width=6)
        self.ammount2_entry = tk.Entry(self, width=6)
        self.ammount3_entry = tk.Entry(self, width=6)
        
        self.ammount1_entry.grid(row=0, column=2)
        self.ammount2_entry.grid(row=1, column=2)
        self.ammount3_entry.grid(row=2, column=2)


class TFRLastInteractions(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master, 
                               text="Last three interactions")
        self.BOLD = tkFont.Font(family='Times', weight='bold')
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.date1_entry = tk.Entry(self)
        self.date2_entry = tk.Entry(self)
        self.date3_entry = tk.Entry(self)

        self.date1_entry.grid(row=0, column=0)
        self.date2_entry.grid(row=1, column=0)
        self.date3_entry.grid(row=2, column=0)

        self.interaction1_entry = tk.Entry(self)
        self.interaction2_entry = tk.Entry(self)
        self.interaction3_entry = tk.Entry(self)
        
        self.interaction1_entry.grid(row=0, column=1)
        self.interaction2_entry.grid(row=1, column=1)
        self.interaction3_entry.grid(row=2, column=1)

class TFRLastOnceOff(tk.LabelFrame):
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master,
                               text="Last once off donation")
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.date_entry = tk.Entry(self, width=10)
        self.date_entry.grid(row=0, column=0)
        
        self.method_entry = tk.Entry(self)
        self.method_entry.grid(row=0, column=1)

        self.amount_entry = tk.Entry(self, width=6)
        self.amount_entry.grid(row=0, column=2)
