 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a//dev/null b/My-web-app/app.py
index 0000000000000000000000000000000000000000..8c1470df792a48659057314b98bfd0c5cb367094 100644
--- a//dev/null
+++ b/My-web-app/app.py
@@ -0,0 +1,66 @@
+import os
+import base64
+from flask import Flask, render_template, request
+import openai
+import requests
+
+app = Flask(__name__)
+
+
+def generate_story(animals: str, story_type: str, character_name: str) -> str:
+    """Use OpenAI to generate a short children's story."""
+    openai.api_key = os.getenv("OPENAI_API_KEY")
+    prompt = (
+        "Write a short children's story in the style of Sandra Boynton. "
+        f"The story type is {story_type}. "
+        f"It should mention these animals: {animals}. "
+        f"The main character is named {character_name}."
+    )
+    response = openai.ChatCompletion.create(
+        model="gpt-3.5-turbo",
+        messages=[{"role": "user", "content": prompt}],
+    )
+    return response.choices[0].message.content.strip()
+
+
+def synthesize_voice(text: str, voice_path: str) -> str:
+    """Send text and voice sample to the Chatterbox model and return base64 audio."""
+    hf_token = os.getenv("HF_API_TOKEN")
+    headers = {"Authorization": f"Bearer {hf_token}"}
+    url = "https://api-inference.huggingface.co/models/ResembleAI/chatterbox"
+    with open(voice_path, "rb") as f:
+        files = {"file": f}
+        payload = {"inputs": {"text": text}}
+        response = requests.post(url, headers=headers, data=payload, files=files)
+    response.raise_for_status()
+    return base64.b64encode(response.content).decode("utf-8")
+
+
+@app.route('/', methods=['GET', 'POST'])
+def index():
+    if request.method == 'POST':
+        animals = request.form.get('animals', '')
+        story_type = request.form.get('story_type', '')
+        character_name = request.form.get('character_name', '')
+        voice_file = request.files.get('voice_sample')
+
+        story = generate_story(animals, story_type, character_name)
+        audio_b64 = None
+
+        if voice_file and voice_file.filename:
+            tmp_path = os.path.join('/tmp', voice_file.filename)
+            voice_file.save(tmp_path)
+            try:
+                audio_b64 = synthesize_voice(story, tmp_path)
+            except Exception as e:
+                print(f"Voice synthesis failed: {e}")
+            finally:
+                os.remove(tmp_path)
+
+        return render_template('result.html', story=story, audio_data=audio_b64)
+
+    return render_template('index.html')
+
+
+if __name__ == '__main__':
+    app.run(debug=True)
 
EOF
)
