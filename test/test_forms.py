from django.test import TestCase

from main.forms import AddForm
from main.models import WordBlock, Chain, Tag, Word


class FormsTests(TestCase):
    def test_valid_form(self):
        form = self.create_form()
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = self.create_form(part_speech='')
        self.assertFalse(form.is_valid())

    @staticmethod
    def create_form(value='value for test', order=1, part_speech='сущ', tag_name='tag'):
        chain = FormsTests.create_chain(value, order, part_speech, tag_name)
        data = {
            # chain.ru_block.ordered_words().first().value
            'ru_value1': chain.ru_block,
            'en_value1': chain.en_block,
            'de_value1': chain.de_block,
            'part_speech': chain.part_speech,
            'tag': chain.tag
        }

        return AddForm(data=data)

    @staticmethod
    def create_chain(value, order, part_speech, tag_name):
        ru_word_block = WordBlock.objects.create()
        Word.objects.create(value=value, order=order, block=ru_word_block)

        en_word_block = WordBlock.objects.create()
        Word.objects.create(value=value, order=order, block=en_word_block)

        de_word_block = WordBlock.objects.create()
        Word.objects.create(value=value, order=order, block=de_word_block)

        part_speech = part_speech

        tag = Tag.objects.create(name=tag_name)
        tag.color = Tag.get_random_color()

        return Chain.objects.create(ru_block=ru_word_block, en_block=en_word_block, de_block=de_word_block,
                                    part_speech=part_speech, tag=tag)
