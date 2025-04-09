import re  # regular expression
import streamlit as st

def check_password_strength(password):
    score = 0
    messages = []
    
    # Length Check
    if len(password) >= 8:
        messages.append("✔️ Length of password is correct.")
        score += 1
    else:
        messages.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        messages.append("✔️ Both uppercase and lowercase letters present in password.")
        score += 1
    else:
        messages.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        messages.append("✔️ Number present in password.")
        score += 1
    else:
        messages.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        messages.append("✔️ Special character present in password.")
        score += 1
    else:
        messages.append("❌ Include at least one special character (!@#$%^&*).")

    # Strength Rating
    if score == 4:
        messages.append("✅ Strong Password!")
    elif score == 3:
        messages.append("⚠️ Moderate Password - Consider adding more security features.")
    else:
        messages.append("❌ Weak Password - Improve it using the suggestions above.")

    return messages


st.title("Password Strength Checker 🔒")

st.subheader("Look at the strength of your password. 👀")

password = st.text_input("Enter your password:", placeholder="Write here", type="password")

if password:
    messages = check_password_strength(password)
    for message in messages:
        if message.startswith("✔️"):
            st.success(message)
        if message.startswith("❌"):
            st.error(message)
        elif message.startswith("⚠️"):
            st.warning(message)
        elif message.startswith("✅"):
            st.success(message)
            