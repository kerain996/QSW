import requests
from bs4 import BeautifulSoup

def website(number):
	return "http://www.quanshuwang.com/all/postdate_0_0_0_0_1_0_{}.html".format(number)
  
# 使用requests获取网页，使用BeautifulSoup创建soup对象处理网页内容
def create_soup_class(url):
	header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
	r = requests.get(url, headers=header)
	r.encoding = 'GBK'
	soupClass = BeautifulSoup(r.text, 'html.parser')
	return soupClass

# 将内容写入txt文件
def txt_write(filename, chapName, text):
	f = open(filename, 'a')
	f.write(chapName)
	f.write(text.replace(u'\xa0', u' ')) # 存在一堆的编码转换问题
	f.close()

# 获得网页的页数
def get_website_number():
	iPageNumber = int(create_soup_class(website(1)).find('a', 'last').get_text())
	return iPageNumber

# 获取i页的小说链接
def get_novel_link(url):
	soup = create_soup_class(url)
	aBooks = soup.find_all('div', 'yd-book-item yd-book-item-pull-left')
	aNovelLinks = []
	for div in aBooks:
		link = div.find('a').get('href')
		aNovelLinks.append(link)
	return aNovelLinks																					# 列表：i页的所有小说链接

# 获取目录网址
def get_novel_catalog(novelUrl):
	soup = create_soup_class(novelUrl)
	return soup.find('a', 'reader').get('href')															# 字符串：小说的目录链接

# 小说的详细信息
def get_novel_chap_info(cataUrl):
	soup = create_soup_class(cataUrl)
	aNovelInfo = soup.find('div', 'chapName').get_text("|").split("|")
	aLi = soup.find_all('li')[13:]
	aTagA = []
	aChapName = []
	aChapLink = []
	for li in aLi:
		a = li.find('a')
		aTagA.append(a)
	for a in aTagA:
		aChapName.append(a.get_text())
		aChapLink.append(a.get('href'))
	return aNovelInfo, aChapName, aChapLink 															# 列表：作者&书名，章节名，章节链接

# 章节文本内容
def get_chap_content(chapUrl):
	soup = create_soup_class(chapUrl)
	content = soup.find(id = 'content')
	aScr = content.find_all('script')
	text = content.get_text()
	for scr in aScr:
		text = text.replace(scr.get_text(), "")
	return text 																						# 字符串：章节内容

# 保存章节内容到txt文件中
def save_novel_all_content(aNovelInfo, aChapNames, aChapLinks):
	filename = aNovelInfo[1] + aNovelInfo[0] + 'txt'
	i = 0
	for link in aChapLinks:
		text = get_chap_content(link)
		chapName = aChapNames[i]
		txt_write(filename, chapName, text)
		i+=1
	print(filename + "Done!")
	return 0

#---------------------------------
iPageNumber = get_website_number()
print("共有{}页".format(iPageNumber))

# 从最后一页开始爬取
while iPageNumber > 0:
	novelLinks = get_novel_link(website(iPageNumber))																# 列表：第i页的小说网址

	for link in novelLinks:

		aNolInfos, aChapNames, aChapLinks = get_novel_chap_info(get_novel_catalog(link))
		save_novel_all_content(aNolInfos, aChapNames, aChapLinks)
	iPageNumber-=1
print("DONE!\n")
