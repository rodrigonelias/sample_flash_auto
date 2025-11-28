from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" #secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3307/flask-crud'#'sqlite:///database.db' # URI - Caminho onde o banco será conectado


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

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):#user.password == password:
         login_user(user)
         print(current_user.is_authenticated)
         return jsonify({"message": "Autenticação realizada com sucesso"})
    
    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realziado com sucesso!"})


@app.route('/user', methods=["POST"])
def create_user():
   data = request.json
   username = data.get("username")
   password = data.get("password")

   if username and password: 
      hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
      user = User(username=username, password=hashed_password, role='user')
      db.session.add(user)
      db.session.commit()
      return jsonify({"message":"Usuário cadastrado com sucesso"})
   return jsonify({"message":"Dados inválidos"}), 400

@app.route("/user/<int:id_user>", methods=["GET"]) # recuperando as informações de usuário cadastrados no banco
@login_required
def read_user(id_user):
   user = User.query.get(id_user)
   if user:
      return{"username": user.username}
   return jsonify({"message":"Usuário não encontrado"}), 404


@app.route("/user/<int:id_user>", methods=["PUT"]) # atualizando as informações de usuário cadastrados no banco
@login_required
def update_user(id_user):
   data = request.json # recupera os dados que o usuário enviou
   user = User.query.get(id_user)
   
   if id_user != current_user.id and current_user.role == "user":
      return jsonify({"message":"Operação não permitida"}),403
   if user and data.get("password"):
      user.password = data.get("password")
      db.session.commit()
      return jsonify({"message":f"Usuário {id_user} atualizado com sucesso"})
   return jsonify({"message":"Usuário não encontrado"}), 404
                                    

@app.route("/user/<int:id_user>", methods=["DELETE"]) # deletando as informações de usuário cadastrados no banco
@login_required
def delete_user(id_user):
   data = request.json # recupera os dados que o usuário enviou
   user = User.query.get(id_user)
   if current_user.role != 'admin':
      return jsonify({"message":"Operação não permitida"}), 403
   if id_user == current_user.id:
      return jsonify({"message":"Deleção não permitida"}), 403
   
   if user:
      db.session.delete(user)
      db.session.commit()
      return jsonify({"message":f"Usuário {id_user} deletado com sucesso"})
   return jsonify({"message":"Usuário não encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)

#bcrypt - criptografia de senhas
#pip install bcrypt=4.1.2

# no CMD
# import bcrypt
#coloque a senha em uma váriavel, ex. password = b"1234"
# utilize a função hashpw para criar o hash e a gensalt para criar uma sequencia de caracteres aleatória
# hashed = bcrypt.hashpw(password, bcrypt.gensalt()
# confere se a senha está correta pelo método checkpw. ex bcrypt.checkpw(b"1234", hashed)