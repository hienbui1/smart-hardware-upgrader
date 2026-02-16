import streamlit as st

# Set page configuration
st.set_page_config(page_title="Smart Hardware Upgrader", page_icon="💻")

# App Title and Subheader
st.title("💻 Smart Hardware Upgrader")
st.subheader("Find the perfect PC upgrade to eliminate your bottleneck.")

# Layout using columns for Current Setup
st.markdown("### Your Current Setup")
col1, col2 = st.columns(2)

with col1:
    current_cpu = st.selectbox(
        "Current CPU",
        ["Select a CPU", "Ryzen 5 5600X", "Ryzen 7 7800X3D", "Core i7-13700K", "Core i5-12400F"]
    )

with col2:
    current_gpu = st.selectbox(
        "Current GPU",
        ["Select a GPU", "RTX 3070", "RTX 4090", "RX 7800 XT", "RX 6700 XT"]
    )

# Layout for Target Goals
st.markdown("### Your Target Goals")
col3, col4 = st.columns(2)

with col3:
    target_game = st.text_input("Target Game", placeholder="e.g., Counter-Strike 2")

with col4:
    upgrade_budget = st.number_input("Upgrade Budget ($ USD)", min_value=0, step=50, value=500)

# Submit Button
if st.button("Analyze Bottleneck & Recommend Upgrade", type="primary"):
    if current_cpu == "Select a CPU" or current_gpu == "Select a GPU":
        st.warning("Please select both your current CPU and GPU.")
    elif not target_game:
        st.warning("Please enter a target game.")
    else:
        # Placeholder success message for Phase 1
        st.success(f"✅ Success! Variables captured:\n\n"
                   f"**CPU:** {current_cpu} | **GPU:** {current_gpu}\n\n"
                   f"**Game:** {target_game} | **Budget:** ${upgrade_budget}")
        st.info("Backend AI logic will be connected here in Phase 2!")