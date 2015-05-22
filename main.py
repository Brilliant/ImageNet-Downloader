from multiprocessing.dummy import Pool
import logging
import os
import threading
import urllib2

TARGET = "target"
PATH = "/tmp/save/"
URL = "http://image-net.org/api/text/imagenet.synset.geturls?wnid="
POOLSIZE = 128
TIMEOUT = 44
logging.basicConfig(filename = "download.log", filemode = "a", format = '%(asctime)s %(levelname)s: %(message)s', level = logging.WARNING)

def download(url, path):
    try:
        data = urllib2.urlopen(url, timeout = 44).read()
    except:
        logging.warning("%s %s", url, path)
        return 
    obj = open(path, "wb")
    obj.write(data)
    obj.close()
def download_helper(s):
    s = s.split();
    download(s[0], s[-1])

def prepare_list(wnid):
    url = URL + wnid
    path = PATH + wnid
    if not os.path.exists(path):
        os.mkdir(path)
    target = os.path.join(path, wnid)
    download(url, target)
    item = []
    count = 0
    aim = open(target)
    for url in aim:
        url = url.strip()
        if url == "":
            continue
        prefix = ("0000" + str(count))[-4:]
        suffix = url[-9:].replace('/', '\\')
        name = prefix + "_" + suffix
        item.append(url + " " + os.path.join(path, name))
        count += 1
    aim.close()
    mutex.acquire()
    parms.extend(item)
    mutex.release()
    
wnid = []
target = open(TARGET)
for line in target:
    wnid.append(line[:9])
target.close()

parms = []
mutex = threading.Lock()
pool = Pool(POOLSIZE)
pool.map(prepare_list, wnid)
pool.close()
pool.join()

print(len(parms))

down = Pool(POOLSIZE)
down.map(download_helper, parms)
down.close()
down.join()
