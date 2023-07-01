from bz2 import BZ2File
from wiktionary_de_parser import Parser

bzfile_path = 'C:/Users/Fabia/Documents/Coding/Brain Stuff/brainwords2/Data/words/dewiktionary-latest-pages-articles-multistream.xml.bz2'
bz_file = BZ2File(bzfile_path)

for record in Parser(bz_file):
    if 'lang_code' not in record or record['lang_code'] != 'de':
      print(record)