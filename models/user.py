from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # id (int), username(text), password (text)
    id = db.Column(db.Integer, primary_key=True) # definindo a coluna da tabela
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


'''comandos sql alchemy
flask shell inicia uma instância do banco de dados
db.create_all() vai criar o banco
db.session verifica a sessão do banco
db.session.commit() aplica as criações ou modificações em banco de dados
exit() sai do flask shell
'''