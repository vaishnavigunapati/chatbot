# 🎤 AI Voice Assistant using Whisper + Groq

This is a simple and powerful **voice-based assistant** built using:

- **Whisper** for real-time speech-to-text
- **Groq (LLaMA3)** for intelligent conversation
- **pyttsx3** for text-to-speech
- **Gradio** for a clean and friendly interface

> Just click a button, speak your question, and hear the answer — like magic! 🧠✨

---

## 📦 Features

✅ Real-time voice input using your microphone  
✅ Transcribes your voice using OpenAI's Whisper model  
✅ Sends your question to **Groq's LLaMA3 model** and gets a smart reply  
✅ Reads the answer back using **text-to-speech**  
✅ Click **"Exit"** or say _"exit"_ to stop the assistant  
✅ Click **"Restart Assistant"** to start a new session  
✅ Logged conversations saved in `transcript_log.txt` for future review  

---

## 🧰 Tech Stack

| Component        | Tool/Library       |
|------------------|--------------------|
| Speech-to-Text   | `whisper`          |
| Voice Recording  | `sounddevice`      |
| Text-to-Speech   | `pyttsx3`          |
| AI Chat Model    | `Groq API (LLaMA3)`|
| UI Frontend      | `gradio`           |
| Backend Language | `Python`           |

---

## 🚀 How to Run

1. **Clone this repo**  
   ```bash
   git clone https://github.com/yourusername/voice-assistant-groq.git
   cd voice-assistant-groq
