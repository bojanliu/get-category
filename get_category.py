#coding:utf-8

from pyquery import PyQuery as pq
import os
import csv
import time

def main():

    file_path=raw_input(u'请输入待处理文件路径：')
    f=open(file_path,'rb')
    data=f.read().split('\r\n')
    f.close()
    
    result_dic={}
    i=1
    
    for item in data:
        if item=='':
            pass
        else:
            new_item=item.replace(' ','+')
            search_url="http://www.made-in-china.com/productdirectory.do?\
subaction=hunt&mode=and&style=b&isOpenCorrection=1&word="+new_item+"&comProvince=nolimit&code=0"

            htmlsource=pq(url=search_url)
            if htmlsource.hasClass('catalogBox'):
                htmlsource=htmlsource('.property')
                try:
                    category=htmlsource.children('a').eq(0).text()
                except Exception, e:
                    category='No category'
            else:
                category='No category'
                
            index=category.find('(')
            if index!=-1:
                try:
                    category=category[:index]
                except Exception, e:
                    category=category
                    
            result_dic[item]=category.rstrip()
            
        print 'Num %i is ok!'%i
        time.sleep(10)
        i=i+1
        
    return result_dic


def create_csv(result_dic):
    f=open(os.path.join(os.getcwd(),'\\category.csv'),'wb')
    writer=csv.writer(f)
    writer.writerow(['keyword','category'])
    
    for k,v in result_dic.items():
        try:
            writer.writerow([k,v])
        except Exception, e:
            writer.writerow(['Error','got an error'])
    f.close()
 

    
if __name__=='__main__':
    result_dic=main()
    create_csv(result_dic)
    
    print 'All have done at %s'%time.strftime(u'%H点%M分%S秒')
