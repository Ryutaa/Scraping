from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

if __name__=='__main__':

#検索
	driver = webdriver.PhantomJS()
	driver.get('https://duet.doshisha.ac.jp/kokai/html/fi/fi020/FI02001G.html')
	
	year = driver.find_element_by_id('form1:kaikoNendolist')
	course = driver.find_element_by_xpath("//*[@id='form1']/div/div/table/tbody/tr[2]/td[1]/select")
	department = driver.find_element_by_xpath("//*[@id='form1']/div/div/table/tbody/tr[2]/td[2]/select")

	selectyear = Select(year)
	selectcourse = Select(course)
	selectdepartment = Select(department)

	selectyear.select_by_value('2017')
	selectcourse.select_by_value('1')
	selectdepartment.select_by_value('11003')
	driver.find_element_by_id('form1:enterDodoZikko').click()

#スクレイプ
	html = driver.page_source.encode('utf-8')
	soup = BeautifulSoup(html)
	table = soup.find('table', class_="data sortable")
	syllabus = soup.find_all(title="シラバス")

	f = open('/Users/ryuta/scrape/doshisha', 'a')

	def sylget():
		for href in syllabus:
			yield href.get('onclick')[25:87]

	gethref = sylget()

	i = 0

	for td in table.stripped_strings:
		if (i < 14):
			i += 1
			continue
		if (td == "授業講評"):
			f.write("\n")
			continue
		if (td == "シラバス"):
			f.write(gethref.__next__())
			f.write(",")
			continue
		f.write(td)
		f.write(",")
		
	f.close()