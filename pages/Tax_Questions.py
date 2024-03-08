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


st.title("Taxes Section")
st.caption("Ask About Income Taxes Here")

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
    ## How Connext Computes Taxes in the Philippines
    ### Step 1: Compute for your taxable income, which is your basic salary (plus additional pays like holiday and overtime pays) minus your contributions.
    Taxable Income = (Monthly Basic Pay + Additional Pay) – (SSS + PhilHealth + PAG-IBIG + Deductions Due to Absences/Tardiness)
    SSS CONTRIBUTION TABLE
    SALARY RANGE    CONTRIBUTION AMOUNT
    1000 – 1249.99  36.30
    1250 – 1749.99  54.50
    1750 – 2249.99  72.70
    2250 – 2749.99  90.80
    2750 – 3249.99  109.00
    3250 – 3749.99  127.20
    3750 – 4249.99  145.30
    4250 – 4749.99  163.50
    4750 – 5249.99  181.70
    5250 – 5749.99  199.80
    5750 – 6249.99  218.00
    6250 – 6749.99  236.20
    6750 – 7249.99  254.30
    7250 – 7749.99  272.50
    7750 – 8249.99  290.70
    8250 – 8749.99  308.80
    8750 – 9249.99  327.00
    9250 – 9749.99  345.20
    9750 – 10249.99 363.30
    10250 – 10749.99    381.50
    10750 – 11249.99    399.70
    11250 – 11749.99    417.80
    11750 – 12249.99    436.00
    12250 – 12749.99    454.20
    12750 – 13249.99    472.30
    13250 – 13749.99    490.50
    13750 – 14249.99    508.70
    14250 – 14749.99    526.80
    14750 – 15249.99    545.00
    15250 – 15749.99    563.20
    15750 and above 581.30
    Below is the PhilHealth contribution table:

    PHILHEALTH CONTRIBUTION TABLE
    SALARY RANGE (x 2.75%)  CONTRIBUTION AMOUNT
    10000 and below 275.00
    10000.01 – 39999.99 275.02 – 1099.99
    40000 and above 1100

    Suppose that you are earning P23000 a month, the computation for the taxable income will be as follows:

    Taxable Income = (23000) – (581.30 + ((23000 * 0.0275) / 2) + 100.00)
    = (23000) – (997.55)
    Taxable Income = 22002.45

    ### Step 2: Compute for the income tax

    ## How to Compute for the Income Tax
    Tax computation in the Philippines changed this January 2018 in the form of the Tax Reform Bill of the Duterte Administration. The current tax table is relatively simpler, and allows employees to take home more money than before.

    BIR TAX TABLE   
    SALARY RANGE (ANNUAL)   INCOME TAX RATE
    250000 and below    0%
    250000.01 to 400000 20% of the excess over 250000
    400000.01 to 800000 30000 + 25% of the excess over 400000
    800000.01 to 2000000    130000 + 30% of the excess over 800000
    2000000.01 to 8000000   490000 + 32% of the excess over 2000000
    8000000.01 and above    2410000 + 35% of the excess over 8000000
    Income Tax = (((Taxable Income * 12) – X) * Y) / 12
    Where X is the minimum value of the particular salary range, and Y is the respective percentage

    Since your taxable income is 22002.45, the computation will be as follows:

    Income Tax = (((22002.45 * 12) – 250000) * 0.20) / 12
    = ((264029.4 – 250000) * 0.20) / 12
    = 2805.88 / 12
    Income Tax = 233.82

    ### Step 3: Subtract your income tax from your taxable income.

    Net Pay = Taxable Income – Income Tax
    = 22002.45 – 233.82
    Net Pay = 21768.63

    Withholding Tax on Compensation are consolidated by Connext and filed in Angeles City. Therefore, only local holidays declared in Angeles City, Pampanga will be tagged as special non-working holidays. All rank-and-file employees in the Philippines are eligible.
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
