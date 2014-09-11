
import datetime 

import Tkinter as tk
import tkMessageBox
import tkFont
import ttk
from socket import error as socket_error

import op_exceptions
import tfr_gui_supporter as gui
import tfr_operator as op
from tfr_gui_supporter import no_connection

INTERFACE_COLOR = '#B2D1B2'


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, background=INTERFACE_COLOR)
        self.BOLD   = tkFont.Font(family='Times', weight='bold')
        self.operator = op.TFROperator()
        self.grid()
        self.create_login()
        self.main_separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.main_separator.grid(row=0, column=1, rowspan=9, sticky='ns')
        self.in_logout_screen = False

    def create_login(self):
        self.login_form = tk.LabelFrame(self, text="Login")
        self.login_form.grid(row=0,column=0)
        
        # Username
        self.lookupid_lbl = tk.Label(self.login_form,
                                     font=self.BOLD, text="Lookup ID:")
        self.lookupid_lbl.grid(row=0, column=0)
        
        self.lookupid_var = tk.StringVar()
        self.lookupid_entry = tk.Entry(self.login_form,
                                       textvariable=self.lookupid_var)
        self.lookupid_entry.grid(row=0, column=1)

        # Password
        self.password_lbl = tk.Label(self.login_form,
                                     font=self.BOLD, text="Password:")
        self.password_lbl.grid(row=1, column=0)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.login_form, show='*',
                                       textvariable=self.password_var)
        self.password_entry.grid(row=1, column=1)
        
        # OK button
        self.ok_button = tk.Button(self.login_form, text="OK",
                                   command=self.password_accept)
        self.ok_button.grid(columnspan=2)
    
    @no_connection
    def password_accept(self):
        lookup_id = self.lookupid_var.get()
        password = self.password_var.get()
        try:
            self.operator.login(lookup_id, password)
            self.login_form.grid_remove()
            self.create_initial()
        except op_exceptions.IDError as e:
            tkMessageBox.showwarning('Login Error', e)
            self.lookupid_var.set('')
            self.password_var.set('')
        except op_exceptions.PWDError as e:
            tkMessageBox.showwarning('Login Error', e)
            self.password_var.set('')

    def create_initial(self):
        self.initial_frame = tk.Frame(self, background=INTERFACE_COLOR)
        self.initial_frame.grid(row=0, column=0)
        
        ## Call Counter
        self.call_counter_lbl = tk.Label(self.initial_frame,
                                         text='Supporters Called:',
                                         font=self.BOLD,
                                         background=INTERFACE_COLOR)
        self.call_counter_lbl.grid(row=0, column=0)
        self.call_counter_entry = tk.Entry(self.initial_frame,
                                           width=3,
                                           state='readonly',
                                           readonlybackground='white')
        self.call_counter_entry.grid(row=0, column=1)
        self.call_counter_sep = ttk.Separator(self.initial_frame,
                                             orient=tk.HORIZONTAL)
        self.call_counter_sep.grid(row=1, columnspan=2, sticky='ew')
        
        self.program_list_lbl = tk.Label(self.initial_frame,
                                         text='Available Programs',
                                         font=self.BOLD,
                                         background=INTERFACE_COLOR)
        self.program_list_lbl.grid(row=2,column=0, columnspan=2)
        # program list
        list_height = len(self.operator.active_programs)
        self.program_list = tk.Listbox(self.initial_frame, height=list_height,
                                       exportselection=0)
        self.program_list.grid(row=3, column=0, columnspan=2)

        # populate program list
        self.program_list.height = list_height
        for program in self.operator.active_programs:
            self.program_list.insert(tk.END, program)
            
        # program list button
        self.button_frame = tk.Frame(self.initial_frame, pady=6,
                                     background=INTERFACE_COLOR)
        self.button_frame.grid(row=4, column=0, columnspan=2)
        self.program_list_button = tk.Button(self.button_frame, 
                                             text='Choose Program',
                                             command=self.choose_program,
                                             background=INTERFACE_COLOR)
        self.program_list_button.grid(row=0, column=0)

        self.create_supporter_button()
        self.create_arranged_calls()
        self.create_postponed_calls()
        
        self.supporter_form = gui.TFRSupporterForm(self.operator, self)
        self.supporter_form.grid(row=0, rowspan=4, column=1)
        
    def choose_program(self):
        try:
            selection = int(self.program_list.curselection()[0])
            program = self.program_list.get(selection)
            self.operator.choose_program(program)
            tkMessageBox.showinfo('Program Choice', 
                                  'You are now calling {}'.format(program))
        except IndexError:
            tkMessageBox.showerror('Program Choice',
                                   'You have not picked a program')
            
                                    
    def create_supporter_button(self):
        self.supporter_frame = tk.Frame(self, pady=6,
                                        background=INTERFACE_COLOR)
        self.supporter_frame.grid(row=1, column=0)
        
        self.prog_separator = ttk.Separator(self.supporter_frame, 
                                            orient=tk.HORIZONTAL)
        self.prog_separator.grid(row=0, column=0, sticky = "ew")

        self.supporter_label = tk.Label(self.supporter_frame, text="Supporters",
                                        font=self.BOLD,
                                        background=INTERFACE_COLOR)
        self.supporter_label.grid(row=1, column=0)
        
        self.sup_button_frame = tk.Frame(self.supporter_frame, pady=6,
                                         background=INTERFACE_COLOR)
        self.sup_button_frame.grid(row=2, column=0)
        
        self.supporter_button = tk.Button(self.sup_button_frame,
                                          text='Next supporter',
                                          command=self.next_supporter,
                                          background=INTERFACE_COLOR)
        self.supporter_button.grid(row=0, column=0)

        self.prev_button_frame = tk.Frame(self.supporter_frame, pady=6,
                                          background=INTERFACE_COLOR)
        self.prev_button_frame.grid(row=3, column=0)
        self.previous_button = tk.Button(self.prev_button_frame,
                                         text='Previous Supporter',
                                         command=self.previous_supporter,
                                         background=INTERFACE_COLOR)

        self.previous_button.grid(row=0, column=0)
        # Separator
        self.supp_by_id_separator = ttk.Separator(self.supporter_frame, 
                                                  orient=tk.HORIZONTAL)
        self.supp_by_id_separator.grid(row=4, column=0, sticky = "ew")

        ### Supporter by id
        self.sup_by_id_frame = tk.Frame(self.supporter_frame, pady=6,
                                        background=INTERFACE_COLOR)
        self.sup_by_id_frame.grid(row=5, column=0)
        # Supporter id 
        self.sup_by_id_label = tk.Label(self.sup_by_id_frame, text="Supporter ID:",
                                        font=self.BOLD,
                                        background=INTERFACE_COLOR)
        self.sup_by_id_label.grid(row=0, column=0)
        self.sup_by_id_entry = tk.Entry(self.sup_by_id_frame, width=12)
        self.sup_by_id_entry.grid(row=0, column=1)
        # Program
        self.program_id_label = tk.Label(self.sup_by_id_frame, text='Program Name:',
                                         font=self.BOLD,
                                         background=INTERFACE_COLOR)
        self.program_id_label.grid(row=1, column=0)
        self.program_id_entry = tk.Entry(self.sup_by_id_frame, width=12)
        self.program_id_entry.grid(row=1, column=1)
        # Button
        self.sup_by_id_button_frame = tk.Frame(self.sup_by_id_frame, pady=6,
                                               background=INTERFACE_COLOR)
        self.sup_by_id_button_frame.grid(row=2, column=0, columnspan=2)
        self.sup_by_id_button = tk.Button(self.sup_by_id_button_frame,
                                          text='Get Supporter by ID', 
                                          command=self.supporter_by_id,
                                          background=INTERFACE_COLOR)
        self.sup_by_id_button.grid()
        
    def refresh_calls_made(self):
        counter = self.operator.no_of_calls
        self.call_counter_entry.configure(state=tk.NORMAL)
        self.call_counter_entry.delete(0, tk.END)
        self.call_counter_entry.insert(0, str(counter))
        self.call_counter_entry.configure(state='readonly')
        
    @no_connection
    def next_supporter(self):
        if self.operator.chosen_program is None:
            tkMessageBox.showerror('Program choice',
                                   'You have not picked a program.')
        else:
            try:
                self.operator.get_next_active_supporter()
                self.supporter_form.clear_form()
                self.supporter_form.fill_form()
                self.supporter_form.interactions.interactions_button.configure(state=tk.NORMAL)
                self.operator.no_of_calls += 1
                self.refresh_calls_made()
            except op_exceptions.NoMoreSupportersError as e:
                tkMessageBox.showwarning('Active supporters', e)

    def previous_supporter(self):
        if self.operator.previous_supporters != []:
            try:
                self.operator.previous_supporter()
                self.supporter_form.clear_form()
                self.supporter_form.fill_form()
                self.supporter_form.interactions.interactions_button.configure(state=tk.NORMAL)
            except op_exceptions.NoPreviousSupporter as e:
                tkMessageBox.showwarning('Previous supporters', e)
        
    @no_connection
    def supporter_by_id(self):
        lookup_id = self.sup_by_id_entry.get()
        program = self.program_id_entry.get()
        try:
            self.operator.get_supporter_by_id(lookup_id, program)
            self.supporter_form.clear_form()
            self.supporter_form.fill_form()
        except op_exceptions.ProgramError as e:
            tkMessageBox.showerror('Find Supporter By ID', e)
        except op_exceptions.SupporterIDError as e:
            tkMessageBox.showerror('Find Supporter By ID', e)
        except op_exceptions.IsBeingCalledError as e:
            tkMessageBox.showerror('Find Supporter By ID', e)
        ###???###
        #else:
        #    self.operator.get_next_active_supporter()
        #    self.supporter_form = gui.TFRSupporterForm(self.operator)
        #    self.supporter_form.grid(row=0, column=1)

    def create_postponed_calls(self):
        self.postponed_frame = tk.Frame(self,
                                        background=INTERFACE_COLOR)
        self.postponed_frame.grid(row=2, column=0, pady=4, padx=6)
        self.post_separator = ttk.Separator(self.postponed_frame,
                                            orient=tk.HORIZONTAL)
        self.post_separator.grid(row=0, column=0, columnspan=5,
                                 sticky='ew')

        self.postponed_lbl = tk.Label(self.postponed_frame,
                                      text='Postponed Calls', font=self.BOLD,
                                      background=INTERFACE_COLOR)
        self.postponed_lbl.grid(row=1, columnspan=4, sticky='w')

        self.psp_index_list = tk.Listbox(self.postponed_frame, width=2,
                                         height=4 ,exportselection=0)
        self.psp_index_list.grid(row=2, column=0)
        self.psp_index_list.bind('<<ListboxSelect>>', self.psp_onselect)

        self.psp_program_list = tk.Listbox(self.postponed_frame, width=12,
                                           height=4, exportselection=0)
        self.psp_program_list.grid(row=2, column=1)
        self.psp_program_list.bind('<<ListboxSelect>>', self.psp_onselect)

        self.psp_time_called_list = tk.Listbox(self.postponed_frame, width=6,
                                               height=4, exportselection=0)
        self.psp_time_called_list.grid(row=2, column=2)
        self.psp_time_called_list.bind('<<ListboxSelect>>', self.psp_onselect)

        self.psp_comment_list = tk.Listbox(self.postponed_frame, width=15,
                                           height=4, exportselection=0)
        self.psp_comment_list.grid(row=2, column=3)
        self.psp_comment_list.bind('<<ListboxSelect>>', self.psp_onselect)

        self.psp_listboxes = [self.psp_program_list,
                              self.psp_time_called_list,
                              self.psp_index_list,
                              self.psp_comment_list]

        self.psp_button_frame = tk.Frame(self.postponed_frame, pady=6, padx=6,
                                         background=INTERFACE_COLOR)
        self.psp_button_frame.grid(row=3, columnspan=4)
        self.psp_button = tk.Button(self.psp_button_frame,
                                    text='Get Postponed Call',
                                    command=self.get_postponed_call,
                                    background=INTERFACE_COLOR)
        self.psp_button.grid()
                                           
    def psp_onselect(self, event):
        widget = event.widget
        index = int(widget.curselection()[0])
        for wdg in self.psp_listboxes:
            size = wdg.size()
            if wdg is not widget:
                wdg.selection_clear(0, size)
                wdg.selection_set(index)

    def fill_postponed_calls(self):
        list_size = 4
        psp_list = self.operator.postponed_calls
        for entry in psp_list:
            time = entry[1].strftime('%H:%M')
            self.psp_index_list.insert(tk.END, entry[0])
            self.psp_program_list.insert(tk.END, entry[2])
            self.psp_time_called_list.insert(tk.END, time)
            self.psp_comment_list.insert(tk.END, entry[4])

    def clear_postponed_calls(self):
        list_size = 4
        for listbox in self.psp_listboxes:
            listbox.delete(0, tk.END)
        
    def refresh_postponed_list(self):
        self.clear_postponed_calls()
        self.fill_postponed_calls()            

    def get_postponed_call(self):
        """Get the postponed call of the operator's choice."""
        try:
            selection = int(self.psp_index_list.curselection()[0])
            psp_id = self.psp_index_list.get(selection)
            self.operator.get_postponed_call(psp_id)
            self.supporter_form.clear_form()
            self.supporter_form.fill_form()
            self.refresh_postponed_list()
        except IndexError as e:
            tkMessageBox.showerror('Postponed calls',
                                   'You did not choose a postponed call.')

    def create_arranged_calls(self):
        self.arranged_frame = tk.Frame(self,
                                       background=INTERFACE_COLOR)
        self.arranged_frame.grid(row=3, column=0, pady=10, padx=6)
        self.arr_separator = ttk.Separator(self.arranged_frame, 
                                            orient=tk.HORIZONTAL)
        self.arr_separator.grid(row=0, column=0, columnspan=5,
                                sticky = "ew")
    
        
        self.arranged_lbl = tk.Label(self.arranged_frame,
                                     text='Scheduled Calls', font=self.BOLD,
                                     background=INTERFACE_COLOR)
        self.arranged_lbl.grid(row=1, columnspan=4, sticky='w')
        # call_number
        self.call_number_list = tk.Listbox(self.arranged_frame, height=8, 
                                           width=4, exportselection=0)
        self.call_number_list.grid(row=2, column=0)
        self.call_number_list.bind('<<ListboxSelect>>', self.onselect)
        # program_name
        self.program_name_list = tk.Listbox(self.arranged_frame, height=8,
                                            width=10, exportselection=0)
        self.program_name_list.grid(row=2, column=1)
        self.program_name_list.bind('<<ListboxSelect>>', self.onselect)
        # datetime
        self.call_datetime_list = tk.Listbox(self.arranged_frame, height=8,
                                             width=10, exportselection=0)
        self.call_datetime_list.grid(row=2, column=2)
        self.call_datetime_list.bind('<<ListboxSelect>>', self.onselect)
        # comments 
        self.comments_list = tk.Listbox(self.arranged_frame, height=8,
                                        width=16, exportselection=0)
        self.comments_list.bind('<<ListboxSelect>>', self.onselect)
        self.comments_list.grid(row=2, column=3)
        
        self.fill_scheduled_calls()
        self.sch_listboxes = [self.call_number_list,
                              self.program_name_list,
                              self.call_datetime_list,
                              self.comments_list]

        self.arr_button_frame = tk.Frame(self.arranged_frame, pady=6,
                                         background=INTERFACE_COLOR)
        self.arr_button_frame.grid(row=3, column=2, columnspan=2)

        self.arranged_button = tk.Button(self.arr_button_frame,
                                         text="Get call",
                                         command=self.get_scheduled_call,
                                         background=INTERFACE_COLOR)
        self.arranged_button.grid(row=0, column=0)

        self.refr_button_frame = tk.Frame(self.arranged_frame, pady=6,
                                          background=INTERFACE_COLOR)
        self.refr_button_frame.grid(row=3, column=1, columnspan=2)

        self.refresh_button = tk.Button(self.refr_button_frame, 
                                        text="Refresh List",
                                        command=self.refresh_sch_list,
                                        background=INTERFACE_COLOR)
        self.refresh_button.grid(row=0, column=0)

        self.log_separator = ttk.Separator(self.arranged_frame, 
                                           orient=tk.HORIZONTAL)
        self.log_separator.grid(row=4, column=0, sticky = "ew", columnspan=6)
        
        self.log_button_frame = tk.Frame(self.arranged_frame, pady=6,
                                         background=INTERFACE_COLOR)
        self.log_button_frame.grid(row=5, columnspan=4)
        
        self.log_button = tk.Button(self.log_button_frame, 
                                    text="Logout",
                                    command=self.deploy_logout_screen,
                                    background=INTERFACE_COLOR)
        self.log_button.grid()

    def fill_scheduled_calls(self):
        listboxes_height = 8
        sch_list = self.operator.scheduled_call_list
        for entry in sch_list[:listboxes_height]:
            for call_tuple in entry:
                field, value = call_tuple
                if field == 'scheduled_id':
                    self.call_number_list.insert(tk.END, value)
                if field == 'program':
                    self.program_name_list.insert(tk.END, value)
                if field == 'datetime':
                    formatted = value.strftime('%d-%m %H:%M')
                    self.call_datetime_list.insert(tk.END, formatted)
                if field == 'operator_comments':
                    self.comments_list.insert(tk.END, value)

    def clear_scheduled_calls(self):
        listboxes_height = 8
        for listbox in self.sch_listboxes:
            listbox.delete(0, tk.END)
            
    def refresh_scheduled_calls(self):
        self.clear_scheduled_calls()
        self.fill_scheduled_calls()

    def onselect(self, event):
        widget = event.widget
        index = int(widget.curselection()[0])
        for wdg in self.sch_listboxes:
            size = wdg.size()
            if wdg is not widget:
                wdg.selection_clear(0, size)
                wdg.selection_set(index)
                
    @no_connection
    def get_scheduled_call(self):
        """Get scheduled call based on the call id.
        
        The call id is provided by the first listbox.
        """
        selection = int(self.call_number_list.curselection()[0])
        call_id = self.call_number_list.get(selection)
        self.operator.get_scheduled_call(call_id)
        self.supporter_form.clear_form()
        self.supporter_form.fill_form()
        ### Fill comment form with comment from scheduled call
        self.supporter_form.calls.sch_comments_entry.insert('0.0', 
                                                            self.operator.scheduled_call_comment)
        self.operator.set_scheduled_call_list()
        self.refresh_scheduled_calls()

    @no_connection
    def refresh_sch_list(self):
        self.operator.set_scheduled_call_list()
        self.refresh_scheduled_calls()

    def deploy_logout_screen(self):
        """Alternate between the logout screen and the supporter screen."""
        if self.in_logout_screen:
            self.logout_frame.grid_forget()
            self.supporter_form.grid(row=0, column=2, rowspan=4)
            self.in_logout_screen = False
        else:
            self.supporter_form.grid_forget()
            if hasattr(self, 'logout_frame'):
                self.logout_frame.grid(row=0, column=2)
            else:
                self.create_logout_screen()
            self.in_logout_screen = True
        
    def create_logout_screen(self):
        self.logout_frame = tk.LabelFrame(self, text='Logout Screen',
                                          pady=6, padx=6)
        self.logout_frame.grid(row=0, column=2)
        self.prog_lbl = tk.Label(self.logout_frame, text="Programs")
        self.prog_lbl.grid(row=0, column=0)
        self.prog_list1 = tk.Listbox(self.logout_frame, height=1, width=15,
                                     exportselection=0)
        self.prog_list1.grid(row=1, column=0)
        self.prog_list2 = tk.Listbox(self.logout_frame, height=1, width=15,
                                     exportselection=0)
        self.prog_list2.grid(row=2, column=0)
        self.prog_list3 = tk.Listbox(self.logout_frame, height=1, width=15,
                                     exportselection=0)
        self.prog_list3.grid(row=3, column=0)
        self.prog_list4 = tk.Listbox(self.logout_frame, height=1, width=15,
                                     exportselection=0)
        self.prog_list4.grid(row=4, column=0)
        
        self.prog_list = [self.prog_list1,
                          self.prog_list2,
                          self.prog_list3,
                          self.prog_list4]

        self.clear1 = tk.Button(self.logout_frame, text='..',
                                command=lambda: self.clear(self.prog_list1))
        self.clear1.grid(row=1, column=1)
        self.clear2 = tk.Button(self.logout_frame, text='..',
                                command=lambda: self.clear(self.prog_list2))
        self.clear2.grid(row=2, column=1)
        self.clear3 = tk.Button(self.logout_frame, text='..',
                                command=lambda: self.clear(self.prog_list3))
        self.clear3.grid(row=3, column=1)
        self.clear4 = tk.Button(self.logout_frame, text='..',
                                command=lambda: self.clear(self.prog_list4))
        self.clear4.grid(row=4, column=1)
        
        ### Start and end time of shift
        
        self.total_hours_lbl = tk.Label(self.logout_frame, text="Hours")
        self.total_hours_lbl.grid(row=0, column=2)
        self.total_hours1 = tk.Entry(self.logout_frame, width=3)
        self.total_hours1.grid(row=1, column=2)
        self.total_hours2 = tk.Entry(self.logout_frame, width=3)
        self.total_hours2.grid(row=2, column=2)
        self.total_hours3 = tk.Entry(self.logout_frame, width=3)
        self.total_hours3.grid(row=3, column=2)
        self.total_hours4 = tk.Entry(self.logout_frame, width=3)
        self.total_hours4.grid(row=4, column=2)

        self.s_sep1 = tk.Label(self.logout_frame, text="--")
        self.s_sep1.grid(row=1, column=3)
        self.s_sep2 = tk.Label(self.logout_frame, text="--")
        self.s_sep2.grid(row=2, column=3)
        self.s_sep3 = tk.Label(self.logout_frame, text="--")
        self.s_sep3.grid(row=3, column=3)
        self.s_sep4 = tk.Label(self.logout_frame, text="--")
        self.s_sep4.grid(row=4, column=3)
                               
        self.start_hour_lbl = tk.Label(self.logout_frame, text="Start")
        self.start_hour_lbl.grid(row=0, column=4, columnspan=3)
        self.start_hour1 = tk.Entry(self.logout_frame, width=2)
        self.start_hour1.grid(row=1, column=4)
        self.start_hour2 = tk.Entry(self.logout_frame, width=2)
        self.start_hour2.grid(row=2, column=4) 
        self.start_hour3 = tk.Entry(self.logout_frame, width=2)
        self.start_hour3.grid(row=3, column=4) 
        self.start_hour4 = tk.Entry(self.logout_frame, width=2)
        self.start_hour4.grid(row=4, column=4) 
 
        self.start_sep1 = tk.Label(self.logout_frame, text=":")
        self.start_sep1.grid(row=1, column=5)
        self.start_sep2 = tk.Label(self.logout_frame, text=":")
        self.start_sep2.grid(row=2, column=5)
        self.start_sep3 = tk.Label(self.logout_frame, text=":")
        self.start_sep3.grid(row=3, column=5)
        self.start_sep4 = tk.Label(self.logout_frame, text=":")
        self.start_sep4.grid(row=4, column=5)

        self.start_min1 = tk.Entry(self.logout_frame, width=2)
        self.start_min1.grid(row=1, column=6) 
        self.start_min2 = tk.Entry(self.logout_frame, width=2)
        self.start_min2.grid(row=2, column=6) 
        self.start_min3 = tk.Entry(self.logout_frame, width=2)
        self.start_min3.grid(row=3, column=6) 
        self.start_min4 = tk.Entry(self.logout_frame, width=2)
        self.start_min4.grid(row=4, column=6) 

        self.e_sep1 = tk.Label(self.logout_frame, text="--")
        self.e_sep1.grid(row=1, column=7)
        self.e_sep2 = tk.Label(self.logout_frame, text="--")
        self.e_sep2.grid(row=2, column=7)
        self.e_sep3 = tk.Label(self.logout_frame, text="--")
        self.e_sep3.grid(row=3, column=7)
        self.e_sep4 = tk.Label(self.logout_frame, text="--")
        self.e_sep4.grid(row=4, column=7)

        self.end_hour_lbl = tk.Label(self.logout_frame, text="End")
        self.end_hour_lbl.grid(row=0, column=8, columnspan=3)
        self.end_hour1 = tk.Entry(self.logout_frame, width=2)
        self.end_hour1.grid(row=1, column=8) 
        self.end_hour2 = tk.Entry(self.logout_frame, width=2)
        self.end_hour2.grid(row=2, column=8) 
        self.end_hour3 = tk.Entry(self.logout_frame, width=2)
        self.end_hour3.grid(row=3, column=8) 
        self.end_hour4 = tk.Entry(self.logout_frame, width=2)
        self.end_hour4.grid(row=4, column=8) 
 
        self.end_sep1 = tk.Label(self.logout_frame, text=":")
        self.end_sep1.grid(row=1, column=9)
        self.end_sep2 = tk.Label(self.logout_frame, text=":")
        self.end_sep2.grid(row=2, column=9)
        self.end_sep3 = tk.Label(self.logout_frame, text=":")
        self.end_sep3.grid(row=3, column=9)
        self.end_sep4 = tk.Label(self.logout_frame, text=":")
        self.end_sep4.grid(row=4, column=9)

        self.end_min1 = tk.Entry(self.logout_frame, width=2)
        self.end_min1.grid(row=1, column=10) 
        self.end_min2 = tk.Entry(self.logout_frame, width=2)
        self.end_min2.grid(row=2, column=10) 
        self.end_min3 = tk.Entry(self.logout_frame, width=2)
        self.end_min3.grid(row=3, column=10) 
        self.end_min4 = tk.Entry(self.logout_frame, width=2)
        self.end_min4.grid(row=4, column=10) 

        self.hours_list = [self.total_hours1, 
                           self.total_hours2, 
                           self.total_hours3, 
                           self.total_hours4]
        
        self.start_end_list = [(self.start_hour1, self.start_min1, self.end_hour1, self.end_min1),
                               (self.start_hour2, self.start_min2, self.end_hour2, self.end_min2),
                               (self.start_hour3, self.start_min3, self.end_hour3, self.end_min3),
                               (self.start_hour4, self.start_min4, self.end_hour4, self.end_min4)]

        self.commit_button_frame = tk.Frame(self.logout_frame, padx=6, pady=6)
        self.commit_button_frame.grid(row=6, column=0 , columnspan=3)
        self.commit_hours_button = tk.Button(self.commit_button_frame,
                                             text='Commit hours and exit porgram.',
                                             command=self.commit_shift)
        self.commit_hours_button.grid()
        self.fill_program_lists()
        
    def clear(self, pr_list):
        pr_list.selection_clear(0, tk.END)

    def fill_program_lists(self):
        for program in self.operator.active_programs:
            self.prog_list1.insert(tk.END, program)
            self.prog_list2.insert(tk.END, program)
            self.prog_list3.insert(tk.END, program)
            self.prog_list4.insert(tk.END, program)
    
    
    def get_shift_hours(self):
        shifts_list = zip(self.prog_list, self.hours_list, self.start_end_list)
        checked_shift_list = []
        for prog, hour, start_end in shifts_list:
            try:
                selection = int(prog.curselection()[0])
                program = prog.get(selection)
                hours = hour.get()
                start_hour, start_min, end_hour, end_min = start_end
                s_hour = start_hour.get()
                s_min = start_min.get()
                e_hour = end_hour.get()
                e_min = end_min.get()
                checked_shift_list.append((program, hours, s_hour, s_min, e_hour, e_min))
            except IndexError as e:                
                pass
        return checked_shift_list
        
    def create_shift_list(self, shift_list):
        returned_list = []
        for prog, hour, s_hour, s_min, e_hour, e_min in shift_list:
            try:
                hour = int(hour)
                s_hour = int(s_hour)
                s_min = int(s_min)
                e_hour = int(e_hour)
                e_min = int(e_min)
                s_time = datetime.time(s_hour, s_min)
                e_time = datetime.time(e_hour, e_min)
                returned_list.append((prog, hour, s_time, e_time))
            except ValueError as e:
                return False
        return returned_list

    @no_connection
    def commit_shift(self):
        shift_list = self.create_shift_list(self.get_shift_hours())
        if shift_list == []:
            tkMessageBox.showerror('Shift Reporting Error',
                                   'You did not choose any program.')
        elif shift_list == False:
            tkMessageBox.showerror('Shift Reporting Error',
                                   'Wrong shift hours input.')
        else:
            if tkMessageBox.askokcancel('Reporting your shift',
                                        'Report hours and exit?'):
                self.operator.update_shift(shift_list)
                self.operator.update_calls_made()
                self.quit()

