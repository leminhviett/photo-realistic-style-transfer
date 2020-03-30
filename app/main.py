from flask import Flask, render_template, request, url_for, redirect
import os

from skimage.color import rgb2gray
import skimage.filters as filters
from skimage.io import imsave
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ".\\upload"

@app.route('/')
def home():
	return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f_dict = request.files
      content = f_dict["content"]
      style = f_dict["style"]	
      print(content)

      content_path = os.path.join(app.config['UPLOAD_FOLDER'], "content\\in1.png")
      style_path = os.path.join(app.config['UPLOAD_FOLDER'], "style\\in1.png")
      content_seg_path = os.path.join(app.config['UPLOAD_FOLDER'], "content_segment\\in1.png")
      style_seg_path = os.path.join(app.config['UPLOAD_FOLDER'], "style_segment\\in1.png")

      content.save(content_path)
      style.save(style_path)
      segment(content_path, content_seg_path)
      segment(style_path, style_seg_path)

      return redirect(url_for('stylize'))

def segment(image_path, seg_path):
	# print(image_path)
	image = plt.imread(image_path)
	gray = rgb2gray(image)
	gray = gray < filters.threshold_local(gray,block_size=501)
	imsave(seg_path, gray*1.0)


@app.route('/stylization')
def stylize():
	os.system('python transfer.py --option_unpool cat5 -e -s --content ./upload/content --style ./upload/style --content_segment ./upload/content_segment --style_segment ./upload/style_segment/ --output ./static/ --verbose --image_size 512')
	return render_template("result.html") 
if __name__ == '__main__':
	app.run(debug = True)