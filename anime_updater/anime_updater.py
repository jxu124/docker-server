from opencc import OpenCC
import os
import re
import time
import argparse
import cfscrape
import datetime
import xml.etree.ElementTree as ET


# docker pull python:3.7.13-slim
# pip install opencc cfscrape
s2t = OpenCC('s2t')
t2c = OpenCC('t2s')
debug = False


class QueryFile():
    def __init__(self, path: str):
        with open(path, 'r') as fp:
            self.raw = fp.readlines()
        self.path = path
        self.meta, self.dbase = self.parse(self.raw)
        self.modified = False
        
    def __getitem__(self, k):
        return self.dbase[k][1]
    
    def __setitem__(self, k, v):
        self.modified = True
        self.dbase[k][1] = v

    def update(self):
        if self.modified:
            for key, (i, stamp) in self.dbase.items():
                stamp = datetime.datetime.fromtimestamp(stamp).strftime('%Y%m%d_%H%M%S')
                self.raw[i] = re.compile('[0-9]{8}_[0-9]{6}').sub(stamp, self.raw[i])
            
            with open('/dev/shm/' + os.path.split(self.path)[1], 'w') as fp:
                fp.writelines(self.raw)
            with open(self.path + '.bak', 'w') as fp:
                fp.writelines(self.raw)
            with open(self.path, 'w') as fp:
                fp.writelines(self.raw)
            self.modified = False

    @staticmethod
    def parse(text_lines):
        meta = {}
        dbase = {}
        for i, text in enumerate(text_lines):
            # 1 去掉每行 #、换行号 之后的部分
            index = re.search('[#\n]', text).span()[0]
            text = text[:index]
            
            # 2 处理 meta 信息
            if text.startswith('meta_'):
                # text = text.replace(' ', '')
                parts = re.split(r"""("[^"]*"|'[^']*')""", text)
                parts[::2] = map(lambda s: "".join(s.split()), parts[::2]) # outside quotes
                text = "".join(parts)
                index = re.search('[=]', text).span()[0]
                k, v = text[5:index], text[index+1:]
                if k not in meta:
                    meta[k] = []
                meta[k].append(v)
                
            # 3 切分时间戳和关键词
            text = text.split(',')
            if len(text) == 2:
                stamp = int(time.mktime(time.strptime(text[0], '%Y%m%d_%H%M%S')))
                kword = text[1]
            else:
                continue
                
            # 4 分割关键词
            kword = [s for s in kword.replace('+', ' ').split(' ') if len(s)]
            if len(kword) == 0:
                continue
            kword = '+'.join(kword)

            # 5 保存记录
            dbase[kword] = [i, stamp]
        return meta, dbase


class DMHYXml():
    def __init__(self, url, delay=10):
        if type(url) is not list:
            url = [url]
        for u in url:
            try:
                with cfscrape.create_scraper(delay) as scraper:
                    web_data = scraper.get(u).content
                self.url = u
                self.xml = ET.fromstring(web_data)
                self.dbase = self.parse(self.xml)
                break
            finally:
                pass

    def find_update(self, kword, stamp):
        global debug
        if debug:
            print('=' * 20)
            print(kword)
        updates = {}
        for k, v in self.dbase.items():
            if debug:
                print(v['title'])
            if self.match_by_keyword(kword, v['title']) and v['stamp'] > stamp:
                if debug:
                    print('Matched: True')
                updates[k] = v
        return updates
 
    @staticmethod
    def match_by_keyword(kword, string):
        flag = True
        for k in kword.lower().split('+'):
            if (re.search(s2t.convert(k).lower(), s2t.convert(string).lower()) is None) and \
               (re.search(t2c.convert(k).lower(), t2c.convert(string).lower()) is None):
                flag = False
                break
        return flag

    @staticmethod
    def parse(xml):
        res_dict = {}
        for c1 in xml[0]:
            if c1.tag != 'item':
                continue
            meta = {'title': '', 'stamp': 0, 'link': ''}
            for c2 in c1:
                if c2.tag == 'title':
                    meta['title'] = c2.text
                elif c2.tag == 'pubDate':
                    meta['stamp'] = int(time.mktime(time.strptime(c2.text, '%a, %d %b %Y %H:%M:%S %z')))
                elif c2.tag == 'enclosure':
                    if c2.attrib['type'] == 'application/x-bittorrent':
                        meta['link'] = c2.attrib['url']
            # if len(meta) == 3:  # title, stamp, link
            #     key = re.findall('magnet:\?xt=urn:btih:([0-9A-Z]*?)&.*', meta['link'])[0]
            #     res_dict[key] = meta
            if len(meta) == 3:  # title, stamp, link
                key = meta['title']
                res_dict[key] = meta
        return res_dict


class Vision():
    @staticmethod
    def info(mlst):
        if len(mlst) > 0:
            message = '\n'.join([f"[info]<{Vision.get_localtime()}> got {len(mlst)} update(s)..."] + [f"[info] {m}" for m in mlst])
            print(message)

    @staticmethod
    def get_localtime(stamp=time.time(), tz_offset=+8):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(stamp + tz_offset*3600))

    @staticmethod
    def command(cmd, ulst):
        cmd = cmd.replace("\"", "").replace("\'", "")
        for u in ulst:
            title, stamp, link = u['title'], u['stamp'], u['link']
            link = "\"" + link + "\""
            assert os.system(cmd.format(link)) == 0


def main():
    global debug
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', type=str, help="/path/to/anime_query.txt")
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    # service
    q = QueryFile(args.query)
    x = DMHYXml(q.meta['rss'])
    debug = args.debug
    
    # model
    update_lst = []
    for kword in q.dbase.keys():
        updates = x.find_update(kword, q[kword])
        if len(updates) > 0:
            q[kword] = max([u['stamp'] for u in updates.values()])
            update_lst += list(updates.values())
    
    # view
    Vision.info([u['title'] for u in update_lst])
    Vision.command(q.meta['postcommand'][-1], update_lst)

    # model
    q.update()


if __name__ == '__main__':
    main()
