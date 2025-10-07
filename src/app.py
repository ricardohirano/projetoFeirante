from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return {"message": "API Vitrine de Feiras - Backend Ativo"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
