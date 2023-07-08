# -*- coding: utf-8 -*-
from typing import List, Dict, Union, Optional
import logging
import pandas as pd
from googlemaps import GoogleMapsScraper
import fire

# Constants
SORT_OPTIONS = {"most_relevant": 0, "newest": 1, "highest_rating": 2, "lowest_rating": 3}

# Logger setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def scrape_reviews(
    url: str, scraper: GoogleMapsScraper, sort_option: str, num_reviews: int, include_source: bool, place_data: Dict
) -> List[Dict[str, Union[str, int]]]:
    """Scrape reviews from a given URL."""

    logger.info(f"Starting to scrape reviews for URL: {url}")
    if scraper.sort_by(url, SORT_OPTIONS[sort_option]) != 0:
        logger.error("Error sorting reviews")
        return []

    reviews_data = []
    review_count = 0
    while review_count < num_reviews:
        logger.info(f"Fetching reviews, current count: {review_count}")
        reviews = scraper.get_reviews(review_count)
        if not reviews:
            logger.info(f"No reviews found for this URL: {url}")
            break

        for review in reviews:
            review_data = review.copy()
            review_data.update(place_data)  # Add place data to review data
            if include_source:
                review_data["url_source"] = url
            reviews_data.append(review_data)
        review_count += len(reviews)
    logger.info(f"Finished scraping reviews for URL: {url}")
    return reviews_data


def main(
    num_reviews: int = 100,
    input_file: str = "urls.txt",
    sort_option: str = "newest",
    include_place: bool = False,
    debug_mode: bool = False,
    include_source: bool = False,
    output_file: str = "gm_reviews.csv",
):
    """Scrape Google Maps reviews and save them to a CSV file."""
    logger.info("Starting the Google Maps reviews scraper.")

    review_dataframe = pd.DataFrame()
    with GoogleMapsScraper(debug=debug_mode) as scraper:
        with open(input_file, "r") as urls_file:
            for url in map(str.strip, urls_file):
                logger.info(f"Scraping URL: {url}")
                place_data = scraper.get_account(url) if include_place else {}
                reviews_data = scrape_reviews(url, scraper, sort_option, num_reviews, include_source, place_data)
                if reviews_data:
                    review_dataframe = pd.concat([review_dataframe, pd.DataFrame(reviews_data)], ignore_index=True)
                else:
                    logger.warning(f"No reviews data obtained for URL: {url}")

    review_dataframe.to_csv(output_file)
    logger.info(f"Saved reviews to {output_file}")


if __name__ == "__main__":
    fire.Fire(main)
