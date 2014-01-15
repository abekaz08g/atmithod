#-*-coding:utf-8-*-
import treetagger
import MeCab
"""
便利なツール集
"""


def getJKeyWords(string):
    """
    日本語文字列をMeCab解析して、レマ形のリストを返す
    """
    m = MeCab.Tagger()
    res = m.parse(string.encode('utf-8'))
    #print res
    words = res.decode('utf-8').split('\n')
    if len(words) > 0:
        keyWords = [w.split(u',')[-3] for w in words if len(w.split(u',')) > 2]
    return keyWords


def getDKeyWords(string):
    """
    ドイツ語文字列をMeCab解析して、レマ形のリストを返す
    """
    t = treetagger.proc()
    ttd = t.run(string.encode('utf-8'))
    keyWords = ttd[u'lemma']
    return keyWords
