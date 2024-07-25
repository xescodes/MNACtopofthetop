    import streamlit as st
    import requests
    from bs4 import BeautifulSoup
    import json

    def scrape_artwork(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        artworks = []
        for artwork in soup.find_all('div', class_='views-row'):
            title_element = artwork.find('h2', class_='node-title')
            title = title_element.text.strip() if title_element else 'Unknown Title'

            image_element = artwork.find('img')
            image = image_element['src'] if image_element and 'src' in image_element.attrs else ''

            artist_element = artwork.find('div', class_='field-name-field-autor')
            artist = artist_element.text.strip() if artist_element else 'Unknown Artist'

            if title != 'Unknown Title' or artist != 'Unknown Artist':
                artworks.append({
                    'title': title,
                    'image': image,
                    'artist': artist,
                })

        return artworks

# Function to load saved favorites
def load_favorites():
    try:
        with open('favorites.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save favorites
def save_favorites(favorites):
    with open('favorites.json', 'w') as f:
        json.dump(favorites, f)

# Streamlit app
    def main():
        st.title("Museu Nacional d'Art de Catalunya - Favorite Artworks")

        # Load favorites
        favorites = load_favorites()

        # Scrape artwork data
        url = "https://www.museunacional.cat/ca/advanced-search-piece"
        artworks = scrape_artwork(url)

        if not artworks:
            st.error("No artworks found. The website structure might have changed.")
        else:
            # Display artworks
            for artwork in artworks:
                st.subheader(artwork['title'])
                if artwork['image']:
                    st.image(artwork['image'], use_column_width=True)
                st.write(f"Artist: {artwork['artist']}")

    # Display artworks
    for artwork in artworks:
        st.subheader(artwork['title'])
        st.image(artwork['image'], use_column_width=True)
        st.write(f"Artist: {artwork['artist']}")

        # Check if the artwork is already in favorites
        is_favorite = any(fav['title'] == artwork['title'] for fav in favorites)

        if is_favorite:
            if st.button(f"Remove from Favorites - {artwork['title']}"):
                favorites = [fav for fav in favorites if fav['title'] != artwork['title']]
                save_favorites(favorites)
                st.success("Removed from favorites!")
        else:
            if st.button(f"Add to Favorites - {artwork['title']}"):
                favorites.append(artwork)
                save_favorites(favorites)
                st.success("Added to favorites!")

        st.markdown("---")

    # Display favorites
    st.header("Your Favorites")
    for fav in favorites:
        st.subheader(fav['title'])
        st.image(fav['image'], use_column_width=True)
        st.write(f"Artist: {fav['artist']}")
        st.markdown("---")

if __name__ == "__main__":
    main()