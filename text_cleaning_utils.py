from __future__ import absolute_import

import re
import logging
import itertools
import unicodedata
import contractions

from bs4 import BeautifulSoup

class TextCleaningUtils:
    '''
        This class contains implementations of various text cleaning operations (Static Methods)
    '''


    cleaning_regex_map = {
        'web_links': r'(?i)(?:(?:http(?:s)?:)|(?:www\.))\S+',
        'special_chars': r'[^a-zA-Z0-9\s\.,!?;:]+',
        'redundant_spaces': r'\s\s+',
        'redundant_newlines': r'[\r|\n|\r\n]+',
        'twitter_handles': r'[#@]\S+',
        'punctuations': r'[\.,!?;:]+'
    }

    @staticmethod
    def clean_text_from_regex(text, text_clean_regex):
        '''
            Follow a particular cleaning expression, provided
            as an input by an user to clean the text.
        '''

        text = text_clean_regex.sub(' ', text).strip()
        return text

    @staticmethod
    def replace_contractions(text):
        '''
            Replace contractions in string of text
        '''

        return contractions.fix(text)

    @staticmethod
    def strip_html(text):
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    @staticmethod
    def remove_special_chars(text):
        '''
            Replace any special character provided as default,
            which is present in the text with space
        '''

        special_chars_regex = re.compile(TextCleaningUtils.cleaning_regex_map['special_chars'])
        text = TextCleaningUtils.clean_text_from_regex(text, special_chars_regex)
        return text

    @staticmethod
    def remove_redundant_spaces(text):
        '''
            Remove any redundant space provided as default,
            that is present in the text.
        '''

        redundant_spaces_regex = re.compile(
            TextCleaningUtils.cleaning_regex_map['redundant_spaces'])
        text = TextCleaningUtils.clean_text_from_regex(text, redundant_spaces_regex)
        return text

    @staticmethod
    def remove_web_links(text):
        '''
            Removes any web link that follows a particular default expression,
            present in the text.
        '''

        web_links_regex = re.compile(TextCleaningUtils.cleaning_regex_map['web_links'])
        text = TextCleaningUtils.clean_text_from_regex(text, web_links_regex)
        return text

    @staticmethod
    def remove_twitter_handles(text):
        '''
            Removes any twitter handle present in the text.
        '''

        twitter_handles_regex = re.compile(TextCleaningUtils.cleaning_regex_map['twitter_handles'])
        text = TextCleaningUtils.clean_text_from_regex(text, twitter_handles_regex)
        return text

    @staticmethod
    def remove_redundant_newlines(text):
        '''
            Removes any redundant new line present in the text.
        '''

        redundant_newlines_regex = re.compile(
            TextCleaningUtils.cleaning_regex_map['redundant_newlines'])
        text = TextCleaningUtils.clean_text_from_regex(text, redundant_newlines_regex)
        return text

    @staticmethod
    def remove_punctuations(text):
        '''
            Removes any punctuation that follows the default expression, in the text.
        '''

        remove_punctuations_regex = re.compile(TextCleaningUtils.cleaning_regex_map['punctuations'])
        text = TextCleaningUtils.clean_text_from_regex(text, remove_punctuations_regex)
        return text

    @staticmethod
    def remove_exaggerated_words(text):
        '''
            Removes any exaggerated word present in the text.
        '''

        return ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))

    @staticmethod
    def replace_multiple_chars(text):
        '''
            Replaces multiple characters present in the text.
        '''

        char_list = ['.', '?', '!', '#', '$', '/', '@', '*', '(', ')', '+']
        final_text = ''
        for i in char_list:
            if i in text:
                pattern = "\\" + i + '{2,}'
                repl_str = i.replace("\\", "")
                text = re.sub(pattern, repl_str, text)
                final_text = ' '.join(text.split())
        return final_text

    @staticmethod
    def replace_sign(text):
        '''
            Replaces any sign with words like & with 'and', in the text.
        '''
        sign_list = {'&': ' and ', '/': ' or ', '\xa0': ' '}
        final_text = ''
        for i in sign_list:
            if i in text:
                text = re.sub(i, sign_list[i], text)
                final_text = ' '.join(text.split())
        return final_text

    @staticmethod
    def remove_accented_char(text):
        text = unicodedata.normalize('NFD', text) \
            .encode('ascii', 'ignore') \
            .decode("utf-8")
        return str(text)

    @staticmethod
    def replace_characters(text, replace_map):
        '''
            Replaces any character custom provided by an user.
        '''

        for char, replace_val in replace_map.items():
            text = text.replace(char, replace_val)
        return text


class TextCleaningRecipes:
    """
        This class contains the recipes for a set of standard text cleaning operations

    """

    DEFAULT_OPERATIONS = ['replace_contractions', 'remove_web_links', 'remove_special_chars',
                          'remove_redundant_newlines', 'remove_redundant_spaces']

    OPERATIONS_MAP = {
        'replace_contractions': TextCleaningUtils.replace_contractions,
        'remove_web_links': TextCleaningUtils.remove_web_links,
        'remove_twitter_handles': TextCleaningUtils.remove_twitter_handles,
        'replace_characters': TextCleaningUtils.replace_characters,
        'remove_special_chars': TextCleaningUtils.remove_special_chars,
        'remove_punctuations': TextCleaningUtils.remove_punctuations,
        'remove_redundant_newlines': TextCleaningUtils.remove_redundant_newlines,
        'remove_redundant_spaces': TextCleaningUtils.remove_redundant_spaces
    }

    OPERATIONS_ORDER = ['replace_contractions', 'remove_web_links', 'remove_twitter_handles',
                        'replace_characters',
                        'remove_special_chars', 'remove_punctuations',
                        'remove_redundant_newlines', 'remove_redundant_spaces']

    @staticmethod
    def exec_cleaning(text_values, config):
        '''
            This method executes various cleaning techniques together
        '''

        operations = TextCleaningRecipes.get_operations(config)
        logging.info("Executing %s Operations", ', '.join(operations))

        cleaning_ops = []
        for _op in operations:
            op_func = TextCleaningRecipes.OPERATIONS_MAP[_op]
            cleaning_ops.append(op_func)

        c_text_values = []
        for text in text_values:

            if text is None:
                c_text = ''
            else:
                c_text = str(text)

            c_text = c_text.replace(')', ') ')

            for _op in cleaning_ops:
                if 'replace_characters' in _op.__name__:

                    c_text = _op(c_text, config['replace_characters'])
                else:
                    c_text = _op(c_text)

            c_text_values.append(c_text)

        return c_text_values

    @staticmethod
    def get_operations(config):

        operations = []
        if len(config) == 0:
            operations = TextCleaningRecipes.DEFAULT_OPERATIONS
            return operations

        for _op in TextCleaningRecipes.OPERATIONS_ORDER:
            if _op in config and config[_op]:
                operations.append(_op)

        if not operations:
            operations = TextCleaningRecipes.DEFAULT_OPERATIONS

        logging.info("Operations: %s", operations)
        return operations