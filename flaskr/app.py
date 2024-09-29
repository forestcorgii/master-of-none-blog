from pathlib import Path
from flask import Flask, render_template
import markdown2, os, re, subprocess

app = Flask(__name__)

blogs_dir = "static/blogs"
if not os.path.exists(blogs_dir):
	blogs_dir = 'flaskr/static/blogs'

# Custom function to handle [[link]] and ![[link]]
def preprocess_custom_links(markdown_text):
	# Convert ![[image]] to standard markdown image syntax ![alt_text](image_path)
	if '.png' in markdown_text:
		markdown_text = re.sub(r'!\[\[(.*?)\]\]', r'![\1](/static/attachments/\1)', markdown_text)
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
	blogs = [f.name for f in Path(blogs_dir).iterdir() if f.is_file()]
		
	return render_template("homepage.html",title="my humpage", blogs=blogs)

@app.route("/blogs/<title>", methods=["GET"])
def blog(title):
	with open(f"{blogs_dir}/{title}", 'r', encoding='utf8') as file:
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
	repo_dir = '/home/ubuntu/mon'
	try:
		if not os.path.exists(repo_dir):
			repo_dir = '/home/sean/workspace/mon'
			
		os.chdir(repo_dir)
		subprocess.run(['git', 'pull'], check=True)
		return 'success ' + 400
		# return subprocess.Popen(['/home/ubuntu/mon','ls'], shell=False, stdout=subprocess.PIPE).stdout.read()
		# return subprocess.Popen('sudo git pull', shell=False, stdout=subprocess.PIPE).stdout.read()
	except Exception as ex:
		return 'exception: '+ repo_dir + str(ex)
