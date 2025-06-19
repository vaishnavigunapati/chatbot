import whisper
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import requests
import numpy as np
import gradio as gr
import datetime
import threading

# Load Whisper model
model = whisper.load_model("medium")

# Groq API Key
GROQ_API_KEY = "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"

# Text-to-Speech engine
engine = pyttsx3.init()

# State tracking
assistant_active = True  # Global flag to control "exit"

def record_audio(duration=5, fs=44100):
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    max_val = np.max(np.abs(audio))
    if max_val < 0.01:
        return None, None, "⚠️ Too quiet! Please speak louder or check mic."
    return audio, fs, None

def chat_with_groq(prompt):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}]
        }
        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Groq Error: {e}"

# The main assistant function
def assistant():
    global assistant_active

    if not assistant_active:
        return "❌ Assistant has been stopped. Reload to restart."

    audio, fs, warning = record_audio()
    if warning:
        return warning

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        write(tmpfile.name, fs, audio)
        try:
            result = model.transcribe(tmpfile.name)
            query = result["text"].strip()
        except Exception as e:
            return f"❌ Whisper Error: {e}"

    if not query or len(query.split()) < 2:
        return f"❌ Couldn't hear clearly. Whisper heard: `{query}`. Try again."

    # Exit check
    if query.lower() in ["exit", "quit", "stop"]:
        assistant_active = False
        return "👋 Assistant stopped. No more responses."

    # Log
    with open("transcript_log.txt", "a") as f:
        f.write(f"[{datetime.datetime.now()}] You said: {query}\n")

    response = chat_with_groq(query)
    engine.say(response)
    threading.Thread(target=engine.runAndWait).start()

    return f"📝 Transcription: `{query}`\n\n🤖 Bot replied:\n{response}"

# Restart assistant manually
def reset_assistant():
    global assistant_active
    assistant_active = True
    return "🔄 Assistant reactivated. You can speak again."

# Gradio UI
with gr.Blocks(css="""
    body { background: #eef2f7; }
    .gradio-container { font-family: 'Segoe UI', sans-serif; }
    .gr-button {
        font-size: 18px;
        padding: 12px 28px;
        border-radius: 8px;
    }
""") as demo:
    gr.Markdown("## 🎤 AI Voice Assistant (Multi-turn)")
    gr.Markdown("Click **Speak** to talk. Say 'exit' anytime to stop the assistant.")

    output = gr.Textbox(label="Conversation Output", lines=8)

    with gr.Row():
        speak_btn = gr.Button("🎙️ Speak")
        reset_btn = gr.Button("🔁 Restart Assistant")
    
    speak_btn.click(fn=assistant, outputs=output)
    reset_btn.click(fn=reset_assistant, outputs=output)

demo.launch()
