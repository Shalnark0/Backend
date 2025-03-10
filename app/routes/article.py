from flask import Blueprint, request, jsonify
from app import db
from app.models.article import Article
from app.services.role_service import role_required, is_author_required
from app.services.auth_service import token_required

article_routes = Blueprint("article", __name__)

@article_routes.route("/article", methods=["POST"])
@token_required
@role_required("editor")  # Только пользователи с ролью "editor" могут создавать статьи
def create_article():
    data = request.get_json()
    user_data = request.user  # Получаем информацию о пользователе из токена

    new_article = Article(
        title=data["title"],
        content=data["content"],
        author_id=user_data["id"]  # Привязываем статью к автору
    )

    db.session.add(new_article)
    db.session.commit()
    return jsonify({"message": "Article created successfully", "article_id": new_article.id}), 201

@article_routes.route("/article/<int:article_id>", methods=["PUT"])
@token_required
@is_author_required  # Только автор статьи может её редактировать
def update_article(article_id):
    data = request.get_json()
    article = db.session.get(Article, article_id)

    article.title = data.get("title", article.title)
    article.content = data.get("content", article.content)

    db.session.commit()
    return jsonify({"message": "Article updated successfully"})
