import streamlit as st
from calculator import calculate_r2_iss

def main():
    # Configure Streamlit page
    st.set_page_config(
        page_title="R2-ISS Staging Calculator",
        layout="centered",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )

    # Set light theme
    st.markdown("""
        <script>
            var elements = window.parent.document.getElementsByTagName('html');
            elements[0].setAttribute('data-theme', 'light');
        </script>
        """, unsafe_allow_html=True)

    # Custom CSS for styling
    st.markdown("""
        <style>
        /* CSS styling here */
        </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown("""
        <div class="main-header">
            <div class="header-title">R2-ISS Staging Calculator</div>
            <div class="header-subtitle">Professional Multiple Myeloma Staging Tool</div>
        </div>
    """, unsafe_allow_html=True)

    # About section
    with st.expander("About R2-ISS"):
        st.info("""
            The Revised International Staging System (R2-ISS) is a validated prognostic tool for multiple myeloma that combines:
            - Traditional ISS criteria (β2-microglobulin and albumin)
            - High-risk chromosomal abnormalities
            - Serum lactate dehydrogenase (LDH)
            
            This calculator provides accurate staging based on the latest clinical guidelines.
        """)

    # Tabs for calculator and reference guide
    tab1, tab2 = st.tabs(["Calculator", "Reference Guide"])

    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        # Inputs for clinical parameters
        with col1:
            st.markdown('<div class="section-title">Clinical Parameters</div>', unsafe_allow_html=True)
            b2m = st.radio(
                "β2-Microglobulin (β2M)",
                options=["< 3.5 mg/L", "3.5 - 5.5 mg/L", "≥ 5.5 mg/L"],
                index=0,
            )
            albumin = st.radio(
                "Albumin",
                options=["≥ 3.5 g/dL", "< 3.5 g/dL"],
                index=0,
            )
            ldh = st.radio(
                "Lactate Dehydrogenase (LDH)",
                options=[
                    "Normal (< 240 U/L)",
                    "Elevated (240 - 300 U/L)",
                    "Significantly Elevated (> 300 U/L)"
                ],
                index=0,
            )

            st.markdown('<div class="section-title">Cytogenetic Abnormalities</div>', unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                del17p = st.checkbox("del(17p)")
            with col_b:
                t414 = st.checkbox("t(4;14)")
            with col_c:
                gain1q = st.checkbox("1q gain/amp")

        # Results section
        with col2:
            # Calculate R2-ISS results and add debug print to confirm structure
            results = calculate_r2_iss(
                b2m=b2m,
                albumin=albumin,
                ldh=ldh,
                del17p=del17p,
                t414=t414,
                gain1q=gain1q
            )

            # Debugging output to verify the structure of `results`
            st.write("Results structure:", results)

            # Ensure results is a dictionary and contains the expected keys
            if isinstance(results, dict) and 'r2_iss_stage' in results and 'breakdown_messages' in results:
                # Add specific detail for ISS Stage II if needed
                if results['r2_iss_stage'] == "R2-ISS II" and "ISS Stage II: 1 point" in results['breakdown_messages']:
                    results['breakdown_messages'] = [
                        msg.replace("ISS Stage II: 1 point", "ISS Stage II: 1 point (β2M between 3.5 and 5.5 mg/L or Albumin < 3.5 g/dL)")
                        for msg in results['breakdown_messages']
                    ]

                # Determine stage color based on risk level
                stage_colors = {
                    "R2-ISS I": "linear-gradient(135deg, #059669 0%, #047857 100%)",
                    "R2-ISS II": "linear-gradient(135deg, #d97706 0%, #b45309 100%)",
                    "R2-ISS III": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)",
                    "R2-ISS IV": "linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%)"
                }
                stage_color = stage_colors.get(results['r2_iss_stage'], "linear-gradient(135deg, #2563eb 0%, #1e40af 100%)")

                # Display stage and total points
                st.markdown(f"""
                    <div class="stage-display" style="background: {stage_color}">
                        <div class="stage-title">{results['r2_iss_stage']}</div>
                        <div class="stage-points">Total Points: {results['total_points']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Display detailed point breakdown
                st.markdown('<div class="section-title">Point Breakdown</div>', unsafe_allow_html=True)
                for message in results['breakdown_messages']:
                    st.markdown(f'<div class="breakdown-item">{message}</div>', unsafe_allow_html=True)
            else:
                st.error("Unexpected result format from `calculate_r2_iss`. Please check the function.")

        st.markdown('</div>', unsafe_allow_html=True)

    # Reference Guide tab
    with tab2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">R2-ISS Stage Reference</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display reference table
            data = {
                "Stage": ["R2-ISS I", "R2-ISS II", "R2-ISS III", "R2-ISS IV"],
                "Points": ["0", "0.5 - 1", "1.5 - 2.5", "3 - 5"],
            }
            st.table(data)
            
        with col2:
            # Display scoring components
            st.info("""
                **Scoring Components:**
                - β2-Microglobulin levels
                - Serum Albumin
                - LDH levels
                - Cytogenetic abnormalities
                    - del(17p)
                    - t(4;14)
                    - 1q gain/amp
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer section
    st.markdown("""
        <div class="footer">
            <p>© 2024 R2-ISS Calculator | Developed by Taya Salman</p>
            <p>For clinical use. Always verify results with laboratory findings.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
