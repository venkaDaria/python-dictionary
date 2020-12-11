# coding: utf-8
import random

from django.db import models

colors = ['aquamarine', 'coral', 'cyan', 'fuchsia', 'gold', 'greenyellow', 'lightseagreen',
          'lightgray', 'lightskyblue', 'limegreen', 'whitesmoke', 'palegreen', 'tomato', 'violet',
          'yellow', 'thistle', 'pink', 'plum', 'powderblue', 'dodgerblue', '#b3daff',
          '#ffccff', '#ccff66', '#ffcc99', '#99ff99', '#66ffcc', '#ccccff', '#ff9999',
          '#ffeb99', '#ffc299', '#ffb3d9', '#e0b3ff', '#c1c18a', '#ccff99', '#e6ccff',
          '#b3ffff', '#ffbb99', '#ff99e6', '#ffd699', '#e6b3b3', '#c2d6d6', '#d1d1e0', ]


class Word(models.Model):
    value = models.CharField(max_length=100)
    lang = models.CharField(max_length=10)
    order = models.IntegerField()
    block = models.ForeignKey('WordBlock', related_name='words')
    info = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.value

    # for compatibility
    def __str__(self):
        return self.__unicode__()


class WordBlock(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.words_string()

    # for compatibility
    def __str__(self):
        return self.__unicode__()

    def words_string(self):
        return ', '.join([w.value for w in self.ordered_words()])

    def ordered_words(self):
        return self.words.order_by('order')


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    # for compatibility
    def __str__(self):
        return self.__unicode__()

    @classmethod
    def get_random_color(cls):
        return random.choice(colors)


class Chain(models.Model):
    ru_block = models.ForeignKey('WordBlock', related_name='ru_chain', null=False, blank=False)
    en_block = models.ForeignKey('WordBlock', related_name='en_chain', null=False, blank=False)
    de_block = models.ForeignKey('WordBlock', related_name='de_chain', null=False, blank=False)
    part_speech = models.CharField(max_length=255)
    tag = models.ForeignKey('Tag', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.ru_block.words_string() + ", " + self.en_block.words_string() + ", " + self.de_block.words_string()

    # for compatibility
    def __str__(self):
        return self.__unicode__()

    def contains(self, s):
        if s in self.part_speech or s in self.tag.name:
            return True
        for words in [self.ru_block.words.all(),
                      self.en_block.words.all(),
                      self.de_block.words.all()]:
            for word in words:
                if s in word.value or s in word.info:
                    return True
        return False
