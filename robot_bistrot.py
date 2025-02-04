import streamlit as st
from streamlit_option_menu import option_menu
import json
from checker import Checker


checker = Checker()

# Vérifier si l'utilisateur est connecté avant de configurer la mise en page
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    st.set_page_config(page_title="Robot Bistrot", layout="wide")
else:
    st.set_page_config(page_title="Robot Bistrot", layout="centered")

def main():
    # Initialiser les variables de session
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = None
        st.session_state["current_page"] = "Landing"  # Page par défaut au démarrage

    # Afficher la page actuelle
    if st.session_state["authenticated"]:
        if st.session_state["current_page"] == "Accueil":
            show_home_page()
        elif st.session_state["current_page"] == "Compte":
            show_account_page()
    else:
        if st.session_state["current_page"] == "Landing":
            show_landing_page()
        elif st.session_state["current_page"] == "Signup":
            show_signup_form()
        elif st.session_state["current_page"] == "Login":
            show_login_form()

def show_landing_page():
    st.title("Think'n'Find")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Créer un compte", use_container_width=True):
            st.session_state["current_page"] = "Signup"
    with col2:
        if st.button("Se connecter", use_container_width=True):
            st.session_state["current_page"] = "Login"

def show_signup_form():
    st.title("Créer un compte")
    # Formulaire de création de compte
    with st.form("signup_form"):
        name = st.text_input("Nom")
        lastname = st.text_input("Prénom")
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Valider")

    if submit:
        if checker.is_email_known(email):
            st.warning("Un compte avec cet email existe déjà !")
        else:
            if checker.validate_user(email, password, name, lastname):
                checker.add_user(email, password, name, lastname)
                st.success("Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                st.session_state["current_page"] = "Login"

def show_login_form():
    st.title("Se connecter")
    # Formulaire de connexion
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Valider")

        if submit:
            # Vérifier les informations d'identification
            if checker.is_authentificate(email, password):
                st.session_state["authenticated"] = True
                st.session_state["current_user"] = email
                st.session_state["current_page"] = "Accueil"
            else:
                st.error("Email ou mot de passe incorrect !")

def show_home_page():
    # Menu de navigation horizontal
    selected_option = option_menu(
    None,
    options=["Recherche", "historique", "Compte", "Déconnexion"],
    orientation="horizontal",
    default_index=0,
)

    if selected_option == "Recherche":
        st.title("Bienvenue sur Think'n'Find")
        st.image("logo.png")
    elif selected_option == "historique":
        st.title("Historique")
    elif selected_option == "Compte":
        st.session_state["current_page"] = "Compte"
    elif selected_option == "Déconnexion":
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = None
        st.session_state["current_page"] = "Landing"

def show_account_page():
    email = st.session_state["current_user"]
    user_data = email
    st.title("Mon compte")
    st.write(f"**Nom**: {user_data['nom']}")
    st.write(f"**Prénom**: {user_data['prenom']}")
    st.write(f"**Email**: {email}")

    if st.button("Retour à l'accueil"):
        st.session_state["current_page"] = "Accueil"

if __name__ == "__main__":
    main()