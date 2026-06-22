# import streamlit as st

# import speech_recognition as sr
# from gtts import gTTS
# from google import genai
# import os
# from dotenv import load_dotenv
# import tempfile


# load_dotenv()

# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# # helper function for STT (speech to text)

# def record_audio(language='en-IN'):
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening... Pleas Speak Now.")
        
#         r.adjust_for_ambient_noise(source)
#         audio= r.listen(source)
#         try:
#             st.success("Audio Captured Transcribing...")
#             text = r.recognize_google(audio,language=language)
#             return text
#         except sr.UnknownValueError:
#             st.error("Sorry, I couldn't clearly understand the audio.")
#             return None
#         except sr.RequestError:
#             st.error("Speech Recognition service is currently unavailable.")
#             return None
    
    
#     # helper to send text to llm (text to gemini)
    
# def get_gemini_response(text):
#     response = client.models.generate_content(
#         model='gemini-2.5-flash',
#         contents=text
#     )
#     return response.text
    
#     # helper for text to voice  TTS
    
# def text_to_speech(text,lang='en'):
#     tts = gTTS(text=text,lang=lang)
#     # using tempfile to prevent saving dozen of old audio files locally 
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp :
#         tts.save(fp.name) 
#         return fp.name
# st.title("Multilingual AI VOice Assistant")
# st.markdown("powered by streamlit, gemini-pro, and gTTS")
    
# # layout control
    
    
    
# col1,col2 = st.columns(2)
# with col1:
#     input_lang = st.selectbox("Input Language (Speak in):", ["en-IN", "hi-IN"])
# with col2:
#     output_lang = st.selectbox("Output Language (Reply in):", ["en", "hi", "gu", "mr"])
    
# if st.button("Start Recodging"):
#     user_text = record_audio(language=input_lang)
#     if user_text:
#         st.write(f"**You said:** {user_text}")
#         # get here ai response
#         with st.spinner("Gemini is thinking..."):
#             ai_response = get_gemini_response(user_text)
#             st.write(f"**AI Response:** {ai_response}")
#         with st.spinner("Generating audio..."):
#             audio_path = text_to_speech(ai_response,lang=output_lang)
                
#             with open(audio_path, 'rb') as audio_file:
#                 audio_bytes = audio_file.read()
#                 st.audio(audio_bytes, format='audio/mp3')
                    

# with multi lingual support
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from google import genai
import os
from dotenv import load_dotenv
import tempfile

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 1. helper function for STT (speech to text)
def record_audio(language='en-IN'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please Speak Now.")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            st.success("Audio Captured Transcribing...")
            text = r.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't clearly understand the audio.")
            return None
        except sr.RequestError:
            st.error("Speech Recognition service is currently unavailable.")
            return None
    
# 2. helper to send text to llm (text to gemini)
def get_gemini_response(text, target_language):
    prompt = f"The user says: '{text}'. Please respond to them directly, but you MUST write your entire response strictly in {target_language} language."
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

# 3. helper for text to voice  TTS
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name) 
        return fp.name

# 4. STREAMLIT UI LOGIC
st.title("🎙️ Multilingual AI Voice Assistant")
st.markdown("Powered by Streamlit, Gemini 2.5, and gTTS")

# Language Mapping Dictionary (Updated with Telugu)
lang_mapping = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "mr": "Marathi",
    "te": "Telugu"  # <-- ADDED TELUGU
}

col1, col2 = st.columns(2)
with col1:
    # Added "te-IN" for Telugu voice recognition input
    input_lang = st.selectbox("Input Language (Speak in):", ["en-IN", "hi-IN", "te-IN"])
with col2:
    # Added "te" for Telugu audio output translation
    output_lang = st.selectbox("Output Language (Reply in):", ["en", "hi", "gu", "mr", "te"])

if st.button("Start Recording"):
    user_text = record_audio(language=input_lang)
    
    if user_text:
        st.write(f"**You said:** {user_text}")
        
        target_lang_name = lang_mapping.get(output_lang, "English")
        
        with st.spinner("Gemini is thinking..."):
            ai_response = get_gemini_response(user_text, target_lang_name)
            st.write(f"**AI Response:** {ai_response}")
            
        with st.spinner("Generating audio..."):
            audio_path = text_to_speech(ai_response, lang=output_lang)
            
            with open(audio_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')