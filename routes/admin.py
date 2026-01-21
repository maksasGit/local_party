# routes/admin.py

from flask import Blueprint, request, jsonify
from database import get_session
from models import Category, Entry

admin_bp = Blueprint("admin", __name__)

# ===== Категории =====
@admin_bp.route("/category", methods=["POST"])
def create_category():
    data = request.json
    session = get_session()
    parent = None
    if data.get("parent_id"):
        parent = session.query(Category).get(data["parent_id"])
    category = Category(title=data["title"], descr=data.get("descr"), parent=parent)
    session.add(category)
    session.commit()
    session.close()
    return jsonify({"message": "Категория создана", "id": category.id})

@admin_bp.route("/category/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.json
    session = get_session()
    category = session.query(Category).get(category_id)
    if not category:
        session.close()
        return jsonify({"error": "Категория не найдена"}), 404
    category.title = data.get("title", category.title)
    category.descr = data.get("descr", category.descr)
    session.commit()
    session.close()
    return jsonify({"message": "Категория обновлена"})

@admin_bp.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    session = get_session()
    category = session.query(Category).get(category_id)
    if not category:
        session.close()
        return jsonify({"error": "Категория не найдена"}), 404
    session.delete(category)
    session.commit()
    session.close()
    return jsonify({"message": "Категория удалена"})


# ===== Записи =====
@admin_bp.route("/entry", methods=["POST"])
def create_entry():
    data = request.json
    session = get_session()
    category = session.query(Category).get(data["category_id"])
    if not category:
        session.close()
        return jsonify({"error": "Категория не найдена"}), 404
    entry = Entry(title=data["title"], descr=data.get("descr"), category=category)
    session.add(entry)
    session.commit()
    session.close()
    return jsonify({"message": "Запись создана", "id": entry.id})

@admin_bp.route("/entry/<int:entry_id>", methods=["PUT"])
def update_entry(entry_id):
    data = request.json
    session = get_session()
    entry = session.query(Entry).get(entry_id)
    if not entry:
        session.close()
        return jsonify({"error": "Запись не найдена"}), 404
    entry.title = data.get("title", entry.title)
    entry.descr = data.get("descr", entry.descr)
    session.commit()
    session.close()
    return jsonify({"message": "Запись обновлена"})

@admin_bp.route("/entry/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    session = get_session()
    entry = session.query(Entry).get(entry_id)
    if not entry:
        session.close()
        return jsonify({"error": "Запись не найдена"}), 404
    session.delete(entry)
    session.commit()
    session.close()
    return jsonify({"message": "Запись удалена"})
