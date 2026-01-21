# routes/admin.py

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from database import get_session
from models import Category, Entry

admin_bp = Blueprint("admin", __name__)

# ===== Константы валидации =====
MAX_TITLE_LENGTH = 100
MAX_DESCR_LENGTH = 500

# ===== Вспомогательные функции =====
def validate_string_field(data, field_name, required=True, max_length=None):
    value = data.get(field_name)
    if required and (value is None or not str(value).strip()):
        return False, f"Поле '{field_name}' обязательно"
    if max_length and value and len(value) > max_length:
        return False, f"Поле '{field_name}' не должно превышать {max_length} символов"
    return True, value.strip() if value else None


# ===== Категории =====
@admin_bp.route("/category", methods=["POST"])
def create_category():
    data = request.json or {}
    session = get_session()
    try:
        valid, title = validate_string_field(data, "title")
        if not valid:
            return jsonify({"error": title}), 400

        valid, descr = validate_string_field(data, "descr", required=False, max_length=MAX_DESCR_LENGTH)
        if not valid:
            return jsonify({"error": descr}), 400

        parent = None
        parent_id = data.get("parent_id")
        if parent_id is not None:
            parent = session.query(Category).get(parent_id)
            if not parent:
                return jsonify({"error": "Родительская категория не найдена"}), 404

        category = Category(title=title, descr=descr, parent=parent)
        session.add(category)
        session.commit()
        return jsonify({"message": "Категория создана", "id": category.id}), 201

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500
    finally:
        session.close()


@admin_bp.route("/category/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.json or {}
    session = get_session()
    try:
        category = session.query(Category).get(category_id)
        if not category:
            return jsonify({"error": "Категория не найдена"}), 404

        valid, title = validate_string_field(data, "title", required=False, max_length=MAX_TITLE_LENGTH)
        if not valid:
            return jsonify({"error": title}), 400
        if title:
            category.title = title

        valid, descr = validate_string_field(data, "descr", required=False, max_length=MAX_DESCR_LENGTH)
        if not valid:
            return jsonify({"error": descr}), 400
        if descr is not None:
            category.descr = descr

        session.commit()
        return jsonify({"message": "Категория обновлена"})

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500
    finally:
        session.close()


@admin_bp.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    session = get_session()
    try:
        category = session.query(Category).get(category_id)
        if not category:
            return jsonify({"error": "Категория не найдена"}), 404
        session.delete(category)
        session.commit()
        return jsonify({"message": "Категория удалена"})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500
    finally:
        session.close()


# ===== Записи =====
@admin_bp.route("/entry", methods=["POST"])
def create_entry():
    data = request.json or {}
    session = get_session()
    try:
        valid, title = validate_string_field(data, "title")
        if not valid:
            return jsonify({"error": title}), 400

        valid, descr = validate_string_field(data, "descr", required=False, max_length=MAX_DESCR_LENGTH)
        if not valid:
            return jsonify({"error": descr}), 400

        category_id = data.get("category_id")
        if category_id is None:
            return jsonify({"error": "Поле 'category_id' обязательно"}), 400

        category = session.query(Category).get(category_id)
        if not category:
            return jsonify({"error": "Категория не найдена"}), 404

        entry = Entry(title=title, descr=descr, category=category)
        session.add(entry)
        session.commit()
        return jsonify({"message": "Запись создана", "id": entry.id}), 201

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500
    finally:
        session.close()


@admin_bp.route("/entry/<int:entry_id>", methods=["PUT"])
def update_entry(entry_id):
    data = request.json or {}
    session = get_session()
    try:
        entry = session.query(Entry).get(entry_id)
        if not entry:
            return jsonify({"error": "Запись не найдена"}), 404

        valid, title = validate_string_field(data, "title", required=False, max_length=MAX_TITLE_LENGTH)
        if not valid:
            return jsonify({"error": title}), 400
        if title:
            entry.title = title

        valid, descr = validate_string_field(data, "descr", required=False, max_length=MAX_DESCR_LENGTH)
        if not valid:
            return jsonify({"error": descr}), 400
        if descr is not None:
            entry.descr = descr

        session.commit()
        return jsonify({"message": "Запись обновлена"})

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500
    finally:
        session.close()


@admin_bp.route("/entry/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    session = get_session()
    try:
        entry = session.query(Entry).get(entry_id)
        if not entry:
            return jsonify({"error": "Запись не найдена"}), 404
        session.delete(entry)
        session.commit()
        return jsonify({"message": "Запись удалена"})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500
    finally:
        session.close()
