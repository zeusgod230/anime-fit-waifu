import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def load_data():
    data = [
        {"title": "The Matrix",
         "overview": "A computer hacker learns about the true nature of his reality and his role in the war against its controllers."},
        {"title": "Inception",
         "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea."},
        {"title": "Interstellar",
         "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."},
        {"title": "The Godfather",
         "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
        {"title": "The Dark Knight",
         "overview": "Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."},
        {"title": "Pulp Fiction",
         "overview": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption."},
        {"title": "Fight Club",
         "overview": "An insomniac office worker and a soap maker form an underground fight club that evolves into something much more."},
        {"title": "Forrest Gump",
         "overview": "The presidencies of Kennedy and Johnson, the Vietnam War, and other events unfold through the perspective of an Alabama man."},
        {"title": "The Shawshank Redemption",
         "overview": "Two imprisoned men bond over several years, finding solace and eventual redemption through acts of common decency."},
        {"title": "Gladiator",
         "overview": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family."},
        {"title": "Titanic",
         "overview": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."},
        {"title": "Avengers: Endgame",
         "overview": "After the devastating events of Avengers: Infinity War, the universe is in ruins. The Avengers assemble once more."},
        {"title": "Avatar",
         "overview": "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following orders and protecting his new home."},
        {"title": "Iron Man",
         "overview": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil."},
        {"title": "The Lion King",
         "overview": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself."},
        {"title": "The Avengers",
         "overview": "Earth's mightiest heroes must come together to learn to fight as a team to stop the mischievous Loki."},
        {"title": "Black Panther",
         "overview": "T'Challa, heir to the hidden but advanced kingdom of Wakanda, must step forward to lead his people."},
        {"title": "Doctor Strange",
         "overview": "After a tragic accident, a brilliant surgeon embarks on a journey of healing only to be drawn into the world of mystic arts."},
        {"title": "Thor: Ragnarok",
         "overview": "Imprisoned on the other side of the universe, Thor must race against time to stop Ragnarok."},
        {"title": "The Social Network",
         "overview": "The story of Harvard student Mark Zuckerberg creating the social networking site Facebook."},
        {"title": "The Imitation Game",
         "overview": "During World War II, the English mathematical genius Alan Turing tries to crack the German Enigma code."},
        {"title": "Joker",
         "overview": "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society."},
        {"title": "Deadpool",
         "overview": "A wisecracking mercenary gets experimented on and becomes immortal but ugly, and sets out to track down the man who ruined his looks."},
        {"title": "The Wolf of Wall Street",
         "overview": "Based on the true story of Jordan Belfort, from his rise to a wealthy stockbroker to his fall involving crime, corruption and the federal government."},
        {"title": "The Revenant",
         "overview": "A frontiersman on a fur trading expedition fights for survival after being mauled by a bear and left for dead."},
        {"title": "The Irishman",
         "overview": "A mob hitman recalls his possible involvement with the slaying of Jimmy Hoffa."},
        {"title": "The Conjuring",
         "overview": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse."},
        {"title": "Parasite",
         "overview": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."},
        {"title": "Everything Everywhere All at Once",
         "overview": "An aging Chinese immigrant is swept up in an insane adventure where she alone can save existence by exploring other universes."},
        {"title": "Spider-Man: No Way Home",
         "overview": "Peter Parker's life and reputation are turned upside down after his identity is revealed."},
        {"title": "Barbie",
         "overview": "Barbie suffers a crisis that leads her to question her world and her existence."},
        {"title": "Oppenheimer",
         "overview": "The story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II."}

    ]
    return pd.DataFrame(data)

def recommend_movies(movie_title, movies_df, similarity_matrix):
    if movie_title not in movies_df['title'].values:
        return ["❗ Mohit Ki Bund Khojo."]

    index = movies_df[movies_df['title'] == movie_title].index[0]
    similarity_scores = list(enumerate(similarity_matrix[index]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = [movies_df.iloc[i[0]]['title'] for i in sorted_scores]
    return recommended_movies

def main():
    st.set_page_config(page_title="condom Recommender", page_icon="🎥")
    st.title("🎬 condom Recommendation System")
    st.write("Enter a movie name to get recommendations based on **content similarity**.")

    movies_df = load_data()

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['overview'])
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    movie_list = movies_df['title'].tolist()
    selected_movie = st.selectbox("Select a movie:", sorted(movie_list))

    if st.button("Get Recommendations"):
        recommendations = recommend_movies(selected_movie, movies_df, similarity_matrix)
        st.subheader("Recommended Movies:")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")

if __name__ == "__main__":
    main()
