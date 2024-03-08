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
        page_title="Bonuses and Benefits Section",
        page_icon="page_icon_path", 
        menu_items={
            'About': ""
        }
    )


st.title("Bonuses and Benefits Section")
st.caption("Ask about Perfect Attendance Bonus and 13th Month Pay Here")

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
    13th Month Pay – FAQs
    Q: How is 13th month pay computed?
    A: Total Basic Pay earned during the calendar year (January 1 – December 31) divided by 12 months. The 13th month pay
    shall not be less than 1/12 of the total basic pay earned by an employee within a calendar year.
    Q: How is Basic Pay for the period of November 16 – December 31 calculated given that the release of 13th month pay will be in the first week of December?
    A: Basic Pay for November 16 – December 31 will be considered in full amount except for those employees whose effective
    date of separation is between the release date of 13th month pay – December 31.
    Q: What does “Basic Pay” comprise of?
    A: “Basic Pay” shall include all remunerations of earnings received by the employee for services rendered but does not
    include allowances and monetary benefits which are not considered or integrated as part of the regular or basic pay, such
    as the overtime pay, holiday pay, night differential pays, and other allowances.
    Here’s an illustration:
    CUT-OFF | PAYOUT | BASIC PAY | ADJUSTMENT-LAST PAYOUT | ABSENCES | LATES | NET BASIC PAY | REMARKS
    --- |  --- | --- | --- | --- | --- | --- | --- 
    JAN 1 - 15 | 25-Jan | 12,500 | | | | 12,500 | 
    REMARKS
    w/ 1 day leave w/out pay
    w/ 20 minutes late
    w/ 2 days absent
    w/ 2 days adjustment (dispute for April 10 payout)
    Employee has a salary increase effective July 1
    Semi-monthly basic pay is considered in full amount
    Semi-monthly basic pay is considered in full amount
    Semi-monthly basic pay is considered in full amount
    Q: Are maternity leave benefits included in the computation of 13th month pay?
    A: No. Maternity leave benefits are not included in the computation of 13 th month pay.
    Q: I have a salary increase but it is scheduled on November 16/December 1/December 16 of the current year. Will this be considered in the computation of my 13th month pay?
    A: Yes. All salary increase for the above-mentioned periods will be considered in the computation provided that the salary increase document was acknowledged and sent back to the HR five business days before the payment of the 13th month pay.
    Q: Who are covered or entitled to the 13th month pay?
    A: All employees who have worked for at least one month during the calendar year or whose date of hire is on or before November 30, are entitled to receive 13th month pay.
    Q: Are separated employees entitled to 13th month pay?
    A: Yes. An employee who has resigned or whose services were terminated at any time before the payment of 13 th month is
    still entitled to the benefit. This will be included in his/her Final Pay.

    # PERFECT ATTENDANCE BONUS

    Eligibility:
    The Employee must be a regular employee and belongs to the category/position level stated below:
    a) Rank-and-File Employees: Team Members/Specialists/Sr. Team Members/Sr. Specialists
    b) Supervisory: Team Leaders, Sr. Team Leaders
    Frequency:
    Monthly – every 10th payout following the applicable month.
    Amount:
    A regular employee will receive PHP 2,000.00 Perfect Attendance Bonus. However, an employee
    whose regularization date falls in the middle of the applicable month will receive a prorated amount of
    bonus based on the number of days that he/she is regular during the month.
    The Perfect Attendance Bonus is also included in the PHP 90,000.00 threshold for Non-Taxable
    Bonuses and 13th month pay every calendar year.
    Policy Element:
    To receive the Perfect Attendance Bonus (PAB), the employee must meet ALL the qualifications stated
    below:
    a) For Rank-and-File and Supervisory Employees:
    ✓ All leave must be Planned and Paid. It must be filed in Sprout HR ahead of time and
    must be approved by the employee’s supervisor before the timesheet locks.
    ✓ The employee is expected to check his/her attendance logs and attendance requests at
    every end of payroll cut-off. Failure to do so may result in PAB disqualification. No PAB
    will be qualified for dispute.✓ The employee does not have any of the following:
    ➢ Unexcused absences – Occurs when the employee is unavailable for work as
    assigned and/or scheduled.
    ➢ Unplanned Leaves – Paid Time-Offs that are not filed ahead of time.
    • Sick Leave
    • Emergency Leave
    • Unplanned Bereavement Leave
    • Unplanned Paternity Leave
    • Unplanned Solo Parent Leave
    • Unplanned Magna-Carta Leave
    ➢ Maternity Leave/Battered Woman Leave
    ➢ Tardiness for more than 3 minutes for the whole month
    ➢ Over-break for more than 3 minutes (Will be monitored by employee’s supervisor)
    ✓ The employee must be active at the time of awarding/payout. All bonuses are
    contingent upon employees being active with Connext. Therefore, no Perfect
    Attendance Bonus will be awarded in employee’s Final Pay
    b) Additional Qualifications for Supervisory Employees:
    ✓ Supervisory employees are expected to manage their team’s attendance and
    performance. That said, 50% of the PAB will be based on their team’s showrate and
    overall KPI while the remaining 50% will be based on his/her own showrate.
    ✓ If the supervisor’s showrate fails, he/she will automatically be disqualified to receive
    100% of the PAB.
    ✓ Since KPI targets vary per team and/or client, the computation of the 50% may also
    vary. The computation will then be decided by the Team Leader’s Manager.
    ✓ Team Leaders’ PAB must be sent to payroll@connextglobal.com not later than 6th of
    every month, following the applicable month.
    Leave Filing During Holidays:
    The employee must file a Paid Time-Off if he/she plans to skip work on the following holidays:
    ✓ Philippine Holidays – (See Pay Guidelines on Philippine Holidays for reference)
    ➢ Regular or Legal Holiday
    ➢ Special Non-Working Holiday and Local Holidays
    ➢ Special Working Holiday
    ✓ Client Mandated Holidays
    ✓ Client Mandated Time-Off
    Important Note:
    All abovementioned eligible employees will receive leave credits for every month of service. They
    are also allowed to file a maximum of 3 Paid Time-Off even with zero leave credits. That said, it is
    expected that employees can manage their leave filing as this may affect their Perfect Attendance Bonus.There will be no exceptions made towards the awarding of Perfect Attendance other than those
    noted above. These guidelines are used to determine Perfect Attendance Bonus ONLY and are not related
    to any other Company Attendance System. Any Company decision as to the interpretation of any of these
    circumstances and/or the facts involved is final. The Company reserves the right to modify and/or
    terminate this policy at any time.    
    """

    combined_prompt = prompt.replace('\n', '  \n') + data
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            full_response = ""
            for chunk in chat.send_message(combined_prompt, stream=True, safety_settings=SAFETY_SETTTINGS):
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
