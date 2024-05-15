import streamlit as st
import assemblyai as aai
import openai

def transcribe_audio(audio_file, assemblyai_api_key):
    # Set up AssemblyAI API key
    aai.settings.api_key = assemblyai_api_key
    
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(audio_file, config)
    transcript_text = "\n".join([f"Speaker {utterance.speaker}: {utterance.text}\n" for utterance in transcript.utterances])
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
