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
