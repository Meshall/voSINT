from serpapi import GoogleSearch

def serpapi_reverse_image_search(image_url, api_key, start):
    google_params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": api_key,
        "start": start,  # Start parameter for pagination
        "device": "desktop",  # Device parameter
        "no_cache": True  # No cache parameter
    }
    yandex_params = {
        "engine": "yandex_images",
        "image_url": image_url,
        "api_key": api_key,
        "p": "1",  # Pagination parameter for Yandex
        "sortby": "ascending",  # Sort order parameter for Yandex
        "no_cache": True  # No cache parameter
    }

    google_search = GoogleSearch(google_params)
    yandex_search = GoogleSearch(yandex_params)

    # Perform Google reverse image search
    google_results = google_search.get_dict()
    google_inline_images = google_results.get("image_results", [])[:10]
    for image in google_inline_images:
        image['engine'] = 'google_reverse_image'

    # Perform Yandex reverse image search
    yandex_results = yandex_search.get_dict()
    yandex_inline_images = yandex_results.get("image_results", [])[:10]
    for image in yandex_inline_images:
        image['engine'] = 'yandex_images'

    # Combine the results from Google and Yandex
    inline_images = google_inline_images + yandex_inline_images

    return inline_images
