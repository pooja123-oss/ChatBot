import streamlit as st
import google.generativeai as genai


def configure_generative_model(api_key):
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error configuring AI model: {e}")
        return None


def generate_language_response(generative_model, user_query):
    try:
        context = """
        You are a language learning assistant. Help users with:
        - Grammar explanations
        - Vocabulary suggestions
        - Sentence translations
        - Pronunciation guidance
        - Language learning tips
        Provide clear, simple, and accurate explanations.
        """

        prompt = f"{context}\n\nUser: {user_query}\nBot:"
        response = generative_model.generate_content(prompt)
        return response.text if response else "Sorry, I couldn't understand your request."
    except Exception as e:
        return f"Error generating response: {e}"


def language_learning_chatbot(generative_model):
    st.title("🗣 Language Learning Chatbot")
    st.write("Ask me anything about learning a new language! 📚")

   
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    
    for message in st.session_state.conversation:
        role, content = message["role"], message["content"]
        color = "#1e90ff" if role == "User" else "#333333"
        text_color = "#ffffff" if role == "User" else "#f8f8f8"

        st.markdown(
            f"<div style='background-color: {color}; color: {text_color}; padding: 10px; "
            f"border-radius: 10px; margin: 5px 0;'>"
            f"<strong>{role}:</strong> {content}</div>", 
            unsafe_allow_html=True
        )

    
    user_query = st.text_input("Your Question:", placeholder="Ask about grammar, vocabulary, or translation...")

    if user_query:
       
        st.session_state.conversation.append({"role": "User", "content": user_query})

        
        with st.spinner("Thinking..."):
            response_text = generate_language_response(generative_model, user_query)
            st.session_state.conversation.append({"role": "Bot", "content": response_text})

            
            st.markdown(
                f"<div style='background-color: #333333; color: #f8f8f8; padding: 10px; "
                f"border-radius: 10px;'>"
                f"<strong>Bot:</strong> {response_text}</div>", 
                unsafe_allow_html=True
            )


def main():
    API_KEY = "AIzaSyA1dZgrt8EpCJ7fvM0KPMsCSFgt829cyRA" 
    if not API_KEY:
        st.error("API key not found.")
        return
    
    generative_model = configure_generative_model(API_KEY)
    if generative_model is None:
        return

    language_learning_chatbot(generative_model)

if __name__ == "__main__":
    main()
