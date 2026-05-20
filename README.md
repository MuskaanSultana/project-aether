# 🚀 Project Aether: The Self-Evolving Digital Twin

> [!NOTE]
> **Project Status: ⚠️ Work in Progress**
> Project Aether is an actively developing private AI voice assistant and digital twin built exactly Like JARVIS . It is designed to run locally, automate operating system actions, learn from demonstrations, and manage user preferences and memories recursively.

---

## 🌟 Overview
Project Aether acts as a persistent, autonomous assistant that controls the host OS, learns from user workflows, and manages the user's digital life. With high-performance voice processing (Whisper/Kokoro) and a dual cognitive model (Gemini 2.0 + local Ollama fallback), Aether acts as a natural extension of the developer.

---

## 🛠 Tech Stack
| Component | Tech | Purpose |
| :--- | :--- | :--- |
| **Primary Cognition** | **Google Gemini 2.0 Flash** | Fast, high-context reasoning and tool calling. |
| **Offline Fallback** | **Ollama (`phi4-mini`)** | Local, low-latency backup when API quota/internet is offline. |
| **Voice Speech-to-Text** | **faster-whisper (small)** | Fast, local voice command transcription. |
| **Voice Text-to-Speech** | **Kokoro TTS (ONNX)** | Ultra-realistic, natural voice generation. |
| **Neural Memory** | **mem0** | Automatic extract-and-store fact management. |
| **Long-Term Memory** | **Obsidian Vault** | Central knowledge base for preferences, skills, and logs. |
| **RAG & Semantic Cache** | **ChromaDB / txtai** | Smart caching to bypass LLM latency on repeated commands. |
| **Automation & OS** | **Playwright / PyAutoGUI** | Browser control and local OS controls (Spotify, volume, apps). |

---

## 📦 What's Finished Until Now
* **Dual LLM Pipeline with Key Rotation**: Integrated Gemini 2.0 Flash with automatic fallback to local Ollama (`phi4-mini`) and API key rotation mechanism to handle rate limits.
* **Local Whisper STT & Kokoro TTS**: Fully offline voice pipeline enabling low-latency transcription and highly realistic speech responses.
* **Persistent Memory & RAG**: Linked `mem0` memory management for automatic facts extraction and Obsidian Vault acting as the Long-Term Memory (LTM). Added semantic caching via `txtai` to deliver sub-100ms response times for cached commands.
* **OS Commands and Navigation**: Capable of launching apps, playing songs on YouTube/Spotify, and learning new search skills on the fly.
* **Zero-Latency Keyword Routing**: Hardcoded routes for commands like toggling Work Mode (engineering mentor prompt), clearing memory cache, reloading system identity, and enabling/disabling voice mode.
* **Voice Stop Command & Memory Syncing**: Reliable voice interruption using "stop" or "done" keywords, which automatically trigger `memory_cli.py` to synchronize memories across different local environments.
* **Action Replay ("Do it again")**: Built-in `last_action` tracking to remember and re-execute the previous task automatically.
* **Instant Greetings**: High-speed interceptor for greetings/basic inputs to respond instantly without hitting the LLM.

---

## 🗺 Roadmap & Next Steps (What Needs to be Done)
### 1. Dedicated Python GUI
* [ ] Build a sleek, modern visual interface (using CustomTkinter or a web-based Streamlit local dashboard) to replace the terminal console.
### 2. Browser "Eyes"
* [ ] Integrate Playwright or Selenium to automate complex web workflows.
* [ ] Build navigators to automatically log into Carleton Brightspace, monitor grades, and fetch updates.
### 3. Teach Mode
* [ ] Implement a recording agent that records browser steps to automate new sites and actions through demonstration.
### 4. Proactive Engagement
* [ ] Enable Aether to start suggesting actions based on routines, day of the week, or calendar deadlines (e.g. prompt to open files for an upcoming Carleton assignment).
### 5. OS Integration Expansion
* [ ] Connect Windows Task Scheduler to run Aether on system boot.
* [ ] Deeper system integration with Spotify API and volume controls.

---

## 📥 Installation

### 1. Clone the repository
```bash
git clone https://github.com/kartik-mem0/Project-Aether.git
cd Project-Aether
```

### 2. Install dependencies
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
```

### 3. Configuration
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Fill in the environment variables:
```ini
# Free Gemini key at aistudio.google.com
GEMINI_API_KEY_1=your_first_gemini_key
GEMINI_API_KEY_2=your_second_gemini_key
GEMINI_API_KEY_3=your_third_gemini_key

# Obsidian Vault location
VAULT_BASE=E:\Aether_Vault\Aether_Vault\_Aether

# Ollama environment (optional)
OLLAMA_HOST=http://localhost:11434
OLLAMA_INTEL_GPU=1
OLLAMA_VULKAN=1
```

---

## ▶️ Usage

To start Project Aether in voice loop mode:
```bash
python main.py
```
* Say **"Voice Mode On"** / **"Voice Mode Off"** to toggle speaking.
* Say **"Stop"** or **"Done"** to exit the voice loop and sync memory to all local workspaces.
* Say **"Switch to Work Mode"** to change Aether's personality to a senior Software Engineering mentor.

To interact with or synchronize memories via CLI:
```bash
python memory_cli.py sync
```

---

## 📁 Project Structure

```
Project-Aether/
├── brain/
│   ├── memory_manager.py     # Handles mem0 facts and Obsidian interactions
│   ├── rag_engine.py         # Handles semantic caching and txtai RAG indexing
│   ├── semantic_matcher.py   # Finds matching skills/URLs for apps and music
│   ├── embeddings.py         # Vector embeddings configuration
│   └── summarizer.py         # Text summarizing helper
├── tools/
│   └── pc_controls.py        # System control for launching apps and routing URLs
├── stt/
│   └── whisper_stt.py        # Whisper Speech-to-Text configuration
├── tts/
│   ├── kokoro_tts.py         # Kokoro Text-to-Speech configuration
│   ├── kokoro-v1.0.onnx      # Kokoro ONNX model file
│   └── voices-v1.0.bin       # Kokoro voice library file
├── main.py                   # Aether Executive Agent core entrypoint
├── memory_cli.py             # CLI utility for memory and RAG synchronization
├── requirements.txt          # Python packages list
├── CONTEXT.md                # Personal developer context file
└── PROJECT_AETHER_BLUEPRINT.md # Architectural roadmap blueprints
```

---

## 🤝 Contributing

We want to make Project Aether as powerful, self-evolving, and robust as possible! Contributions from the community are highly welcome. 

If you want to contribute, please:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

**High priority areas where we need help:**
* Sleek CustomTkinter UI widgets.
* Playwright scripts for Carleton Brightspace automation.
* Custom speech triggers and gesture recognition integrations.
* Performance optimizations for running heavy voice models on local CPUs/GPUs.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
