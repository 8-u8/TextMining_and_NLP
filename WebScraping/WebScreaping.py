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
    #nameToEncode = Title
    #JapaneseLang = r'[^\x00-\x7F]' # 日本語の全表現
    #JapaneseWardList = re.findall(JapaneseLang, Title) # 入力から日本語だけのリストを抽出
    #Encodedname = urllib.parse.quote_plus(JapaneseWardList,encoding='utf-8')
    Encodedname = urllib.parse.quote_plus(Title, encoding = 'utf-8')
    return Encodedname

# scraper
def scraper(wikiTitle):
    WikiDomain = "https://ja.wikipedia.org/wiki/" # wikipedia日本語版
    # wikiurl
    '''
    日本語が入るのでちょっと考えた．
    参考: https://qiita.com/mix/items/87d094414e46f857de45
    今回はUrlリストが確実に日本語なので割と雑にしていいと思った．
    '''
    url = WikiDomain + JapaneseEncoding(wikiTitle)
    html = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(html, "html.parser")
    # wikipediaから得られたソースコードから適当名部分を抜いてくる
    # "<p></p>"を持ってくると間違いなさそう。あとはここから「○○映画」などを抜いてくれば……
    # <table>か？
    TitleIndex = soup.find("ul",attrs = {"<table><tbody>"})
    Description = TitleIndex.find_all("span", attrs = {"a","b"})
    for description in Description:
        print(description.contents[0], description.span.string)
