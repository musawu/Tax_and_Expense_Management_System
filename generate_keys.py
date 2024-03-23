import pickle
from pathlib import Path  # Import Path explicitly
import streamlit_authenticator as stauth

names = ["Lavin", "Taher", "Syntiche", "Elvis"]
usernames = ["Llavin", "Ttaher", "Ssyntiche", "Eelvis"]
passwords = ["lavin123", "taher123", "syntiche123", "elvis123"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"  # Create a Path object
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
