from flask import Flask, request, render_template, jsonify
import os
from pymorphy2 import MorphAnalyzer
from search import load_tfidf_documents, load_inverted_index, search
from flask import send_from_directory

app = Flask(__name__)
morph = MorphAnalyzer()

source_files_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework1/files")
input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework4/result")
inverted_index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../homework3/inverted_index.txt")

doc_vectors, all_terms = load_tfidf_documents(input_folder)
inverted_index = load_inverted_index(inverted_index_path)

@app.route("/search", methods=["GET"])
def search_view():
    query = request.args.get("q", "")
    results = search(query, doc_vectors, all_terms, inverted_index) if query else []
    return render_template("search.html", results=results)

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(directory=source_files_folder, path=filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)