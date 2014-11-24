import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import threading

import tfr_agent

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "TFRAgent"
    _svc_display_name_ = "TFR Agent"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.agent.shutdown()

    def SvcDoRun(self):
        import tfr_agent
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        IP = tfr_agent.IP
        PORT = tfr_agent.PORT
        address = (IP, PORT)
        self.agent = tfr_agent.ThreadedTCPServer(address, tfr_agent.ThreadedTCPRequestHandler)
        self.agent.serve_forever()
            

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
