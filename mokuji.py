#-*-coding:utf-8-*-
import re
import database

"""
教科書データベース，目次モジュール
"""


def getPageNumbers(pageRange):
    """
    目次ファイルから項目ごとにページ番号を抽出。簡単なパターン判断のロジックも含む。
    """
    st_end = pageRange.split(u'-')
    if len(st_end) == 2:
        pageNumbers = [i for i in range(int(st_end[0]), int(st_end[1]) + 1)]
    else:
        pageNumbers = [int(st_end[0])]
    return pageNumbers


def run(fin, lbid, col, cat):
    """
    実行メソッド
    """
    #col = startUpDB()
    f = open(fin)
    for line in f:
        uline = line.decode('utf-8')[:-1]
        rec = uline.split('\t')
        if len(rec) == 2:
            pnums = getPageNumbers(rec[1])
            params = {}
            params[u'cat'] = cat
            params[u'title'] = rec[0]
            params[u'pageNumbers'] = pnums
            params[u'lbid'] = lbid
            col.insert(params)


class mokujiItem:
    def __init__(self, mokujiData):
        self.mokujiData = mokujiData

    def getMokujiData(self):
        """
        目次データの取得
        """
        return self.mokujiData

    def getLbid(self):
        """
        教科書idの取得
        """
        return self.mokujiData[u'lbid']

    def getPageNumbers(self):
        """
        頁数の取得。リスト。
        """
        return self.mokujiData[u'pageNumbers']

    def getCat(self):
        """
        カテゴリーの取得。リスト。
        """
        return self.mokujiData[u'cat']

    def getTitle(self):
        """
        タイトルの取得
        """
        return self.mokujiData[u'title']


class lbbase:
    def __init__(self):
        """
        教科書目次データベースのコンストラクタ
        """
        self.db = database.database('config.xml')
        self.col = self.db.getLBbase()

    def setMokuji(self, fin, lbid, cat):
        """
        目次をデータベースに追加
        """
        if self.col.find({u'lbid': lbid}).count() > 0:
            print u'The Lbid is already used! Take another one.'
            return None
        run(fin, lbid, self.col, cat)

    def getMokuji(self, lbid):
        """
        lbidを指定して目次データを取得。
        """
        if self.col.find({u'lbid': lbid}).count() > 0:
            return [r for r in self.col.find({u'lbid': lbid})]
        else:
            return None

    def removeMokuji(self, lbid):
        """
        lbidを指定して目次データを削除
        """
        self.col.remove({u'lbid': lbid})

    def findWord(self, w):
        """
        単語を指定してタイトル検索。結果は目次アイテムオブジェクトの集合
        """
        pat = re.compile()
        if self.col.find({u'title': pat}) > 0:
            return [mokujiItem(r) for r in self.col.find({u'title': pat})]
