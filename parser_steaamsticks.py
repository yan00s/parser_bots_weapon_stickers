from os import mkdir,listdir
import requests
import json
import time
import re
__author__ = "telegram = @yan00s"
__version__ = "1.0"
print(f"author = yan00s")


def assetid_search(assetid_list,classid):
    for assetid in assetid_list:
        if assetid['classid'] == classid:
            assetid = assetid['assetid']
            return assetid
def descriptions_and_assetid_list(url):
    resp = requests.get(url)
    steamid = re.findall(r'"steamid":"(.{17})",',resp.text)[0]
    items_resp = requests.get(f'https://steamcommunity.com/inventory/{steamid}/730/2?l=english&count=2000').json()
    descriptions = items_resp['descriptions']
    assetid_list = items_resp['assets']
    return steamid,descriptions,assetid_list

def sum_min_max_gun(descriptions):
    l = 0
    for name_gun in descriptions:
        if 'Well-Worn' or 'Factory New' or 'Field-Tested' or 'Battle-Scarred' or 'Minimal Wear' in name_gun:
            check_stik = str(name_gun['descriptions'])
            if 'stickers' in check_stik or 'Наклейка' in check_stik:
                l += 1
    return l



def item_links(descriptions,assetid_list,steamid):
    with open('./stikers_search.txt','r') as f:
        stik_search_list = f.read().split('\n')
        if len(stik_search_list) < 1:
            print('please add key words in file "stikers_search.txt"')
            input()
            exit(0)
    max_num = sum_min_max_gun(descriptions)
    min_num = 1
    for item_link in descriptions:
        name_gun = item_link['market_name']
        est = 0
        if 'Well-Worn' or 'Factory New' or 'Field-Tested' or 'Battle-Scarred' or 'Minimal Wear' in name_gun:
            check_stik = str(item_link['descriptions'])
            if 'stickers' in check_stik or 'Наклейка' in check_stik:
                print(f'[{min_num}/{max_num}] parsing stickers')
                min_num += 1
                classid = item_link['classid']
                stickers = str(re.findall(r'<br>(.*?)<',str(item_link))[1]).split(',')
                if len(stik_search_list) <= 1:
                    if stik_search_list[0] == '':
                        return print("you didn't uploads name or keyworld")
                for name_stiker in stickers:
                    for ear in stik_search_list:
                        ear = str(ear).strip()
                        if ear in name_stiker or name_stiker in stik_search_list:
                            print('what you were looking for found!!!')
                            est += 1
                if est > 0:
                    wear = None
                    asset = assetid_search(assetid_list,classid)
                    url_profile = f"https://steamcommunity.com/profiles/{steamid}"
                    url = f'steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S{steamid}A{asset}D000'
                    f = 0
                    resp0 = None
                    while f < 3:
                        f += 1
                        try:
                            hed = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'}
                            resp0 = requests.get(f"https://api.csgofloat.com/?url={url}",headers=hed,timeout=1) # {"error":"Valve's servers didn't reply in time","code":4,"status":500}
                            resp:dict = resp0.json()
                            if not 'error' in resp.keys():
                                if 'iteminfo' in resp.keys():
                                    break
                                time.sleep(0.5)
                            else:
                                time.sleep(0.5)
                        except:
                            time.sleep(3)
                    if f == 3:
                        with open(f'./result/complete_search.txt', 'a', encoding="utf-8") as fp:
                            info = f"{url_profile}\nname_gun == {name_gun} float == '???????'\nstikers: (stickers 'wear' unknown)\n{stickers}\n\n" 
                            fp.write(info)
                        continue
                    getr = resp['iteminfo']
                    stiker_list = []
                    for stikers in getr['stickers']:
                        wear = None
                        stikers:dict = stikers
                        name_stiker = stikers['name']
                        try:
                            if 'wear' in stikers.keys():
                                wear = stikers['wear']
                                if wear != None:
                                    wear = f'{str(wear)[2:4]}%'
                        except:
                            pass
                        if not wear == None:
                            stiker_list.append({'name_stiker':name_stiker,'wear':wear})
                        else:
                            stiker_list.append({'name_stiker':name_stiker})
                    with open(f'./result/complete_search.txt', 'a', encoding="utf-8") as fp:
                        info = f"{url_profile}\nname_gun == {getr['full_item_name']} float == {getr['floatvalue']}\nstikers:\n{stiker_list}\n\n" 
                        fp.write(info)
                        continue
            else:
                continue




with open('./links_profile.txt','r') as f:
    links = f.read().split('\n')
    if len(links) < 1:
        print('please add link in file "links_profile.txt"')
        input()
        exit(0)
dirs = listdir('./')
if 'result' not in dirs:
    mkdir('./result')
if 'links_profile.txt' not in dirs:
    t = 'please create and add key worlds in file "links_profile.txt"'
    print(t)
    input()
    exit(0)
if 'stikers_search.txt' not in dirs:
    t = 'please create and add link in file "stikers_search.txt"'
    print(t)
    input()
    exit(0)


for url_ivent in links:
    if len(url_ivent) < 3:
        continue
    print(f'[{links.index(url_ivent)+1}/{len(links)}] getting steamid...')
    try:
        steamid,descriptions,assetid_list = descriptions_and_assetid_list(url_ivent)
    except Exception as e:
        print(f'error on 0 {e}')
        input()
    try:
        item_links(descriptions,assetid_list,steamid)
    except Exception as e:
        print(f'error on 1 {e}')
        input()
    time.sleep(5)
print('complete successfully')
input()
