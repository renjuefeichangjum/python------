#--coding:utf-8--

from  tkinter import *
import tkMessageBox
from tkinter import scrolledtext
from tkinter import ttk
import time
import re
import random
from lxml import html
#import cssselect
import lxml.cssselect
import lxml.etree
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import threading
ARTICLE_READ_TIME = 4*60+3  # 4分钟/1分
RADIO_WATCH_TIME = 5*60+3  # 5分钟/1分
WAIT_POINTS_TIME = 5 # 分数刷新需要时间
global driver
driver = webdriver.Chrome(executable_path='chromedriver.exe')
urls = {
    "home" : 'https://pc.xuexi.cn/points/login.html?ref=https://pc.xuexi.cn/points/my-study.html',
    "points": "https://pc.xuexi.cn/points/my-points.html", #分数
    #"study": "https://www.xuexi.cn/", #文章
    "radio": "https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html" #视频
}
def get_random_article(randomvalue):
    article_tap_list = ['Cds1ok08g8ns00',
                        'C4b17trj9ay600',
                        'Cnr0zbz511qo0',
                        'Ce2rkubt4www00',
                        'Cdlocclyt4yo00',
                        'Ccu22ps7iam800']
    article_url_list = [
        'https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html?pageNumber=',
        'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html?pageNumber=',
        ' https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html?pageNumber=',
        'https://www.xuexi.cn/105c2fa2843fa9e6d17440e172115c92/9a3668c13f6e303932b5e0e100fc248b.html?pageNumber=',
        'https://www.xuexi.cn/03c8b56d5bce4b3619a9d6c2dfb180ef/9a3668c13f6e303932b5e0e100fc248b.html?pageNumber=',
        'https://www.xuexi.cn/bab787a637b47d3e51166f6a0daeafdb/9a3668c13f6e303932b5e0e100fc248b.html?pageNumber=',
        ]
    return [article_tap_list[randomvalue],article_url_list[randomvalue]]
def move(target):
    driver.execute_script("arguments[0].scrollIntoView();", target)

def login():

    scr.insert(END,"【提示】请用app扫描，进行登录...\n")
    driver.get(urls["home"])  # 主页
    # 定位到二维码
    move(driver.find_element_by_id('ddlogin'))
    scr.insert(END, "【提示】扫描成功后请按确认按钮...\n")
    # 登录成功确认
    #input("【提示】扫描完成后，请输入y，后回车...\n")

def update_points():
    driver.get(urls["points"])
    time.sleep(10)

    html = driver.page_source
    tree = lxml.html.fromstring(html)
    #tree = etree.HTML(html)
    # 今日得分
    try:
        points = tree.cssselect(".my-points-points")
        today_points_str = points[1].text
        today_points = int(today_points_str)
        tips="[今日总分]" +str(today_points)+"\n"
        scr.insert(END,tips)
    except Exception as e:
        return
    #print("[今日总分]%d" % today_points)
    # 每项得分
    scores = {}
    try:
        cards = tree.cssselect(".my-points-card")
        for card in cards:
            title = card.cssselect(".my-points-card-title")[0].text  # 标题
            score_str = card.cssselect(".my-points-card-text")[0].text  # 得分情况
            scores[title] = score_str
    except Exception as e:
        scr.insert(END, "错误，重新扫码\n")
        driver.quit()
        return
    tips="[今日得分细则]\n"
    scr.insert(END, tips)
    for scorename in scores:
        tips=scorename+":"+scores[scorename]+'\n'
        scr.insert(END, tips)
    #print(tips)
    #scr.insert(END,"[今日得分细则]")
    scr.insert(END,tips)


    return today_points, scores


def get_score(scores, score_name):
    score_str = scores[score_name]  # 得到score_name细则
    tips=score_name+score_str+"\n"
    scr.insert(END,tips)
    #print("\t[%s] %s" % (score_name, score_str))
    result = re.match("([0-9]+)分/([0-9]+)分", score_str.encode("utf-8")  )
    score = int(result.group(1))
    total = int(result.group(2))
    return score, total
def watch_video(flag):
    #url='https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html'
    driver.get(urls["radio"] )
    time.sleep(10)
    try:
        radios = driver.find_elements_by_css_selector('.radio-inline')
        index=random.randint(0,10)
        radios[index].click()
    except Exception as e:
        driver.switch_to_window(driver.window_handles[-1])
        driver.close()
        return
    driver.switch_to_window(driver.window_handles[-1])
    try:
        radios = driver.find_elements_by_css_selector('.radio-inline')
        index=random.randint(11,len(radios)-1)
        radios[index].click()
    except Exception as e:
        return
    driver.switch_to_window(driver.window_handles[-1])
    try:
        page= driver.find_element_by_css_selector('.pagination')
        finalpag=int(page.text.split('\n')[-1])
    except Exception as e:
        return
    pageNumber=random.randint(1,finalpag)
    for i in range(pageNumber):
        try:
            nextpage = driver.find_element_by_css_selector('.next')
            nextpage.click()
        except Exception as e:
            break

        driver.switch_to_window(driver.window_handles[-1])
        time.sleep(5)
    driver.switch_to_window(driver.window_handles[-1])
    try:
        words=driver.find_elements_by_css_selector('.word-item')
    except Exception as e:
        scr.insert(END, "没有找到视频！！！\n")
        return
    if(len(words)==0):
        return
    index=random.randint(0,len(words)-1)
    words[index].click()
    driver.switch_to_window(driver.window_handles[-1])
    try:
        move( driver.find_element_by_css_selector("video") )
    except Exception as e:
        scr.insert(END, "这不是视频！！！\n")
        return
    if flag:
        scr.insert(END, "【等我】 我在看视频...\n")
        time.sleep(RADIO_WATCH_TIME )
    else:
        scr.insert(END, "【等我】 我在看视频...\n")
        time.sleep(RADIO_WATCH_TIME)
    driver.switch_to_window(driver.window_handles[-1])
    driver.close()
    driver.switch_to_window(driver.window_handles[-1])

