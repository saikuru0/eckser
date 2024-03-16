import sys
from playwright.sync_api import sync_playwright

def scrape_tweet(url: str) -> list:
	_xhr_calls = []

	def intercept_response(response):
		if response.request.resource_type == "xhr":
			_xhr_calls.append(response)
		return response

	with sync_playwright() as pw:
		browser = pw.chromium.launch(headless=True)
		context = browser.new_context()
		page = context.new_page()

		page.on("response", intercept_response)
		page.goto(url)
		page.wait_for_selector("[data-testid='tweet']")

		tweet_calls = [f for f in _xhr_calls if "TweetResultByRestId" in f.url]
		media_urls = []
		for xhr in tweet_calls:
			data = xhr.json()
			for item in data['data']['tweetResult']['result']['legacy']['extended_entities']['media']:
				if 'video_info' in item:
					best_variant = max(item['video_info']['variants'], key=lambda x: x.get('bitrate', 0))
					if 'url' in best_variant:
						media_urls.append(best_variant['url'])
				elif 'media_url_https' in item:
					media_urls.append(item['media_url_https'])
		return media_urls

if __name__ == "__main__":
	
	video_formats = (".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm")
	image_formats = (".jpg", ".jpeg", ".png", ".webp")

	final_urls = []
	
	if len(sys.argv) == 2:
		try:
			media_urls = scrape_tweet(sys.argv[1])
			for url in media_urls:
				if any(format in url and url.split('/') for format in video_formats):
					final_urls.append("[video]" + url + "[/video]")
				elif any(format in url for format in image_formats):
					final_urls.append("[img]" + url + "[/img]")
		except:
			pass
	
	for final_url in final_urls:
		print(final_url)
