from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" #secret key
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
      user = User(username=username, password=password)
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

   if id_user == current_user.id:
      return jsonify({"message":"Deleção não permitida"}), 403
   
   if user:
      db.session.delete(user)
      db.session.commit()
      return jsonify({"message":f"Usuário {id_user} deletado com sucesso"})
   return jsonify({"message":"Usuário não encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)

