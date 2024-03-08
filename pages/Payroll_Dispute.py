from PIL import Image
import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read API key from environment variable
app_key = os.getenv("GOOGLE_APP_KEY")

st.set_page_config(
    page_title="Payroll Disputes",
    page_icon="🔥",
    menu_items={
        'About': "by Juan"
    }
)

st.title('Payroll Disputes')
st.caption('Ask your Payroll Disputes Here, Including the Process')

st.session_state.app_key = app_key

try:
    genai.configure(api_key = st.session_state.app_key)
    model = genai.GenerativeModel('gemini-pro-vision')
except AttributeError as e:
    st.warning(e)


def show_message(prompt, image, loading_str):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(loading_str)
        full_response = ""

        data = """
        Use this are reference: 
        # Payroll Dispute Process
        The new process involves hierarchy to ensure that disputes are validated by the employee's immediate supervisor before it gets sent to payroll for processing.
        ## Filing a Payroll Dispute
        Step 1. Log in to Megaform (https://megaform.connextglobal.com)
        Step 2. In the frontpage, click on the Payroll Dispute option in the menu bar
        Step 3. Click + Add Dispute Form to open the request
        Step 4. Fill up the form with the following details:Employee Details:
        - Employee ID - auto-populated
        - Employee Name - Auto-populated

        Dispute Details:- Pay-out Month, Date and Year - Select the date of the payout in question

        - Cut-off Month and Period

        - Team Leader and Manager - Selected Team Leader and Manager will get a notification email for them to be notified and need to validate the dispute.

        - Client - select the client you are assigned with

        - Dispute Reason - select the closes option related to your dispute

        - Dispute - select the closes option that best describes your dispute

        - Dispute details - Important to fill up the details the supervisor, manager and payroll to properly assess the dispute

        Step 5. click SAVE and CLOSE button to submit the dispute.

        Upon submission, team leader and manager identified in the request will get an email notification to inform them to review and validate. Until validated, the request will not be forwarded to payroll. Once the supervisor or manager validates and approves the dispute, payroll will be notified of the dispute and be able to update the request with appropriate disposition.

        ## Validating and Approving the Dispute - Leaders Only

        Validating payroll dispute can only be done if you are the one tagged as either the employee's Team Leader or Manager. Either a Team Lead and Manager can validate and approve the dispute. Until the dispute is validated by either a Team Leader or a Manager, it will not be queued to the payroll team. It is important that the team leader or the manager validates the dispute by providing more information or evidences to support the dispute otherwise, it should be declined or put on hold until pertinent information is added to support the dispute.

        For security and confidentiality reasons, leaders will see all the disputes where they are tagged as the team leader or manager. 

        Follow the steps below to validate and approve the disputes:

        1. Click on the edit icon to open the dispute

        2. In the Team Leader / Manager Details, change the status accordingly based on gathered information. Ensure to put notes to provide payroll additional information to support the dispute. By adding additional details, it will make it easier for payroll to close the dispute. 

        ## Dispositioning the Dispute - Payroll Team Only

        This section is for payroll use only. This should serve as additional info to all users to have full appreciation of the entire dispute process. 

        Upon validation and approval of either the team leader or manager, Payroll team will be notified via e-mail notification.
        """


        prompt = prompt.replace('\n', '  \n') + data

        try:
            for chunk in model.generate_content([prompt, image], stream = True, safety_settings = SAFETY_SETTTINGS):                   
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "_")
                        word_count = 0
                        random_int = random.randint(5, 10)
        except genai.types.generation_types.BlockedPromptException as e:
            st.exception(e)
        except Exception as e:
            st.exception(e)
        message_placeholder.markdown(full_response)
        st.session_state.history_pic.append({"role": "assistant", "text": full_response})

def clear_state():
    st.session_state.history_pic = []


if "history_pic" not in st.session_state:
    st.session_state.history_pic = []


image = None
if "app_key" in st.session_state:
    uploaded_file = st.file_uploader("choose a pic...", type=["jpg", "png", "jpeg", "gif"], label_visibility='collapsed', on_change = clear_state)
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        width, height = image.size
        resized_img = image.resize((128, int(height/(width/128))), Image.LANCZOS)
        st.image(image)    

if len(st.session_state.history_pic) > 0:
    for item in st.session_state.history_pic:
        with st.chat_message(item["role"]):
            st.markdown(item["text"])

if "app_key" in st.session_state:
    if prompt := st.chat_input("Analyze my pay slip"):
        if image is None:
            st.warning("Please upload an image first", icon="⚠️")
        else:
            prompt = prompt.replace('\n', '  \n')
            with st.chat_message("user"):
                st.markdown(prompt)
                st.session_state.history_pic.append({"role": "user", "text": prompt})
            
            show_message(prompt, resized_img, "Thinking...")