import urllib.request
import urllib.parse
import json
import os
cityList = [
['东城区','110101'],
['西城区','110102'],
['朝阳区','110105'],
['丰台区','110106'],
['石景山区'	,'110107'],
['海淀区','110108'],
['门头沟区','110109'],
['房山区','110111'],
['通州区','110112'],
['顺义区','110113'],
['昌平区','110114'],
['大兴区','110115'],
['怀柔区','110116'],
['平谷区	','110117'],
['密云区','110118'],
['延庆区','110119'],
]
def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8','ignore')
    return html
#
def get_urlList():
    key = "8497a4c99fdd42e0ad3152f8a77f41aa"
    engGS = urllib.parse.quote("麦当劳")
    urlList = []
    for city in cityList:
        url = "http://restapi.amap.com/v3/place/text?key="+key+"&keywords="+engGS+"&city="+city[1]+"&children=1&extensions=all&citylimit=true"
        urlList.append(url)
    return urlList

def total_gasStation():
    urlList = get_urlList()
    i = 0
    totalNum = 0
    cityListNo = []
    for url in urlList:
        html = url_open(url)
        target = json.loads(html)
        gsNo = int(target['count'])
        pageNo = divmod(gsNo,20)[0]+1 if divmod(gsNo,20)[1]>0 else divmod(gsNo,20)[0]
        cityListNo.append([cityList[i][0],cityList[i][1],gsNo,pageNo])
        totalNum = totalNum + gsNo
        i = i + 1
    # ['024', '沈阳', 528, 27]
    return cityListNo

def get_GSByCity():
    cityListNo = total_gasStation()
    key = "8497a4c99fdd42e0ad3152f8a77f41aa"
    engGS = urllib.parse.quote("麦当劳")
    cityUrlList = []
    for city in cityListNo:
        urlList = []
        for i in range(city[3]):
            url = "http://restapi.amap.com/v3/place/text?key="+key+"&keywords="+engGS+"&city="+city[1]+"&children=1&offset=20&page="+str(i+1)+"&extensions=all&citylimit=true"
            urlList.append(url)
        cityUrlList.append(urlList)
    return cityUrlList

def get_gsList():
    cityUrlList = get_GSByCity()
    #cityurl为沈阳市的27个url
    allList = []
    for cityUrl in cityUrlList:
        cityPoisList = []
        for url in cityUrl:
            html = url_open(url)
            target = json.loads(html)
            pagePoisList = target['pois']
            cityPoisList.append(pagePoisList)
        cityPoisList = sum(cityPoisList,[])
        allList.append(cityPoisList)
    allList = sum(allList,[])
    ffff = []
    i= 0
    for aList in allList:
        try:
            print(aList['type'])
            dddd =aList['name']+'\t'+aList['pname']+'\t'+aList['adname']+'\t'+aList['adcode']+'\t'+aList['address']+'\t'+aList['type']+'\t'+aList['location']+'\n'
            i=i+1
        except Exception as e:
            continue
        else:
            ffff.append(dddd)

    
    os.getcwd()
    file_name = 'McDonald.txt'
    f = open(file_name,'w')
    f.writelines(ffff)
    f.close()
    
if __name__ == '__main__':
    get_gsList()
