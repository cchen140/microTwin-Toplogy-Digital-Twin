import time

import stomp
import javaobj  #pip install javaobj-py3


class Wrapper(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)
    def on_message(self, headers, message):
        print('received a message "%s"' % message)
        #jobj = self.read_file("obj5.ser")
        pobj = javaobj.loads(message)
        print(pobj)
    def on_receipt(self, headers, body):
        print("Hi")
    def on_receiver_loop_completed(self, headers, body):
        print("Hi2")
    def __init__(self):
        conn = stomp.Connection([('127.0.0.1', 61613)])
        conn.set_listener('', self)
        conn.start()
        conn.connect('admin', 'password', wait=True)
        conn.subscribe(destination='/topic/test topic', id=1, ack='auto', transformation='jms-object-xml')
        #conn.send(body='Test test message.', destination='/topic/test topic')
        conn.send(destination='/topic/test topic', body=str.encode("Test test message"))

        #conn.subscribe(destination=queue, id=123421, ack='auto')

        while 1:
            time.sleep(2)

        conn.disconnect()

if (__name__ == '__main__'):
    testPublisher = Wrapper()
