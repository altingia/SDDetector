#!/usr/bin/env python

import logging

from SDDetector.Entities.Chain import Chain

class AlignmentChainer(object):

    def __init__(self, db, maxGap=3000, logLevel='ERROR'):
        """AlignmentChainer constructor"""

        self.db = db
        self.maxGap = maxGap
        self.logLevel = logLevel
        self.dIndex = {}
        self.lChains = []

        logging.basicConfig(level=logLevel)


<<<<<<< HEAD
    def chainAlignments2(self, lAlgmts):
=======
    def chainAlignments(self, lAlgmts):
        """Build the list of chains and keep position of alignments in chains"""
>>>>>>> eebe332c5cce0d1e6ee1a022995181b7e151de68

        maxOverlap = 0

        for algmt in lAlgmts:
            if algmt.id not in self.dIndex:
                chain = Chain([algmt])
                index = len(self.lChains)
                self.lChains.append(chain)
                self.dIndex[algmt.id] = [index]

	    lProximalAlgmts = self.db.selectProximalAlgmts(algmt.id, self.maxGap)

            for proxAlgmt in lProximalAlgmts:
                if abs(self.distanceBetweenQueryAlgmts(algmt,proxAlgmt)) < self.maxGap and self.distanceBetweenQueryAlgmts(algmt,proxAlgmt) > -maxOverlap:
                    if abs(self.distanceBetweenSbjctAlgmts(algmt,proxAlgmt)) < self.maxGap and self.distanceBetweenSbjctAlgmts(algmt,proxAlgmt) > -maxOverlap:
                        if self.distanceBetweenQuerySbjctAlgmts(algmt,proxAlgmt) > -maxOverlap:
                            if self.distanceBetweenQuerySbjctAlgmts(proxAlgmt,algmt) > -maxOverlap:

                                lChainIdsCurrentAlgmt = self.dIndex[algmt.id]
                                newChainTodo = False
                                for chainId in lChainIdsCurrentAlgmt:
                                    lAlgmtsCurrentChain = self.lChains[chainId].sortListOfAlgmts()
                                    ToInclude = True
                                    for cAlgmt in lAlgmtsCurrentChain:
                                        if self.distanceBetweenQueryAlgmts(proxAlgmt,cAlgmt) < -maxOverlap:
                                            ToInclude = False
                                            break
                                        if self.distanceBetweenSbjctAlgmts(proxAlgmt,cAlgmt) < -maxOverlap:
                                            ToInclude = False
                                            break
                                        if self.distanceBetweenQuerySbjctAlgmts(proxAlgmt,cAlgmt) < -maxOverlap:
                                            ToInclude = False
                                            break
                                        if self.distanceBetweenQuerySbjctAlgmts(cAlgmt,proxAlgmt) < -maxOverlap:
                                            ToInclude = False
                                            break
<<<<<<< HEAD

                                        if not self.assertRankForAlgmts(lAlgmtsCurrentChain[::1],proxAlgmt):
                                            print "NOTASSERRANK !!"
=======
                                        if not self.assertRankForAlgmts(lAlgmtsCurrentChain[::1],proxAlgmt):
>>>>>>> eebe332c5cce0d1e6ee1a022995181b7e151de68
                                            ToInclude = False


                                    if ToInclude:
                                        if proxAlgmt.id not in self.lChains[chainId].getIdListOfAlgmts():
                                            self.lChains[chainId].lAlgmts.append(proxAlgmt)
                                            if proxAlgmt.id in self.dIndex:
                                                self.dIndex[proxAlgmt.id].append(chainId)
                                            else:
                                                self.dIndex[proxAlgmt.id] = [chainId]
                                        else:
<<<<<<< HEAD
                                            print "BUGBUGNUG"

=======
                                            logging.error("error in chaining - possible bug")
>>>>>>> eebe332c5cce0d1e6ee1a022995181b7e151de68
                                    else:
                                        newChainTodo = True

                                if newChainTodo:
                                    chain = Chain([algmt,proxAlgmt])
                                    index = len(self.lChains)
                                    self.lChains.append(chain)
                                    self.dIndex[algmt.id] = [index]



    def assertRankForAlgmts(self,lAlgmts,algmt):
<<<<<<< HEAD
        lAlgmts.append(algmt)
        lSortedSbjct = lAlgmts.sort(key=lambda algmt: algmt.sstart)
        lSortedQuery = lAlgmts.sort(key=lambda algmt: algmt.qstart)

