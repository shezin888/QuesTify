from flask import Flask, request, render_template, flash, redirect, url_for,session, Response, render_template_string
from objective import ObjectiveTest
from subjective import SubjectiveTest
# from readpdf import Extractpdf
from questiongenerator import QuestionGenerator
import PyPDF2
import whisper
from transformers import logging
logging.set_verbosity_warning()
from transformers import pipeline
from moviepy.editor import VideoFileClip
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Set the maximum number of sentences to include in the summary
MAX_SENTENCES = 3
app.secret_key= 'aica2'

# import nltk
# nltk.download("all")
# exit()
# @app.route('/')
# def home():
# 	return render_template('home.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home')
def home():
	return render_template('home2.html')


# @app.route('/home2')
# def home2():
# 	return render_template('home2.html')

@app.route('/question', methods=["POST"])
def question():
	return render_template('question.html')

@app.route('/input', methods=["POST"])
def input():
	return render_template('input.html')

@app.route('/upload', methods=["POST"])
def upload():
	return render_template('upload.html')

@app.route('/summ', methods=["POST"])
def summ():
	return render_template('summ.html')

@app.route('/summ_text', methods=["POST"])
def summ_text():
	return render_template('summ_text.html')

@app.route('/summ_upload', methods=["POST"])
def summ_upload():
	return render_template('summ_upload.html')

@app.route('/summ_file_generate', methods=["POST"])
def summ_file_generate():
	if request.method == "POST":
		inputFile = request.files["filename"]
		pgnostart = request.form["pgnostart"]
		pgnoend = request.form["pgnoend"]
		
		pdf = PyPDF2.PdfFileReader(inputFile)
    
		extracted_text = ''
		for page_num in range(int(pgnostart) - 1, int(pgnoend)):
			page = pdf.getPage(page_num)
			page_text = page.extractText()
			extracted_text += page_text
		
		inputText = extracted_text
		#print(inputText)

		sentences = sent_tokenize(inputText)
		words = word_tokenize(inputText)

		# Remove stop words
		stop_words = set(stopwords.words('english'))
		words = [word for word in words if word.casefold() not in stop_words]

		# Calculate the frequency of each word
		word_freq = FreqDist(words)

		# Calculate the score for each sentence by adding up the frequencies of its constituent words
		sent_scores = {}
		for i, sentence in enumerate(sentences):
			for word in word_tokenize(sentence.lower()):
				if word in word_freq:
					if i not in sent_scores:
						sent_scores[i] = word_freq[word]
					else:
						sent_scores[i] += word_freq[word]

		# Select the top N sentences with the highest scores
		top_sentences = sorted(sent_scores, key=sent_scores.get, reverse=True)[:MAX_SENTENCES]

		# Sort the top sentences in their original order
		summary = [sentences[i] for i in sorted(top_sentences)]
		print(summary)
		summary = '\n'.join(summary)
		return render_template('summ_text_data.html', cresults = summary)		
















@app.route('/summ_generate', methods=["POST"])
def summ_generate():
	if request.method == "POST":
		inputText = request.form["itext"]

		sentences = sent_tokenize(inputText)
		words = word_tokenize(inputText)

		# Remove stop words
		stop_words = set(stopwords.words('english'))
		words = [word for word in words if word.casefold() not in stop_words]

		# Calculate the frequency of each word
		word_freq = FreqDist(words)

		# Calculate the score for each sentence by adding up the frequencies of its constituent words
		sent_scores = {}
		for i, sentence in enumerate(sentences):
			for word in word_tokenize(sentence.lower()):
				if word in word_freq:
					if i not in sent_scores:
						sent_scores[i] = word_freq[word]
					else:
						sent_scores[i] += word_freq[word]

		# Select the top N sentences with the highest scores
		top_sentences = sorted(sent_scores, key=sent_scores.get, reverse=True)[:MAX_SENTENCES]

		# Sort the top sentences in their original order
		summary = [sentences[i] for i in sorted(top_sentences)]
		summary = '\n'.join(summary)
		return render_template('summ_text_data.html', cresults = summary)

