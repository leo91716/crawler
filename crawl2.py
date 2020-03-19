import pyquery
import time
import urllib.parse as UP
import chardet
import requests
import pickle

def search():
    with open('main.html', 'r', encoding='utf-8') as f:
        html = f.read()
        dom = pyquery.PyQuery(html)
        authors=dom('div.r-ent>div.title>a').items()
        collect=[]
        #print(UP.urlparse('https://www.ptt.cc/bbs/Gossiping/index.html').hostname)
        for author in authors:
            #print('https://'+UP.urlparse('https://www.ptt.cc/bbs/Gossiping/index.html').hostname+author.attr('href'))
            getPage('https://'+UP.urlparse('https://www.ptt.cc/bbs/Gossiping/index.html').hostname+author.attr('href'),'_ga=GA1.2.960197224.1511101055; __cfduid=dbcc14ee81f396ae8d5e97baf227e83891582558387; _gid=GA1.2.543228460.1584540368; over18=1' ,'ptt.html')
            parseHTML(collect)
            time.sleep(5)




def getPage(url, cookie, saveFile):
    response = requests.get(
        url,
        headers={
            'Cookie': cookie
        }
        )
    if response.status_code != 200:
        print(f'status is not 200 ({response.status_code})')
        return
    det = chardet.detect(response.content)
    #print(response.content.decode(det['encoding']))
    with open(saveFile, 'wb') as f:
        f.write(response.content)



def parseHTML(collect):
    with open('ptt.html', 'r', encoding='utf-8') as f:
        html = f.read()
        dom = pyquery.PyQuery(html)
        item={}
        author=dom('span.article-meta-tag').filter(lambda i: pyquery.PyQuery(this).text() == '作者').siblings('span.article-meta-value').text()
        authorID=author.split()[0]
        authorName=''.join(author.split()[1:])
        authorName= authorName.replace(')','').replace('(','')
        item['authorID']=authorID
        item['authorName']=authorName
        #print(authorID,'\n', authorName)



        title=dom('span.article-meta-tag').filter(lambda i: pyquery.PyQuery(this).text() == '標題').siblings('span.article-meta-value').text()
        title=title.split('] ')[-1]
        #print(title)
        item['title']=title


        publish_time=dom('span.article-meta-tag').filter(lambda i: pyquery.PyQuery(this).text() == '時間').siblings('span.article-meta-value').text()
        publish_time=publish_time.split('] ')[-1]
        #print(publish_time)
        item['publish_time']=publish_time



        print('content---------------')
        # contents=dom('div#main-content:last-child')
        # print(contents.text())
        
        contents =dom('div#main-content').children().items()
        #print(contents.items())
        final_content=''
        for content in contents:
            #print(content.children().text())
            
            if '時間' in content.children().text():
                #print('\n'.join(content.__str__().split('\n')[1:]))
                final_content='\n'.join(content.__str__().split('\n')[1:])
                item['time']=final_content
                break;
            

        print('final content', final_content)
        
        
        pushes = dom('div.push').items()
        #print(type(pushes))
        
        for push in pushes:
            item2={}
            #print(push.children('span.push-userid').text())
            #print(push.children('span.push-content').text())
            #print(''.join(push.children('span.push-ipdatetime').text().split(' ')[1:]))
            item2['userID']=push.children('span.push-userid').text()
            item2['userComment']=push.children('span.push-content').text()
            item2['userTime']=''.join(push.children('span.push-ipdatetime').text().split(' ')[1:])
            #print('--------------------------')
            item2.update(item)
            #print('item2',item2)
            collect.append(item2)
        
        with open('crawler.pickle', 'wb') as f:
            pickle.dump(collect,f, protocol=pickle.HIGHEST_PROTOCOL)
        
        





if __name__ == '__main__':
    getPage('https://www.ptt.cc/bbs/Gossiping/index.html', '_ga=GA1.2.960197224.1511101055; __cfduid=dbcc14ee81f396ae8d5e97baf227e83891582558387; _gid=GA1.2.543228460.1584540368; over18=1','main.html')
    search()
    #getPage('https://www.ptt.cc/bbs/Gossiping/M.1580810317.A.16C.html', '_ga=GA1.2.960197224.1511101055; __cfduid=dbcc14ee81f396ae8d5e97baf227e83891582558387; _gid=GA1.2.543228460.1584540368; over18=1', 'ptt.html')
    #getPage('https://www.ptt.cc/bbs/Gossiping/M.1584622063.A.315.html', '_ga=GA1.2.960197224.1511101055; __cfduid=dbcc14ee81f396ae8d5e97baf227e83891582558387; _gid=GA1.2.543228460.1584540368; over18=1')
    #parseHTML()


    #with open('crawler.pickle', 'rb') as file:
    #      a=pickle.load(file)
    #print(a)