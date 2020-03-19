在 cmd 下， python crawl2.py 會分批爬下八卦板的每一篇文章，並存成 pickle 檔。
可在 python 使用以下方法來讀出一筆一筆的資料

with open('crawler.pickle', 'rb') as file:
          a=pickle.load(file)

print(a[0])


