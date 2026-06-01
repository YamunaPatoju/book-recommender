from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

books = pickle.load(open(os.path.join(BASE_DIR, 'books.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(BASE_DIR, 'pt.pkl'), 'rb'))
similarity_scores = pickle.load(open(os.path.join(BASE_DIR, 'similarity_scores.pkl'), 'rb'))
popular_df = pickle.load(open(os.path.join(BASE_DIR, 'popular.pkl'), 'rb'))


@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        if user_input not in pt.index:
            return render_template('recommend.html', data=[], message="Book not found")

        index = np.where(pt.index == user_input)[0][0]

        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]

            item = [
                temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0],
                temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0],
                temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
            ]

            data.append(item)

        return render_template('recommend.html', data=data, message="")

    return render_template('recommend.html', data=[], message="")


if __name__ == '__main__':
    app.run(debug=True)