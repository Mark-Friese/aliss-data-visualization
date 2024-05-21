# ALISS Data Visualization

This project fetches, processes, and visualizes data from the ALISS (A Local Information System for Scotland) API, focusing on allotments and community gardens. The data is displayed on an interactive map using Folium and exported to a CSV file.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/aliss-data-visualization.git
    cd aliss-data-visualization
    ```

2. Install the required Python libraries:
    ```sh
    pip install requests pandas geopandas folium
    ```

## Usage

1. Run the main script:
    ```sh
    python main.py
    ```

2. The script will:
    - Fetch data from the ALISS API for the specified categories.
    - Process the data and filter out non-UK locations.
    - Save an interactive map as `allotments_map.html`.
    - Export the processed data to `allotments_data.csv`.

## Files

- `main.py`: The main script to run the project.
- `allotments_map.html`: The output interactive map.
- `allotments_data.csv`: The processed data in CSV format.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

