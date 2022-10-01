import pandas as pd

# Makes words like action and actions into one word
def stem(text):
    l=[]
    for i in text.split(" "):
        l.append(ps.stem(i))
    return " ".join(l)

# Removes the duplicate words
def repeat(text):
    dict={} # Name repeat counter
    l=[]
    for i in text.split():
        count=0
        if i not in dict:
            count+=1
            dict.update({i:count})
            l.append(i)
    return " ".join(l)

def recommend(song):
    song_index=new_df[new_df['title']==song].index[0]
    distances=similarity[song_index]
    song_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in song_list:
        print(new_df.iloc[i[0]].title)

songs=pd.read_csv('D:/Song Recommendation System/Beta/Top 500 Songs.csv',encoding='unicode_escape')

songs=songs[['title','artist','writers','producer']]

artist_lst=songs['artist'].tolist()
writer_lst=songs['writers'].tolist()
producer_lst=songs['producer'].tolist()

tags=[]
for i in range(len(artist_lst)):
    tag=artist_lst[i]+" "+writer_lst[i]+" "+producer_lst[i]
    tags.append(tag)
songs['tags']=tags

new_df=songs[['title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:"".join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

# Text vectorization
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(stop_words='english',max_features=500)
vectors=cv.fit_transform(new_df['tags']).toarray()

# Remove similar words and same words like action, actions should be one
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
new_df['tags']=new_df['tags'].apply(stem) # action, actions
new_df['tags']=new_df['tags'].apply(repeat) # repetition

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vectors)
print(recommend('Smells Like Teen Spirit')) # Can input any song from dataset