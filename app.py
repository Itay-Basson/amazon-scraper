from flask import Flask, render_template, request, jsonify
from scraping import get_amazon_com_search_results, get_product_details_parallel
from database import get_past_searches

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    search_query = request.json["search_query"]
    try:
        results = get_amazon_com_search_results(search_query)
        return jsonify(results)
    except Exception as e:
        print(e)
        return "Error fetching search results", 500

@app.route("/product_details", methods=["POST"])
def product_details():
    asin = request.json["asin"]
    try:
        product_details = get_product_details_parallel(asin)
        return jsonify(product_details)
    except Exception as e:
        print(f"Error fetching product details: {e}")
        return "Error fetching product details", 500

@app.route("/get_past_searches", methods=["GET"])
def handle_get_past_searches():
    past_searches = get_past_searches()
    return jsonify(past_searches)

if __name__ == "__main__":
    app.run(debug=True)