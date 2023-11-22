from flask import Flask, request, jsonify
from flask_cors import CORS
from Generativos import Generativo
from SentenceBert import SimilitudSemantica


app = Flask(__name__)
CORS(app)

# solo cargan los modelos una vez
g_model = Generativo(model="santyzenith/train_causal",
                     tokenizer="santyzenith/train_causal")

# model = "santyzenith/prueba"
# tokenizer = "santyzenith/prueba"

sem_model = SimilitudSemantica(model="hiiamsid/sentence_similarity_spanish_es",
                               corpus_df="frases_no_deacc_spell.csv")

# Para el modelo de similitud semántica, se codifica el corpus una sola vez
sem_model.encode_corpus()


# TERMINAL :waitress-serve --listen=127.0.0.1:2020 w_app_pictos:app

def clean_sentences(lista_oraciones):
    new_list = []
    for oracion in lista_oraciones:
        oracion = str(oracion).replace('<SF>', '')
        oracion = str(oracion).replace('<EF>', '')
        oracion = str(oracion).replace('>', '')
        oracion = str(oracion).replace('[CLS]', '')
        oracion = str(oracion).replace('[SEP]', '')
        new_list.append(oracion)

    return new_list


"""
@app.route('/sumar', methods=['GET'])
def sumar():
    numero1 = int(request.args.get('numero1'))
    numero2 = int(request.args.get('numero2'))
    resultado = numero1 + numero2
    return jsonify({'resultado': resultado})
    #http://127.0.0.1:2020/sumar?numero1=12&numero2=343
"""


@app.route('/generar', methods=['POST'])
def get_words_list():
    w_list = request.get_json('lista')
    # frase = str(w_list['lista']).replace('/', ' ').strip() # cuando se recibe una secuencia separada por /
    frase = ' '.join(w_list['lista'])
    frases = g_model.gen_frase(frase)  # Utilizando la nueva clase creada
    # frases = gen_frase(frase)
    frases_clean = clean_sentences(frases)
    # frases_semantic = semantic_search(frase)
    frases_semantic = sem_model.semantic_search(frase)  # Utilizando la nueva clase
    frase_sem_clean = clean_sentences(frases_semantic)

    response = jsonify({'frases': frases_clean,
                        'frases_sem': frase_sem_clean})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True)
