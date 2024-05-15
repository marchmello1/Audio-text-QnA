# Audio Transcription and Q&A App

This is a Streamlit web application that allows users to upload an MP3 audio file, transcribe the audio, and ask questions based on the transcript. The app utilizes AssemblyAI for audio transcription and OpenAI's ChatGPT model for answering user questions.

## Features

- Upload MP3 audio files for transcription.
- Display the transcript with timestamps.
- Ask questions based on the transcript.
- Get answers from OpenAI's ChatGPT model.
- View previous questions and answers.

## Setup

1. Clone this repository.
2. Install the required dependencies by running:
    ```
    pip install -r requirements.txt
    ```
3. Obtain API keys for AssemblyAI and OpenAI.
4. Create a `secrets.toml` file in the root directory with the following structure:
    ```toml
    [api_keys]
    assemblyai = "YOUR_ASSEMBLYAI_API_KEY"
    openai = "YOUR_OPENAI_API_KEY"
    ```
    Replace `"YOUR_ASSEMBLYAI_API_KEY"` and `"YOUR_OPENAI_API_KEY"` with your actual API keys.

## Usage

1. Run the Streamlit app by executing the following command:
    ```
    streamlit run app.py
    ```
2. Once the app is running, you can upload an MP3 audio file using the file uploader.
3. After uploading, the audio player and transcript will be displayed.
4. Enter your question in the text input field and click "Ask".
5. The app will provide an answer based on the transcript.
6. Previous questions and answers will be displayed below the current session.

## Dependencies

- Streamlit
- AssemblyAI
- OpenAI
