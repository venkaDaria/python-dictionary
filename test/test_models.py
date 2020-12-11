from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from main.models import Word, WordBlock


class ModelsTests(TestCase):
    def test_example(self):
        self.assertEqual(True, True)

    def test_word_block_create(self):
        time = timezone.now()
        word_block = WordBlock.objects.create()

        expected = time.replace(microsecond=0)
        actual = word_block.created_at.replace(microsecond=0)

        self.assertTrue(isinstance(word_block, WordBlock))
        self.assertEqual(expected, actual)

    def test_exception_example(self):
        self.assertRaises(IntegrityError, self.create_word)

    @staticmethod
    def create_word(value='value for test'):
        Word.objects.create(value=value)
