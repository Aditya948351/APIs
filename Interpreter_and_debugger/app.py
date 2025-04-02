from flask import Flask, render_template_string, request, jsonify
import subprocess
import sys

app = Flask(__name__)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Web Compiler</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/mode/python/python.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/codemirror.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; background: #111; color: #2196F3; padding: 15px; text-align: center; }
.container { max-width: 100%; padding: 10px; }
h2 { font-size: 22px; margin-bottom: 10px; color: #2196F3; }
textarea, pre { width: 100%; max-width: 100%; }
button { width: 100%; padding: 12px; margin: 5px 0; font-size: 16px; background: #2196F3; color: white; border: none; border-radius: 5px; cursor: pointer; }
button:hover { background: #1976D2; }
pre { background: #222; color: #2196F3; padding: 10px; border-radius: 5px; text-align: left; overflow-x: auto; max-height: 200px; }
#infoBox { display: none; background: #333; color: white; padding: 10px; border-radius: 5px; margin-top: 10px; }

    </style>
</head>
<body>
    <div class="container">
        <h2>Python Web Compiler</h2>
        <textarea id="code" placeholder="Write your Python code here..."></textarea>
        <button onclick="runCode()">▶ Run the Code</button>
        <button onclick="installPackage()">📦 Install Package</button>
        <button onclick="toggleInfo()">ℹ️ Info</button>
        <div id="infoBox">
            <p>💡 Type the code in the textfield and press 'Run Code' to run the code.</p>
            <p>⚠️ "Reality is often disappointing" - Some Advanced codes including various modules will terminate early.</p>
            <p>📌 To install a package, just type the module name in the Alert box.</p>
        </div>
        <h3>Output:</h3>
        <pre id="output"></pre>
    </div>
    <script>
        let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
            mode: "python", lineNumbers: true, viewportMargin: Infinity
        });
        function runCode() {
            let code = editor.getValue();
            fetch("/run", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code })
            })
            .then(res => res.json())
            .then(data => document.getElementById("output").innerText = data.output)
            .catch(err => console.error(err));
        }
        function installPackage() {
            let package = prompt("Enter package name to install:");
            if (package) {
                fetch("/install", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ package })
                })
                .then(res => res.json())
                .then(data => document.getElementById("output").innerHTML += "\\n" + data.output)
                .catch(err => console.error(err));
            }
        }
        function toggleInfo() {
            let infoBox = document.getElementById("infoBox");
            infoBox.style.display = infoBox.style.display === "none" ? "block" : "none";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run', methods=['POST'])
def run_python():
    try:
        code = request.json.get('code')
        result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, timeout=5)
        return jsonify({"output": result.stdout + result.stderr})
    except Exception as e:
        return jsonify({"output": str(e)})


@app.route('/install', methods=['POST'])
def install_package():
    try:
        package = request.json.get('package')
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], capture_output=True, text=True)
        return jsonify({"output": result.stdout + result.stderr})
    except Exception as e:
        return jsonify({"output": str(e)})
        
if __name__ == '__main__':
    app.run(debug=True)
