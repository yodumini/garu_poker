#!/usr/bin/env python
# encoding: utf-8
'''
@time: 2021/12/17 下午5:56
@author: Sherwin (sherwin@pokermaster.com)
@file: Card.py
@type:
@project:
@desc: 發牌程序
'''

# 發牌
##設計發牌順序：

import random
import itertools
from PokerModel import PokerHelper

# Cards Module 代表一張牌
class Card:
    """A playing card"""
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    SUITS = ['s', 'h', 'c', 'd']

    def __init__(self, rank, suit, face_up=True):
        self.rank = rank
        self.suit = suit
        self.is_face_up = face_up

    def __str__(self):  # 重寫print訊息，打印一張牌
        if self.is_face_up:
            rep = self.rank + self.suit
        else:
            rep = "XX"
        return rep

    def pic_order(self):
        if self.rank == "A":
            FaceNum = 1
        elif self.rank == "T":
            FaceNum = 10
        elif self.rank == "J":
            FaceNum = 11
        elif self.rank == "Q":
            FaceNum = 12
        elif self.rank == "K":
            FaceNum = 13
        else:
            FaceNum = int(self.rank)

        if self.suit == "s":
            Suit = 1
        elif self.suit == "h":
            Suit = 2
        elif self.suit == "c":
            Suit = 3
        else:
            Suit = 4

        return (Suit - 1) * 13 + FaceNum

    def flip(self):
        self.is_face_up = not self.is_face_up

# 牌桌
class Deck:

    def __init__(self):
        self.cards = []

    def InitializeDeck(self):
        self.cards = []
        # write some codes for initialize the deck
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(rank, suit))

    def ShuffleDeck(self):
        """洗牌"""
        return random.shuffle(self.cards)

    def Pop_card(self):
        return self.cards.pop()

    def PrintDeck(self):
        for card in self.cards:
            print (card)
        print (len(self.cards))

class Pot:
    def __init__(self):
        self.pot_money = 0

class Community:
    def __init__(self):
        self.community_cards = []

    def add_cards(self, aCard):
        self.community_cards.append(aCard)

class Player:

    def __init__(self, name, position, buyin=100):
        self.name = name
        self.position = position
        self.holecards = []
        self.round_result = None
        self.result = None
        self.buyin = buyin
        self.current_status = "Alive"

    def add_cards(self, aCard):
        self.holecards.append(aCard)

    def init_holecards(self):
        self.holecards = []

    def choice_best_cards(self, community_cards):
        new_list = self.holecards + community_cards
        new_list = [str(x) for x in new_list]
        result = PokerHelper.GetBestChoise(new_list)
        self.round_result = result
        self.result = PokerHelper.evaluate_hand(result)

    def bet_money(self, bet_amount):
        if(self.current_money >= bet_amount):
            return self.withdraw_money(bet_amount)

    def withdraw_money(self, withdraw_amount):
        if(self.current_money > withdraw_amount):
            self.current_money -= withdraw_amount
            return "normal"
        elif(self.current_money == withdraw_amount):
            self.current_money = 0
            return "allin"
        else:
            return "abnormal"

    def get_pot_money(self, pot_amount):
        return self.save_money(pot_amount)

    def save_money(self, save_amount):
        self.current_money += save_amount
        return "saved"

    def the_action(self, action):
        self.action = action


