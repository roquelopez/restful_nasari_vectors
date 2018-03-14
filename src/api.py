#-*- coding: UTF-8 -*-

from flask import Flask
from flask_restful import Resource, Api, reqparse
from sklearn.metrics.pairwise import cosine_similarity
from os.path import join, dirname

app = Flask(__name__)
api = Api(app)

vector_indexs = {}
wn31_bn35 = {}

def load_mappings(path_file):
    ''' Loading mapping between Wordnet 3.1 and Babelnet 3.5 '''
    with open(path_file) as fin:
        for line in fin:
            id_list = line.strip().split(' ')
            id_wordnet = id_list[2][1:]
            id_babelnet = 'bn:' + id_list[0][1:]
            wn31_bn35[id_wordnet] = id_babelnet

def load_nasari_file(path_file):
    '''Loading Nasari vectors into a dictionary '''
    with open(path_file) as fin:
        for line in fin:
            line_tokens = line.strip().split(' ')
            vector = [float(i) for i in line_tokens[2:]]
            id_babelnet = line_tokens[0]
            vector_indexs[id_babelnet] = vector

class NasariVector(Resource):

    def get(self):
        ''' Get the Nasari vector of a given Wordnet or Babelnet ID '''
        parser = reqparse.RequestParser()
        parser.add_argument('key')
        args = parser.parse_args()
        vector_id = str(args['key'])

        if vector_id in wn31_bn35: vector_id = wn31_bn35[vector_id]

        if vector_id in vector_indexs:
            return {'vector': vector_indexs[vector_id]}
        else:
            return {'error': "KeyError: '%s' not found" % vector_id}

class NasariCosine(Resource):

    def get(self):
        ''' Calculate cosine similarity between two Nasari vectors given their Wordnet or Babelnet IDs '''
        parser = reqparse.RequestParser()
        parser.add_argument('key1')
        parser.add_argument('key2')
        args = parser.parse_args()
        vector1_id = str(args['key1'])
        vector2_id = str(args['key2'])
        if vector1_id in wn31_bn35: vector1_id = wn31_bn35[vector1_id]
        if vector2_id in wn31_bn35: vector2_id = wn31_bn35[vector2_id]

        if vector1_id not in vector_indexs:
            return {'error': "KeyError: '%s' not found" % vector1_id}
        elif vector2_id not in vector_indexs:
            return {'error': "KeyError: '%s' not found" % vector2_id}
        elif vector1_id == vector2_id:
            return {'similarity': 1.0}
        else:
            similarity = cosine_similarity(vector_indexs[vector1_id], vector_indexs[vector2_id])
            return {'similarity': round(similarity[0][0], 4)}


api.add_resource(NasariVector, '/nasari/vector')
api.add_resource(NasariCosine, '/nasari/cosine')


if __name__ == '__main__':
    mapping_bn2wn_path = join(dirname(__file__), '../resource/bn35-wn31.map')
    nasari_vectors_path = join(dirname(__file__), '../resource/NASARI_embed_english_sample.txt')

    load_mappings(mapping_bn2wn_path)
    load_nasari_file(nasari_vectors_path)
    app.run(debug=False)