def read_article(flag):
    randomvalue=random.randint(0,5)
    article_url=get_random_article(randomvalue)
    url='https://www.xuexi.cn/'
    driver.get(url)
    time.sleep(10)
    articletype = driver.find_element_by_id(str(article_url[0]))
    ActionChains(driver).click(articletype).perform()
    driver.switch_to_window(driver.window_handles[-1])

    try:
        getpage= driver.find_element_by_css_selector('.pagination')
        finalpag=int(getpage.text.split('\n')[-1])
        pageNumber=str(random.randint(1,finalpag))
    except Exception as e:
        scr.insert(END,"错误，请重新点击扫码确认！！！\n")
        pageNumber = 1
        #return
    newurl=article_url[1]+pageNumber
    driver.get(newurl)
    driver.switch_to_window(driver.window_handles[-1])
    words=driver.find_elements_by_css_selector('.word-item')
    if(len(words)==0):
        print("没有找到文章！！！\n")
        return
    index = random.randint(0,len(words)-1)
    try:
        words[index].click()
        driver.switch_to_window(driver.window_handles[-1])
    except Exception as e:
        return
    try:
        move(driver.find_element_by_css_selector(".dyxx-rich-content"))
    except Exception as e:
        scr.insert(END,e)
        scr.insert(END, "这不是文章\n")
        return
    if flag:
        scr.insert(END, "[等我] 我在看文章...\n")
        time.sleep(ARTICLE_READ_TIME)
    else :
        scr.insert(END, "[等我] 我在看文章...\n")
        time.sleep(ARTICLE_READ_TIME)
    driver.close()
    driver.switch_to_window(driver.window_handles[-1])


def cnt_time(today_points, scores):
    gapscores=str(30-today_points)
    tips="【提醒】 还差"+gapscores+"分！！\n"
    scr.insert(END, tips)
    time = 0
    score, total = get_score(scores, u'文章学习时长')
    time += (total-score) * ARTICLE_READ_TIME

    score, total = get_score(scores, u'阅读文章')
    time += (total-score) * 5

    score, total = get_score(scores, u'视频学习时长')
    time += (total-score) * RADIO_WATCH_TIME

    score, total = get_score(scores, u'观看视频')
    time += (total-score) * 5
    predict_time=str(int(time/60))
    tips="【提醒】预估时间"+predict_time+"分钟（若在活跃时间可减半）\n"
    scr.insert(END, tips)
    #print("【提醒】预估时间%d分钟（若在活跃时间可减半）" % int(time/60) )


def start():
    login()
def autuStudy():
    today_points, scores = update_points()
    cnt_time(today_points, scores)
    while today_points < 30:
        score, total = get_score(scores, u'文章学习时长')
        for i in range(score, total, 1):
            try:
                read_article(True)  # 长时间看文章
            except Exception as e:
                scr.insert(END,e+'\n')
                return
        update_points()
        score, total = get_score(scores, u'阅读文章')
        for i in range(score, total, 1):
            try:
                read_article(FALSE)  # 长时间看文章
            except Exception as e:
                scr.insert(END, e)
                return
             # 短时时间看文章
        update_points()
        score, total = get_score(scores, u'视频学习时长')
        for i in range(score, total, 1):
            try:
                watch_video(TRUE)  # 长时间看视频
            except Exception as e:
                scr.insert(END,e)
                #return
        update_points()
        score, total = get_score(scores, u'观看视频')
        for i in range(score, total, 1):
            try:
               watch_video(FALSE)  # 短时间看视频
            except Exception as e:
                scr.insert(END, e)
                #return
        get_score(scores, u'观看视频')
        driver.switch_to_window(driver.window_handles[-1])
        driver.close()
        driver.switch_to_window(driver.window_handles[-1])
        today_points, scores = update_points()
    scr.insert(END,"刷分完成\n")
    driver.quit()
def confirm():
    #tkMessageBox.showinfo('提示',"点击成功")
    try:
        t=threading.Thread(target= autuStudy)
        t.start()
    except Exception as e:
        tkMessageBox.showinfo('提示', e)
    #tkMessageBox.showinfo('提示', "点击成功")

root=Tk()
root.title("按键精灵")
root.geometry('450x450')
root.minsize(450, 450)
root.resizable(width=False, height=False)
btn_start=Button(root,text="点击开始",command=start)
btn_start.pack()
btn_confirm=Button(root,text="扫码确认",command=confirm)
btn_confirm.pack()
monty = ttk.LabelFrame(root, text="消息列表") # 创建一个容器，其父容器为win
monty.pack()
#monty.pa(column=0, row=0, padx=10, pady=10)
scr = scrolledtext.ScrolledText(monty, width=80, height=20)
scr.pack()
ad_label=Label(root,text="@接：Python批处理、爬虫、GDAL/OGR、ArcGIS空间分析")
ad_label.pack()
mail_label=Label(root,text="邮箱 : passerqi@gmail.com")
mail_label.pack()
#scr.grid(column=0, columnspan=3)
#root.mainloop()

root.mainloop()