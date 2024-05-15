import streamlit as st
import assemblyai as aai
import openai
from datetime import datetime, timedelta

def transcribe_audio(audio_file, assemblyai_api_key):
    aai.settings.api_key = assemblyai_api_key

    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(audio_file, config)
    
    transcript_text = ""
    for utterance in transcript.utterances:
        # Extract speaker, text, start and end times
        speaker = utterance.speaker
        text = utterance.text
        start_time = utterance.start / 1000  # Convert milliseconds to seconds
        end_time = utterance.end / 1000

        # Convert seconds to minutes and format timestamp string (customize format)
        start_minutes = start_time // 60  # Integer division for minutes
        start_seconds = start_time % 60  # Remainder for seconds within the minute
        end_minutes = end_time // 60
        end_seconds = end_time % 60
        timestamp = f"[{start_minutes:02d}:{start_seconds:02d} - {end_minutes:02d}:{end_seconds:02d}]"

        # Prepend timestamp and combine
        transcript_text += f"{timestamp} Speaker {speaker}: {text}\n"

    return transcript_text


def main():
    st.title("Audio Transcription and Q&A App")
    st.write("Upload your MP3 audio file and ask a question. The app will transcribe the audio and answer your question based on the transcript.")

    # Load API keys from config.toml
    config = st.secrets["api_keys"]
    assemblyai_api_key = config["assemblyai"]
    openai_api_key = config["openai"]

    # Upload audio file
    audio_file = st.file_uploader("Upload MP3 audio file", type=["mp3"])

    if audio_file:
        # Display audio player
        st.audio(audio_file, format='audio/mp3')

        # Transcribe the audio file
        transcript_text = transcribe_audio(audio_file, assemblyai_api_key)

        # Display transcript
        st.subheader("Transcript:")
        st.write(transcript_text)

        # Ask the user for a question
        question = st.text_input("Enter your question:")

        if st.button("Ask"):
            # Define system message
            system_message = """ 
            You are not an AI language model.
            Answer only from prompt.
            You will be provided a transcript answer from it."""

            messages = [{"role": "system", "content": system_message}]

            # Add user question and transcript as prompt
            prompt = f"{question}\n{transcript_text}"
            messages.append({"role": "user", "content": prompt})

            # Call OpenAI's ChatGPT model
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
                api_key=openai_api_key
            )

            # Display the response
            st.subheader("Answer:")
            st.write(response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    main()
