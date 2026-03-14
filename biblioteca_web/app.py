"""
Punto de arranque de la aplicación web Biblioteca Digital.
Despliega la estructura MVC: modelos, vistas (plantillas) y controladores.
"""
import os
from flask import Flask, render_template
from config import CLAVE_SECRETA
from database import preparar_almacenamiento

from controllers.autor_controller import blueprint_escritores
from controllers.libro_controller import blueprint_catalogo
from controllers.usuario_controller import blueprint_socios
from controllers.prestamo_controller import blueprint_movimientos


def inicializar_aplicacion():
    """Crea la instancia de Flask, registra blueprints y configura la BD."""
    aplicacion = Flask(__name__, template_folder='views', static_folder='static')
    aplicacion.config['SECRET_KEY'] = CLAVE_SECRETA
    aplicacion.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))

    preparar_almacenamiento()

    aplicacion.register_blueprint(blueprint_escritores)
    aplicacion.register_blueprint(blueprint_catalogo)
    aplicacion.register_blueprint(blueprint_socios)
    aplicacion.register_blueprint(blueprint_movimientos)

    @aplicacion.route('/')
    def pagina_raiz():
        return render_template('index.html')

    return aplicacion


app = inicializar_aplicacion()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
