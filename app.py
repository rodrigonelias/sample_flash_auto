from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = "testetesteteste123" #secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # URI - Caminho onde o banco será conectado


login_manager = LoginManager()
db.init_app(app) # iniciando o banco de dados no apicativo
login_manager.init_app(app)

#view login

login_manager.login_view = 'login' # vai pegar a rota de login 

#  Session <- conexão ativa

# usuario para ser armazenado em banco de dados
@login_manager.user_loader
def load_user(user_id): # recuperar o nosso objeto cadastrado no banco de dados
   return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password: 
        #login
        user = User.query.filter_by(username=username).first() # buscando no banco o primeiro registro referente ao usuário listado

        if user and user.password == password:
         login_user(user)
         
         return jsonify({"message": "Autenticação realizada com sucesso"})
    
    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)

