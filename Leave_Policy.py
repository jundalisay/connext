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

st.title("Leave Policy Section")
st.caption("Ask About Leave Policies Here")

try:
    genai.configure(api_key=google_api_key)
except AttributeError as e:
    st.warning("Please Configure Gemini App Key First.")

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()



with st.sidebar:

    st.header("Ask Your AI HR")
    
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.rerun()

for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)


if prompt := st.chat_input(""):

    # leavepolicy
    data = """
    Use this as referece: 
    PAID TIME-OFF (PTO)/LEAVE POLICY in Connext in the Philippines (PH)

    ### Definitions:
    - A Paid Time-Off or Paid Day-Off is a leave from working on that time or day.


    All active employees will be given leave credits for every month of service and can file for leaves for holidays.

    ## Leave Credit Guidelines

    Employee Type | Leave Credits Per Year | Leave Credits Per Month 
    --- | --- | --- 
    Rank-and-File Employees | 20 | 1.67 
    Supervisory, Managerial, and Executive | 22 | 1.83

    All employees will start earning leave credits on his/her first month with Connext.

    Example:

    Start date | First leave Accrual
    --- | --- 
    January 1 | February 1 | 

    - Paid Time-Off should be filed at least 2 weeks before the time-off date to give time for the leaders to project staffing. It must be filed in Sprout HR ahead of time and must be approved by the employee’s supervisor before the timesheet locks.
    - If a leave is filed within 2 weeks before the PTO date, leave approval is based on the discretion of the direct supervisor.
    - Paid Time-Offs that are filed on or after the actual time-off date will be tagged as unplanned leave which is a Perfect Attendance Bonus disqualifier
    - A maximum of 5 unused Paid Time-Off will be carried over for the following year. All other unused Paid Time-Off will expire at the end of the year
    - All employees are encouraged to take their paid time off for the year. As such, unused PTOs are not convertible to cash.
    - Paid Time-Off is deducted from the total leave credits on the actual date of the leave, not when the leave is filed. See illustration below:


    Title | Details
    --- | ---
    Total Leave Credits before filing PTO | 6 days
    Filing Date | December 15, 2023
    Scenario | The employee filed a 3-day PTO for January 8 - 10, 2024.
    Total Leave Credits after the employees' PTO | 2 days
    Reason | The 3 days PTO was deducted from the 5 unused PTO that was carried over for the
    year 2024. The other 1 day expired December 31.

    - If the employee filed a resignation, all unused leave credits after separation will expire and will not be converted into cash.

    - Employees on maternity leave, floating status, and preventive suspension are deemed inactive and will not earn Paid Time-Offs during the month that they are out.
    - A rank-and-file employee who’s promoted to supervisory role will accrue 1.83 Paid Time-Offs every month after the effective date of his/her promotion. 
    - An employee with zero leave credits can still file a Paid Time-Off for a maximum of 3 paid time-off days provided that the employee ran out of leaves and there is a client mandated time-off.
    - Employees’ supervisors are responsible in making sure that the Paid Time-Offs filed by their team members for these 3 days allowable are for client mandated holidays/client mandated time-off only.
    - Employees with a negative number of leave credits upon separation with Connext will be deducted to the corresponding amount from their final pay. The formula is: negative leave balance x employee’s daily rate = deduction

    ## PAY GUIDELINES FOR WORK ON PHILIPPINE HOLIDAYS For Rank-and-File Employees

    Sometimes, work goes on even during Philippine holidays. 

    For Rank-and-File Employees: 
    - Team Members
    - Specialists
    - Sr. Team Members
    - Sr. Specialists

    ### Working on a Regular or Legal Holiday:

    Scenario | Outcome
    --- | ---
    An employee has filed for Paid Time-Off yet still is called to work and goes to work | The employee is entitled to 200% of his/her daily rate.
    An employee has filed for Paid Time-Off yet still is called to work and does not go to work | The employee gets paid time off, but it will still be considered as unplanned off and will be a Perfect Attendance Bonus disqualifier.

    ### Special Non-Working Holiday and Local Holidays

    Scenario | Outcome
    --- | ---
    An employee works during the holiday | He gets 130% of his/her daily rate
    An employee is on Paid-Time Off during the holiday yet is called to work and goes to work | He gets 100% of his daily rate
    An employee is called to work yet does not go to work and has not filed for a Paid Time-Off  | “No Work, No Pay” principle shall apply. This is considered as absence and a Perfect Attendance Bonus disqualifier.

    ##### Income Tax and Withholding Tax Policy

    Withholding Tax on Compensation are calculated, consolidated, and filed in Angeles City. Therefore, only local holidays declared in Angeles City, Pampanga will be tagged as special non-working holidays. All rank-and-file employees in the Philippines are considered
    eligible.

    ### Special Working Holiday:

    ➢ For work performed on a declared Special Working Day, an employee is entitled only to his/her basic pay. No premium pay will be given since work performed on Special Working Day is considered work on an ordinary day.

    ## PAY GUIDELINES FOR WORK ON PHILIPPINE HOLIDAYS For Supervisory/Managerial Employees

    Supervisory/Managerial Employees are:
    - Team Leaders and Up

    ### Regular or Legal Holiday:

    Scenario | Outcome
    --- | ---
    The employee works or on a Paid Time-Off during the holiday | He is entitled only to his basic pay. 22 days are given to
    supervisory/managerial employees since no premium pay is given to them during the PH holidays

    ### Special Non-Working Holiday, Local Holidays and Special Working Holiday:

    Scenario | Outcome
    --- | ---
    The employee works or on a Paid Time-Off during the holiday |  He gets only basic pay. No premium pay is given to
    supervisory/managerial employees
    The employee does not work and not on a Paid-Time Off | The “No Work, No Pay” principle shall apply regardless of the employee’s employment status. This will also be taken against employees Showrate and will impact any bonus
    related to Showrate.

    ## FAQS
    1. Q: What to expect on September 1, 2023?
    A1: Employees with zero leave credits are now allowed to file a Paid Time-Off for a maximum of 3 days if there is a client mandated time-off.
    A.2: Employees hired after September 1, 2023 will start earning leave credits on their 1st month with Connext.
    A.3: Employees on probationary status as of September 1, 2023: will earn leave credits on their next monthly tenure with Connext.
    2. Q: What is the impact to supervisory and managerial employee’s salary if he/she skips work and did not file a Paid Time-Off during a Regular/Legal PH Holiday?
    A: When it comes to salary, the supervisory – managerial employee is still entitled to his/her daily rate regardless if he/she is absent, or did not file a Paid Time-Off during the Regular/LegalPH holiday provided he/she reports to work or is on Paid Time-Off on the day immediately preceding the holiday. If the day immediately preceding the holiday is the scheduled rest day, it
    will be based on the day immediately preceding his/her rest day. However, this is taken against his/her showrate, and may affect his/her Perfect Attendance Bonus (for Team Leaders) or Quarterly Manger’s Bonus (for Managers).
    3. Q: The Local Government Unit in Davao declared March 3, 2023 as “Araw ng Davao”. Am I eligible for a holiday pay premium given that I’m living in Davao and my work set up is PWFH?
    A: No, only local holidays declared in Angeles City, Pampanga will be tagged as special non-working holidays.
    4. Q: Today is a PH holiday but my schedule starts at 11:00 PM. How many hours of holiday premium should I expect on payday?
    A: If an employee’s shift starts during the holiday, he or she may expect a total of 8 hours premium per holiday even if his/her schedule crossed on another day.
    5. Q: How many hours of holiday premium should I expect if my schedule falls during night differential hours?
    A: Employee should expect a total of 8 hours premium per holiday regardless of his/her working schedule. To further illustrate this, employees’ whose schedule is from:
    12:00 AM to 09:00 AM = 6 Hours LH-ND + 2 Hours LH (total of 8 hours holiday premium)
    02:00 AM to 11:00 AM = 4 Hours LH-ND + 4 Hours LH (total of 8 hours holiday premium)
    04:00 AM to 01:00 PM = 2 Hours LH-ND + 6 Hours LH (total of 8 hours holiday premium)
    06:00 AM to 03:00 PM = 8 Hours LH (total of 8 hours holiday premium)
    10:00 PM to 07:00 AM = 8 Hours LH-ND (total of 8 hours holiday premium)
    Important Note: Holiday Rates used in Payroll Computation are consolidated rates. This means
    that all Night Differential Rates during Holidays were considered and have a higher multiplier
    compared to Night Differential Rate during an Ordinary Day.
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
