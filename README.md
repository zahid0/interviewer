# Job Interview Preparation Workflow

## Prerequisites

- A valid API key from [Groq Console](https://console.groq.com).
- Python>=3.10.
- Git installed on your machine.

## Setup

1. **Clone the Repository:**
   Clone this repository to your local machine by running the following command in your terminal:

   ```bash
   git clone https://github.com/zahid0/interviewer.git
   ```

2. **Navigate to the Repository:**
   Change your current working directory to the cloned repository:

   ```bash
   cd interviewer
   ```

3. **Environment Variables:**
   Add your API key to the environment variables by running the following command in your terminal:

   ```bash
   export GROQ_API_KEY=your-api-key
   ```

   Replace `your-api-key` with your actual API key obtained from Groq Console.

4. **Set Up and Activate Virtual Environment:**
   Create a virtual environment and activate it using the following commands in your terminal:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On MacOS/Linux
   ```

5. **Install Python Dependencies:**
   Once the virtual environment is activated, install the required Python packages by running the following command in your terminal:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

To run the Job Interview Preparation Workflow, execute the following command in your terminal:

```bash
python main.py
```

After the script is running successfully, open your web browser and navigate to [http://127.0.0.1:7860](http://127.0.0.1:7860) to access the application.

