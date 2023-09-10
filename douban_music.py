
import re
import requests
import pandas
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup






class Data:
    """从网页中获取信息"""

    def __init__(self, soup):
        self.soup = soup

    def get_book_price(self, soup, prices_list):
        """解析网页并获取书的价格"""
        prices = soup.findAll('p', attrs={'class': 'price_color'})
        for price in prices:
            prices_list.append(price.string[2:])
        return prices_list

    def get_douban_price(self, soup, price_list):
        """得到价格"""
        price_text = soup.findAll('div', attrs={'class': 'pub'})
        priceptn = r"([0-9]{2}.[0-9]{2})元"
        prices = [re.match(priceptn, str(_)) for _ in price_text]

        while None in prices:
            prices.remove(None)

        for _ in prices:
            price_list.append(_.group())

        return price_list

    def get_urls(self, soup, url_list):
        """对获取到链接的文本进一步解析，获取具体网址"""
        link_text = soup.findAll('h2')
        link_a = [link.find('a') for link in link_text]
        links = [_.get("href") for _ in link_a]
        urlptn = r"(.+)/index.html"
        urls = [re.match(urlptn, str(_)) for _ in links]

        while None in urls:
            urls.remove(None)
        for _ in urls:
            url_list.append(_.group())

        return url_list

    def get_douban_book_urls(self, soup, urls):
        """对获取到链接的文本进一步解析，获取具体网址"""
        link_text = soup.findAll('h2')
        for link in link_text:
            link_a = link.find('a')
            urls.append(link_a)

        while None in urls:
            urls.remove(None)

        url_list = [_.get("href") for _ in urls]
        return url_list

    def get_douban_music_urls(self, soup, urls):
        """对获取到链接的文本进一步解析，获取具体网址"""
        link_text = soup.findAll('div', attrs={'class': 'll'})
        for link in link_text:
            link_a = link.find('a')
            urls.append(link_a)

        while None in urls:
            urls.remove(None)

        url_list = [_.get("href") for _ in urls]
        return url_list

    def get_book_name(self, soup, names):
        """解析网页并获取书名"""
        link_text = soup.findAll('h2')
        for link in link_text:
            link_a = link.find('a')
            names.append(link_a)

        while None in names:
            names.remove(None)

        titles = [_.get("title") for _ in names]
        return titles

    def get_music_name(self, soup, names):
        """解析网页并获取书名"""
        link_text = soup.findAll('div', attrs={'class': 'll'})
        for link in link_text:
            link_a = link.find('a')
            names.append(link_a.string)

        return names

    def get_douban_point(self, soup, points):
        """获取评分"""
        point_org = soup.findAll('span', attrs={'class': 'rating_nums'})
        for point in point_org:
            points.append(point.string)

        return points

    def get_comment_number(self, soup, comment_number):
        """获取评价数"""
        comment_num_org = soup.findAll('span', attrs={'class': 'pl'})
        for comment_num in comment_num_org:
            num = re.findall(r'\(.+?\)', str(comment_num))
            comment_number.append(num.pop())

        return comment_number

    def get_music_likenum(self, soup, like_number):
        """获取评价数"""
        like_num_org = soup.findAll('div', attrs={'class': 'pl'})
        for like_num in like_num_org:
            num = re.findall(r'\(.+?\)', str(like_num))
            like_number.append(num.pop())

        return like_number

class Scrape:
    """用于管理爬取网页的过程"""

    def __init__(self):
        self.name = ''

    def get_html_text(self, url):
        """模拟爬虫初步获取与解析"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_page_url(self, url, page_number):
        """获取首页的网址"""
        new_url = f'{url}/page-{page_number}.html?'
        return new_url

    def get_book_url(self, url):
        """获取具体书籍的网址"""
        new_url = f'https://books.toscrape.com/catalogue/{url}'
        return new_url

    def douban_music_page_url(self, url, page_number):
        """获取豆瓣的音乐网址"""
        new_url = f'{url}/3/{page_number}'
        return new_url

    def douban_book_page_url(self, url, page_number):
        """获取豆瓣的图书网址"""
        new_url = f'{url}?start={page_number}&type=T'
        return new_url

class View:
    """进程与结果的可视化"""

    def __init__(self, into):
        self.into = into

    def make_book_exexl(self, name, com_num, url):
        """所有获取到的数据进行汇总放到字典中并传入execl中"""
        info = {'书名': name, '评论数': com_num, '资源地址': url}
        book_file = pandas.DataFrame(info)
        book_file.to_excel('C:douban_book.xlsx', sheet_name="网站书籍爬取")

    def make_music_exexl(self, name, url):
        """所有获取到的数据进行汇总放到字典中并传入execl中"""
        info = {'歌手名': name, '资源地址': url}
        book_file = pandas.DataFrame(info)
        book_file.to_excel('C:douban_music.xlsx', sheet_name="网站电子乐爬取")

    def make_view(self, info):
        """对收集到的数据绘制可视化的图表"""
        book_name = info[0]
        book_price = info[1]

        # 为了坐标轴上能显示中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # ***********价格条形图
        fig, ax1 = plt.subplots()
        plt.bar(book_name, book_price, color='red')  # 设置柱状图
        plt.title('histogram')  # 表标题
        ax1.tick_params(labelsize=6)
        plt.xlabel('书名')  # 横轴名
        plt.ylabel('价格')  # 纵轴名
        plt.xticks(rotation=90, color='green')  # 设置横坐标变量名旋转度数和颜色

        plt.savefig(r'C:1.png', dpi=1000, bbox_inches='tight')  # 保存至本地

        # ************收藏数饼状图
        fig, ax2 = plt.subplots()
        plt.pie(book_price, labels=book_name, radius=1.65)  # 设置饼状图
        plt.title('chart', color="black")  # 表标题
        plt.savefig(r'C:2.png', dpi=200, bbox_inches='tight')  # 保存至本地

        plt.show()

    def show_process(self, i, end_num):
        """进度条"""
        pro = format(i / (end_num - 1) * 100, '.4f')
        print(f'已完成任务的{pro}%。')
        while i == end_num - 1:
            print('任务完成！！！')
            break


class MusicList:
    """一个用于爬虫运行的类"""
    def __init__(self):
        self.name = '歌曲爬虫'

        self.scrape = Scrape()
        self.data = Data(self)
        self.view = View(self)



    def main(self):
        """爬虫运行主进程"""
        print('让我们开始出发！！！')
        name = []
        like_num = []
        urls = []

        start_num = 1
        end_num = 149
        url = 'https://music.douban.com/artists/genre_page'
        for i in range(start_num, end_num):
            url_1 = self.scrape.douban_music_page_url(url, i)
            soup = self.scrape.get_html_text(url_1)
            name_list = self.data.get_music_name(soup, name)
            like_list = self.data.get_music_likenum(soup, like_num)
            url_list = self.data.get_douban_music_urls(soup, urls)
            self.view.show_process(i, end_num)

        self.view.make_music_exexl(name_list, url_list)


if __name__ == '__main__':
    # 创建并运行实例
    music = MusicList()
    music.main()



