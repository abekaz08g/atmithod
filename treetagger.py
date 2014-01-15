# -*- coding:utf-8 -*-
from subprocess import PIPE
from subprocess import Popen


class proc:
    def run(__self__, _input):
        ttg = 'tree-tagger-german-utf8'
        ttb = Popen([ttg], shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = ttb.communicate(_input.encode('UTF-8'))
        lines = [l.decode('UTF-8') for l in stdout.split('\n')]
        ttdict = {u'surface': [], u'pos': [], u'lemma': [], u'text': _input}
        for line in lines:
            rec = line.split('\t')
            if len(rec) == 3:
                ttdict[u'surface'].append(rec[0])
                ttdict[u'pos'].append(rec[1])
                ttdict[u'lemma'].append(rec[2])
        return ttdict
