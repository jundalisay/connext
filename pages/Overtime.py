import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS

# Load environment variables from .env file
load_dotenv()

# Get the GOOGLE_API_KEY from the environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

page_icon_path = "logo.png"
if os.path.exists(page_icon_path):
    st.set_page_config(
        page_title="Overtime",
        page_icon="page_icon_path", 
        menu_items={
            'About': ""
        }
    )


st.title("Overtime Section")
st.caption("Ask About Overtime and Rest-Day-Work Here")

try:
    genai.configure(api_key=google_api_key)
except AttributeError as e:
    st.warning("Please Configure Gemini App Key First.")

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()


with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.rerun()

for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)


if prompt := st.chat_input(""):

    data = """
    Use this as referece: 
    ## Setting-Up Rest Day Work and Overtime
    Did you report to work during your rest day to do some work overtime?
    There are times when you need to render a Working Rest Day or even have to work beyond your scheduled rest day shift. As such, necessary applications should be filed to get the premium rate.
    
    Employees who were asked to work during their rest day must file a schedule adjustment for the system to recognize that there is a work scheduled assigned on that day. To do this:
    Step 1: Go to My Stuff
    Step 2: Select Schedule Adjustment
    Step 3: Set Effectivity Date.
    
    If you worked beyond the approved 8-hour rest day work schedule, only then can you file an Overtime in Sprout:
    Step 1: Go to Sprout HR
    Step 2: Go to New Work Schedule
    Step 3: Enter the date and times of the overtime
    Step 4: the checkbox should be ticked, and the padlock should be open on the filing.
    
    Example:
        Regular Working Days: Tuesday to Saturday
        Rest Days: Sunday and Monday
        Rest Day Schedule Adjustment Request: Monday 6:00 AM to 3:00 PM
        Monthly Basic Salary: PHP 22,000.00 (Semi-monthly: PHP 11,000.00)
    Note: There is no need to file overtime if you applied for a RD-work (schedule adjustment) unless there is a work beyond the 8-hour approved schedule (9 hours including break).
    Any work within the approved schedule adjustment will be paid as RD premium.
    Any work beyond the approved schedule will be paid as RD-OT premium.
    This is how a successful Rest Day Work and Rest Day – OT application looks like in employee’s payslip:
    w/ approved RD-work - Monday (6:00 AM – 3:00 PM)
    w/ approved RD-work - Monday (6:00 AM – 3:00 PM)
    w/ approved RD-OT - Monday (3:00 PM – 5:00 PM)
    ## Pre-shift & Post Shift Thresholds
    ### How do Pre-Shift & Post- Shift Thresholds Work?
    Pre-shift and Post-shift thresholds were put in place to prevent logs from getting assigned to the incorrect shift.
    Understanding how they work is more important than it would seem at first, especially when it already applies to filing overtimes and crediting the work hours properly to their respective dates.
    Log ins and log outs must be within the following thresholds on Sprout HR:
    For employees on Normal and Flexi-per-week schedule type:
        Log in/s – must be within 6 hours before the shift start
        Log out/s – must be within 8 hours after the shift end
    Here are some examples:
    1. If your schedule is from 7:00 AM to 4:00 PM
    -Log in must be within 1:00 AM to 7:00 AM
    -Log out must be within 4:00 PM to 12:00 AM.
    2. If your schedule is from 9:00 PM to 6:00 AM
    -Log in must be within 3:00 PM to 9:00 PM
    -Log out must be within 6:00 AM to 2:00 PM.
    3. If your schedule is from 2:00 AM to 11:00 AM
    -Log in must be within 8:00 PM to 2:00 AM
    -Log out must be within 11:00 AM to 7:00 PM
    Note: If you are tagged with Missing Logs for a day but you have logs, make sure to check if your logs are within your
    pre-shift & post-shift threshold. If not, please make sure to file your Certificate of Attendance (COA).  
    """

    prompt = prompt.replace('\n', '  \n') + data
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            full_response = ""
            for chunk in chat.send_message(prompt, stream=True, safety_settings=SAFETY_SETTTINGS):
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
            message_placeholder.markdown(full_response)
        except genai.types.generation_types.BlockedPromptException as e:
            st.exception(e)
        except Exception as e:
            st.exception(e)
