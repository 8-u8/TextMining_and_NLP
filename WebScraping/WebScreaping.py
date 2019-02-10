# coding: utf-8
# scraping Wikipedia description from Movie Title.
import pandas as pd
import numpy as np
import bs4
import urllib
import csv
import re

# Japanese Language Encoder
def JapaneseEncoding(Title):
    nameToEncode = str(Title)
    JapaneseLang = r'[^\x00-\x7F]' # 日本語の全表現
    JapaneseWardList = re.findall(JapaneseLang, Title) # 入力から日本語だけのリストを抽出
    Encodedname = nameToEncode.replace(JapaneseWardList, urllib.parse.quote_plus(JapaneseWardList, safe = "/?=&",encoding='utf-8'))
    return Encodedname

# scraper
def scraper(wikiTitle):
    WikiDomain = "https://ja.wikipedia.org/" # wikipedia日本語版
    # wikiurl
    '''
    日本語が入るのでちょっと考えた．
    参考: https://qiita.com/mix/items/87d094414e46f857de45
    今回はUrlリストが確実に日本語なので割と雑にしていいと思った．
    '''
    url = WikiDomain + JapaneseEncoding(wikiTitle)
    html = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(html, "html.parser")

    TitleIndex = soup.find("ul",attrs = {"ここにWikipediaのhtmlからそれっぽいものを持ってくる．"})
    Description = TitleIndex.find_all("span", attrs = {"a","b"})
    for description in Description:
        print(description.contents[0], description.span.string)
