import bs4
import requests
import progressbar

import re
import os
import sys
import time

def get_links():
	r = requests.get('https://www.constituteproject.org/service/constitutions')
	con_list = r.json()
	bar = progressbar.ProgressBar()
	with open("links.txt", "w") as f:
		print("Writing links to /htmls/links.txt")
		for val in bar(con_list):
			f.write("https://constituteproject.org/service/html?cons_id=" + val["id"] + "\n")

def pull_html():
	with open('links.txt') as f:
		urls = f.readlines()
	bar = progressbar.ProgressBar()
	print("Writing html to files in /htmls")
	for url in bar(urls):
		r = requests.get(url.strip(" \n"))
		html_s = r.json()["html"]
		filename = re.search("[A-Z]\w*", url).group(0)
		with open("htmls/" + filename + ".txt", "w") as f:
			f.write(html_s)
		time.sleep(2)

def write_constitutions():
	bar = progressbar.ProgressBar()
	files = sorted(os.listdir("htmls/"))
	print("Writing constitution texts to files in /texts")
	for file_ in bar(files):
		with open("htmls/" + file_, "r") as f:
			html = f.read()
		soup = bs4.BeautifulSoup(html, "lxml")
		paragraphs = soup.find_all("p")
		with open("texts/" + file_, "w") as f:
			for p in paragraphs:
				f.write(p.text)
				f.write("\n")

def run_cli():
	print("\nWould you like to:")
	print("A) Get links?")
	print("B) Get html from links?")
	print("C) Get text from html?")
	print("D) All the above?")
	print("E) Exit")
	choice = input("Choice: ").lower()
	if choice in {"a", "d"}:
	    get_links()
	if choice in {"b", "d"}:
	    pull_html()
	if choice in {"c", "d"}:
		write_constitutions()
	if choice in {"a", "b", "c"}:
		print("Run another operation?")
		cont = input("Y/N ").lower()
		if cont == "y":
			run_cli()

if __name__=="__main__":
	run_cli()
