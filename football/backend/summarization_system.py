import collections
import numpy
import articles_processor as ap

'''
Summarization algorithm for multiple documents based on centroid
based summarization(CBS) algorithm
'''


class CBS:
    # def __init__(self):
    #     self.document_frequencies = {}
    #     self.terms = []
    #     self.average_term_frequencies = {}

    def get_selection(self, group_sentences, percentage):
        total_summary = []
        group = 0
        for i in range(len(group_sentences)):
            ap.average_term_frequencies.append({})

        sentence_scores = []
        for sentences in group_sentences:
            self.build_model(sentences, group)
            group = group + 1

        group = 0
        for sentences in group_sentences:
            centroid_values = self.make_centroid_values(sentences, len(sentences), group)
            centroid_document = self.make_centroid_document(centroid_values)
            document_centroid_values = self.make_document_centroids(sentences, centroid_values, centroid_document)
            max_centroid_value = max(document_centroid_values)
            positional_values = self.make_positional_values(len(sentences), max_centroid_value)
            sentence_vectors = self.make_sentence_vectors(sentences, ap.terms)
            overlaps = self.make_first_sentence_overlap(sentence_vectors)
            sentence_scores += self.make_sentence_scores(document_centroid_values, positional_values, overlaps, group)
            group = group+1

        summary_selection = self.make_summary_selection(sentence_scores, percentage)

        return sorted(summary_selection, reverse=True, key=lambda x: x[1])

    def build_model(self, sentences, group):
        '''
        Read sentences and extract df, unique terms and avg. tf
        :param sentences:
        :return:
        '''

        self.make_document_frequencies(sentences)
        self.make_terms()
        self.make_average_term_frequencies(sentences, group)

    @staticmethod
    def make_summary_selection(sentence_scores, percentage):

        summary_length = int(len(sentence_scores) * percentage / 100.0) # Number of sentences in summary

        if summary_length < 1:  # ensure that summary is of length 1
            summary_length = 1

        sentence_scores.sort(reverse=True, key=lambda x: x[1])
        #for i in range(len(sentence_scores)):
        #    print('Sentence scores: {0}'.format(sentence_scores[i]))

        indices = []
        for i in range(0, summary_length-1):
            indices.append(sentence_scores[i])

        return sorted(indices, reverse=True, key=lambda x: x[1])


    @staticmethod
    def make_sentence_scores(document_centroid_values, positional_values, overlaps, group):
        '''
        Calculates the score for each sentence in the collection
        :param document_centroid_values:
        :param positional_values:
        :param overlaps:
        :return:
        '''
        pairs = []

        for i in range(len(document_centroid_values)-1):
            pair = (i, document_centroid_values[i] + positional_values[i] + overlaps[i], group)
            pairs.append(pair)
        return pairs

    @staticmethod
    def make_sentence_vectors(sentences, sentence_terms):
        '''
        Sentence vectors of length N where N is the number of different words in document and value at the index
        is the number of times that word occurs in the sentence
        :param sentences:
        :param sentence_terms:
        :return:
        '''
        sentence_vectors = []

        for document in sentences:
            sentence_vector = []
            for term in sentence_terms:
                freq = 0
                for word in document:
                    if word == term:
                        freq = freq + 1
                sentence_vector.append(freq)

            sentence_vectors.append(sentence_vector)

        return sentence_vectors

    @staticmethod
    def make_first_sentence_overlap(sentence_vectors):
        '''
        Calculate dot product of all sentence vectors and the first sentence
        :param sentence_vectors:
        :return:
        '''
        overlaps = []
        first_sentence = sentence_vectors[0]

        for i in range(len(sentence_vectors)):
            overlap = 0
            vector = sentence_vectors[i]

            for j in range(len(vector)):
                overlap += vector[j] * first_sentence[j]

            overlaps.append(overlap)
        return overlaps

    @staticmethod
    def make_positional_values(size, max_centroid_value):
        '''
        Calculate positional values of sentences
        :param size:
        :param max_centroid_value:
        :return:
        '''
        positional_values = []

        for i in range(0, size-1):
            positional_value = ((size - i) / size) * max_centroid_value
            positional_values.append(positional_value)

        return positional_values

    @staticmethod
    def make_document_centroids(sentences, centroid_values, centroid_document):
        '''
        Calculate centroid values of sentences
        :param sentences:
        :param centroid_values:
        :param centroid_document:
        :return:
        '''
        document_centroid_values = []

        for document in sentences:
            total = 0.0
            for term in centroid_document:
                if term in document:
                    total += centroid_values[ap.terms.index(term)]
            document_centroid_values.append(total)
        return document_centroid_values

    @staticmethod
    def make_document_frequencies(sentences):
        '''
        Determines the frequency of each word in document
        :param sentences:
        :return:
        '''
        for i in range(len(sentences)):
            for word in sentences[i]:
                if word not in ap.document_frequencies:
                    documents_with_term = []
                    documents_with_term.append(i)
                    ap.document_frequencies[word] = documents_with_term
                else:
                    if i not in ap.document_frequencies[word]:
                        ap.document_frequencies[word].append(i)

    @staticmethod
    def make_terms():
        '''
        Creates alphabetized list of words in document
        :return:
        '''
        keys = list(ap.document_frequencies.keys())
        ap.terms = list(set(ap.terms + keys))
        ap.terms.sort()

    @staticmethod
    def make_average_term_frequencies(sentences, group):
        '''
        Compute average term frequency for each word in document
        :param sentences:
        :return:
        '''
        for document in sentences:
            for term in document:
                if term in ap.average_term_frequencies[group]:
                    ap.average_term_frequencies[group][term] = ap.average_term_frequencies[group][term] + 1.0
                else:
                    ap.average_term_frequencies[group][term] = 1.0
        documents_number = len(sentences)
        if documents_number != 0:
            for term in ap.average_term_frequencies[group].keys():
                ap.average_term_frequencies[group][term] = ap.average_term_frequencies[group][term] / documents_number

    @staticmethod
    def make_centroid_values(sentences, sentences_size, group):
        '''
        Calculate centroid value for each unique word
        :param sentences_size:
        :return:
        '''
        centroid_values = []

        for sentence in sentences:
            for word in sentence:
                tf = ap.average_term_frequencies[group].get(word)

                df = len(ap.document_frequencies[word])

                centroid_values.append(tf * numpy.log10(sentences_size / df))

        return centroid_values

    @staticmethod
    def make_centroid_document(centroid_values):
        '''
        Builds Centroid document by taking the words with a centroid value above certain threshold
        :param centroid_values:
        :return:
        '''
        pairs = []

        for i in range(len(centroid_values)):
            pair = (i, centroid_values[i])
            pairs.append(pair)

        pairs = sorted(pairs, reverse=True, key=lambda x: x[1])

        total_terms = len(pairs)
        top_terms = int(total_terms * 0.1)

        if top_terms < 1 and len(centroid_values) > 0:
            top_terms = 1

        centroid_document = []
        for i in range(0, top_terms-1):
            centroid_document.append(ap.terms[pairs[i][0]])
        return centroid_document
