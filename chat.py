import streamlit as st
from gepetto import Robot_bistro
import requests
import json

# Liste des étapes
options = ["Etape 1", "Etape 2", "Etape 3"]

# Initialisation de l'étape courante dans session_state si elle n'existe pas
if "current_step" not in st.session_state:
    st.session_state["current_step"] = "Etape 1"

# Ajout d'un flag pour éviter le rechargement constant
if "has_moved_to_step_2" not in st.session_state:
    st.session_state["has_moved_to_step_2"] = False

# Affichage des étapes avec st.pills
selection = st.pills("Les étapes :", options, selection_mode="single", default=st.session_state["current_step"])

# Si l'utilisateur a choisi une autre étape, on met à jour l'état
if selection != st.session_state["current_step"]:
    st.session_state["current_step"] = selection


if st.session_state["current_step"] == "Etape 1":
    # Fonction pour ajouter un message et générer une réponse avec contexte
    def addtext():
        user_input = st.session_state["prompt"]  # Récupère le message utilisateur
        if user_input:
            # Ajoute le message utilisateur à l'historique
            st.session_state.messages.append({"role": "user", "text": user_input})

            # Stockage temporaire des réponses utilisateur (tous les messages de type 'user')
            st.session_state["history"] = []
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.session_state["history"].append(message["text"])

            # Crée un contexte pour le chatbot en concaténant les anciens messages
            context = "\n".join([msg["text"] for msg in st.session_state.messages])

            # Obtenir la réponse du bot en lui donnant le contexte
            response_bot = st.session_state["robot"].talk(context)

            # Ajoute la réponse du bot à l'historique
            st.session_state.messages.append({"role": "assistant", "text": response_bot})


    # Initialisation du chatbot
    if "robot" not in st.session_state:
        st.session_state["robot"] = Robot_bistro()
        st.session_state["robot"].preprompt("robot_chat.txt")

    # Initialisation de l'historique des messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Affiche le message de bienvenue
    st.chat_message("assistant").write(st.session_state["robot"].get_welcome())

    # Affiche les messages précédents dans l'ordre chronologique
    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["text"])

    # Champ de saisie du chat
    st.chat_input("Say something", key="prompt", on_submit=addtext)


elif st.session_state["current_step"] == "Etape 2":
    url_mage = "https://mage-ai-portfolio.up.railway.app/api/pipeline_schedules/1/pipeline_runs/fc5054b950ec4285b6952126db31e054"
    st.write("Vous êtes maintenant à l'étape 2.")
    st.write("Informations analysées :", st.session_state["extracted_info"])
    payload =  {
        "pipeline_run": {
            "variables": {
                "chat_bot": st.session_state["extracted_info"],
            }
        }
    }

    # Envoi de la requête POST
    response = requests.post(url_mage, data=json.dumps(payload))

    # Affichage de la réponse
    if response.status_code == 200:
        st.write("✅ Pipeline déclenché avec succès !")
    else:
        st.write(f"❌ Erreur : {response.status_code}, {response.text}")


# Vérification de la présence du message spécifique
if any("Très bien. Tout est bon, je lance la recherche !" in msg["text"] for msg in st.session_state.messages) and not st.session_state["has_moved_to_step_2"]:

    # Création de Robot_hist pour extraire les informations
    st.session_state["robot_hist"] = Robot_bistro()

    st.session_state["robot_hist"].preprompt("robot_hist.txt")

    history = [f'{dico["role"]}:{dico["text"]}' for dico in st.session_state.messages]
    st.session_state["robot_hist"].talk(history)

    # Stockage des informations extraites
    st.session_state["extracted_info"] = st.session_state["robot_hist"].talk(history)

    # Passage à l'étape 2 automatiquement
    st.session_state["current_step"] = "Etape 2"

    # Marque que l'étape 2 a été atteinte pour éviter la boucle infinie
    st.session_state["has_moved_to_step_2"] = True

    # 🚀 Force le rechargement de la page pour afficher directement l'Étape 2
    st.rerun()
