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
        page_title="Ask HR Bot",
        page_icon="page_icon_path", 
        menu_items={
            'About': ""
        }
    )


st.title("How To Section")
st.caption("Ask How To's here.")

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
    Use this are reference: 
    ## How To Cancel/Edit an Approved Attendance Requests in Sprout
    As a manager, you can cancel an approved Attendance Request. Here’s How:
    1. Under the My Team tab on the Navigation toolbar on your dashboard, select Approval Center from the drop-down list that appears.
    2. Narrow your results by date range, employee name, and department if necessary. Then Select Apply Filter.
    3. You can find the approved application under the Processed tab.
    4. You can either select the Pencil button to edit or X button to cancel the application, after which you’ll be
    required to enter the reason for canceling.
    5. Click the Cancel Application button and you’ll be notified when cancellation is successful.
    ## How to file for a Certificate of Attendance (COA) Application:
    You can easily file for Certificate of Attendance (COA) through Sprout HR, and the request will go to your supervisor
    immediately. The COA replaces biologs on days when an employee either forgets or is unable to manually log into the
    system via the biometric device. There are two ways to file a COA. Let's take a closer look at these two below:
    Via the My Stuff panel on the dashboard
    1. Under the My Stuff panel, click Apply and select Certificate of Attendance from the drop-down list that appears.
    2. Input the correct details by choosing the reason as to why you were unable to log, and adding the details of the Attendance log (Biometric Mode - In/Out, Date, Time).
    3. Click the submit button, and a notification message will appear if your application was submitted successfully.
    Via My Requests/Approvals tab on the Navigation toolbar. 
    Click the My Requests/Approvals tab and choose My Certificate of Attendance from the drop-down list that appears.
    2. Select the +Add icon at the right-hand side
    3. Input the correct details by choosing the reason as to why you were unable to log, and adding the details of the Attendance log (Biometric Mode - In/Out, Date, Time).
    4. Click the submit button, and a notification message will appear if your application was submitted successfully.
    How to update the details of a filed Certificate of Attendance (COA):
    There are times when you find that you have inadvertently input the wrong information on your Certificate of Attendance. Fortunately, Sprout HR allows you to edit your application even after submitting it for approval, but only if the filing hasn't been approved yet by your immediate manager.
    ### Via My Stuff panel on the Dashboard
    1. Under the My Stuff Panel, look for the specific COA application you want to update. Click on the Pencil icon beside theCOA.
    2. Input the changes in the COA details and the reason for the update.
    3. Click the Save button, and a notification message will appear if your application was submitted successfully.
    ### Via My Requests tab on the Dashboard
    1. Click the My Requests tab, and choose My Certificates of Attendance from the drop-down list that appears.
    2. Under the Pending/Resubmitted for Editing tab, look for the specific COA application you want to update, and click the Update button.
    3. Input the changes in the COA details.
    4. Click the Submit button, and a notification message will appear if your application was submitted successfully. Click the OK button.
    ## How to cancel a filed Certificate of Attendance (COA):
    Cancellation of COA applications can be done by either the employee, the manager, or the administrator. This can be
    done in a number of ways:
    ### Via My Stuff panel on the Dashboard:
    1. Under the My Stuff panel, look for the specific COA you wish to cancel. Click the X icon.
    2. The details of the selected COA will be shown. Click the X button at the bottom of the pop-up box and add a
    reason for cancellation.
    3. Click the Submit button and a notification message will appear if your application was canceled successfully.
    ### Via My Requests tab in the Dashboard
    1. Click the My Requests tab and choose My Certificate of Attendance.
    2. Under the Pending/Resubmitted for Editing tab, look for the specific COA, and click Cancel
    3. Input the Reason for Cancellation.
    4. Click the OK button and a notification message will appear if your application was cancelled successfully.
    ## How to file for a Schedule Adjustment (SA) Application via the My Stuff panel in Sprout dashboard:
    1. Click 'Apply' then select 'Schedule Adjustment' from the drop-down list that appears.
    2. Enter the following:
        a. Effectivity Date of the schedule change
        b. Shift Start and Shift End
        c. Break Start and Break End
    3. The Schedule Adjustment Request will then appear based on the changes entered. Enter the reason for the change in the schedule then click Apply.
    4. Click the OK button after reviewing the application.
    5. You will be notified when the request is successfully submitted to your supervisor.
    Important Reminder: The Schedule Adjustment (SA) is for a temporary change of shift:
    - for a day
    - for a couple of weeks or months
    - for rest days and holidays
    If you wish to change your schedule permanently, contact your manager or the Sprout Administrator: payroll@connextglobal.com.
    To apply the Schedule Adjustment (SA) to the rest of the selected period, use the copy Icon
    Step 1: Select the copy Icon in the right side of your screen.
    Step 2: Tick all the working days and click “Copy”.
    Step 3: Click the apply button after reviewing the application.
    Note: You will notice that the padlock for November 1 and 2 are unlocked since these are PH holidays
    ## Best Practices when filing a Schedule Adjustment
    1. The details that you enter in the Schedule Adjustment (SA) application must be accurate. Double-check PM and AM.
    2. If you are changing your schedule to work on holidays, make sure to open the padlock and enter the details on those holiday dates.
    3. If you are changing your schedule to work on your Rest Day, make sure to tick the check box and make sure that the padlock is open.
    4. If you are a manager and wants to change the default schedule of your team member, ensure that the “Working Hours Including Break” is set to “9” hours.
    5. Make it a habit to check your attendance summary before the timesheet locks.
    ## How To Update Pending Attendance Application
    It is not unheard of in Sprout HR to find yourself in a situation where your attendance application is still pending with
    your immediate supervisor when for some reason, the organizational chart shifts, or your position changes, and you
    suddenly have a new manager to report to.
    In this situation, who gets the duty of approving an employee's pending applications?
    The short answer: The pending application stays within your previous approver but you can simply opt to update or
    resubmit your application so your new approver will be given the task to approve your request.
    Here’s How:
    1. On Employee dashboard, click on the My Requests tab and select Pending applications.
    2. Click on the Update button.
    3. This will take you to the application page itself.
    4. Upon clicking the Apply button, the application will be transferred to the employee’s new approver for his
    approval.    
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
