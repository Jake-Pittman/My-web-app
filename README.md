 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a//dev/null b/My-web-app/README.md
index 0000000000000000000000000000000000000000..efeee873fd26f224f19acd05aec7c2202f62d50e 100644
--- a//dev/null
+++ b/My-web-app/README.md
@@ -0,0 +1,20 @@
+# My-web-app
+
+This simple Flask application generates a short children's story in the style of **Sandra Boynton** using OpenAI's API. It can optionally clone the user's voice via the [Chatterbox](https://huggingface.co/spaces/ResembleAI/Chatterbox) model hosted on Hugging Face to read the story aloud.
+
+## Setup
+
+1. Install dependencies:
+   ```bash
+   pip install -r requirements.txt
+   ```
+2. Provide API keys via environment variables:
+   - `OPENAI_API_KEY` – your OpenAI key.
+   - `HF_API_TOKEN` – Hugging Face token with access to the Chatterbox space.
+
+3. Run the app:
+   ```bash
+   python app.py
+   ```
+
+Open your browser at `http://localhost:5000` and fill in the form to generate a story. If you upload a short voice sample, the app attempts to clone it for reading the story aloud.
 
EOF
)
