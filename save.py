import time
import requests
while True:
    t = time.localtime()

    out = ("%d-%d-%d-%d-%d-%d.mp3" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))

    print(out)
    time.sleep(2)

    stream_url = "http://scturkmedya.radyotvonline.com/stream/80/"
    r = requests.get(stream_url, stream=True)

    with open(out, 'wb') as f:
        for block in r.iter_content(1024):

            f.write(block)
            break