=======

        lAlgmts.append(algmt)
        lSortedSbjct = sorted(lAlgmts,key=lambda algmtc: algmtc.sstart)
        lSortedQuery = sorted(lAlgmts,key=lambda algmtc: algmtc.qstart)
>>>>>>> eebe332c5cce0d1e6ee1a022995181b7e151de68
        if lSortedSbjct == lSortedQuery or lSortedSbjct == lSortedQuery[::-1]:
            return True
        else:
            return False


<<<<<<< HEAD
    def chainAlignments(self, lAlgmts):
        """Build the list of chains and keep position of alignments in chains"""

        for algmt in lAlgmts:
            if algmt.id not in self.dIndex:
                chain = Chain([algmt])
                index = len(self.lChains)
                self.lChains.append(chain)
                self.dIndex[algmt.id] = [index]

            lChainIdsCurrentAlgmt = self.dIndex[algmt.id]
	    lProximalAlgmts = self.db.selectProximalAlgmts(algmt.id, self.maxGap)
            for proxAlgmt in lProximalAlgmts:
                for chainId in lChainIdsCurrentAlgmt:
                    if self.distanceBetweenQueryAlgmts(algmt,proxAlgmt) < self.maxGap and self.distanceBetweenQueryAlgmts(algmt,proxAlgmt) > 0:
                        if proxAlgmt.id not in self.lChains[chainId].getIdListOfAlgmts():
                            self.lChains[chainId].lAlgmts.append(proxAlgmt)
                            if proxAlgmt.id in self.dIndex:
                                self.dIndex[proxAlgmt.id].append(chainId)
                            else:
                               self.dIndex[proxAlgmt.id] = [chainId]


        self.removeInternalAlignments()


        return
