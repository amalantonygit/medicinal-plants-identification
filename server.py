from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
import tempfile
import predict
import sqlite3

app = Flask(__name__)
app.logger.setLevel('INFO')
class Image(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image',
                            type=FileStorage,
                            location='files',
                            required=True,
                            help='provide an image file')
        parser.add_argument('api-key',
                            required=True,
                            help='API authetication key')
        args = parser.parse_args()
        input_file = args['image']
        auth_key="WIskvwZRzpfd2CG9"
        if args['api-key']==auth_key:
            ofile, ofname = tempfile.mkstemp()
            input_file.save(ofname)
            result_class,confidence = predict.predict_class(ofname)
            print(result_class, confidence)
            if confidence>0.8:
                conn = sqlite3.connect('database/plant_database.db')
                c = conn.cursor()
                parameters=(str(result_class),)
                c.execute("SELECT common_name,scientific_name,\
                          family,description FROM plants WHERE id=? LIMIT 1",parameters)
                rows=c.fetchall()
                if(len(rows)>0):
                    output = {'class': int(result_class),
                          'confidence':float(confidence*100),
                          'common_name':rows[0][0],
                           'scientific_name':rows[0][1],
                           'family':rows[0][2],
                           'description':rows[0][3]
                           }
                    return {'results':[output]}
                else:
                    return {'message':"No results found."}
            else:
                    return {'message':"No results found."}
        else:
            return {'message':"API key authentication failed."}

class Keyword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword',
                            required=True,
                            help='provide a search term')
        parser.add_argument('api-key',
                            required=True,
                            help='API authetication key')
        args = parser.parse_args()
        search_term = args['keyword']
        search_term=" ".join(search_term.split())
        search_terms=search_term.split(" ")
        valid_search=False
        for value in search_terms:
            if len(value)>=3:
                valid_search=True;
                break
            else:
                continue
        search_terms=[x for x in search_terms if len(x)>=3]
        auth_key="WIskvwZRzpfd2CG9"
        if args['api-key']==auth_key:
            if valid_search:
                conn = sqlite3.connect('database/plant_database.db')
                c = conn.cursor()
                parameters=[]
                where_clauses=[]
                for word in search_terms:
                    parameters.append("%"+word+"%")
                    where_clauses.append(" keyword LIKE ?")
                parameters=tuple(parameters)
                query_string="SELECT DISTINCT plants_index.id,plants.common_name,\
                                    plants.scientific_name,plants.family,plants.description \
                                        FROM plants_index INNER JOIN plants ON plants.id=plants_index.id WHERE"
                query_string+=(" OR".join(where_clauses))
                c.execute(query_string, parameters)
                rows = c.fetchall()
                if len(rows)>0:
                    output=[]
                    print(rows)
                    for row in rows:
                        print("INFO "+str(len(row)))
                        output+=[{'class': row[0],
                                  'common_name':row[1],
                                   'scientific_name':row[2],
                                   'family':row[3],
                                   'description':row[4]
                                   }]
                    return {'results':output}
                else:
                    return {'message':"No results found."}
            else:
                return {'message':"No results found. Use valid keywords with at least 3 characters in your search."}
        else:
            return {'message':"API key authentication failed."}

api = Api(app)
api.add_resource(Image, '/api/image')
api.add_resource(Keyword, '/api/keyword')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)