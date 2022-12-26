from flask import Flask,render_template,request
import pickle
import numpy as np


popular_book_df = pickle.load(open('popular_book.pkl','rb'))
df_pt = pickle.load(open('df_pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
    book_name = list(popular_book_df['Book-Title'].values),
    author = list(popular_book_df['Book-Author'].values),
    publication = list(popular_book_df['Year-Of-Publication'].values),
    images = list(popular_book_df['Image-URL-M'].values),
    num_rating = list(popular_book_df['num_of_rating'].values),
    avg_rating = list(popular_book_df['avg-rating'].values) )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        print(user_input)
        index = np.where(df_pt.index== user_input)[0][0]
        
        similar_items = sorted(list(enumerate(similarity_score[index])),key= lambda x:x[1],reverse=True)[1:5]
        
        data = []
        for ind in similar_items:
            item=[]
            temp_df = books[books['Book-Title']==df_pt.index[ind[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
        return render_template('recommend.html',data=data)  
    except :
        return ("<html><body><h1 style='text-align:center;color:red;margin-top:20%;font-size:3rem'>The book not in the database or check the spelling of the book you Enter</h1></body></html>")      



if  __name__ =='__main__':
    app.run(debug=True)