'''
匯入套件
'''
# 爬蟲
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# 時間
import time
from time import sleep
# 線程與佇列
import threading
import queue
# 文件
import json
import os
# 正則表達式
import re
'''
職缺網址
'''
# 只包含新北市與台北市的所有職缺
# total 代表該職務類型的職缺總數(可以在這頁爬到職缺總數，但實際職缺的資料，如果大於150頁，只會顯示前150頁)
# actual 是用產業去劃分該職務類型的職缺總數，讓它小於150頁，以便完整抓到所有職缺
jobList = {
    "資訊軟體系統類": {
        "軟體設計工程師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001004&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001004&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1001001001%2C1001001003%2C1001001004%2C1001001005%2C1001001006&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001004&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1001001002&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001004&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1001002000%2C1001003000%2C1001004000%2C1001005000%2C1001006000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001004&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1003000000%2C1006000000%2C1009000000%2C1002000000%2C1010000000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001004&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1004000000%2C1011000000%2C1015000000%2C1005000000%2C1007000000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001004&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1014000000%2C1013000000%2C1008000000%2C1012000000%2C1016000000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "Internet程式設計師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001006&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001006&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1003000000%2C1006000000%2C1009000000%2C1002000000%2C1010000000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001006&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1004000000%2C1011000000%2C1015000000%2C1005000000%2C1007000000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001006&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001006&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1001002000%2C1001003000%2C1001004000%2C1001005000%2C1001006000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001006&jobcatExpansionType=1&area=6001002000%2C6001001000&indcat=1014000000%2C1013000000%2C1008000000%2C1012000000%2C1016000000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "韌體設計工程師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001005&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001005&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "電腦系統分析師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001007&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001007&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "其他資訊專業人員": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001009&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001009&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "通訊軟體工程師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001003&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001003&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "軟體專案主管": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001001&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001001&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "演算法開發工程師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001012&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001012&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "電玩程式設計師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001008&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001008&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "資訊助理人員": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001010&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001010&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "電子商務技術主管": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001002&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001002&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }, 
        "BIOS工程師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001011&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007001011&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }
    },
    "MIS&網管類人員": {
        "MIS&網管主管": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002001&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002001&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        },
        "資料庫管理人員": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002002&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002002&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        },
        "MIS程式設計師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002003&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002003&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        },
        "MES工程師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002004&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002004&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        },
        "網路管理工程師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002005&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002005&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        },
        "系統維護&操作人員": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002006&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002006&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        },
        "資訊設備管制人員": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002007&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002007&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        },
        "網路安全分析師": {
            "total": "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002008&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc",
            "actual": [
                "https://www.104.com.tw/jobs/search/?ro=1&jobcat=2007002008&jobcatExpansionType=1&area=6001002000%2C6001001000&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc"
            ]
        }
    }
}
'''
class
'''
class Crawler(threading.Thread):
    def __init__(self, queue, num, semaphore):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num
        self.semaphore = semaphore
        self.visitDelay = 0.5 # 超連結延遲，讓訪問有緩衝時間，避免太快開始爬蟲，導致錯誤。
        
    # 職缺列爬文
    def listCrawling_bs4(self, driver, data_queue):
        # 整頁抓
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except Exception as e:
            print(f'錯誤訊息: {e}')
            return True
        # 抓重點
        buf = soup.find('div', {'id': 'js-job-content'}) \
            .find_all('article', {'class': 'b-block--top-bord job-list-item b-clearfix js-job-item'})
        for i in range(len(buf)):
            # 公司名稱
            comp = buf[i].select('div.b-block__left > ul.b-list-inline.b-clearfix > li > a')[0].get('title')
            comp = comp[comp.find("公司名：") + 4: comp.find("\n")]
            comp_url = buf[i].select('div.b-block__left > ul.b-list-inline.b-clearfix > li > a')[0].get('href')
            if "https:" not in comp_url:
                comp_url = f"https:{comp_url}"
            # print(f"公司名稱: {comp}")
            # print(f"公司介紹網址： {comp_url}")
            # 職缺名稱
            title = buf[i].select('div.b-block__left > h2 > a')[0].text
            # print(f"標題： {title}")
            # 內文網址
            url = buf[i].select('div.b-block__left > h2 > a')[0].get('href')
            if "https:" not in url:
                url = f"https:{url}"
            # print(f"網址： {url}")
            # 應徵人數
            apply_pop = buf[i].select('div.b-block__right.b-pos-relative > a')[0].text
            # print(f"應徵人數： {apply_pop}")
            # 應徵者資訊網址
            apply_url = buf[i].select('div.b-block__right.b-pos-relative > a')[0].get('href')
            if "https:" not in apply_url:
                apply_url = f"https:{apply_url}"
            # print(f"應徵者資訊網址： {apply_url}")
            # 儲存json資料
            data_queue.put({
                "company": comp,
                "job_title": title,
                "apply_pop": apply_pop,
                "company_url": comp_url,
                "context_url": url,
                "apply_url": apply_url
            })
        return False
    
    def detailCrawling_bs4(self, driver, buf, delay):
        detailData = {}
        detailData.update(buf[1])
        driver.get(detailData['context_url'])
        sleep(self.visitDelay * delay)
        # 整頁抓
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except Exception as e:
            print(f'錯誤訊息: {e}-{detailData["context_url"]}')
            return True
        # 工作內容
        # print("--------------------工作內容--------------------")
        try:
            description = soup.find('p', {'class': 'mb-5 r3 job-description__content text-break'}).text # 說明
            # print(description)
            detailData.update({'工作內容': description})
        except Exception as e:
                print(f'錯誤訊息: 發生在[工作內容]-{e}-{detailData["context_url"]}')
        # 條件要求
        # print("--------------------條件要求--------------------")
        require = soup.find('div', {'class': 'col main'})
        detailData.update({'條件要求': {}})
        for item in require.find_all('div', {'class': 'row mb-2'}):
            try:
                item_t = item.find('h3', {'class': 'h3'}).text.strip()
            except Exception as e:
                print(f'錯誤訊息: {e}-{detailData["context_url"]}')
                return True
            item_d = []
            # print(f"{item_t}:")
            try:
                if item_t == '職務類別':
                    for i in require.find_all('div', {'class': 't3 mb-0 identity-type d-inline-block align-bottom'}):
                        # print(f"   {i.find('div', {'class': 'trigger'}).text.strip()}")
                        item_d.append(i.find('div', {'class': 'trigger'}).text.strip())
                elif item_t == "接受身份":
                    for i in item.select('span'):
                        if '、' in i.text.strip():
                            continue
                        # print(f"   {i.text.strip()}")
                        item_d.append(i.text.strip())
                elif item_t == '語文條件' or item_t == '其他條件':
                    # print(f"   {item.find('p').text.strip()}")
                    item_d.append(item.find('p').text.strip())
                elif item_t == '工作技能':
                    pass
                elif item_t == '擅長工具':
                    for i in item.select('u'):
                        # print(f"   {i.text.strip()}")
                        item_d.append(i.text.strip())
                else:
                    i = item.select("p.t3.mb-0")
                    # print(f"   {i[0].text.strip()}")
                    item_d.append(i[0].text.strip())
                detailData['條件要求'].update({item_t: item_d})
            except Exception as e:
                print(f'錯誤訊息: 發生在[條件要求][{item_t}]-{e}-{detailData["context_url"]}')
        # 福利制度
        # print("--------------------福利制度--------------------")
        try:
            welfare = soup.find('div', {'class': 'row benefits-description'}) \
                          .find('p', {'class': 'r3 mb-0 text-break'}).text
            # print(welfare)
            detailData.update({'福利制度':welfare})
        except Exception as e:
            print(f'錯誤訊息: 發生在[福利制度]-{e}-{detailData["context_url"]}')
        buf[2].put(detailData)
        return False
        
    # 職缺列爬文管理
    def crawlerMgr(self, driver, buf):
        if buf[0] == "total":
            driver.get(buf[1])
            sleep(self.visitDelay)
            total_num = int(re.findall(r"\d+\d*", driver.find_element(By.CSS_SELECTOR, '#js-job-tab > li.b-nav-tabs__active > span').text)[0])
            buf[2].put(total_num) # "total"
        elif buf[0] == "actual":
            driver.get(buf[1])
            sleep(self.visitDelay)
            total_num = int(re.findall(r"\d+\d*", driver.find_element(By.CSS_SELECTOR, '#js-job-tab > li.b-nav-tabs__active > span').text)[0])
            buf[2].put(total_num) # "p_total"
            # 抓所有頁數，一頁一頁爬不用擔心滾輪
            pages = len(driver.find_elements(By.CSS_SELECTOR, '#js-job-header select.page-select.js-paging-select.gtm-paging-top option'))
            # 一頁一頁處理
            for i in range(pages):
                # 如果不是第一頁，就點下去
                if i > 0:
                    driver.find_elements(By.CSS_SELECTOR, '#js-job-header select.page-select.js-paging-select.gtm-paging-top option')[i].click()
                    sleep(self.visitDelay*3)
                while True: 
                    fail = self.listCrawling_bs4(driver, buf[3])
                    if fail: # 如果出現錯誤
                        sleep(self.visitDelay*2)
                    else:
                        break
        elif buf[0] == "context":
            for i in range(1, 4):
                try:
                    fail = self.detailCrawling_bs4(driver, buf, i)
                except Exception as e:
                    fail = True
                    print(f'錯誤訊息: {e}')
                if not fail: # 如果出現錯誤
                    break
        else:
            pass
        
    def run(self):
        driver = webdriver.Chrome() # 使用 Chrome 的 WebDriver
        driver.maximize_window() # 螢幕最大化
        while self.queue.qsize() > 0:
            buf = self.queue.get()
            # 取得旗標
            self.semaphore.acquire() # 僅允許有限個執行緒同時進的工作
            print("Semaphore acquired by Crawler %d" % self.num)
            # 開始工作
            # print("Crawler %d: %s" % (self.num, buf))
            self.crawlerMgr(driver, buf)
            # 釋放旗標
            print("Semaphore released by Crawler %d" % self.num)
            self.semaphore.release()
        # 所有工作完成後，關閉瀏覽器
        driver.close()
