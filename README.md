# Audio Transcription and Q&A App

This Streamlit web application allows users to upload an MP3 audio file, transcribe the audio, and ask questions based on the transcript. The app utilizes AssemblyAI for audio transcription and OpenAI's GPT-3.5 model for answering questions.

## Usage

1. **Upload MP3 Audio File**: Users can upload their MP3 audio file using the file uploader.

2. **Transcription**: The uploaded audio file is transcribed using AssemblyAI. The transcript, along with speaker timestamps, is displayed.

3. **Ask a Question**: Users can enter a question related to the audio content.

4. **Ask**: Clicking the "Ask" button will prompt the app to use the question and transcript as input to OpenAI's GPT-3.5 model. The model generates an answer based on the provided input.

5. **View Previous Q&A**: After asking multiple questions, users can view their previous questions and the corresponding answers.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/marchmello1/Audio-text-QnA
