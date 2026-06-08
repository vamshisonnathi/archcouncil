import streamlit as st

st.set_page_config(
    page_title="ArchCouncil",
    page_icon="🏛️",
    layout="wide",
)

st.title("🏛️ ArchCouncil")
st.subheader("Paste your architecture doc. Get a CTO-level review in under 3 minutes.")

st.markdown("---")

arch_doc = st.text_area(
    "Paste your system architecture document below:",
    height=300,
    placeholder=(
        "System: My Platform\n"
        "Stack: Node.js, PostgreSQL, Redis, deployed on AWS EC2...\n"
        "Describe your components, data flow, auth, deployment, etc."
    ),
)

if st.button("🚀 Submit for Review", type="primary", disabled=not arch_doc):
    st.info("⏳ Architecture doc submitted to ArchCouncil agents. Waiting for findings...")
    # TODO: Connect to Band room via API once credentials are live (June 12)
    st.warning("Band integration pending — agents will connect after June 12 kickoff.")

st.markdown("---")

st.markdown(
    """
    ### How it works
    1. **You paste** your architecture document above
    2. **CTO Coordinator** dispatches it to 3 specialist agents simultaneously
    3. **Security Agent** — audits auth, encryption, injection risks
    4. **Scalability Agent** — finds bottlenecks, SPOF, scaling gaps
    5. **Cost Agent** — estimates spend, finds waste, suggests savings
    6. **Coordinator** resolves conflicts → produces final prioritized report
    7. **You approve** or push back — human always in the loop
    """
)

st.markdown("---")
st.caption("ArchCouncil | Sonnathi Labs | Band of Agents Hackathon 2026")
