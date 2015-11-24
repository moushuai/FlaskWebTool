# -*- coding: utf-8 -*-
# Author: Mou Shuai

import threading
import urllib2
import sys
import random

max_thread = 50
# initial lock
lock = threading.RLock()

class Downloader(threading.Thread):
    def __init__(self, url, start_size, end_size, fobj, buffer):
        self.url = url
        self.buffer = buffer
        self.start_size = start_size
        self.end_size = end_size
        self.fobj = fobj
        threading.Thread.__init__(self)

    def run(self):
        """
            test
        """
        with lock:
            print 'starting: %s' % self.getName()
        self._download()

    def _download(self):
        """
            working on it
        """
        req = urllib2.Request(self.url)
        # add HTTP Header(RANGE) to find the data range
        req.headers['Range'] = 'bytes=%s-%s' % (self.start_size, self.end_size)
        f = urllib2.urlopen(req)
        # initial the offset address of document object
        offset = self.start_size
        while 1:
            block = f.read(self.buffer)
            if not block:
                with lock:
                    print '%s done.' % self.getName()
                break
            # lock the thread while writing data
            # use with lock to replace lock.acquire().....lock.release()
            # python >= 2.5
            with lock:
                sys.stdout.write('%s saveing block...' % self.getName())
                # set offset address of document object
                self.fobj.seek(offset)
                # write data
                self.fobj.write(block)
                offset = offset + len(block)
                sys.stdout.write('done.\n')


def main(thread=20, buffer=1024):
    thread = thread if thread <= max_thread else max_thread
    prefix = '/home/shuaimou/scratch/meitu/'
    download_list = [prefix + 'normal26743.csv', prefix + 'politic.log', prefix + 'porn.log']
    # data_prefix = '/data4/meitu/vedio/'
    save_list =  ['normal.csv',  'politic.csv', 'porn.csv']
    data_list = [prefix + 'normal2/', prefix + 'politic/', prefix + 'porn/']

    for i in range(3):
        file_reader = open(download_list[i])
        file_save_list = []
        index = 0
        for line in file_reader:
            start = line.find('http:')
            end = line.find('mp4') + 3
            if start != -1 and end !=2:
                url = line[start:end]
                file_name = '%d' %index
                record = url + ' ' + data_list[i] + file_name + '.mp4'
                file_save_list.append(record)
                index = index + 1
        random.shuffle(file_save_list)

        file_writer = open(prefix + save_list[i],'w')
        for line in file_save_list:
            try:
                file_writer.write(line + '\n')
            except Exception, e:
                print e
        file_writer.close()

        for line in file_save_list:
            print line
            try:
                start = line.find('http:')
                
                end = line.find('mp4') + 3
               
                start_f = line.index(prefix)

                if start != -1 and end != 2 and start_f != -1:
                    save_file = line[start_f:]
                    # get vedio size
                    url = line[start:end]
                    print url
                    req = urllib2.urlopen(url)
                    size = int(req.info().getheaders('Content-Length')[0])
                    # initial 
                    fobj = open(save_file, 'wb')
                    # computing the http Range size according the number of thread
                    avg_size, pad_size = divmod(size, thread)
                    plist = []
                    for i in xrange(thread):
                        start_size = i*avg_size
                        end_size = start_size + avg_size - 1
                        if i == thread - 1:
                            # add the pad_size to the last thread
                            end_size = end_size + pad_size + 1
                        t = Downloader(url, start_size, end_size, fobj, buffer)
                        plist.append(t)

                    #  downloading
                    for t in plist:
                        t.start()

                    # waiting for all threads
                    for t in plist:
                        t.join()

                    # 
                    # index = index +1
                    print 'Download completed!'
            except Exception, e:
                print e
        file_reader.close()
        # write the saving list
        # random.shuffle(file_save_list)
        # for line in file_save_list:
        #     file_writer.write(line)
        # file_writer.close()

if __name__ == '__main__':
    #url = 'http://mvvideo2.meitudata.com/53f1ede46ee2d531.mp4'
    main(thread=20, buffer=4096)