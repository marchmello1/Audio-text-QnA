import streamlit as st
import assemblyai as aai
from together import Together

def transcribe_audio(audio_file, assemblyai_api_key):
    aai.settings.api_key = assemblyai_api_key
    
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(audio_file, config)
    
    current_time = transcript.utterances[0].start / 60000  
    
    transcript_with_timestamps = ""
    current_speaker = None
    for utterance in transcript.utterances:
        if utterance.speaker != current_speaker:
            transcript_with_timestamps += "\n"
            current_speaker = utterance.speaker
        
        duration_minutes = (utterance.end - utterance.start) / 60000  
        minutes = int(current_time)
        seconds = int((current_time - minutes) * 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        transcript_with_timestamps += f"[{timestamp}] Speaker {utterance.speaker}: {utterance.text}\n"
        current_time += duration_minutes
    
    return transcript_with_timestamps

def main():
    st.title("Audio Transcription and Q&A App")
    st.write("Upload your MP3 audio file and ask a question. The app will transcribe the audio and answer your question based on the transcript.")

    config = st.secrets["api_keys"]
    assemblyai_api_key = config["assemblyai"]
    together_api_key =  config["together_api_key"]

    if "qna_history" not in st.session_state:
        st.session_state.qna_history = []

    audio_file = st.file_uploader("Upload MP3 audio file", type=["mp3"])

    if audio_file:
        st.audio(audio_file, format='audio/mp3')

        transcript_text = transcribe_audio(audio_file, assemblyai_api_key)

        st.subheader("Transcript:")
        st.write(transcript_text)

        question = st.text_input("Enter your question:")

        if st.button("Ask"):
            system_message = """ 
            You are not an AI language model.
            Answer only from prompt.
            You will be provided a transcript answer from it."""
            messages = [{"role": "system", "content": system_message}]

            prompt = f"{question}\n{transcript_text}"
            messages.append({"role": "user", "content": prompt})

            together_client = Together(api_key=together_api_key)
            try:
                response = together_client.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=messages,
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"Error: {e}"
                print(f"Error occurred with Together.io: {e}")

            st.session_state.qna_history.append({"question": question, "answer": answer})

            st.subheader("Answer:")
            st.write(answer)

            if len(st.session_state.qna_history) >= 2:
                st.subheader("Previous Q&A:")
                for item in st.session_state.qna_history:
                    st.write(f"Question: {item['question']}")
                    st.write(f"Answer: {item['answer']}")
                    st.write("---")

if __name__ == "__main__":
    main()