'''
function
'''
# 儲存資料
def saveJson(path, data):
    fp = open(path, "w", encoding='utf-8') # lowPay mediumPay hiPay
    fp.write( json.dumps(data, ensure_ascii=False) )
    fp.close() 
    
# 讀取資料
def readJson(path):
    fp = open(path, "r", encoding='utf-8') # lowPay mediumPay hiPay
    data = json.load(fp)
    fp.close()
    return data

# 安排爬蟲工作佇列 & 存放佇列列表
def listQueueMgr(job, jType, in_queue, out_queue_list): 
    out_queue_list.update({jType: {
        "total": queue.Queue(),
        "p_total": queue.Queue(),
        "data": queue.Queue()
    }})
    in_queue.put(["total", jobList[job][jType]["total"], out_queue_list[jType]["total"]])
    for url in jobList[job][jType]["actual"]:
        # print(url)
        in_queue.put(["actual", url, out_queue_list[jType]["p_total"], out_queue_list[jType]["data"]])
    
# 安排爬蟲工作佇列 & 存放佇列列表
def contextQueueMgr(data, jType, in_queue, out_queue_list): 
    out_queue_list.update({jType: {
        "data": queue.Queue()
    }})
    for i in data:
        in_queue.put(['context', i, out_queue_list[jType]["data"]])