@app.route('/file_test_generate', methods=["POST"])
def file_test_generate():
	if request.method == "POST":
		inputFile = request.files["filename"]
		pgnostart = request.form["pgnostart"]
		pgnoend = request.form["pgnoend"]
		testType = request.form["test_type"]
		noOfQues = request.form["noq"]
		print("################################################################################")
		print(type(noOfQues))
		pdf = PyPDF2.PdfFileReader(inputFile)
    
		extracted_text = ''
		for page_num in range(int(pgnostart) - 1, int(pgnoend)):
			page = pdf.getPage(page_num)
			page_text = page.extractText()
			extracted_text += page_text
		
		inputText = extracted_text
		#print(inputText)

		# readpdf_obj = Extractpdf(inputFile, pgno)	
		# inputText = readpdf_obj.read_content()

		if testType == "objective":
			# qg = QuestionGenerator()
			# res = qg.generate(inputText,num_questions=int(noOfQues), answer_style='multiple_choice')
			# question_list = [(d['question']) for d in res]
			# answer_list = [(d['answer']) for d in res]
			# testgenerate = zip(question_list, answer_list)
			# return render_template('generatedtestdata_obj.html', cresults = testgenerate)

			objective_generator = ObjectiveTest(inputText,noOfQues)
			question_list, answer_list = objective_generator.generate_test()
			testgenerate = zip(question_list, answer_list)
			return render_template('generatedtestdata_obj.html', cresults = testgenerate)
		elif testType == "subjective":
			qg = QuestionGenerator()
			res = qg.generate(inputText,num_questions=int(noOfQues), answer_style='sentences')
			question_list = [(d['question']) for d in res]
			answer_list = [(d['answer']) for d in res]
			testgenerate = zip(question_list, answer_list)
			return render_template('generatedtestdata_sub.html', cresults = testgenerate)

			# subjective_generator = SubjectiveTest(inputText,noOfQues)
			# question_list, answer_list, bloom_list = subjective_generator.generate_test()
			# testgenerate = zip(question_list, answer_list, bloom_list)
			# return render_template('generatedtestdata_sub.html', cresults = testgenerate)
		# elif testType == "subjective":
		# 	subjective_generator = SubjectiveTest(inputText,noOfQues)
		# 	question_list, answer_list, bloom_list = subjective_generator.generate_test()
		# 	testgenerate = zip(question_list, answer_list, bloom_list)
		# 	return render_template('generatedtestdata_sub.html', cresults = testgenerate)
		else:
			flash('Error Ocuured!')
			return redirect(url_for('/'))
		

@app.route('/test_generate', methods=["POST"])
def test_generate():
	if request.method == "POST":
		inputText = request.form["itext"]
		testType = request.form["test_type"]
		noOfQues = request.form["noq"]
		print(inputText)
		if testType == "objective":
			objective_generator = ObjectiveTest(inputText,noOfQues)
			question_list, answer_list = objective_generator.generate_test()
			print(question_list)
			testgenerate = zip(question_list, answer_list)
			
			return render_template('generatedtestdata_obj.html', cresults = testgenerate)
			
		elif testType == "subjective":
			subjective_generator = SubjectiveTest(inputText,noOfQues)
			question_list, answer_list, bloom_list = subjective_generator.generate_test()
			testgenerate = zip(question_list, answer_list, bloom_list)
			return render_template('generatedtestdata_sub.html', cresults = testgenerate)
		else:
			flash('Error Ocuured!')
			return redirect(url_for('/'))
		

@app.route('/vid', methods=["POST"])
def vid():
	return render_template('vid.html')


@app.route('/vid_file_generate', methods=["GET","POST"])
def vid_file_generate():
	if request.method == "POST":
		#inputFile = request.files["filename"]
		file = request.files['filename']
		testType = request.form["test_type"]
		noOfQues = request.form["noq"]
		print('################################################')
		print(file)

		file = request.files['filename']
        # if user does not select file, browser also
        # submit an empty part without filename
		if file.filename == '':
			return 'No selected file'
		if file:
			# filename = secure_filename(file.filename)
			# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# # process the video file
			# input_video = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			# clip = VideoFileClip(input_video)

			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# Extract the audio from the video
			clip = VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			audio_filename = os.path.splitext(filename)[0] + '.mp3'
			audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
			clip.audio.write_audiofile(audio_filepath)
		
			model = whisper.load_model("tiny")
			result = model.transcribe(audio_filepath)
			res = (result["text"])
			#print(res)

			if testType == 'multiple_choice':
				objective_generator = ObjectiveTest(res,noOfQues)
				question_list, answer_list = objective_generator.generate_test()
				testgenerate = zip(question_list, answer_list)
				return render_template('generatedtestdata_obj.html', cresults = testgenerate)

			elif testType == 'sentences':
				qg = QuestionGenerator()
				res = qg.generate(res,num_questions=int(noOfQues), answer_style=testType)
				#print(res)
				question_list = [(d['question']) for d in res]
				answer_list = [(d['answer']) for d in res]
				#print(question_list)
				#print(answer_list)
				testgenerate = zip(question_list, answer_list)
				return render_template('vid_data.html', cresults = testgenerate)
		else:
			return 'Invalid file type. Please upload an MP4 file.'

		# if inputFile.filename is not None and inputFile.filename.endswith('.mp4'):
		# 	# process the MP4 file
		# 	clip = VideoFileClip(inputFile)
		
		# 	model = whisper.load_model("tiny")
		# 	result = model.transcribe(clip)
		# 	res = (result["text"])
		# 	print(res)

		# 	qg = QuestionGenerator()
		# 	res = qg.generate(res,num_questions=noOfQues, answer_style=testType)
		# 	#print(res)
		# 	question_list = [(d['question']) for d in res]
		# 	answer_list = [(d['answer']) for d in res]
		# 	print(question_list)
		# 	print(answer_list)
		# 	testgenerate = zip(question_list, answer_list)
		# 	return render_template('vid_data.html', cresults = testgenerate)
		# else:
			return 'Invalid file type. Please upload an MP4 file.'

		
		

if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 5001, debug=True)