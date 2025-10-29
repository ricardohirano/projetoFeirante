from flask import Flask, url_for, render_template
from routes.home import home_route
from routes.usuario import usuario_route
#Inicilaização
app =  Flask(__name__)

#Rotas
app.register_blueprint(home_route)
app.register_blueprint(usuario_route, url_prefix='/usuario')


#Execução

app.run(debug=True)