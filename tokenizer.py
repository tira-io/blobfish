import tokenize
import token
import nltk
import re
from training_data import create_dataset
from nltk import trigrams
import numpy as np
from collections import Counter

#data = getData(modified=True)


def tokenizer(data, unlab=False):
    """ Tokenize data 
    
    Parameters
    ----------
    data : list
        list of dictionay elements to be tokenized
    unlab : bool, default False
        is setted if data is labeled
    
    Returns
    ----------
    tokens: list
        list where every element is a list of strings
    post_pos: list
        list where every element is a list of tuples (str, strPOS)
    sent_only_pos: list
        list where every element is a list of POS
    ids: list
        list where every element is id

    """
    print("+++++++++++++++++++TOKENIZER+++++++++++++++++++")

    sent_only_pos = []
    post_pos = []
    tokens = []

    ids = []
    i = 0

    if unlab:
        for post in data:
            ids.append(post['id'])
            feature = post['postText'][0]
            if len(post['targetTitle']) != 0:
                feature = feature + post['targetTitle']
            if len(post['targetParagraphs']) != 0:
                for phrasePar in range(len(post['targetParagraphs'])):
                    feature = feature + post['targetParagraphs'][phrasePar]
            tokenizer = nltk.word_tokenize(feature)
            tokens.append(tokenizer)
            pos_tags = nltk.pos_tag(tokenizer)
            post_pos.append(pos_tags)
            print(i, "  -  ", feature)
            i = i + 1
    else:
        for post in data:
            ids.append(post['id'])
            feature = post['postText'][0]
            tokenizer = nltk.word_tokenize(feature)
            tokens.append(tokenizer)
            pos_tags = nltk.pos_tag(tokenizer)
            post_pos.append(pos_tags)
            '''
            Replace special chars POS with dedicated tags
            '''
            if 'usertag' in tokenizer:
                ut = np.where(np.isin(tokenizer, 'usertag'))[0]
                for ind in ut:
                    mod = list(post_pos[i][ind])
                    mod[1] = "UT"
                    post_pos[i][ind] = mod
            if 'linkurl' in tokenizer:
                lu = np.where(np.isin(tokenizer, 'linkurl'))[0]
                for ind in lu:
                    mod = list(post_pos[i][ind])
                    mod[1] = "LU"
                    post_pos[i][ind] = mod
            if 'hashtagtag' in tokenizer:
                ht = np.where(np.isin(tokenizer, 'hashtagtag'))[0]
                for ind in ht:
                    mod = list(post_pos[i][ind])
                    mod[1] = "HT"
                    post_pos[i][ind] = mod
            i = i + 1

    pos = []
    k = 0
    for pst in post_pos:
        for tkn in pst:
            pos.append(tkn[1])
        sent_only_pos.insert(k, pos)
        k = k + 1
        pos = []

    return tokens, post_pos, sent_only_pos, ids


def special_char(data, name, unlab=False, test=False):
    """ Locate people tags, links and hashtags and save a modified datasets with words replaced by these keywords

    Parameters
    ----------
    data : list
        list of dictionay elements
    name: string
        name of file
    unlab : bool, default False
        is setted if data is labeled
    test : bool, default False
        is setted if data is test dataset
    
    Returns
    ----------
    data: list
        list of dictionay elements

    """
    if unlab:
        i = 0
        for el in data:
            post = el['postText'][0]
            post = re.sub(r".@\w+", " usertag", post)
            post = re.sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", " linkurl",
                          post)
            post = re.sub(r"https?:?\/\S+\b|www\.(\w+\.)+\S*", " linkurl",
                          post)
            post = re.sub(r"https?:?", " linkurl", post)
            post = re.sub(r"#\S+", " hashtagtag", post)
            post = re.sub(r"\\n|\/n", "", post)
            el['postText'][0] = post

            if len(el['targetParagraphs']) != 0:
                for phrasePar in range(len(el['targetParagraphs'])):
                    post = el['targetParagraphs'][phrasePar]
                    post = re.sub(r".@\w+", " usertag", post)
                    post = re.sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*",
                                  " linkurl", post)
                    post = re.sub(r"https?:?\/\S+\b|www\.(\w+\.)+\S*",
                                  " linkurl", post)
                    post = re.sub(r"https?:?", " linkurl", post)
                    post = re.sub(r"#\S+", " hashtagtag", post)
                    post = re.sub(r"\\n|\/n", "", post)
                    el['targetParagraphs'][phrasePar] = post

            if len(el['targetTitle']) != 0:
                if type(el['targetTitle']) == 'str':
                    post = el['targetTitle']
                    post = re.sub(r".@\w+", " usertag", post)
                    post = re.sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*",
                                  " linkurl", post)
                    post = re.sub(r"https?:?\/\S+\b|www\.(\w+\.)+\S*",
                                  " linkurl", post)
                    post = re.sub(r"https?:?", " linkurl", post)
                    post = re.sub(r"#\S+", " hashtagtag", post)
                    post = re.sub(r"\\n|\/n", "", post)
                    el['targetTitle'] = post
                elif type(el['targetTitle']) == 'list':
                    for phraseTitle in range(len(el['targetTitle'])):
                        post = el['targetTitle'][phraseTitle]
                        post = re.sub(r".@\w+", " usertag", post)
                        post = re.sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*",
                                      " linkurl", post)
                        post = re.sub(r"https?:?\/\S+\b|www\.(\w+\.)+\S*",
                                      " linkurl", post)
                        post = re.sub(r"https?:?", " linkurl", post)
                        post = re.sub(r"#\S+", " hashtagtag", post)
                        post = re.sub(r"\\n|\/n", "", post)
                        el['targetTitle'][phraseTitle] = post
            i = i + 1
    else:
        for el in data:
            post = el['postText'][0]
            post = re.sub(r".@\w+", " usertag", post)
            post = re.sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", " linkurl",
                          post)
            post = re.sub(r"https?:?\/\S+\b|www\.(\w+\.)+\S*", " linkurl",
                          post)
            post = re.sub(r"https?:?", " linkurl", post)
            post = re.sub(r"#\S+", " hashtagtag", post)
            post = re.sub(r"\\n|\/n", "", post)
            el['postText'][0] = post

    if test:
        return data
    else:
        create_dataset(data, name)
        return data
