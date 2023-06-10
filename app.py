
from flask import Flask, render_template, request, jsonify , make_response

import openai

app = Flask(__name__, template_folder='templates')

openai.api_key = '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'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def generate_response(destination, days, season, budget_slabs, activities_for_kids, age_group, search_query):
    query = f"Plan a {days}-day trip to {destination} during {season} season with a budget of {budget_slabs}. I would like suggestions for a detailed day-by-day plan that minimizes travel each day."

    if activities_for_kids:
        query += f" Also, include activities for kids aged {age_group}."

    if search_query:
        search_terms = ', '.join(search_query)  # Convert the list of selected options to a string
        query += f" Additionally, give suggestions and tourist attractions for {search_terms} in {destination}."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            max_tokens=1000,
            temperature=0.7
        )
        completion_text = response.choices[0].text.strip()
        print("Input Query:", query)
        print("Completion Text:", completion_text)
        return completion_text

    except Exception as e:
        print("Error:", str(e))
        return "An error occurred while generating the response."

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    destination = request.form['destination']
    days = request.form['days']
    season = request.form['season']
    budget_slabs = request.form['budget_slabs']
    age_group = request.form.get('age_group')
    search_query = request.form.getlist('search_query')

    # Set activities_for_kids based on button clicked
    activities_for_kids = False
    if request.form.get('activities_for_kids') == 'Yes':
        activities_for_kids = True

    response = generate_response(destination, days, season, budget_slabs, activities_for_kids, age_group, search_query)


    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
