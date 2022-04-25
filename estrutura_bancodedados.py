
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# criar um API flask
app = Flask(__name__)
# criar uma instancia de SQLAlchemy
app.config['SECRET_KEY'] = 'ABCD1234'
# referencis as do db ou se for localmente colocar o /// connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
db: SQLAlchemy  # Definindo a variavel em sqlalchemy

# definir uma estrutura da tabela Postagem
# deve possuir uma id, titulo, autor


class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey(
        'autor.id_autor'))  # referenciando outra tabela
# definir uma estrutura da tabela Autor
# deve ter autor, nome, email, senha, admin, postagens


class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')  # nome da classe aqui


# Executar o banco de dados
# db.drop_all()
# db.create_all()

# # criar admins
# autor = Autor(nome='diego', email='diego@email.com',
#               senha='123456', admin=True)
# db.session.add(autor)
# db.session.commit()
