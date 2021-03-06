#!/usr/bin/env python
# encoding: utf-8
'''
@time: 2021/12/17 下午5:07
@author: Sherwin (sherwin@sh88w.com)
@file: PokerModel.py
@type: 
@project: 
@desc: 辨識最佳手牌
'''
import itertools
from collections import Counter


# 最佳手牌
class PokerHelper:
    def __init__(self):
        pass

    @staticmethod
    def numeric_ranks(cards):
        """
        numeric_ranks(['AS','3S','4S','5S','JC'])
        returns ['14S','3S','4S','5S','11C']
        """
        FACE_VALUES = {'A': 14, 'J': 11, 'Q': 12, 'K': 13, 'T': 10}
        return [str(FACE_VALUES.get(card[:-1], card[:-1]))+card[-1] for card in cards]


    @staticmethod
    def sort_cards(cards):
        """
        sort_cards(['AS','3S','4S','5S','JC'])
        returns
        ['3S','4S','5S','11C','14S']
        """
        cards = PokerHelper.numeric_ranks(cards)
        new_order = [(int(i[:-1]), i) for i in cards]
        new_order.sort(key=lambda x: x[0], reverse=True)
        return [i[1] for i in new_order]


    @staticmethod
    def get_ranks(cards):
        """
        取出手牌數字
        2-14 一至兩位數所以選取[:-1]
        """
        return [int(card[:-1]) for card in cards]


    @staticmethod
    def get_suits(cards):
        """
        取出手牌花色
        """
        return [card[-1] for card in cards]


    @staticmethod
    def evaluate_hand(cards):
        """
        手牌牌型
        """
        ranks = PokerHelper.get_ranks(cards)
        suits = PokerHelper.get_suits(cards)

        if len(set(cards)) < len(cards) or max(ranks) > 14 or min(ranks) < 1 or set(suits).difference(['s', 'h', 'c', 'd']):
            return '無效'

        if PokerHelper.isconsecutive(ranks):
            return (
                '順子' if not PokerHelper.all_equal(suits) else
                '同花順' if max(ranks) < 14 else
                '皇家同花順'
            )
        if PokerHelper.all_equal(suits):
            return '同花'
        total = sum([ranks.count(x) for x in ranks])
        hand_names = {
            4 + 4 + 4 + 4 + 1: '四條',
            3 + 3 + 3 + 2 + 2: '葫蘆',
            3 + 3 + 3 + 1 + 1: '三條',
            2 + 2 + 2 + 2 + 1: '兩對',
            2 + 2 + 1 + 1 + 1: '一對',
            1 + 1 + 1 + 1 + 1: '高牌',}
        return hand_names[total]


    @staticmethod
    def all_equal(lst):
        """
        確認花色是否一致 for Flush
        all_equal(['S,'S','S']) returns True
        """
        return len(set(lst)) == 1

    @staticmethod
    def isconsecutive(lst):
        """
        確認花色是否一致 for Straight
        """
        return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1

    @staticmethod
    def GetBestChoise(cards):
        cards = PokerHelper.sort_cards(cards)
        hand_score = lambda x: ['高牌', '一對', '兩對', '三條', '順子', '同花', '葫蘆', '四條', '同花順', '皇家同花順', '無效'].\
            index(PokerHelper.evaluate_hand(x))
        cards = [i for i in itertools.combinations(cards, 5)]
        best_card = max(cards, key=hand_score)
        # return self.evaluate_hand(best_card)
        return best_card

    @staticmethod
    def PrintCards(card_list):
        print(card_list)
        print(PokerHelper.evaluate_hand(card_list))

    @staticmethod
    def cmp_to_key(mycmp):
        # 'Convert a cmp= function into a key= function'
        class K:
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K

    @staticmethod
    def Compare_Recursion(sett1, sett2, num=0):
        if sett1.most_common()[num][0] > sett2.most_common()[num][0]:
            return 1
        elif sett1.most_common()[num][0] < sett2.most_common()[num][0]:
            return -1
        else:
            num += 1
            while num < len(sett1):
                return PokerHelper.Compare_Recursion(sett1, sett2, num=num)
            return 0


    @staticmethod
    def CompareTwoPlayerHands(h1, h2):
        CARKRANKLIST = ['無效', '高牌', '一對', '兩對', '三條', '順子', '同花', '葫蘆', '四條', '同花順', '皇家同花順']
        one, two = CARKRANKLIST.index(h1.result), CARKRANKLIST.index(h2.result)
        if one > two:
            return 1
        elif one < two:
            return -1
        else:
            h1, h2 = PokerHelper.sort_cards(h1.round_result), PokerHelper.sort_cards(h2.round_result)
            sett1, sett2 = PokerHelper.get_ranks(h1), PokerHelper.get_ranks(h2)
            sett1, sett2 = Counter(sett1), Counter(sett2)
            return PokerHelper.Compare_Recursion(sett1, sett2)


if __name__ == '__main__':

    # DESK_CARD = ['Qs', 'Qc']
    # HAND_CARD = ['Qd', 'Qh', '9d', 'As', '8c']
    #
    # cards = DESK_CARD+HAND_CARD
    # best_hand = PokerHelper().GetBestChoise(cards)
    # print(best_hand, PokerHelper().evaluate_hand(best_hand))


    # full house
    # flush
    a = ['11h', '11s', '11c', '8h', '8c']
    s = ['11d', '11s', '11c', '8h', '8c']
    print(PokerHelper.CompareTwoPlayerHands(a, s))
