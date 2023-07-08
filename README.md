# Google Maps Scraper

Scraper of Google Maps reviews.
The code allows to extract the **most recent** reviews starting from the url of a specific Point Of Interest (POI) in Google Maps.
An additional extension helps to monitor and incrementally store the reviews in a MongoDB instance.

## Installation

Follow these steps to use the scraper:

-   Download Chromedrive from [here](https://chromedriver.storage.googleapis.com/index.html?path=2.45/).
-   Install Python packages from requirements file, either using pip, conda or virtualenv:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

**Note**: Python >= 3.6 is required.

## Basic Usage

The scraper.py script needs two main parameters as input:

-   `--num_reviews`: number of reviews to retrieve, starting from the most recent (default: 100)
-   `--input_file`: input file name, containing a list of urls that point to Google Maps place reviews (default: _urls.txt_)
-   `--sort_option`: string value among most_relevant, newest, highest_rating or lowest_rating (default: newest), developed by @quaesito and that allows to change sorting behavior of reviews
-   `--include_place`: boolean value that allows to scrape POI metadata instead of reviews (default: false)
-   `--debug_mode`: boolean value that allows to run the browser using the graphical interface (default: false)
-   `--include_source`: boolean value that allows to store source URL as additional field in CSV (default: false)
-   `--output_file`: path of output file

Example:

`python scraper.py --num_reviews 100 --input_file urls.txt --sort_option newest --include_place True --debug_mode False --include_source False --output_file data/reviews.csv`

For a basic description of logic and approach about this software development, have a look at the [Medium post](https://towardsdatascience.com/scraping-google-maps-reviews-in-python-2b153c655fc2)

## Monitoring functionality

The monitor.py script can be used to have an incremental scraper and override the limitation about the number of reviews that can be retrieved.
The only additional requirement is to install MongoDB on your laptop: you can find a detailed guide on the [official site](https://docs.mongodb.com/manual/installation/)

The script takes two input:

-   `--i`: same as monitor.py script
-   `--from-date`: string date in the format YYYY-MM-DD, gives the minimum date that the scraper tries to obtain

The main idea is to **periodically** run the script to obtain latest reviews: the scraper stores them in MongoDB up to get either the latest review of previous run or the day indicated in the input parameter.

Take a look to this [Medium post](https://medium.com/@mattiagasparini2/monitoring-of-google-maps-reviews-29e5d35f9d17) to have more details about the idea behind this feature.

## Notes

Url must be provided as expected, you can check the example file urls.txt to have an idea of what is a correct url.
If you want to generate the correct url:

1. Go to Google Maps and look for a specific place;
2. Click on the number of reviews in the parenthesis;
3. Save the url that is generated from previous interaction.