class Game:

    STATE_INITIAL = 'initial'
    STATE_PREPARING = 'preparing'
    STATE_PREFLOP = 'preflop'
    STATE_FLOP = 'flop'
    STATE_TURN = 'turn'
    STATE_RIVER = 'river'
    STATE_SHOWDOWN = 'showdown'

    def __init__(self):
        self.game_deck = Deck()
        self.players = []
        self.community_cards = []
        self.state = Game.STATE_INITIAL

    def Notify(self):
        if self.state == Game.STATE_INITIAL:
            self.Start()

        if self.state == Game.STATE_PREPARING:
            self.Preflop()
        elif self.state == Game.STATE_PREFLOP:
            self.Flop()
        elif self.state == Game.STATE_FLOP:
            self.Turn()
        elif self.state == Game.STATE_TURN:
            self.River()
        elif self.state == Game.STATE_RIVER:
            self.Showdown()
        elif self.state == Game.STATE_SHOWDOWN:
            self.InitializeRound()

    def Start(self):
        print('-------------------------------------------------------')
        print('Initialize Game: ')
        self.community_cards = []
        self.InitializePlayers()
        self.InitializePot()
        self.InitializeRound()
        print ('InitializeRound')

    def InitializeRound(self):
        self.state = Game.STATE_PREPARING
        # Initialize Round
        self.game_deck.InitializeDeck()
        self.game_deck.ShuffleDeck()
        self.community_cards = []
        self.InitializePot()

        #Initialize Players's holecards
        for player in self.players:
            player.init_holecards()


    def InitializePlayers(self):
        self.players = []
        self.players.append(Player('Sherwin', 0))
        self.players.append(Player('Bill', 1))
        self.players.append(Player('Hayley', 2))
        self.players.append(Player('Eric', 3))
        self.players.append(Player('Eve', 4))

    def InitializePot(self):
        self.pot = Pot()

    def Preflop(self):
        self.state = Game.STATE_PREFLOP
        print ('-------------------------------------------------------')
        print ('Pre-Flop Stage: Deal 2 Hold Cards for each players')

        player_count = len(self.players)
        # allocate card to players (2 per each)
        for i in range(player_count * 2):
            self.players[i % player_count].add_cards(self.game_deck.Pop_card())

        self.PrintCards()

    def Flop(self):
        self.state = Game.STATE_FLOP
        print ('-------------------------------------------------------')
        print ('Flop Stage: Deal 3 Community Cards')
        self.game_deck.Pop_card()
        for i in range(3):
            self.community_cards.append(self.game_deck.Pop_card())
        self.PrintCards()

    def Turn(self):
        self.state = Game.STATE_TURN
        print ('-------------------------------------------------------')
        print ('Turn Stage: Deal 1 Community Card')
        self.game_deck.Pop_card()
        self.community_cards.append(self.game_deck.Pop_card())
        self.PrintCards()

    def River(self):
        self.state = Game.STATE_RIVER
        print ('-------------------------------------------------------')
        print ('River Stage: Deal 1 Community Card')
        self.game_deck.Pop_card()
        self.community_cards.append(self.game_deck.Pop_card())
        self.PrintCards()

    def Showdown(self):
        self.state = Game.STATE_SHOWDOWN
        print('-------------------------------------------------------')
        print('ShowDown Stage: Check BestCards and Choose Winner')
        for player in self.players:
            print('\nPlayer ' + str(player.name) + ':')
            player.choice_best_cards(self.community_cards)
            PokerHelper.PrintCards(player.round_result)
            # PokerHelper.PrintCards(player.result)
        winner = self.GetWinner()

    def GetWinner(self):
        players = self.players
        sorted_player = sorted(players, key=PokerHelper.cmp_to_key(PokerHelper.CompareTwoPlayerHands), reverse=True)

        print ('--------------------- sorted players ---------------------')
        for player in sorted_player:
            print (player.name)
            print (player.round_result)

        winner = sorted_player[0]

        print ('\nWinner => ' + winner.name + ', P' + str(winner.position))
        print (winner.round_result)

        return winner

    def PrintCards(self):
        #print hole cards
        print ('Hole Cards:')
        for player in self.players:
            print(player.name, [str(x) for x in player.holecards])
        print ('Community Cards:', [str(x) for x in self.community_cards])


    def main(self):
        print("遊戲開始")
        self.Start()
        self.Preflop()
        self.Flop()
        self.Turn()
        self.River()
        self.Showdown()


if __name__ == '__main__':
    print("開始德州撲克發牌流程")

    new_hand = Game()
    new_hand.main()
