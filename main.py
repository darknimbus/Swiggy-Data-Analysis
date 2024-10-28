import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
BASE_URL = "https://www.swiggy.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Function to scrape restaurant data from Swiggy
def scrape_data(page):
    url = f"{BASE_URL}restaurants?page={page}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find restaurant listings
    restaurants = soup.find_all('div', class_='restaurant-card')
    
    data = []
    for restaurant in restaurants:
        name = restaurant.find('h3', class_='restaurant-name').text.strip()
        cuisine = restaurant.find('p', class_='cuisine').text.strip()
        rating = restaurant.find('span', class_='rating').text.strip()
        delivery_time = restaurant.find('span', class_='delivery-time').text.strip()
        
        data.append({
            'Name': name,
            'Cuisine': cuisine,
            'Rating': rating,
            'Delivery Time': delivery_time
        })
    
    return data

# Main function to collect data from multiple pages
def main():
    all_data = []
    for page in range(1, 6):  # Scraping first 5 pages
        all_data.extend(scrape_data(page))
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Data Cleaning
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Delivery Time'] = df['Delivery Time'].str.extract('(\d+)').astype(int)
    
    # Analysis - Average Rating by Cuisine
    avg_rating_by_cuisine = df.groupby('Cuisine')['Rating'].mean().reset_index()
    
    # Visualization - Bar Plot of Average Rating by Cuisine
    plt.figure(figsize=(12, 6))
    sns.barplot(data=avg_rating_by_cuisine.sort_values(by='Rating', ascending=False), x='Cuisine', y='Rating')
    plt.title('Average Rating by Cuisine')
    plt.xticks(rotation=45)
    plt.ylabel('Average Rating')
    plt.xlabel('Cuisine')
    plt.tight_layout()
    plt.savefig('average_rating_by_cuisine.png')  # Save the figure
    
    # Additional Metrics - Peak Ordering Hours (Assuming we have time data)
    # This part would require additional time-related data which is not included here.

if __name__ == "__main__":
    main()
