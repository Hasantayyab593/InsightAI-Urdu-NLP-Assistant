
# import streamlit as st
# # from chatbot import get_response
# # from database import initialize_database, save_message

# #NEW CODE ADDED BY HASAN
# # from database import (
# #     get_response,
# #     initialize_database,
# #     save_message,
# # )


# #hasan add new code 31-10-2026

# import streamlit as st

# # Import AI response generation from chatbot.py
# from chatbot import get_response

# # Import database functions from database.py
# from database import initialize_database, save_message 

# st.set_page_config(
#     page_title="InsightAI — Urdu NLP Assistant",
#     page_icon="💬",
#     layout="centered",
# )

# st.title("💬 InsightAI")
# st.subheader("Urdu NLP Assistant")
# st.write(
#     "اردو یا Roman Urdu میں بات کریں۔ "
#     "Chat in Urdu or Roman Urdu."
# )

# # Step 1: Connect to PostgreSQL and initialize the table
# try:
#     initialize_database()
# except Exception:
#     st.error(
#         "Could not connect to PostgreSQL. "
#         "Please check your database server and .env settings."
#     )
#     st.stop()

# # Step 2: Initialize the chat session
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {
#             "role": "assistant",
#             "content": (
#                 "السلام علیکم! میں InsightAI ہوں۔ "
#                 "آپ کی کیا مدد کر سکتا ہوں؟"
#             ),
#         }
#     ]

# # Step 3: Display previous messages in the current session
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Step 4: Accept and process a new message
# if prompt := st.chat_input(
#     "اپنا پیغام لکھیں... / Type a message"
# ):
#     # Display and save the user's message
#     st.session_state.messages.append(
#         {"role": "user", "content": prompt}
#     )

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     try:
#         save_message("user", prompt)
#     except Exception:
#         st.error("Could not save your message to PostgreSQL.")
#         st.stop()

#     # Generate the chatbot's response
#     response = get_response(prompt)

#     # Display and save the assistant's response
#     st.session_state.messages.append(
#         {"role": "assistant", "content": response}
#     )

#     with st.chat_message("assistant"):
#         st.markdown(response)

#     try:
#         save_message("assistant", response)
#     except Exception:
#         st.error(
#             "The response was generated, but could not be "
#             "saved to PostgreSQL."
#         )





import streamlit as st

# Import AI response generation from chatbot.py
from chatbot import get_response

# Import PostgreSQL functions from database.py
from database import initialize_database, save_message


st.set_page_config(
    page_title="InsightAI — Urdu NLP Assistant",
    page_icon="💬",
    layout="centered",
)

st.title("💬 InsightAI")
st.subheader("Urdu NLP Assistant")

st.write(
    "اردو یا Roman Urdu میں بات کریں۔ "
    "Chat in Urdu or Roman Urdu."
)

# Step 1: Connect to PostgreSQL and initialize the table
try:
    initialize_database()
except Exception as error:
    st.error(
        "Could not connect to PostgreSQL. "
        "Please check your database server and .env settings."
    )
    st.error(str(error))
    st.stop()

# Step 2: Initialize the chat session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "السلام علیکم! میں InsightAI ہوں۔ "
                "آپ کی کیا مدد کر سکتا ہوں؟"
            ),
        }
    ]

# Step 3: Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Step 4: Accept and process a new message
if prompt := st.chat_input(
    "اپنا پیغام لکھیں... / Type a message"
):

    # Display and save the user's message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        save_message("user", prompt)
    except Exception:
        st.error("Could not save your message to PostgreSQL.")
        st.stop()

    # Generate AI response using Qwen through Ollama
    with st.chat_message("assistant"):
        with st.spinner("InsightAI is thinking..."):
            response = get_response(prompt)

        st.markdown(response)

    # Store the assistant response in session state
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    # Save assistant response in PostgreSQL
    try:
        save_message("assistant", response)
    except Exception:
        st.error(
            "The response was generated, but could not be "
            "saved to PostgreSQL."
        )