=======
>>>>>>> eebe332c5cce0d1e6ee1a022995181b7e151de68

    def removeInternalAlignments(self):
        """
           remove match with internal similarity

                 a     b   c              d
           q1  --|-----|---|--------------|--


           s1  ------------|----|-----|---|--

                           c'   a'    b'  d'
        """

        ltmp = []
        #print "nb chains: {}".format(len(self.lChains))
        for i,chain in enumerate(self.lChains):
            lAlgmtIds = set(self.db.selectQueryOnlySuboptimalAlgmts(chain.getIdListOfAlgmts()))
            lAlgmtIds.union(self.db.selectSubjectOnlySuboptimalAlgmts(chain.getIdListOfAlgmts()))
        #    print lAlgmtIds
        #    print "nb algmts chain id: {}, nb {}".format(i, chain.getNbAlgmts())
            chain.deleteListOfAlgmts(lAlgmtIds)
        #    print "nb algmts chain id: {}, nb {} - after".format(i, chain.getNbAlgmts())
            for algmtId in lAlgmtIds:
                index = self.dIndex[algmtId].index(i)
                del(self.dIndex[algmtId][index])
            if chain.getNbAlgmts() == 1:
                ltmp.append(chain)
            if chain.getNbAlgmts() > 1:
                for i,algmt in enumerate(chain.sortListOfAlgmts()[:-1]):
                    if self.distanceBetweenQueryAlgmts(chain.sortListOfAlgmts()[i],chain.sortListOfAlgmts()[i+1]) < self.maxGap:
                        ltmp.append(chain)
        self.lChains = ltmp

    def distanceBetweenQueryAlgmts(self, algmt1, algmt2):
        """Compute and return the distance between 2 alignments

        hypthesis to check !!! algmt1 always start before algmt2 """

        if algmt1.qstart < algmt2.qstart:
            return algmt2.qstart - algmt1.qend - 1
        else:
            return algmt1.qstart - algmt2.qend - 1

    def distanceBetweenSbjctAlgmts(self, algmt1, algmt2):
        """Compute and return the distance between 2 alignments

        algmt1 start before 2"""


        if algmt1.sstart < algmt2.sstart:
            return algmt2.sstart - algmt1.send - 1
        else:
            return algmt1.sstart - algmt2.send - 1

    def distanceBetweenQuerySbjctAlgmts(self, algmt1, algmt2):
        """Compute and return the distance between 2 alignments

        hypthesis to check !!! algmt1 always start before algmt2 """

        if algmt1.sstart < algmt2.qstart:
            return algmt2.qstart - algmt1.send - 1
        else:
            return algmt1.sstart - algmt2.qend - 1


    def sortListOfChains(self, lChains):
        """Return a sorted list of chains"""

        ltmp = []
        for i, chain in enumerate(lChains):
            lAlgmts = chain.sortListOfAlgmts()
            for j,algmt in enumerate(lAlgmts):
                if j == 0:
                    sstartMin = algmt.sstart
                    sendMax = algmt.send
                if algmt.sstart < sstartMin:
                    sstartMin = algmt.sstart
                if algmt.send > sendMax:
                    sendMax = algmt.send
            ltmp.append((algmt.sbjct, sstartMin, sendMax, algmt.query, i))
        ltmp.sort(key=lambda x: ('{0:0>150}'.format(x[0]).lower(), x[1], x[2], '{0:0>150}'.format(x[3])))
        return [ lChains[row[4]] for row in ltmp  ]


    def removeChainsWithInternalSimilarity(self, lChains):
        """
           return a non-internal similarity list of chains

                 a       b   c              d
           chr1  --|-----|---|--------------|--------------------


           chr1  ---------------------|-----|---|----------------|--

                                      a'    b'  d'               a'

           internal similarity between both alignments

        """

        ltmp = []

        for i,chain in enumerate(lChains):
            if chain.lAlgmts[0].query == chain.lAlgmts[0].sbjct:
                if (chain.getSStart() >= chain.getQStart() and chain.getSStart() < chain.getQEnd()):
                    ltmp.append(i)
                elif (chain.getSStart() <= chain.getQStart() and chain.getSEnd() > chain.getQStart()):
                    ltmp.append(i)
                elif (chain.getSEnd() > chain.getQStart() and chain.getSEnd() <= chain.getQEnd()):
                    ltmp.append(i)

        lChains = [ chain for i, chain in enumerate(lChains) if i not in ltmp ]

        return self.sortListOfChains(lChains)

    def removeOverlappingChains(self, lChains):
        """Return a non-overlapping list of chains"""

        ltmp = []

        for i, chain1 in enumerate(lChains[:-1]):
            for j, chain2 in enumerate(lChains[i+1:]):
                sTrue = False
                qTrue = False
        #        print 'chain {} (q:{},s:{}) vs chain {} (q:{},s{})'.format(i,chain1.lAlgmts[0].query,chain1.lAlgmts[0].sbjct,i+1,chain2.lAlgmts[0].query,chain2.lAlgmts[0].sbjct)

                if (chain1.lAlgmts[0].query == chain2.lAlgmts[0].query and chain1.lAlgmts[0].sbjct == chain2.lAlgmts[0].sbjct):

                    if (chain1.getSStart() >= chain2.getSStart() and chain1.getSStart() < chain2.getSEnd()):
                        sTrue = True
                    elif (chain1.getSStart() <= chain2.getSStart() and chain1.getSEnd() > chain2.getSStart()):
                        sTrue = True
                    elif (chain1.getSEnd() > chain2.getSStart() and chain1.getSEnd() <= chain2.getSEnd()):
                        sTrue = True
                    if (chain1.getQStart() >= chain2.getQStart() and chain1.getQStart() < chain2.getQEnd()):
                        qTrue = True
                    elif (chain1.getQStart() <= chain2.getQStart() and chain1.getQEnd() > chain2.getQStart()):
                        qTrue = True
                    elif (chain1.getQEnd() > chain2.getQStart() and chain1.getQEnd() <= chain2.getQEnd()):
                        qTrue = True

        #            print sTrue
        #            print qTrue

                    if sTrue and qTrue:
                        if chain1.getLength() > chain2.getLength():
                            ltmp.append(i+1)
                        elif chain1.getLength() < chain2.getLength():
                            ltmp.append(i)
                        elif chain1.getLength() == chain2.getLength():
                            if chain1.getNbAlgmts() > chain2.getNbAlgmts():
                               ltmp.append(i)
                            elif chain1.getNbAlgmts() < chain2.getNbAlgmts():
                               ltmp.append(i+1)
                            elif chain1.getNbAlgmts() == chain2.getNbAlgmts():
                               if chain1.getAlgmtMaxLength() > chain2.getAlgmtMaxLength():
                                   ltmp.append(i+1)
                               elif chain1.getAlgmtMaxLength() < chain2.getAlgmtMaxLength():
                                   ltmp.append(i)
                               else:
                                   ltmp.append(i+1)

        lChains = [ chain for i, chain in enumerate(lChains) if i not in ltmp ]

        return self.sortListOfChains(lChains)
