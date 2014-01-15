#-*-coding:utf-8-*-
import toolbox
import database


"""
serepo --- sentenceRepository
"""


class sentenceRepository:
    """
    sentenceRepository にアクセスするためのオブジェクトを生成
    """
    def __init__(self):
        """
        事例データの集合を格納するためのコレクションcolnameを指定して接続
        """
        self.db = database.database('config.xml')
        self.col = self.db.getSerepo()

    def editDescription(self, desc):
        """
        コレクションの説明を記述。任意。
        """
        self.col.update({u'name': u'description'}, {u'cont': desc}, True)

    def setSentence(self, sentence_d, sentence_j, tags):
        """
        データベースに文データとタグ，キーワードを保存
        """
        kwj = toolbox.getJKeyWords(sentence_j)
        kwd = toolbox.getDKeyWords(sentence_d)
        params = {}
        params[u'sentence_d'] = sentence_d
        params[u'sentence_j'] = sentence_j
        params[u'keyword_j'] = kwj
        params[u'keyword_d'] = kwd
        params[u'tags'] = tags
        self.col.insert(params)

    def getSentencesByTags(self, tags):
        """
        tag のリストを使って文データ取得
        """
        res = self.col.find({u'tags': {u'$all': tags}})
        return [sentence(r) for r in res]

    def getSentencesByKeywords(self, kws, jd):
        """
        keywordのリストkwsを使って文データ取得。jdで日本語・ドイツ語の別を指定
        """
        paramname = u'keyword_%s' % jd
        res = self.col.find({paramname: {u'$all': kws}})
        return [sentence(r) for r in res]

    def updateSentence(self, sid, param, value):
        """
        sentence id を使って，sentenceDataをアップデート。
        paramとパラメータの対応は以下のとおり：
        u'sentence_j': 日本語文。
        u'sentence_d': ドイツ語文。
        u'tags': タグ
        """
        if param == u'sentence_j':
            kwj = toolbox.getJKeyWords(value)
            udata = {param: value, u'keyword_j': kwj}
            self.col.update({u'_id': sid}, udata, False)
        elif param == u'sentence_d':
            kwd = toolbox.getDKeyWords(value)
            udata = {param: value, u'keyword_d': kwd}
            self.col.update({u'_id': sid}, udata, False)
        else:
            self.col.update({u'_id': sid}, {param: value}, False)

    def removeSentenceBySid(self, sid):
        self.col.remove({u'_id': sid})


class sentence:
    def __init__(self, sentenceData):
        """
        sentence オブジェクト
        """
        self.sentenceData = sentenceData

    def getJSentence(self):
        """
        日本語文取得
        """
        return self.sentenceData[u'sentence_j']

    def getDSentence(self):
        """
        ドイツ語文取得
        """
        return self.sentenceData[u'sentence_d']

    def getTags(self):
        """
        tag取得
        """
        return self.sentenceData[u'tags']

    def getSid(self):
        """
        文id取得。文の編集は親のsentenceRepositoryオグジェクトを介して行うが，
        その時にsidが必要。
        """
        return self.sentenceData[u'_id']
