import streamlit as st
from anthropic import Anthropic

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
    
    try:
        # Inizializza il client Anthropic usando Streamlit secrets
        client = Anthropic(api_key=st.secrets["anthropic_api_key"])
        
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
                    
                    # Aggiorna la cronologia
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    st.session_state.chat_history.append((user_message, response))
            else:
                st.warning("Inserisci un messaggio prima di inviare.")
        
        # Mostra la cronologia delle conversazioni
        if 'chat_history' in st.session_state and st.session_state.chat_history:
            st.markdown("### Cronologia conversazioni")
            for i, (msg, resp) in enumerate(st.session_state.chat_history):
                with st.expander(f"Conversazione {i+1}"):
                    st.markdown("**Tu:**")
                    st.markdown(msg)
                    st.markdown("**Claude:**")
                    st.markdown(resp)
    
    except Exception as e:
        st.error(f"Errore: assicurati di aver configurato correttamente la chiave API nelle Streamlit secrets. Dettaglio: {str(e)}")

if __name__ == "__main__":
    main()