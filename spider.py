import requests
from lxml import etree
from requests.exceptions import ConnectionError


class DdSpider():
    def __init__(self):
        self.header = {
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

    def parse_url(self, url):
        try:
            resp = requests.get(url, headers=self.header)
            if resp.status_code ==200:
                resp.encoding = 'utf-8'
                return resp.text
            return None
        except ConnectionError:
            print('Error.')
        return None

    def get_index_result(self, search, page=0):
        """搜索结果"""
        profiles= []
        if page == 0:
            url = 'http://zhannei.baidu.com/cse/search?s=1682272515249779940&entry=1&q={search}'.format(search=search)
        else:
            url ='http://zhannei.baidu.com/cse/search?q={search}&p={page}&s=1682272515249779940'.format(
                search=search, page=page)
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        titles = html.xpath('//*[@id="results"]/div/div/div/h3/a/@title')
        urls = html.xpath('//*[@id="results"]/div/div/div/h3/a/@href')
        images = html.xpath('//*[@id="results"]/div/div/div/a/img/@src')
        authors = html.xpath('//*[@id="results"]/div/div/div/div/p[1]/span[2]/text()')
        data1 = html.xpath('//p[@class="result-game-item-desc"]')
        for i in data1:
            profiles.append(i.xpath('string(.)'))
        styles = html.xpath('//*[@id="results"]/div/div/div/div/p[2]/span[2]/text()')
        times = html.xpath('//*[@id="results"]/div/div/div/div/p[3]/span[2]/text()')
        for title, url, image, author, profile, style, tim in zip(titles, urls, images, authors, profiles, styles, times):
            data = {
                'title':title.strip(),
                'url':url,
                'image':image,
                'author':author.strip(),
                'profile':profile.strip().replace('\u3000', '').replace('\n', ''),
                'style':style.strip(),
                'time':tim.strip(),
            }
            print(data)
            # yield data


    def get_chapter(self, url):
        """章节目录"""
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        chapters = html.xpath('//*[@id="main"]/div/dl/dd/a/text()')
        urls = html.xpath('//*[@id="main"]/div/dl/dd/a/@href')
        for chapter_url, chapter in zip(urls, chapters):
            data = {
                'url':str(url) + chapter_url,
                'chapter':chapter,
            }
            # yield chapter
            print(data)

    def get_article(self, url):
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        content = html.xpath('//*[@id="content"]/text()')
        return '<br>'.join(content)

a= DdSpider()
a.get_index_result('盘龙')
# print(a.get_article('http://www.23us.cc/html/4/4579/6912721.html'))
# a.get_chapter('http://www.23us.cc/html/4/4579/')
