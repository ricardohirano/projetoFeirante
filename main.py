from flask import Flask, url_for, render_template
from routes.home import home_route
#Inicilaização
app =  Flask(__name__)

#Rotas
app.register_blueprint(home_route)


#Execução

app.run(debug=True)