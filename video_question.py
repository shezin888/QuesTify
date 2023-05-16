import whisper
from transformers import logging
logging.set_verbosity_warning()
from transformers import pipeline
from questiongenerator import QuestionGenerator


################## MP4 to MP3 conversion ################
# # Load the mp4 file
# video = VideoFileClip("/home/shezin/Desktop/question_generator/sample5.mp4")
# # Extract audio from video
# video.audio.write_audiofile("sample10.mp3")

################# Text Extraction #######################
model = whisper.load_model("tiny")
result = model.transcribe("/home/shezin/Desktop/question_generator/sample_videos/What is pervasive computing .mp4")
res = (result["text"])
print(res)

qg = QuestionGenerator()
res = qg.generate(res,num_questions=5, answer_style='sentences')
print(res)
question_list = [(d['question']) for d in res]
answer_list = [(d['answer']) for d in res]
print(question_list)
print(answer_list)
# from summarizer import Summarizer     
# model = Summarizer()
# print(model(res))

# summarizer = pipeline('summarization')
# s = summarizer(res, max_length=130, min_length=30, do_sample=False)
# print('SUMMARY \n')
# print(s)


