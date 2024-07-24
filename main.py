import streamlit as st
import requests
import json
from PIL import Image
import pytesseract

st.title("GrAIder")
st.header("Teacher's Section")

question_paper = st.text_area("Enter Question Paper", height=200, key="question_paper")
answer_key = st.text_area("Enter Answer Key", height=200, key="answer_key")
marking_scheme_text = st.text_area("Enter Marking Scheme (space-separated integers)", height=200, key="marking_scheme")
st.header("Student's Section")

student_answers = st.text_area("Enter Student's Answers", height=200, key="student_answers")
uploaded_student_answers = st.file_uploader("Upload Student's Answers (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], key="upload_student_answers")

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

if uploaded_student_answers is not None:
    student_answers = extract_text_from_image(uploaded_student_answers)
    st.text_area("Student's Answers", student_answers, key="display_student_answers", height=200)
def evaluate_answer(question_paper, answer_key, student_answers, marking_scheme):
    url = "https://api.aimlapi.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer e59ad51957a04dd388f68bdcca421c0b"
    }
    prompt = f"""
    Here is the question paper: {question_paper}
    Here is the answer key: {answer_key}
    Here is the marking scheme: {marking_scheme}
    Here is the student's answer sheet: {student_answers}
    Evaluate the student's answers based on the marking scheme. Provide feedback and mark each answer according to the marking scheme.
    """
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a teacher grading an exam."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result['choices'][0]['message']['content']

if st.button("Evaluate"):
    if question_paper and answer_key and student_answers and marking_scheme_text:
        marking_scheme = marking_scheme_text.split()
        marking_scheme = [int(mark) for mark in marking_scheme]
        if len(question_paper.split('\n')) == len(answer_key.split('\n')) == len(student_answers.split('\n')) == len(marking_scheme):
            evaluation = evaluate_answer(question_paper, answer_key, student_answers, marking_scheme)
            st.header("Evaluation:")
            st.write(evaluation)
        else:
            st.error("The number of questions, answers, student responses, and marking scheme entries must match.")
    else:
        st.error("Please make sure all fields are filled out correctly.")