# eckser

Very simple script for getting media URLs from Twitter (presently X) in BBCode form.

## Usage

The script can be ran using

```bash
python3 ./eckser url_of_post
```

and will print out the highest quality media links for all image and video attachments of that post, formatted line by line as `[img]url[/img]` or `[video]url[/video]` for images and videos respectively.

## Requirements

You're gonna need Python 3.x and the ScrapFly playwright scraper library.

Given that you already have Python, all the dependencies can be installed by running either of these commands

```bash
pip install playwright jmespath scrapfly-sdk
pip install -r ./requirements.txt
```
