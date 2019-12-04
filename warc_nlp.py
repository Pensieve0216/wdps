# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# from nltk.stem import WordNetLemmatizer

# class nlp_warc():
#     def __init__(self,mylist):
#        # print("inside class")
#         self.mylist = mylist

#     def nlp(self):
#         clean_list = self.mylist[:]
#         stop = stopwords.words('english')
#         #print(clean_list)
#         for x in self.mylist:
#             if x in stop:
#                 clean_list.remove(x)
#         stem_initialize = PorterStemmer()
#         stem_output = [stem_initialize.stem(word) for word in clean_list]
#         return stem_output


import gzip
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import RegexpTokenizer

from nltk.tag import StanfordNERTagger
jar = './lib/stanford-ner-2018-10-16/stanford-ner.jar'
model = './lib/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz'



def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element,Comment):
        return False
    return True

def nlp_process(data):
        token = word_tokenize(data)
        stop = set(stopwords.words('english'))
        filter_sent = [w for w in token if not w in stop ]
        filter_sent = []
        
        for w in token:
            if w not in stop:
                filter_sent.append(w)
        #print(token)
        #print(filter_sent)
        
        #NER part below --- could be separated into diff function maybe ----
        st = StanfordNERTagger(model_filename = model, path_to_jar = jar)
        entities = st.tag(filter_sent)
        print(entities)

if __name__ == "__main__":
    with gzip.open('./data/sample.warc.gz','rb') as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                if record.http_headers != None:
                    record_id = record.rec_headers.get_header('WARC-TREC-ID')
                    #print(record_id)
                    html = record.content_stream().read()
                    soup = BeautifulSoup(html,"lxml")
                    body = soup.findAll(text=True)
                    result = filter(visible,body)
                    tt =[str(t) for t in result]
                    string = "".join(tt)
                    token_finals = string.split()
                    nlp_process(string)
