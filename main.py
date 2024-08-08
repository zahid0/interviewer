import gradio as gr
from litellm import completion, transcription
import io

# Define your model and parameters
TRANSCRIPTION_MODEL = "groq/whisper-large-v3"
COMPLETION_MODEL = "groq/llama-3.1-8b-instant"  # Adjust as needed
SYSTEM_PROMPT = "You are an assistant that provides feedback on interview answers."
MAX_TOKENS = 512  # Adjust as needed

def generate_job_requirements(job_title, years_experience):
    prompt = f"Generate job technical expertise requirements for the role of {job_title} for total experience of {years_experience}"
    response = completion(
        model=COMPLETION_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content

def generate_interview_questions(requirements):
    prompt = f"Randomly select one of the expertise listed in the below job requirements and generate one interview question:\n\n{requirements}"
    response = completion(
        model=COMPLETION_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content

def transcribe_audio(audio):
    # Use litellm for transcription
    with open(audio, 'rb') as f:
        response = transcription(model=TRANSCRIPTION_MODEL, file=f, response_format="text")
    return response['text']

def generate_feedback(question, answer):
    # Use litellm for completion to generate feedback
    prompt = f"Here is an interview question:\n{question}\n\n\nProvide feedback on the following answer: {answer}"
    response = completion(
        model=COMPLETION_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def workflow(years_experience, job_title, audio):
    requirements = generate_job_requirements(job_title, years_experience)
    questions = generate_interview_questions(requirements)
    
    # Transcribe the audio answer
    answer = transcribe_audio(audio)
    
    # Generate feedback on the answer
    feedback = generate_feedback(answer)
    
    return requirements, questions, answer, feedback

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Job Interview Preparation Workflow")
    
    with gr.Row():
        years_experience = gr.Number(label="Years of Experience", value=3)
        job_title = gr.Textbox(label="Job Title", value="Software Engineer")
    
    submit_button1 = gr.Button("Submit")

    requirements_output = gr.Textbox(label="Job Requirements", interactive=False)

    submit_button1.click(
        generate_job_requirements,
        inputs=[years_experience, job_title],
        outputs=[requirements_output]
    )

    
    generate_question_button = gr.Button("Generate Question")
    question = gr.Textbox(label="Question", interactive=False)

    generate_question_button.click(
        generate_interview_questions,
        inputs=[requirements_output],
        outputs=[question]
    )
    
    audio_input=gr.Audio(sources=["microphone"], type="filepath"),
    # 
    submit_button = gr.Button("Submit")
    answer = gr.Textbox(label="Answer", interactive=False)

    # questions_output = gr.Textbox(label="Interview Questions", interactive=False)
    # answer_output = gr.Textbox(label="Transcribed Answer", interactive=False)
    # feedback_output = gr.Textbox(label="Feedback", interactive=False)

    submit_button.click(
        transcribe_audio,
        inputs=audio_input,
        outputs=[answer],
    )

    submit_button2 = gr.Button("Generate Feedback")
    feedback = gr.Textbox(label="Feedback", interactive=False)

    submit_button2.click(
        generate_feedback,
        inputs=[question, answer],
        outputs=[feedback],
    )

demo.launch()
