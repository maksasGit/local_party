from flask import Blueprint, jsonify
from models import Category, Entry
from database import get_session

bestiary_bp = Blueprint("bestiary", __name__)

def category_to_dict(category):
    return {
        "id": category.id,
        "title": category.title,
        "descr": category.descr,
        "children": [category_to_dict(c) for c in category.children],
        "entries": [{"id": e.id, "title": e.title, "descr": e.descr} for e in category.entries]
    }

@bestiary_bp.route("/bestiary")
def get_bestiary():
    session = get_session()
    roots = session.query(Category).filter(Category.parent_id == None).all()
    return jsonify([category_to_dict(c) for c in roots])
