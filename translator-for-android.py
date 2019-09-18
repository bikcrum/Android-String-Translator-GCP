from ResourceTranslator import ResourceTranslator, get_all_langs
import sys

DEBUG = False

avail_langs =  get_all_langs()
avail_lang_codes = [code[0] for code in avail_langs]

if 'en' in avail_lang_codes:
    avail_lang_codes.remove('en')

if not DEBUG:
    input_file = sys.argv[1]
    if len(sys.argv) == 3:
        langs = sys.argv[2]
        langs = list(set(langs.split(',')) & set(avail_lang_codes))
    else:
        langs = avail_lang_codes
else:
    input_file = 'strings.xml'
    langs = avail_lang_codes

rt = ResourceTranslator(input_file)
rt.translate(langs,replace=False)
