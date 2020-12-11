from django.test import TestCase
from django.urls import reverse

from test.test_forms import FormsTests


class ViewsTests(TestCase):
    def test_list_view(self):
        expected = self.create_chain()
        url = reverse('home')

        resp = self.client.get(url)
        actual = resp.context_data['chain_list'].first()  # object_list

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expected, actual)

    @staticmethod
    def create_chain(value='value for test', order=1, part_speech='сущ', tag_name='tag'):
        return FormsTests.create_chain(value, order, part_speech, tag_name)

    def test_detail_view(self):
        expected = self.create_chain()
        url = reverse('edit', args=[expected.id])

        resp = self.client.get(url)
        actual = resp.context_data['chain']  # object

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expected, actual)
