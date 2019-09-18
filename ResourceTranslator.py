from bs4 import BeautifulSoup
import os
import json
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

CREDENTIAL_FILE = 'project-service-account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_FILE

from google.cloud import translate_v3beta1 as translate

client = translate.TranslationServiceClient()

project_id = json.load(open(CREDENTIAL_FILE))['project_id']
location = 'global'

parent = client.location_path(project_id, location)


def get_all_langs():
    lang = []
    response = client.get_supported_languages(parent=parent, display_language_code='en')
    for language in response.languages:
        lang.append((language.language_code, language.display_name))

    return lang


def is_directory(path):
    return os.path.exists(path) and not os.path.isfile(path)

class ResourceTranslator:
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.bs = BeautifulSoup(file)

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def translate(self, langs, replace=False):
        for lang in langs:
            dir = 'values-%s' % lang
            if os.path.exists(dir):
                if os.path.isfile(dir):
                    os.mkdir(dir)
            else:
                os.mkdir(dir)
            out_file = dir + '/' + 'strings.xml'

            out = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'

            already_translated = set()
            if (os.path.exists(out_file)):
                file = open(out_file, 'r')
                bs = BeautifulSoup(file)
                for text in bs.find_all('string'):
                    if text.string is None or text.attrs['name'] is None:
                        continue

                    already_translated.add(text.attrs['name'])
                    out += '    <string name="%s">%s</string>\n' % (text.attrs['name'], text.string)

            names = []
            texts = []
            for text in self.bs.find_all('string', attrs={'translatable': None}):
                if text.string is None or text.attrs['name'] is None or text.attrs['name'] in already_translated:
                    continue

                names.append(text.attrs['name'])
                texts.append(text.string)

            texts_list = self.chunks(texts, 128)
            translations_list = []

            for texts in texts_list:
                translations = client.translate_text(
                    parent=parent,
                    contents=texts,
                    mime_type='text/plain',  # mime types: text/plain, text/html
                    source_language_code='en-US',
                    target_language_code=lang)

                for translation in translations.translations:
                    translations_list.append(translation.translated_text)

            print("Translated %d in %s"%(len(translations_list), lang))

            for i in range(len(names)):
                out += '    <string name="%s">%s</string>\n' % (names[i], translations_list[i])

            out += '</resources>'
            f = open(out_file, "w")
            f.write(out)
            f.close()
