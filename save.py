import sys
import time
import requests
from pydub import AudioSegment
while True:
    DELAY = 1 * 1 * 1
    t = time.localtime()
    out = ("%d-%d-%d-%d-%d-%d.mp3" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
    time.sleep(DELAY)
    print(out)

    files_path = "C:\\Users\\hp\\PycharmProjects\\orenıoz\\"
    file_name = out

    startMin = 0
    startSec = 00

    endMin = 0
    endSec = 8
    startTime = startMin * 1 * 1 + startSec * 1
    endTime = endMin * 1 * 1 + endSec * 1

    stream_url = "http://scturkmedya.radyotvonline.com/stream/80/"
    r = requests.get(stream_url, stream=True)
    with open(out, 'wb') as f:
        try:
            for block in r.iter_content(1024):
                f.write(block)
        except KeyboardInterrupt:
            pass

    song = AudioSegment.from_mp3(files_path + file_name)
    extract = song[startTime: endTime]
    extract.export(file_name + '-extract.mp3', format="mp3")
