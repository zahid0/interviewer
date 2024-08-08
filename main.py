import gradio as gr
from litellm import completion, transcription

# Define your model and parameters
TRANSCRIPTION_MODEL = "groq/whisper-large-v3"
COMPLETION_MODEL = "groq/llama-3.1-8b-instant"  # Adjust as needed
MAX_TOKENS = 2048


def generate_with_llm(prompt, system_prompt):
    response = completion(
        model=COMPLETION_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content


def generate_requirement_prompt(job_title, years_experience):
    prompt = f"Compose a detailed and comprehensive list of technical expertise requirements for the position of {job_title}, considering a total experience of {years_experience} years. Ensure the list includes specific skills, technologies, and frameworks that are essential for the role."
    system_prompt = f"You are a seasoned engineering professional with 20 years of experience. As a part of the hiring process for the {job_title} position, your role is to draft detailed requirements that accurately assess a candidate's technical competence."
    return {
        requirement_user_prompt: prompt,
        requirement_system_prompt: system_prompt,
        requirements_prompt_fields: gr.Row(visible=True),
    }


def generate_job_requirements(user_prompt, system_prompt):
    return {
        requirements_output: generate_with_llm(user_prompt, system_prompt),
        question_generation_fields: gr.Column(visible=True),
    }


def generate_interview_questions(requirements):
    system_prompt = f"You are an experienced interviewer. As a part of the hiring process for the {job_title} position, your role is to conduct an interview that effectively tests a candidate's technical competence. Ask detailed questions, challenge assumptions, and consider edge cases to evaluate their skills accurately."
    prompt = f"Given the following job requirements, please select one of the listed expertises and create a tailored interview question to assess the candidate's proficiency in that area:\n\n{requirements}"
    return {
        question: generate_with_llm(prompt, system_prompt),
        answer_recording_fields: gr.Column(visible=True),
    }


def transcribe_audio(audio):
    with open(audio, "rb") as f:
        response = transcription(
            model=TRANSCRIPTION_MODEL, file=f, response_format="text"
        )
    return {answer: response["text"], feedback_fields: gr.Column(visible=True)}


def generate_feedback(question, answer):
    system_prompt = """
    You are an expert in providing constructive feedback. Your role is to evaluate a candidate's answer to a technical interview question, and provide critical feedback along with actionable suggestions for improvement.
    """

    prompt = f"""
    Here is an interview question:
    {question}
    
    The candidate provided the following answer:
    {answer}
    
    Please provide detailed feedback on the answer, highlighting any strengths and weaknesses. Additionally, suggest specific actions the candidate could take to improve their answer in future interviews.
    """
    return {
        feedback: generate_with_llm(prompt, system_prompt),
        ideal_answer_fields: gr.Column(visible=True),
    }


def generate_ideal_answer(question, job_title, years_experience):
    system_prompt = f"You are a seasoned {job_title}. With {years_experience} years of experience in the field, you are familiar with the skills and qualities that are essential for success."
    prompt = f"""
    Here is an interview question:
    {question}
    
    Please provide a detailed and well-structured response that demonstrates your understanding, experience, and skills relevant to the position."""
    return generate_with_llm(prompt, system_prompt)


# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Job Interview Preparation Workflow")

    with gr.Row():
        years_experience = gr.Number(label="Years of Experience", value=5)
        job_title = gr.Textbox(label="Job Title", value="Software Engineer")

    requirement_prompt_button = gr.Button("Start")

    with gr.Row():
        requirement_system_prompt = gr.Textbox(
            label="System prompt to generate requirements"
        )
        requirement_user_prompt = gr.Textbox(
            label="User prompt to generate requirements"
        )

    with gr.Column(visible=False) as requirements_prompt_fields:
        submit_button1 = gr.Button("Generate Requirement")

        requirements_output = gr.Markdown(label="Job Requirements")

    requirement_prompt_button.click(
        generate_requirement_prompt,
        inputs=[job_title, years_experience],
        outputs=[
            requirement_user_prompt,
            requirement_system_prompt,
            requirements_prompt_fields,
        ],
    )

    with gr.Column(visible=False) as question_generation_fields:
        generate_question_button = gr.Button("Generate Interview Question")
        question = gr.Markdown(label="Question")

    submit_button1.click(
        generate_job_requirements,
        inputs=[requirement_user_prompt, requirement_system_prompt],
        outputs=[requirements_output, question_generation_fields],
    )

    with gr.Column(visible=False) as answer_recording_fields:
        with gr.Row():
            audio_input = (
                gr.Audio(
                    label="Record Answer",
                    sources=["microphone"],
                    type="filepath",
                    format="mp3",
                ),
            )
            transcribe_button = gr.Button("Transcribe the Answer")
        answer = gr.Textbox(label="Transcription", interactive=False)

    generate_question_button.click(
        generate_interview_questions,
        inputs=[requirements_output],
        outputs=[question, answer_recording_fields],
    )

    with gr.Column(visible=False) as feedback_fields:
        submit_button2 = gr.Button("Generate Feedback")
        feedback = gr.Markdown(label="Feedback")

    transcribe_button.click(
        transcribe_audio,
        inputs=audio_input,
        outputs=[answer, feedback_fields],
    )

    with gr.Column(visible=False) as ideal_answer_fields:
        ideal_answer_button = gr.Button("Generate Ideal Answer")
        ideal_answer = gr.Markdown(label="Ideal Answer")

    submit_button2.click(
        generate_feedback,
        inputs=[question, answer],
        outputs=[feedback, ideal_answer_fields],
    )

    ideal_answer_button.click(
        generate_ideal_answer,
        inputs=[question, job_title, years_experience],
        outputs=[ideal_answer],
    )

demo.launch()
