"""
Full project health check — tests every component without needing mic/speakers.
"""
import sys
import os
import traceback
from pathlib import Path

os.chdir(Path(__file__).parent)

PASS = []
FAIL = []

def test(name, fn):
    try:
        result = fn()
        PASS.append(f"  PASS  {name}" + (f" — {result}" if result else ""))
    except Exception as e:
        FAIL.append(f"  FAIL  {name} — {e}")

# ── 1. Syntax / import checks ─────────────────────────────────────────────────
print("\n[1] IMPORTS")

def check_dotenv():
    from dotenv import load_dotenv
    load_dotenv()
    return "loaded"
test("python-dotenv", check_dotenv)

def check_ollama():
    import ollama
    client = ollama.Client()
    models = client.list()
    names = [m.model for m in models.models]
    return f"models: {names}"
test("ollama", check_ollama)

def check_mem0():
    import mem0
    return mem0.__version__
test("mem0", check_mem0)

def check_chromadb():
    import chromadb
    return chromadb.__version__
test("chromadb", check_chromadb)

def check_whisper():
    from faster_whisper import WhisperModel
    return "importable"
test("faster-whisper", check_whisper)

def check_kokoro():
    from kokoro_onnx import Kokoro
    return "importable"
test("kokoro-onnx", check_kokoro)

def check_sounddevice():
    import sounddevice
    return f"devices: {len(sounddevice.query_devices())}"
test("sounddevice", check_sounddevice)

def check_ddg():
    from duckduckgo_search import DDGS
    return "importable"
test("duckduckgo-search", check_ddg)

def check_gemini():
    import google.generativeai
    return "importable"
test("google-generativeai", check_gemini)

def check_txtai():
    from txtai.embeddings import Embeddings
    return "importable"
test("txtai", check_txtai)

def check_sentence_transformers():
    from sentence_transformers import SentenceTransformer
    return "importable"
test("sentence-transformers", check_sentence_transformers)

# ── 2. Project modules ────────────────────────────────────────────────────────
print("\n[2] PROJECT MODULES")

def check_memory_manager():
    from brain.memory_manager import MemoryManager, VAULT_BASE
    mm = MemoryManager()
    return f"VAULT_BASE={VAULT_BASE[:30]}..."
test("brain.memory_manager", check_memory_manager)

def check_embeddings():
    from brain.embeddings import get_model
    m = get_model()
    return f"model loaded: {m is not None}"
test("brain.embeddings", check_embeddings)

def check_semantic_matcher():
    from brain.semantic_matcher import find_best_skill
    result = find_best_skill("youtube", {"youtube": "https://youtube.com"})
    return f"match score: {result[2]:.2f}"
test("brain.semantic_matcher", check_semantic_matcher)

def check_rag_engine():
    from brain.rag_engine import _init_indexes
    v, c = _init_indexes()
    return "vault+cache indexes ready"
test("brain.rag_engine", check_rag_engine)

def check_pc_controls():
    from tools.pc_controls import get_disk_space
    info = get_disk_space()
    return info
test("tools.pc_controls", check_pc_controls)

# ── 3. .env config ────────────────────────────────────────────────────────────
print("\n[3] CONFIGURATION")

def check_env():
    from dotenv import load_dotenv
    load_dotenv()
    keys = [os.environ.get(f"GEMINI_API_KEY_{i}","") for i in range(1,4)]
    filled = [k for k in keys if k.strip()]
    vault = os.environ.get("VAULT_BASE","NOT SET")
    return f"{len(filled)}/3 Gemini keys set | VAULT_BASE={'set' if vault != 'NOT SET' else 'MISSING'}"
test(".env", check_env)

def check_context_md():
    p = Path("CONTEXT.md")
    if not p.exists():
        raise FileNotFoundError("CONTEXT.md missing — run: python memory_cli.py sync")
    lines = len(p.read_text(encoding="utf-8").splitlines())
    return f"{lines} lines"
