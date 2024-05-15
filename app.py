def main():
    st.title("Audio Transcription and Q&A App")
    st.write("Upload your MP3 audio file and ask a question. The app will transcribe the audio and answer your question based on the transcript.")

    config = st.secrets["api_keys"]
    assemblyai_api_key = config["assemblyai"]
    openai_api_key = config["openai"]

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

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
                api_key=openai_api_key
            )

            st.subheader("Answer:")
            st.write(response["choices"][0]["message"]["content"])

            # Display previous question and answer
            if len(st.session_state.qna_history) >= 1:
                st.subheader("Previous Q&A:")
                previous_qna = st.session_state.qna_history[-1]
                st.write(f"Question: {previous_qna['question']}")
                st.write(f"Answer: {previous_qna['answer']}")
                st.write("---")

            st.session_state.qna_history.append({"question": question, "answer": response["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    main()
