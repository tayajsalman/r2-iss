import streamlit as st
from calculator import calculate_r2_iss

def main():
    # Force light mode and other settings
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

    # Force light theme
    st.markdown("""
        <script>
            var elements = window.parent.document.getElementsByTagName('html');
            elements[0].setAttribute('data-theme', 'light');
        </script>
        """, unsafe_allow_html=True)

    # Add this to your existing CSS to ensure text visibility
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        :root {
            /* Use Streamlit's CSS variables for theming */
            --primary-color: var(--primary-color, #2563eb);
            --background-color: var(--background-color, #ffffff);
            --secondary-background-color: var(--secondary-background-color, #f8fafc);
            --text-color: var(--text-color, #0F172A);
            --font: 'Inter', sans-serif;
        }

        /* Update component styles to use theme variables */
        .main-header {
            padding: 2rem 0;
            margin: 1rem 0 2rem 0;
        }

        .header-title {
            color: var(--text-color);
            font-family: var(--font);
            font-size: 2.25rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            margin-bottom: 0.5rem;
            text-align: center;
        }

        .header-subtitle {
            color: var(--text-color);
            opacity: 0.8;
            font-size: 1.1rem;
            text-align: center;
            font-weight: 400;
        }

        .content-card {
            background: var(--background-color);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        }

        .section-title {
            color: var(--text-color);
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(0, 0, 0, 0.1);
        }

        /* Radio and Checkbox containers */
        .stRadio > div, .stCheckbox > div {
            background: var(--secondary-background-color);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            margin: 0.5rem 0;
            transition: all 0.2s ease;
        }

        .stRadio > div:hover, .stCheckbox > div:hover {
            border-color: var(--primary-color);
            background: color-mix(in srgb, var(--primary-color) 10%, var(--secondary-background-color));
        }

        /* Results section */
        .breakdown-item {
            background: var(--secondary-background-color);
            color: var(--text-color);
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            border-left: 4px solid var(--primary-color);
        }

        /* Stage display - keep original colors for risk levels */
        .stage-display {
            padding: 2rem;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 1.5rem;
            color: white !important;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .stage-display .stage-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }

        .stage-display .stage-points {
            font-size: 1.1rem;
            opacity: 0.9;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding-top: 2rem;
            margin-top: 3rem;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
            color: var(--text-color);
            opacity: 0.8;
        }

        .footer p {
            margin: 0.5rem 0;
            font-size: 0.875rem;
        }

        /* Table styles */
        .stTable {
            color: var(--text-color);
        }

        /* Info boxes */
        .stAlert {
            color: var(--text-color);
            background: var(--secondary-background-color);
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class="main-header">
            <div class="header-title">R2-ISS Staging Calculator</div>
            <div class="header-subtitle">Professional Multiple Myeloma Staging Tool</div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("About R2-ISS"):
        st.info("""
            The Revised International Staging System (R2-ISS) is a validated prognostic tool for multiple myeloma that combines:
            - Traditional ISS criteria (β2-microglobulin and albumin)
            - High-risk chromosomal abnormalities
            - Serum lactate dehydrogenase (LDH)
            
            This calculator provides accurate staging based on the latest clinical guidelines.
        """)

    tab1, tab2 = st.tabs(["Calculator", "Reference Guide"])

    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
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

        with col2:
            results = calculate_r2_iss(
                b2m=b2m,
                albumin=albumin,
                ldh=ldh,
                del17p=del17p,
                t414=t414,
                gain1q=gain1q
            )

            # Determine stage color based on risk
            stage_colors = {
                "R2-ISS I": "linear-gradient(135deg, #059669 0%, #047857 100%)",
                "R2-ISS II": "linear-gradient(135deg, #d97706 0%, #b45309 100%)",
                "R2-ISS III": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)",
                "R2-ISS IV": "linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%)"
            }
            stage_color = stage_colors.get(results.r2_iss_stage.split(" ")[0] + " " + results.r2_iss_stage.split(" ")[1], "linear-gradient(135deg, #2563eb 0%, #1e40af 100%)")

            st.markdown(f"""
                <div class="stage-display" style="background: {stage_color}">
                    <div class="stage-title">{results.r2_iss_stage}</div>
                    <div class="stage-points">Total Points: {results.total_points}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="section-title">Point Breakdown</div>', unsafe_allow_html=True)
            for message in results.breakdown_messages:
                st.markdown(f'<div class="breakdown-item">{message}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">R2-ISS Stage Reference</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            data = {
                "Stage": ["R2-ISS I", "R2-ISS II", "R2-ISS III", "R2-ISS IV"],
                "Points": ["0", "0.5 - 1", "1.5 - 2.5", "3 - 5"],
            }
            st.table(data)
            
        with col2:
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

    st.markdown("""
        <div class="footer">
            <p>© 2024 R2-ISS Calculator | Developed by Taya Salman</p>
            <p>For clinical use. Always verify results with laboratory findings.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