def executionQueuePath(state, today, in_queue, out_queue_list):
    # 確認/建立人力銀行資料夾
    if not os.path.isdir(f"{os.getcwd()}\\人力銀行"):
            os.mkdir(f"{os.getcwd()}\\人力銀行")
    # 確認/建立日期資料夾
    if not os.path.isdir(f"{os.getcwd()}\\人力銀行\\{today}"):
            os.mkdir(f"{os.getcwd()}\\人力銀行\\{today}")
    for job in jobList.keys(): # 職務類別
        path = f"{os.getcwd()}\\人力銀行\\{today}\\{job}"
        # print(path)
        # 確認/建立職務類別資料夾
        if not os.path.isdir(path): 
            os.mkdir(path)
        for jType in jobList[job]: # 職務類型
            path = f"{os.getcwd()}\\人力銀行\\{today}\\{job}\\{jType}"
            # print(path)
            # 確認/建立職務類型資料夾
            if not os.path.isdir(path):
                os.mkdir(path)
            if state == 'crawlList': # 爬取職缺列
                listQueueMgr(job, jType, in_queue, out_queue_list)
            elif state == 'saveList': # 保存職缺列
                listData = [] # json暫存列表
                logData = [] # log暫存列表
                p_total_sum = 0 # 每頁可爬總數
                # 每頁可爬總數加總
                for _ in range(out_queue_list[jType]['p_total'].qsize()):
                    p_total_sum = p_total_sum + out_queue_list[jType]['p_total'].get()
                # 整理log
                logData.append({
                    "總筆數": out_queue_list[jType]['total'].get(),
                    "每頁筆數加總": p_total_sum,
                    "實際筆數": out_queue_list[jType]['data'].qsize()
                })
                # 資料彙集
                for _ in range(out_queue_list[jType]['data'].qsize()):
                    listData.append(out_queue_list[jType]['data'].get())
                # 存檔
                path = f"{os.getcwd()}\\人力銀行\\{today}\\{job}\\{jType}\\recruit_list.json"
                saveJson(path, listData)
                path = f"{os.getcwd()}\\人力銀行\\{today}\\{job}\\{jType}\\log.json"
                saveJson(path, logData)
            elif state == 'crawlContext': # 爬取內文
                for file in os.listdir(path):
                    if file == 'recruit_list.json':
                        path = path + f'/{file}'
                        # print(path)
                        data = readJson(path)
                        contextQueueMgr(data, jType, in_queue, out_queue_list)
            elif state == 'saveContext': # 保存內文
                listData = [] # json暫存列表
                # logData = [] # log暫存列表
                 # 資料彙集
                for _ in range(out_queue_list[jType]['data'].qsize()):
                    listData.append(out_queue_list[jType]['data'].get())
                # 存檔
                path = f"{os.getcwd()}\\人力銀行\\{today}\\{job}\\{jType}\\recruit_context.json"
                saveJson(path, listData)
                # path = f"{os.getcwd()}\\人力銀行\\{today}\\{job}\\{jType}\\context_log.json"
                # saveJson(path, logData)
            else:
                pass