if __name__=='__main__':
    master = tk.Tk()
    master.title = 'TFR Program'

    frameSizeX = 1073
    frameSizeY = 848
    framePosX = 80
    framePosY = 80

    master.geometry("%sx%s+%s+%s" % (frameSizeX, frameSizeY,
                                     framePosX, framePosY))
    
    frame = tk.Frame(master)
    frame.pack(fill=tk.BOTH, expand=1)

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=1)

    def _on_mousewheel(event):
        canvas.yview_scroll(-1*(event.delta/120), "units")

    canvas = tk.Canvas(frame,
                       yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    scrollbar.config(command=canvas.yview)

    def _on_mousewheel(event):
        canvas.yview_scroll(-1*(event.delta/120), "units")

    app = Application(canvas)
    app_id = canvas.create_window(0, 0, window=app,
                                  anchor=tk.NW)
    def _configure_app(event):
        size = (app.winfo_reqwidth(), app.winfo_reqheight())
        canvas.config(scrollregion="0 0 %s %s" % size)
        if app.winfo_reqwidth() != canvas.winfo_width():
            canvas.config(width=app.winfo_reqwidth())
    app.bind('<Configure>', _configure_app)

    def _configure_canvas(event):
        if app.winfo_reqwidth() != canvas.winfo_width():
            canvas.itemconfigure(app_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

    master.mainloop()


        
        
