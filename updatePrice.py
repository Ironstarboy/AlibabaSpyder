import demo
import pandas as pd

spyder = demo.Spyder()

goodsInfo:pd.DataFrame=getGoodsInfo()
for index, goodsInfo in goodsInfo.iterrows():
    haveNan=0
    for i in goodsInfo:
        if pd.isna(i):
            haveNan=1
            print(f"{goodsInfo['productName']} 暂未在alibaba搜寻到")
            break
    if not haveNan:
        spyder.getPrice(goodsInfo)
print('价格更新完成')