import wx
import wx.lib.newevent
import socket
import asyncore
import threading
import Queue

to_network = Queue.Queue()
LogEvent, EVT_LOG_EVENT = wx.lib.newevent.NewEvent()

#for high bandwidth applications, you are going to want to handle the
#out_buffer via a different mechanism, perhaps similar to asynchat or
#otherwise
class DispatcherConnection(asyncore.dispatcher_with_send):
    def __init__(self, connection, mainwindow):
        self.mainwindow = mainwindow
        asyncore.dispatcher_with_send.__init__(self, connection)
    def writable(self):
        return bool(self.out_buffer)
    def handle_write(self):
        self.initiate_send()
    def log(self, message):
        self.mainwindow.LogString(message, sock=self)
    def log_info(self, message, type='info'):
        if type != 'info':
            self.log(message)
    def handle_close(self):
        self.log("Connection dropped: %s"%(self.addr,))
        self.close()
    
    #implement your client logic as a subclass

class LineEchoConnection(DispatcherConnection):
    inc_buffer = ''
    def handle_read(self):
        self.inc_buffer += self.recv(512)
        while '\n' in self.inc_buffer:
            snd, self.inc_buffer = self.inc_buffer.split('\n', 1)
            snd += '\n'
            self.log("Line from %s: %r"%(self.addr, snd))
            self.send(snd)

class DispatcherServer(asyncore.dispatcher):
    def __init__(self, host, port, mainwindow, factory=LineEchoConnection):
        self.mainwindow = mainwindow
        self.factory = factory
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)
    def handle_accept(self):
        connection, info = self.accept()
        self.mainwindow.LogString("Got connection: %s"%(info,), sock=self)
        self.factory(connection, self.mainwindow)

def loop():
    while 1:
        while not to_network.empty():
            message = to_network.get()
            #process and handle message
            #
            #remember to validate any possible
            #socket objects recieved from the GUI,
            #they could already be closed
        asyncore.poll(timeout=.01)

class MainWindow(wx.Frame):
    def __init__(self, host, port, threaded=0):
        wx.Frame.__init__(self, None, title="Sample echo server")
        
        #add any other GUI objects here
        
        sz = wx.BoxSizer(wx.VERTICAL)
        self.log = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE|wx.TE_RICH2)
        sz.Add(self.log, 1, wx.EXPAND|wx.ALL, 3)
        
        self.Bind(EVT_LOG_EVENT, self.LogEvent)
        DispatcherServer(host, port, self)
        if not threaded:
            self.poller = wx.Timer(self, wx.NewId())
            self.Bind(wx.EVT_TIMER, self.OnPoll)
            #poll 50 times/second, should be enough for low-bandwidth apps
            self.poller.Start(20, wx.TIMER_CONTINUOUS)
        else:
            t = threading.Thread(target=loop)
            t.setDaemon(1)
            t.start()
    
    def LogString(self, message, **kwargs):
        event = LogEvent(msg=message, **kwargs)
        if threading.activeCount() == 1:
            self.LogEvent(event)
        else:
            wx.PostEvent(self, event)
    
    def LogEvent(self, evt):
        self.log.AppendText(evt.msg)
        if not evt.msg.endswith('\n'):
            self.log.AppendText('\n')

    def OnPoll(self, evt):
        asyncore.poll(timeout=0)
    #add other methods as necessary

if __name__ == '__main__':
    a = wx.App(0)
    b = MainWindow('localhost', 1199, 0)
    b.Show(1)
    a.MainLoop()
