import wx,wx.py
from wx.py.dispatcher import connect, send, Anonymous

# Create unique id() for separate sender classes
# This allows us to have a class of senders.  The usual approach is
# to simply let the widget itself be the sender.  The send() and
# connect() sides of the signalling must agree on signal names,
# sender classes and extra keyword attributes.
class Sender: pass
plottable_sender = Sender()
catalog_sender = Sender()

# Define a message receiver
class Receiver(wx.Button):
  def onHello(self,who=None): 
    print 'hi to',self.GetLabel(),'from',who

# Create the app with buttons for sending and slots for receiving
app = wx.App(redirect=False)
root = wx.Frame(None)
bs = wx.BoxSizer(wx.HORIZONTAL)

# Create slot and tell to expect connections from signal special and
# extraspecial; it accepts signals from any sender
f1 = Receiver(root,-1,'Receiver 1')
bs.Add(f1)
connect(f1.onHello,signal='special')
connect(f1.onHello,signal='extraspecial')

# Create slot for 'special' from catalog_sender, whatever that is.
f3 = Receiver(root,-1,'Receiver 2')
bs.Add(f3)
connect(f3.onHello,signal='special',sender=catalog_sender)

# Define a parameterized event handler which can produce the
# appropriate signal type given a button press event.
def signaller(signal,who,sender=Anonymous):
  def sendsignal(event): send(signal,sender=sender,who=who)
  return sendsignal

f2 = wx.Button(root,-1,'Sender 1')
f2.Bind(wx.EVT_BUTTON,signaller('special','Sender 1',plottable_sender))
bs.Add(f2)

f4 = wx.Button(root,-1,'Sender 2')
f4.Bind(wx.EVT_BUTTON,signaller('special','Sender 2',catalog_sender))
bs.Add(f4)

f5 = wx.Button(root,-1,'Sender extraspecial')
f5.Bind(wx.EVT_BUTTON,signaller('extraspecial','Sender extraspecial',catalog_sender))
bs.Add(f5)


root.SetSizer(bs)
root.Show()

app.MainLoop()
