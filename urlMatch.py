# 根据产品名，在阿里巴巴上进行搜索，获取搜索结果的链接和产品名字
import pandas as pd
import demo
from tqdm import tqdm
df=pd.read_excel('Global SP Competitor grade and price tracking for Jiarong.xlsx')


titles=[]
urls=[]

productNames=df['Grade name'].tolist()
companyNames=df['Company'].tolist()

details=pd.read_excel('./Global SP Competitor grade and price tracking for Jiarong.xlsx')
urls=['']*len(productNames)
count=0
for i in tqdm(range(len(productNames))):
    searchKeys=f'{companyNames[i]} {productNames[i]}'
    print(f'###### searching {searchKeys} #############')
    spyder = demo.Spyder()
    title, url=spyder.saveUrlFromSearch(searchKeys)
    urls[i]=url

df['url']=urls
print()