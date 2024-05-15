import streamlit as st
import assemblyai as aai
import openai

def transcribe_audio(audio_file, assemblyai_api_key):
    # Set up AssemblyAI API key
    aai.settings.api_key = assemblyai_api_key
    
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(audio_file, config)
    
    # Initialize timestamp with the start time of the first utterance in minutes
    current_time = transcript.utterances[0].start / 60000  # Convert start time to minutes
    
    # Generate transcript with timestamps in minutes
    transcript_with_timestamps = ""
    current_speaker = None
    for utterance in transcript.utterances:
        # Check if the speaker has changed
        if utterance.speaker != current_speaker:
            # Start a new line for the new speaker
            transcript_with_timestamps += "\n"
            current_speaker = utterance.speaker
        
        # Calculate duration of the current utterance in minutes
        duration_minutes = (utterance.end - utterance.start) / 60000  # Convert duration to minutes
        # Format timestamp as MM:SS
        minutes = int(current_time)
        seconds = int((current_time - minutes) * 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        # Append timestamp and text to transcript
        transcript_with_timestamps += f"[{timestamp}] Speaker {utterance.speaker}: {utterance.text}\n"
        # Update current time
        current_time += duration_minutes
    
    return transcript_with_timestamps

def main():
    st.title("Audio Transcription and Q&A App")
    st.write("Upload your MP3 audio file and ask a question. The app will transcribe the audio and answer your question based on the transcript.")

    # Load API keys from config.toml
    config = st.secrets["api_keys"]
    assemblyai_api_key = config["assemblyai"]
    openai_api_key = config["openai"]

    # Initialize session state to store previous questions and answers
    if "qna_history" not in st.session_state:
        st.session_state.qna_history = []

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

            # Store the question and answer in session state
            st.session_state.qna_history.append({"question": question, "answer": response["choices"][0]["message"]["content"]})

            # Display the response
            st.subheader("Answer:")
            st.write(response["choices"][0]["message"]["content"])

    # Display previous questions and answers
    st.subheader("Previous Q&A:")
    for item in st.session_state.qna_history:
        st.write(f"Question: {item['question']}")
        st.write(f"Answer: {item['answer']}")
        st.write("---")

if __name__ == "__main__":
    main()