'''
主程式
'''
def main():
    '''
    通用變數初始化
    '''
    today = time.strftime("%Y-%m-%d", time.localtime()) # 今天日期
    
    in_queue = queue.Queue() # 爬蟲工作佇列
    out_queue_list = {} # 檔案存放佇列列表
    
    max_t_num = 10 # 子線程數量
    semaphore = threading.Semaphore(max_t_num) # 建立旗標，限制子線程最大數量
    threads = [] # 子線程列表
    if True: # 開關
        '''
        安排工作: 爬取職缺列
        '''
        executionQueuePath('crawlList', today, in_queue, out_queue_list)
        '''
        執行工作: 爬取職缺列
        '''
        # 建立子線程列表
        for i in range(1, max_t_num+1):
            list_crawler = Crawler(in_queue, i, semaphore) 
            list_crawler.start()
            threads.append(list_crawler)
        # 等待所有子線程完成工作
        for thread in threads:
            thread.join()
        '''
        安排/執行工作: 保存職缺列
        '''
        executionQueuePath('saveList', today, in_queue, out_queue_list)
    if False: # 開關
        '''
        安排工作: 爬取內文
        '''
        in_queue = queue.Queue() # 爬蟲工作佇列
        out_queue_list = {} # 檔案存放佇列列表
        executionQueuePath('crawlContext', today, in_queue, out_queue_list)
        '''
        執行工作: 爬取內文
        '''
        # 建立子線程列表
        threads = [] # 子線程列表
        for i in range(1, max_t_num+1):
            list_crawler = Crawler(in_queue, i, semaphore) 
            list_crawler.start()
            threads.append(list_crawler)
        # 等待所有子線程完成工作
        for thread in threads:
            thread.join()
        '''
        安排/執行工作: 保存內文
        '''
        executionQueuePath('saveContext', today, in_queue, out_queue_list)

if __name__ == '__main__':
    start = time.strftime("%H:%M:%S", time.localtime())
    main()
    end = time.strftime("%H:%M:%S", time.localtime())
    print(f'{start} ~ {end}')
