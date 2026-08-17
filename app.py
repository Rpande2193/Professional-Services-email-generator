import streamlit as st
import anthropic

# 1. System Page Configuration & Styling
st.set_page_config(
    page_title="Darwinbox Cortex | PS Play Picker",
    page_icon="🤖",
    layout="centered"
)

# Apply sleek, professional styling match
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; max-width: 750px; }
    h1 { color: #1E293B; font-weight: 700; margin-bottom: 0.5rem; }
    .subtitle { color: #64748B; font-size: 1.1rem; margin-bottom: 2rem; }
    div[data-testid="stForm"] { border: 1px solid #E2E8F0; border-radius: 12px; background-color: #F8FAFC; padding: 2rem; }
    .stButton>button { width: 100%; background-color: #2563EB; color: white; border-radius: 6px; font-weight: 600; }
    .stButton>button:hover { background-color: #1D4ED8; }
    .output-box { border: 1px dashed #CBD5E1; background-color: #FFFFFF; padding: 1.5rem; border-radius: 8px; font-family: monospace; }
    </style>
""", unsafe_with_html=True)

st.title("Darwinbox • Professional Services Play Picker")
st.markdown("<p class='subtitle'>Darwinbox • US West • GTM Enablement</p>", unsafe_with_html=True)

st.markdown("""
Pick the **sub-segment**, the **employee band**, and the **prospect's title** — add an **account trigger** if you have one — then tap **Apply**. 
The problem in the email is written for that *specific sub-industry through that role's lens*.
""")

# 2. Form Interface
with st.form("play_picker_form"):
    st.subheader("Set the play")
    
    sub_segment = st.selectbox(
        "1. Sub-segment cluster",
        ["Legal Firms", "Accounting & Audit", "Business Process Outsourcing (BPO)", "Management Consulting", "Engineering & Architecture Services"]
    )
    
    headcount = st.selectbox(
        "2. Employee headcount",
        ["100 - 500 employees", "501 - 2,000 employees", "2,001 - 5,000 employees", "5,001+ employees"]
    )
    
    title = st.selectbox(
        "3. Prospect title / designation",
        ["VP of HR / CHRO", "VP of IT / CIO", "Director of Talent Acquisition", "Head of People Operations", "Operations Director / COO"]
    )
    
    trigger = st.text_input(
        "4. Account trigger (OPTIONAL)",
        placeholder="e.g., recent funding, M&A, new CHRO, geographical expansion, RIF-then-rehire..."
    )
    
    variant = st.radio(
        "Angle variant",
        ["A · proof & CTA", "B · alternate structural pitch"],
        horizontal=True
    )
    
    sender_signoff = st.selectbox(
        "Sender name Sign-off",
        ["Business Development, Darwinbox", "BDR Manager, US West, Darwinbox"]
    )

    submit_button = st.form_submit_button("Apply — generate email")

# 3. Secure Claude API Processing Logic
if submit_button:
    # Safely extract the secret key from Streamlit Cloud's environment environment variables
    if "ANTHROPIC_API_KEY" not in st.secrets:
        st.error("Error: ANTHROPIC_API_KEY is missing from App Secrets! Please add it in your Streamlit Cloud Dashboard settings.")
    else:
        with st.spinner("Cortex system correlating signals and drafting your copy..."):
            try:
                # Initialize client using the cloud secret
                client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                
                # Craft the prompt context instructing Claude to use your exact structural matrix rules
                prompt_content = f"""
                You are a premium BDR copywriting assistant for Darwinbox US West. 
                Generate a highly tailored, conversion-focused first-touch cold email targeting the Professional Services sector.
                
                Inputs selected by user:
                - Sub-segment cluster: {sub_segment}
                - Employee headcount: {headcount}
                - Prospect title/designation: {title}
                - Account trigger: {trigger if trigger else 'None provided'}
                - Angle variant: {variant}
                - Sign-off: {sender_signoff}

                Strict Structural Guardrails:
                1. Length target: 60–90 words total for the email body. Keep it punchy, high-impact, and short.
                2. Do not explicitly call out the headcount numbers or name the exact segment inside the body text. Let it naturally rewrite the structural context.
                3. The operational problem highlighted must map specifically to the sub-industry lens of a '{sub_segment}' as seen by a '{title}'. 
                4. Set up the core value of Darwinbox Cortex: sensing fragmented workforce signals (like shifts in unplanned leave patterns, overwork, stagnation) and acting natively via an AI context graph before operations break down or get expensive.
                5. If a trigger is provided, craft a clean, logical bridging line that links the trigger directly into the industry operational problem instead of just pasting it awkwardly at the top.
                6. Include standard bracketed placeholders for personalizations: [First Name], [Company].
                7. Angle Variant Context:
                   - If variant A: Emphasize signal-first proof and soft resonance CTA.
                   - If variant B: Emphasize structural agility and proactive operational playbooks.

                Format your final response cleanly with a 'Subject:' line at the top, followed by the email body. Below the email body, provide a brief 'Why this play' strategy breakdown explaining the persona angle you used.
                """

                # Execute request securely across cloud server
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=600,
                    temperature=0.3,
                    system="You are an expert enterprise outbound strategist. Your goal is to write hyper-personalized emails that read completely naturally, avoiding standard cheesy AI marketing jargon.",
                    messages=[
                        {"role": "user", "content": prompt_content}
                    ]
                )
                
                response_text = message.content[0].text
                
                # 4. Render output gracefully onto screen
                st.success("Play Generated Successfully!")
                st.markdown("### Generated first-touch")
                st.code(response_text, language="markdown")
                
            except Exception as e:
                st.error(f"An error occurred while connecting to Claude: {str(e)}")
