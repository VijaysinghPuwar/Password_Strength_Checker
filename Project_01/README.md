# 🔒 Password Strength Checker

A lightweight Streamlit app to **evaluate password strength** by checking character composition and giving helpful tips.

👉 **Live Demo:** [https://supreme-umbrella-7w9gjrvwpqx3rxww-8501.app.github.dev/](https://supreme-umbrella-7w9gjrvwpqx3rxww-8501.app.github.dev/)

---

## ✨ Features

- Checks for **lowercase**, **uppercase**, **digits**, **spaces**, and **special characters**
- Computes a **strength score (0–5)** and shows a **progress bar**
- Displays a quick **breakdown** of character counts
- Presents **tips** to improve weak passwords
- Runs in the **browser** (perfect for GitHub Codespaces)

---

## 📂 Project Structure

```

Password\_Strength\_Checker/
├── Project\_01/
│   ├── password\_checker.py   # Streamlit app (main entry point)
│   └── README.md             # (optional) project-specific notes
├── requirements.txt          # Dependencies (Streamlit)
└── README.md                 # <— this file

````

---

## 🚀 Getting Started

### 1) Clone & enter the repo
```bash
git clone https://github.com/VijaysinghPuwar/Password_Strength_Checker.git
cd Password_Strength_Checker
````

### 2) Create a virtual environment (recommended)

```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Run the app

```bash
streamlit run Project_01/password_checker.py
```

Open the printed URL (usually `http://localhost:8501`).

---

## 🌐 Run in GitHub Codespaces (and share a public link)

1. Open your repo → **Code** → **Codespaces** → **Create codespace on main**
2. In the codespace terminal:

   ```bash
   pip install -r requirements.txt
   streamlit run Project_01/password_checker.py
   ```
3. Open the **Ports** panel → find port **8501** → set **Visibility** to **Public**.
4. Copy the generated URL (similar to the live demo link above) and share it.

---

## 🧠 Code (for reference)

`Project_01/password_checker.py`:

```python
import string
import streamlit as st

st.set_page_config(page_title="Password Strength Checker", layout="centered")
st.title("🔒 Password Strength Checker")

def analyze(pw: str):
    lower = sum(c in string.ascii_lowercase for c in pw)
    upper = sum(c in string.ascii_uppercase for c in pw)
    digits = sum(c in string.digits for c in pw)
    spaces = pw.count(" ")
    special = len(pw) - lower - upper - digits - spaces
    strength = sum([lower>0, upper>0, digits>0, spaces>0, special>0])
    if strength <= 1: remark = "Very bad — change ASAP."
    elif strength == 2: remark = "Not good — change ASAP."
    elif strength == 3: remark = "Weak — consider improving."
    elif strength == 4: remark = "Good, but can be better."
    else: remark = "Very strong."
    return lower, upper, digits, spaces, special, strength, remark

pw = st.text_input("Enter password", type="password", help="Input is not stored.")
if pw:
    lower, upper, digits, spaces, special, strength, remark = analyze(pw)
    st.progress(strength/5)
    st.write(f"**Score:** {strength}/5  •  {remark}")
    c1,c2,c3 = st.columns(3)
    c1.metric("Lowercase", lower); c2.metric("Uppercase", upper); c3.metric("Digits", digits)
    c1.metric("Spaces", spaces);   c2.metric("Special", special)
    tips = []
    if len(pw) < 12: tips.append("Use at least 12–16 characters.")
    if lower==0: tips.append("Add lowercase letters.")
    if upper==0: tips.append("Add uppercase letters.")
    if digits==0: tips.append("Add numbers.")
    if special==0: tips.append("Add special characters (e.g., !@#$%).")
    if tips:
        st.subheader("How to improve")
        for t in tips: st.write("• " + t)

st.caption("Checks composition only; does not validate against breached-password lists.")
```

---

## 🔍 Detailed Explanation (line-by-line logic)

### Imports & page setup

```python
import string
import streamlit as st
st.set_page_config(page_title="Password Strength Checker", layout="centered")
st.title("🔒 Password Strength Checker")
```

* `string` provides convenient character groups (`ascii_lowercase`, `ascii_uppercase`, `digits`).
* `streamlit` renders a web UI in the browser.
* `set_page_config` and `title` configure the app header/metadata.

### The analyzer function

```python
def analyze(pw: str):
    lower = sum(c in string.ascii_lowercase for c in pw)
    upper = sum(c in string.ascii_uppercase for c in pw)
    digits = sum(c in string.digits for c in pw)
    spaces = pw.count(" ")
    special = len(pw) - lower - upper - digits - spaces
```

* Counts characters by category:

  * `lower`, `upper`, `digits` are straightforward membership checks.
  * `spaces` counts literal spaces (`" "`).
  * `special` is computed as *everything else*: total length minus the other categories.

    > Note: this treats punctuation (e.g., `!@#$`) and non-space symbols as special characters.

```python
    strength = sum([lower>0, upper>0, digits>0, spaces>0, special>0])
```

* **Strength score** is the number of **distinct categories present** (0–5).

  * If a password has at least one lowercase + uppercase + digit + special, that’s already 4/5.
  * Including a space makes it 5/5.

```python
    if strength <= 1: remark = "Very bad — change ASAP."
    elif strength == 2: remark = "Not good — change ASAP."
    elif strength == 3: remark = "Weak — consider improving."
    elif strength == 4: remark = "Good, but can be better."
    else: remark = "Very strong."
```

* Converts numeric score into a human-readable **remark**.

```python
    return lower, upper, digits, spaces, special, strength, remark
```

* Returns raw counts plus the score and the remark for display.

### Input & UI rendering

```python
pw = st.text_input("Enter password", type="password", help="Input is not stored.")
```

* Secure input field (masks characters). Streamlit does *not* persist the value after the session.

```python
if pw:
    lower, upper, digits, spaces, special, strength, remark = analyze(pw)
    st.progress(strength/5)
    st.write(f"**Score:** {strength}/5  •  {remark}")
```

* Only analyze once the user has typed something.
* Shows a **progress bar** (0–1) and the **score/remark**.

```python
    c1,c2,c3 = st.columns(3)
    c1.metric("Lowercase", lower); c2.metric("Uppercase", upper); c3.metric("Digits", digits)
    c1.metric("Spaces", spaces);   c2.metric("Special", special)
```

* Displays **metrics** in columns for a clean dashboard look.

### Tips / guidance

```python
    tips = []
    if len(pw) < 12: tips.append("Use at least 12–16 characters.")
    if lower==0: tips.append("Add lowercase letters.")
    if upper==0: tips.append("Add uppercase letters.")
    if digits==0: tips.append("Add numbers.")
    if special==0: tips.append("Add special characters (e.g., !@#$%).")
```

* Builds a list of **actionable tips** based on what’s missing.

```python
    if tips:
        st.subheader("How to improve")
        for t in tips: st.write("• " + t)
```

* Renders the tips as bullet points.

### Footer note

```python
st.caption("Checks composition only; does not validate against breached-password lists.")
```

* Transparency about scope: this is a **composition check**, not a breach/entropy audit.

---

## 🛡️ Security Considerations

* **Do not** enter **real passwords** in the live demo; use test strings.
* Composition checks can be **misleading** if the password is common (e.g., `Password@123`).
* For production:

  * Add length & entropy thresholds (e.g., ≥ 12–16 chars).
  * Check against breach lists (k-anonymous HIBP API).
  * Enforce modern policies (passphrases, MFA, rate limiting).

---

## 📌 Roadmap

* [ ] Optional **entropy estimate** and length policy
* [ ] **Have I Been Pwned** (k-anon) breach check
* [ ] Unit tests (`pytest`) + GitHub Actions CI
* [ ] Containerized dev setup (`devcontainer.json`)
* [ ] Public cloud deployment (Render/Heroku)

---

## 🧑‍💻 Author

**Vijaysingh Puwar**

* LinkedIn: [https://www.linkedin.com/in/vijaysinghpuwar](https://www.linkedin.com/in/vijaysinghpuwar)
* GitHub:  [https://github.com/VijaysinghPuwar](https://github.com/VijaysinghPuwar)

If this helped, ⭐ **star the repo**!

```

---

If you’d like, I can also add a **badge header** (Python version, Streamlit, Codespaces ready) and a tiny **pytest** file for future CI.
```
