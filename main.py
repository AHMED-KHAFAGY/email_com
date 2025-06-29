from flask import Flask, render_template, request, send_file
import random
import os

app = Flask(__name__)

def generate_emails(name, count=15):
    name = name.strip().lower()
    parts = name.split()
    first = parts[0] if len(parts) > 0 else "user"
    last = parts[1] if len(parts) > 1 else ""

    suggestions = set()
    while len(suggestions) < count:
        suggestion_parts = [
            f"{first}{last}",
            f"{first}.{last}" if last else f"{first}.{random.randint(1, 99)}",
            f"{last}.{first}" if last else f"{first}{random.randint(100, 999)}",
            f"{first}_{last}" if last else f"{first}_{random.randint(10, 99)}",
            f"{first}{random.randint(10, 99)}",
            f"{first}.{random.randint(100, 999)}",
            f"{first}{last}{random.randint(1, 999)}" if last else f"{first}{random.randint(1000, 9999)}",
            f"{first[0]}{last}{random.randint(1, 99)}" if last else f"{first[0]}_{random.randint(100, 999)}",
            f"{first}{last[0]}{random.randint(1, 999)}" if last else f"{first}{random.randint(1000, 1999)}",
            f"{first}_dev",
            f"{first}.code",
            f"{first}.ai",
            f"{first}123",
            f"{first}.{random.choice(['pro', 'x', 'official'])}",
            f"{first}{last}_2025" if last else f"{first}_2025"
        ]
        suggestion = random.choice(suggestion_parts)
        suggestions.add(suggestion + "@gmail.com")

    return list(suggestions)

@app.route("/", methods=["GET", "POST"])
def index():
    emails = []
    name = ""
    if request.method == "POST":
        name = request.form.get("name", "")
        if name.strip():
            emails = generate_emails(name)

            # حفظ في ملف مؤقت للتنزيل
            with open("emails.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(emails))

    return render_template("index.html", emails=emails, name=name)

@app.route("/download")
def download_file():
    path = "emails.txt"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "❌ لا يوجد ملف للتحميل"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)


