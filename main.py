import requests
import pandas as pd
import folium
from shapely.geometry import Point

# Define the base URL for the API endpoint
base_url = "https://api.aliss.org/v4/services"

# Define the headers for the request
headers = {
    "Accept": "application/json"
}

def fetch_all_pages(url, headers, params):
    all_results = []
    while True:
        # Make the GET request to the API
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                print("Failed to parse JSON response")
                break

            # Check if the 'data' key is in the JSON response
            if 'data' in data:
                # Append the results of the current page
                all_results.extend(data['data'])
            else:
                print("The key 'data' was not found in the response")
                break
            
            # Check if there is a next page
            if 'next' in data and data['next']:
                # Update the params for the next page
                params['page'] += 1
            else:
                # No more pages, break the loop
                break
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break
    return all_results

def fetch_data_for_categories(categories):
    all_data = []
    for category in categories:
        params = {
            "category": category,
            "page": 1
        }
        data = fetch_all_pages(base_url, headers, params)
        all_data.extend(data)
    return all_data

def main():
    categories = ["allotments", "community-garden"]  # List of categories
    all_data = fetch_data_for_categories(categories)

    # Create a DataFrame from the data
    df = pd.DataFrame(all_data)
    
    # Check if 'locations' is in the DataFrame columns
    if 'locations' in df.columns:
        df = df.explode('locations')  # Expand the list of locations
        df = df.dropna(subset=['locations'])  # Drop rows without location data
        # Expand location data into multiple columns
        location_df = df['locations'].apply(pd.Series)
        df = pd.concat([df.drop(columns=['locations']), location_df], axis=1)
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)
        
        # Filter for UK locations (latitude: 49.9 to 60.9, longitude: -8.6 to 1.9)
        uk_mask = (df['latitude'].between(49.9, 60.9)) & (df['longitude'].between(-8.6, 1.9))
        df = df[uk_mask]

        df = df.dropna(subset=['latitude', 'longitude'])  # Drop rows without lat/long data
        
        # Create an interactive map
        map_center = [55.3781, -3.4360]  # Center of the UK
        m = folium.Map(location=map_center, zoom_start=6)

        # Add points to the map
        for _, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=row.get('name', 'No Name')
            ).add_to(m)

        # Save the interactive map as an HTML file
        m.save('allotments_map.html')
        print("Interactive map saved as allotments_map.html")

    else:
        print("Location data not found in the dataframe.")

    # Export the data to CSV
    df.to_csv('allotments_data.csv', index=False)
    print("Data exported to allotments_data.csv")

if __name__ == "__main__":
    main()
