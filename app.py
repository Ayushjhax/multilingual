from flask import Flask, request, render_template
import weaviate

app = Flask(__name__)

cohere_api_key = 'T7E5YdqYVduosUnRrTAGvimDFbrSXFSdUOmk3nHA'
auth_config = weaviate.auth.AuthApiKey(api_key="76320a90-53d8-42bc-b41d-678647c6672e") 
client = weaviate.Client(
    url="https://cohere-demo.weaviate.network/",
    auth_client_secret=auth_config,
    additional_headers={
        "X-Cohere-Api-Key": cohere_api_key,
    }
)

def semantic_search(query, results_lang=''):
    try:
        nearText = {"concepts": [query]}
        properties = ["text", "title", "url", "views", "lang", "_additional {distance}"]

        if results_lang != '':
            where_filter = {
                "path": ["lang"],
                "operator": "Equal",
                "valueString": results_lang
            }
            response = (
                client.query
                .get("Articles", properties)
                .with_where(where_filter)
                .with_near_text(nearText)
                .with_limit(5)
                .do()
            )
        else:
            response = (
                client.query
                .get("Articles", properties)
                .with_near_text(nearText)
                .with_limit(5)
                .do()
            )

        result = response.get('data', {}).get('Get', {}).get('Articles', [])
        return result

    except Exception as e:
        print(f"Error during semantic search: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        language = request.form['language']
        results = semantic_search(query, language)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)