from flask import Flask, jsonify, request, render_template, send_from_directory
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint

from api.swagger import spec
from api.controllers.todo_controller import bp as todo_bp
from api.middleware import middleware
from api.responses import success_response
from infrastructure.databases import init_db
# from config import Config, SwaggerConfig  # Nếu chưa dùng thì tắt đi để tránh cảnh báo

def create_app():
    app = Flask(__name__)

    # --- Swagger (flasgger) ---
    Swagger(app)

    # --- Blueprint API ---
    app.register_blueprint(todo_bp)

    # --- Swagger UI (/docs) ---
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Todo API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # --- DB & middleware ---
    init_db(app)
    middleware(app)

    # --- Tự động add các path vào OpenAPI spec ---
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith('todo.'):
                view_func = app.view_functions[rule.endpoint]
                print(f"Adding path: {rule.rule} -> {view_func}")
                spec.path(view=view_func)

    # --- Xuất swagger.json ---
    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    # === ROUTES CHO FRONTEND ===
    # Trang chủ -> templates/index.html
    @app.route("/")
    def home_page():
        return render_template("index.html")

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory("static/img", "favicon.ico", mimetype="image/vnd.microsoft.icon")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=6868, debug=True)
