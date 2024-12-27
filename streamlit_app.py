import streamlit as st
from anthropic import Anthropic
import json

def initialize_anthropic():
    """Inizializza il client Anthropic con la chiave API."""
    # Ottieni la chiave API da Streamlit Secrets o input utente
   

        anthropic_api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
anthropic = Anthropic(api_key=anthropic_api_key)
    
    if st.session_state.anthropic_api_key:
        return Anthropic(api_key=st.session_state.anthropic_api_key)
    return None

def send_message_to_claude(client, message, system_prompt=None):
    """Invia un messaggio a Claude e riceve la risposta."""
    try:
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": message
        })

        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=messages
        )
        
        return response.content[0].text
    except Exception as e:
        return f"Errore durante l'invio del messaggio: {str(e)}"

def main():
    st.title("Interfaccia Claude API")
    
    # Inizializza il client Anthropic
    client = initialize_anthropic()
    
    if client:
        # Area per il system prompt (opzionale)
        with st.expander("Impostazioni avanzate"):
            system_prompt = st.text_area(
                "System Prompt (opzionale):",
                help="Inserisci un prompt di sistema per personalizzare il comportamento di Claude"
            )
        
        # Area per il messaggio dell'utente
        user_message = st.text_area("Inserisci il tuo messaggio per Claude:", height=150)
        
        # Pulsante per inviare il messaggio
        if st.button("Invia a Claude"):
            if user_message:
                with st.spinner("Attendi la risposta di Claude..."):
                    response = send_message_to_claude(client, user_message, system_prompt)
                    st.markdown("### Risposta di Claude:")
                    st.markdown(response)
            else:
                st.warning("Inserisci un messaggio prima di inviare.")
        
        # Aggiungi una sezione per la cronologia delle conversazioni
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Mostra la cronologia delle conversazioni
        if st.session_state.chat_history:
            st.markdown("### Cronologia conversazioni")
            for i, (msg, resp) in enumerate(st.session_state.chat_history):
                with st.expander(f"Conversazione {i+1}"):
                    st.markdown("**Tu:**")
                    st.markdown(msg)
                    st.markdown("**Claude:**")
                    st.markdown(resp)
    
    else:
        st.warning("Inserisci una chiave API valida per iniziare.")

if __name__ == "__main__":
    main()