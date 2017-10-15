document_frequencies = {}
terms = []
average_term_frequencies = []


def build_model(sentences):
    '''
    Read sentences and extract df, unique terms and avg. tf
    :param sentences:
    :return:
    '''
    make_document_frequencies(sentences)
    make_terms()
    make_average_term_frequencies(sentences)


def make_document_frequencies(sentences):
    '''
       Determines the frequency of each word in document
       :param sentences:
       :return:
    '''
    for i in range(len(sentences)):
        #print(sentences.size)
        for word in sentences[i]:
            if word not in document_frequencies:
                #print('asdasdasdasd')
                documents_with_term = []
                documents_with_term.append(i)
                document_frequencies[word] = documents_with_term
                #print(document_frequencies)
            else:
                if i not in document_frequencies[word]:
                    document_frequencies[word].append(i)


def make_terms():
    '''
    Creates alphabetized list of words in document
    :return:
    '''
    keys = set(document_frequencies.keys())
    for key in keys:
        terms.append(key)
    terms.sort()


def make_average_term_frequencies(sentences):
    '''
    Compute average term frequency for each word in document
    :param sentences:
    :return:
    '''
    for document in sentences:
        for term in document:
            if term in average_term_frequencies:
                average_term_frequencies[term] = average_term_frequencies[term] + 1.0
            else:
                average_term_frequencies[term] = 1.0
    documents_number = len(sentences)
    for term in average_term_frequencies.keys():
        average_term_frequencies[term] = average_term_frequencies[term] / documents_number
