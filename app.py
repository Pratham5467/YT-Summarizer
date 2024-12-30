import streamlit as st
from download import download_audio_from_url
from summarize import summarize_transcript
from transcribe import transcribe_audio


st.set_page_config(page_title="YT Summariser",page_icon="📜",layout="wide")

st.title("YT Summariser",anchor=False)
st.header("Summarise any YouTube video in seconds!",anchor=False)

st.divider()
url=st.text_input("Enter the URL",value="")

st.divider()
if url:
    with st.status("Processing...",state="running",expanded=True)as status:
        st.write("Downloading audio file from Youtube...")
        audio_file,length=download_audio_from_url(url)
        st.write("Transcribing audio file...")
        transcript=transcribe_audio(audio_file)
        st.write("Summarizing transcript...")
        with open("transcript.txt","w")as f:
            f.write(transcript)
        summary=summarize_transcript("transcript.txt")
        status.update(label="Finished",state="complete")
        
        st.divider()
        st.audio(audio_file,format='audio/mp3')
        
        st.subheader("Summary:",anchor=False)
        st.write(summary)