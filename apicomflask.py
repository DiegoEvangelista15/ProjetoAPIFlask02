from estrutura_bancodedados import Autor, Postagem, app, db
from flask import Flask, jsonify, request, make_response
import json
import jwt  
from datetime import datetime, timedelta
from functools import wraps

# Nossa 1 API -  Usar Flask ou Django

# app = Flask(__name__) # utilizar a outra

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verificar se um token foi enviado
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem': 'Token não foi incluído!'}, 401)
        # Se temos um token, validar acesso consultando o BD
        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'])
            autor = Autor.query.filter_by(
                id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'mensagem': 'Token é inválido'}, 401)
        return f(autor, *args, **kwargs)
    return decorated
                
        
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login Invalido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatorio"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login Invalido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatorio"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow() +  timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Login Invalido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatorio"'})

    
        


postagens = [
    {
        'titulo': 'Minha historia 01',
        'Autor': 'Diego Evangelista'
    },
    {
        'titulo': 'Space X e Tesla',
        'Autor': 'Elon Musk'
    },
    {
        'titulo': 'Lancamento do ano',
        'Autor': 'Jeff Bezos'
    },
]

# Rota padrao - GET - http://localhost:5000/postagens/1

@app.route('/postagens', methods=['GET'])
def obter_postagens():
    return jsonify(postagens)

@app.route('/postagens/<int:indice>', methods=['GET'])
def obter_postagens_por_id(indice):
    return jsonify(postagens[indice], 200)

# Criar uma nova postagens = POST - http://localhost:5000/postagens
@app.route('/postagens', methods=['POST'])
def nova_postagem():
    data = request.get_json()
    postagens.append(data)
    
    return jsonify(postagens, 200)

# Alterar uma postagem existente - PUT

@app.route('/postagens/<int:indice>', methods=['PUT'])
def alterar_postagem(indice):
    postagem_alterada = request.get_json()
    postagens[indice].update(postagem_alterada)
    
    return jsonify(postagens[indice], 200)

# Deletando uma postagem - DELETE

@app.route('/postagens/<int:indice>', methods=['DELETE'])
def deletar_postagem(indice):
    try:
        if postagens[indice] is not None:
            del postagens[indice]
            return jsonify(f'Excluido com sucessoa a postagem {postagens[indice]}',200)           
    except:
        return jsonify('Nao foi possivel excluir', 500)
    
#adicionando o DB
    
@app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_de_autores.append(autor_atual)
        
    return jsonify({'Autores': lista_de_autores})
        
    
@app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatorio
def obter_autores_porid(autor,id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f'Autor nao encontrado!!!')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email
    
    return jsonify({'Autor': autor_atual})
        
@app.route('/autores', methods=['POST'])
@token_obrigatorio
def novo_autor(autor):
    novo_autor = request.get_json()
    autor = Autor(nome=novo_autor['nome'],
                  senha=novo_autor['senha'],
                  email=novo_autor['email'])
    
    db.session.add(autor)
    db.session.commit()
     
    return jsonify({'mensagem': 'Usuario criado com sucesso'}, 200)
    
@app.route('/autores/<int:id_autor>', methods=['PUT'])
@token_obrigatorio
def alterar_autor(autor, id_autor):
    usuario_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem': 'Este Usuario nao foi encontrado!!!'})
    try: 
        if usuario_alterar['nome']:
            autor.nome = usuario_alterar['nome']
    except:
        pass
    try:
        if usuario_alterar['senha']:
            autor.senha = usuario_alterar['senha']
    except:
        pass
    try:
        if usuario_alterar['email']:
            autor.email = usuario_alterar['email']
    except:
        pass
    
    db.session.commit()
    return jsonify({'Mensagem': 'Usuario alterado com sucesso'}, 200)
        
        
@app.route('/autores/<int:id_autor>', methods=['DELETE'])
@token_obrigatorio
def excluir_autor(autor, id_autor):
    postagem_a_excluir = Autor.query.filter_by(id_autor=id_autor).first()
    if not postagem_a_excluir:
        return jsonify ({'mensagem': "Nenhuma postagem encotrada com esse ID"})
    db.session.delete(postagem_a_excluir)
    db.session.commit()
    
    return jsonify({'Mensagem': " Postagem excluida com sucesso!!!!"})    
    
 
app.run(host='localhost', debug=True)