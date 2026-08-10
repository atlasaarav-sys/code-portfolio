"""Notes CRUD REST API."""

import os

from flask import Flask, jsonify, request

import models

DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")


def create_app(db_path=DB_PATH):
    app = Flask(__name__)

    # A single long-lived connection, opened once at app creation. sqlite3's
    # ":memory:" database is scoped to the connection that created it -- a
    # fresh connection per request (e.g. via Flask's `g`) would see an empty
    # database every time, since each connection gets its own in-memory DB.
    connection = models.get_connection(db_path)

    def get_db():
        return connection

    @app.post("/notes")
    def create_note():
        data = request.get_json(silent=True) or {}
        title = data.get("title")
        if not title:
            return jsonify({"error": "title is required"}), 400
        note_id = models.create_note(get_db(), title, data.get("body", ""))
        return jsonify(models.get_note(get_db(), note_id)), 201

    @app.get("/notes")
    def list_notes():
        query = request.args.get("q")
        return jsonify(models.list_notes(get_db(), query))

    @app.get("/notes/<int:note_id>")
    def get_note(note_id):
        note = models.get_note(get_db(), note_id)
        if note is None:
            return jsonify({"error": "note not found"}), 404
        return jsonify(note)

    @app.put("/notes/<int:note_id>")
    def update_note(note_id):
        data = request.get_json(silent=True) or {}
        title = data.get("title")
        if not title:
            return jsonify({"error": "title is required"}), 400
        updated = models.update_note(get_db(), note_id, title, data.get("body", ""))
        if not updated:
            return jsonify({"error": "note not found"}), 404
        return jsonify(models.get_note(get_db(), note_id))

    @app.delete("/notes/<int:note_id>")
    def delete_note(note_id):
        deleted = models.delete_note(get_db(), note_id)
        if not deleted:
            return jsonify({"error": "note not found"}), 404
        return "", 204

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
