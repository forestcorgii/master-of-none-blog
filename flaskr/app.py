from pathlib import Path
from flask import Flask, render_template
import markdown2
import re
import subprocess

app = Flask(__name__)

# Custom function to handle [[link]] and ![[link]]
def preprocess_custom_links(markdown_text):
	# Convert ![[image]] to standard markdown image syntax ![alt_text](image_path)
	if '.png' in markdown_text:
		markdown_text = re.sub(r'!\[\[(.*?)\]\]', r'![\1](/static/mon/attachments/\1)', markdown_text)
	else:
		markdown_text = re.sub(r'!\[\[(.*?)\]\]', r'![\1](/static/\1)', markdown_text)
	# Convert ![[link]] to standard markdown image syntax ![alt_text](link)
	markdown_text = re.sub(r'!\[\[(.*?)\]\]', r'![\1](\1)', markdown_text)
	# Convert [[link]] to standard markdown link syntax [link](link)
	markdown_text = re.sub(r'\[\[(.*?)\]\]', r'[\1](\1)', markdown_text)
	# Convert ==text== to <mark>text</mark> for highlighting
	markdown_text = re.sub(r'==(.*?)==', r'<mark>\1</mark>', markdown_text)
	return markdown_text

@app.route("/")
def homepage():
	
	blogs_dir = "flaskr/static/mon/blogs"
	blogs = [f.name for f in Path(blogs_dir).iterdir() if f.is_file()]
		
	return render_template("homepage.html",title="my humpage", blogs=blogs)

@app.route("/blogs/<title>", methods=["GET"])
def blog(title):
	with open(f"flaskr/static/mon/blogs/{title}", 'r', encoding='utf8') as file:
		file_content = file.read()

	# Preprocess the custom markdown syntax
	processed_content = preprocess_custom_links(file_content)

	# Convert the markdown with syntax highlighting and other extras
	processed_content_lines = processed_content.split('\n') 
	new_title = processed_content_lines[0].replace('# ', '')
	converted_content = markdown2.markdown('\n'.join(processed_content_lines[1:]), extras=["strike", "fenced-code-blocks", "highlight"])

	return render_template("blog.html", title=new_title, message=converted_content)

@app.route('/pull')
def executePull():
	# testing remote git pull
	return subprocess.Popen('git pull', shell=False, stdout=subprocess.PIPE).stdout.read()