test("CONTEXT.md", check_context_md)

def check_cursorrules():
    p = Path(".cursorrules")
    if not p.exists():
        raise FileNotFoundError(".cursorrules missing")
    return "exists"
test(".cursorrules", check_cursorrules)

# ── 4. Gemini API ─────────────────────────────────────────────────────────────
print("\n[4] GEMINI API")

def check_gemini_api():
    from dotenv import load_dotenv
    load_dotenv()
    keys = [os.environ.get(f"GEMINI_API_KEY_{i}","") for i in range(1,4)]
    filled = [k for k in keys if k.strip()]
    if not filled:
        raise ValueError("No Gemini API keys in .env")
    import google.generativeai as genai
    genai.configure(api_key=filled[0])
    model = genai.GenerativeModel("gemini-2.0-flash")
    resp = model.generate_content("Reply with exactly: OK")
    return f"response: {resp.text.strip()[:20]}"
test("Gemini API call", check_gemini_api)

# ── 5. mem0 memory ────────────────────────────────────────────────────────────
print("\n[5] MEMORY (mem0)")

def check_mem0_search():
    from mem0 import Memory
    from pathlib import Path
    config = {
        "llm": {
            "provider": "ollama",
            "config": {"model": "phi4-mini", "ollama_base_url": "http://localhost:11434", "temperature": 0.1}
        },
        "embedder": {
            "provider": "huggingface",
            "config": {"model": "sentence-transformers/all-MiniLM-L6-v2"}
        },
        "vector_store": {
            "provider": "chroma",
            "config": {"collection_name": "aether_memory", "path": str(Path(".chroma_db"))}
        },
        "history_db_path": str(Path(".mem0_history.db")),
    }
    m = Memory.from_config(config)
    results = m.search("Adithya", filters={"user_id": "adithya"}, limit=3)
    return f"{len(results)} memories found"
test("mem0 search", check_mem0_search)

# ── 6. DuckDuckGo search ──────────────────────────────────────────────────────
print("\n[6] TOOLS")

def check_web_search():
    from duckduckgo_search import DDGS
    results = DDGS().text("Python programming", max_results=1)
    return f"got {len(results)} result(s)"
test("DuckDuckGo search", check_web_search)

def check_youtube_search():
    from tools.pc_controls import get_direct_youtube_link
    url = get_direct_youtube_link("coldplay")
    return f"url: {url[:40] if url else 'None'}..."
test("YouTube link finder", check_youtube_search)

# ── 7. STT model file ─────────────────────────────────────────────────────────
print("\n[7] VOICE PIPELINE")

def check_stt_model():
    import huggingface_hub
    cache = huggingface_hub.constants.HF_HUB_CACHE
    model_dirs = list(Path(cache).glob("models--Systran--faster-whisper-small"))
    if model_dirs:
        return "whisper small cached locally"
    raise FileNotFoundError("Whisper small not cached yet — will download on first voice use")
test("Whisper small model cache", check_stt_model)

def check_kokoro_models():
    onnx = Path("tts/kokoro-v1.0.onnx").exists()
    voices = Path("tts/voices-v1.0.bin").exists()
    if not onnx or not voices:
        missing = []
        if not onnx: missing.append("kokoro-v1.0.onnx")
        if not voices: missing.append("voices-v1.0.bin")
        raise FileNotFoundError(f"Missing: {', '.join(missing)} (not in git, download manually)")
    return "both model files present"
test("Kokoro TTS models", check_kokoro_models)

# ── Results ───────────────────────────────────────────────────────────────────
print("\n" + "="*55)
print(f"RESULTS: {len(PASS)} passed, {len(FAIL)} failed")
print("="*55)

if PASS:
    print("\nPASSED:")
    for p in PASS: print(p)

if FAIL:
    print("\nFAILED:")
    for f in FAIL: print(f)

print()
sys.exit(0 if not FAIL else 1)
