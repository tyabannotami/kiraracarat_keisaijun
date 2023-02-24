import re
import sys
import requests
import collections
from bs4 import BeautifulSoup
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys, csv, operator
import pandas as pd

month_list=['年1月','年2月','年3月','年4月','年5月','年6月','年7月','年8月','年9月','年10月','年11月','年12月']
#アドレス末尾のリスト
#mid_list=['836', '840', '844']
mid_list=['296', '301', '306', '311', '316', '321', '326', '331', '336', '342', '347', '352', '357', '361', '367', '372', '377', '382', '387', '392', '397', '402', '407', '412', '417', '422', '427', '432', '437', '442', '447', '452', '457', '462', '467', '472', '477', '482', '487', '492', '497', '502', '507', '512', '517', '522', '527', '532', '537', '542', '547', '552', '557', '562', '567', '572', '577', '582', '587', '592', '596', '600', '604', '608', '612', '616', '620', '624', '628', '632', '636', '640', '644', '648', '652', '656', '660', '664', '668', '672', '676', '680', '684', '688', '692', '696', '700', '704', '708', '712', '716', '720', '724', '728', '732', '736', '740', '744', '748', '752', '756', '760', '764', '768', '772', '776', '780', '784', '788', '792', '796', '800', '804', '808', '812', '816', '820', '824', '828', '832', '836', '840', '844']

#開始年月を指定
year=2013
month=1

#ファイルネーム
h_filename="keisaijun"

#センターカラーの配列を作成
center_colors=[]
center_colors_month=np.full(5,"カラー")
center_color_all=[]
count_cc={}

df_color=pd.DataFrame(center_colors_month)
#掲載順の配列を作成
keisaijun=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26])
df_keisaijun= pd.DataFrame(keisaijun)
#表紙の配列を作成
top=[]
top.append("表紙")

#タイトル行設定
date_list=[]
date_list.append("年月")

class Article:
    def __init__(self,_label,_keyword):
        self.label=_label
        self.keyword=_keyword
        self.list=[]
        self.center_list=[]
    #センターカラーであれば配列に格納
    def is_centercolor(self,center_colors):
        flag=False
        for cc in center_colors:
            if self.keyword in cc:
                flag=True
                break
        if flag==False:
         self.center_list.append(flag)
        return flag

#検索対象を記載
Article_list=[  Article("ひだまり,","ひだまり"),
                Article("Aチャンネル,","チャンネル"),
                Article("キルミー,","キルミー"),
                Article("NEWGAME,","GAME"),
                Article("ブレンド・S,","ブレンド"),
                Article("アニマ,","アニマエ"),
                Article("まぞく,","まちカド"),
                Article("恋アス,","恋する"),
                Article("おちフル,","おちこぼれ"),
                Article("RPG,","不動産"),
                Article("はるみ,","はるみ"),
                Article("ごきチャ,","ごきチャ"),
                Article("ぱわーおぶすまいる,","ぱわー"),
                Article("異なる次元の管理人さん,","異なる"),
                Article("すわすわ,","すわっぷ"),
                Article("精霊さまの難儀な日常 ,","精霊さま"),
                Article("しずねちゃんは今日も眠れない,","しずねちゃん"),
                Article("死神ドットコム,","死神ドットコム"),
                Article("mono,","mono"),                
                Article("ばっどがーる,","ばっどがーる"),
                Article("つむつき,","紡ぐ"),
                Article("またぞろ,","またぞろ")]




index=0
while index < len(mid_list):

    print ("\n{}年{}月号".format(year,month))
    
    #年月を格納
    date_list.append(str(year)+""+month_list[month-1])
    
    #スクレイピング
    url='http://www.dokidokivisual.com/magazine/carat/book/index.php?mid={0}'.format(mid_list[index])
    html=requests.get(url)

    source=BeautifulSoup(html.content,"html.parser")

    strongs=source.find_all("strong")
    
    keisai=[]
    center_colors=[]
    info=(source.find_all("div",class_="info"))[1]
    strongs=info.find_all("strong")

    #表紙と巻頭カラーが別かどうかで分ける
    if re.search('表紙(&|＆)巻頭カラー',info.text):
        print("both")
        start=0
        end=5
    elif re.search('表紙(&|＆)センターカラー',info.text):
        print("both")
        start=0
        end=5
    else:
        print("other")
        start=1
        end=6
    
    top_flag=0
    #センターカラー、表紙の格納
    for color in strongs[start:end]:
        if top_flag==0:
         #top.append(re.search('「.+',color.next).group())
         top.append(re.search('「.+',strongs[0].next).group())
         top_flag+=1
        center_colors.append(re.search('「.+',color.next).group())
        center_color_all.append(center_colors[-1])
    print(center_colors)
    
    #カラーのDataFrame型での格納
    #center_colors_month=np.vstack([center_colors_month,center_colors])
    df_color=pd.concat([df_color,pd.DataFrame(center_colors)],axis=1)
    
    print(center_colors_month)

    i=0
    articles=source.find("ul",class_="lineup").find_all("strong")
    for art in articles:
        try:
            i+=1
            name=art.string
            
            print(i,name)
            keisai.append(name)
            for color_index,art in enumerate(Article_list):
                if art.keyword in name and len(art.list)==index:
                    art.list.append(i)
                    if art.is_centercolor(center_colors):
                        art.center_list.append(i)
        except:
            pass 
    print(keisai) 
    #掲載順の格納
    df_keisaijun=pd.concat([df_keisaijun,pd.DataFrame(keisai)],axis=1)
    print(df_keisaijun)    


    for art in Article_list:
        if len(art.list)==index:
            art.list.append(None)
        if len(art.center_list)==index:
            art.center_list.append(None)

    index+=1

    if month==12:
        year+=1
        month=1
    else:
        month+=1

    sleep(1)

print(collections.Counter(center_color_all))



for art in Article_list:
    print(art.label)
    print(art.list)
    print(art.center_list)

#カラーの２次元配列の縦横を並び替える
df_color= pd.DataFrame(df_color).T

#掲載順の２次元配列の縦横を並び替える
df_keisaijun = pd.DataFrame(df_keisaijun).T
print(df_color)
print(df_keisaijun)

#作品ごとの掲載順位を出力
file_name = h_filename + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))+".csv"
with open(file_name, encoding='utf-8_sig',mode="w", newline='')as f: 
    writer = csv.writer(f,delimiter=',')
    #年月を出力
    writer.writerow(date_list)
    #表紙を表示
    writer.writerow(top) 
    #カラー掲載を表示
    for color in df_color:  
        writer.writerow(df_color[color])
    #掲載順を表示
    for kei in df_keisaijun:  
        writer.writerow(df_keisaijun[kei])
    #作品ごとの掲載順を表示
    for art in Article_list: 
        f.write(art.label)
        writer.writerow(art.list)
        f.write(art.label)
        writer.writerow(art.center_list)

    