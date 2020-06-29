# Python web scraping with Scrapy
> Demo: https://www.youtube.com/watch?v=ysyskgjsPI0&t=1m45s

## Features:
+ Download Images
+ Store data in many kinds of database: SQLite, MySQL, MongDB
+ Store data in many formats: csv, json, xml
+ Using User Agent, Proxy

## Installation:
1. run `pip install -r requirements.txt`
2. Install and connect SQLite, MySQL, MongDB

## Usage:
+ for .csv: `scrapy crawl amazon -o "store by formats"/products.csv`
+ for .json: `scrapy crawl amazon -o "store by formats"/products.json`
+ for .xml: `scrapy crawl amazon -o "store by formats"/products.xml`
