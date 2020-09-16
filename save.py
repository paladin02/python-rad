import threading
import time
import requests
exitFlag = 0
while True:
   class myThread (threading.Thread):

      def __init__(self, threadID, name, counter):
         threading.Thread.__init__(self)
         self.threadID = threadID
         self.name = name
         self.counter = counter

      def run(self):
         print ("Starting " + self.name)
         print_time(self.name, self.counter, 86400)
         print ("Exiting " + self.name)

   def print_time(threadName, delay, counter):
      while counter:
         if exitFlag:
            threadName.exit()
         time.sleep(delay)
         print ("%s: %s" % (threadName, time.ctime(time.time())))
         counter -= 1

   thread1 = myThread(1, "stream.mp3", 1)

   thread1.start()
   stream_url = "http://scturkmedya.radyotvonline.com/stream/80/"
   r = requests.get(stream_url, stream=True)
   with open('stream.mp3', 'wb') as f:
      try:
         for block in r.iter_content(1024):
            f.write(block)
      except KeyboardInterrupt:
         pass
   thread1.join()


