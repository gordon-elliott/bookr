from flask import Flask, request as flask_request, jsonify

from acme.bookr.db.book_request import delete_book_request, get_book_request, list_book_requests, create_book_request


app = Flask(__name__)


@app.route("/request", methods=['GET'])
def request_get_all():
    return jsonify([book_request for book_request in list_book_requests()])


@app.route("/request/<uuid:id_>", methods=['GET'])
def request_get(id_: str):
    book_request = get_book_request(id_)
    return jsonify(book_request if book_request else {})


@app.route("/request", methods=['POST'])
def request_post():
    email = flask_request.form["email"]
    title = flask_request.form["title"]
    book_request_dict = create_book_request(email, title)
    return jsonify(book_request_dict)


@app.route("/request/<uuid:id_>", methods=['DELETE'])
def request_delete(id_: str):
    delete_book_request(id_)
    return jsonify({})


@app.before_first_request
def init_db():
    from acme.bookr.db.catalogue import create_catalogue
    from acme.bookr.db.engine import engine
    from acme.bookr.db.mapping import metadata

    metadata.drop_all(engine)
    metadata.create_all(engine)
    create_catalogue()
    app.logger.info("Database is configured.")


if __name__ == '__main__':
    app.run(debug=False, threaded=True)
