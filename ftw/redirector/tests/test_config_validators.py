from ftw.redirector.config import RulesValidator
from ftw.redirector.tests.helpers import make_rules
from unittest2 import TestCase
from zope.i18n import translate
from zope.interface import Invalid


def invalid_message(exc):
    return translate(exc.args[0], target_language='en')


class TestRulesValidator(TestCase):

    def test_source_path_required(self):
        self.assert_invalid(
            u'Row 1: source path required.',
            [('', '/bar')])

    def test_source_path_root_not_allowed(self):
        self.assert_invalid(
            u'Row 2: invalid source path: cannot redirect from root.',
            [('/foo', '/bar'),
             ('/', '/bar')])

    def test_source_path_starting_slash_required(self):
        self.assert_invalid(
            u'Row 3: the source path "invalid" must start with a slash.',
            [('/valid1', '/bar'),
             ('/valid2', '/bar'),
             ('invalid', '/bar')])

    def test_source_path_url_not_allowed(self):
        self.assert_invalid(
            u'Row 4: the source path "http://google.ch/" must start with a slash.',
            [('/valid1', '/bar'),
             ('/valid2', '/bar'),
             ('/valid3', '/bar'),
             ('http://google.ch/', '/bar')])

    def test_destionation_required(self):
        self.assert_invalid(
            u'Row 1: destination required.',
            [('/valid1', '')])

    def test_destionation_must_be_path_or_url(self):
        self.assert_invalid(
            u'Row 2: the destination "invalid" must be a path'
            u' (start with slash) or a full qualified URL.',

            [('/valid1', '/valid2'),
             ('/valid3', 'invalid')])

    def test_paths_are_valid(self):
        self.assert_valid(
            [('/valid/source', '/valid/target'),
             ('/valid/source/slash/', '/valid/target/slash/')])

    def test_destination_url_is_allowed(self):
        self.assert_valid([('/google', 'http://www.google.com/')])

    def assert_invalid(self, expected_validation_error, redirects):
        with self.assertRaises(Invalid) as cm:
            self.validate(make_rules(*redirects))

        self.assertEquals(expected_validation_error,
                          invalid_message(cm.exception))

    def assert_valid(self, redirects):
        try:
            self.validate(make_rules(*redirects))
        except Invalid, exc:
            raise AssertionError('Unexpected validation error: {}'.format(
                invalid_message(exc)))

    def validate(self, rules):
        RulesValidator(None, None, None, None, None).validate(rules)
