import streamlit as st
import requests

st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medical Report Analyzer")
st.write("Upload your medical report PDF and get a simple explanation!")

uploaded_file = st.file_uploader(
    "Upload Medical Report (PDF only)",
    type=["pdf"]
)

if uploaded_file is not None:

    st.info("Report uploaded! Click analyze to get results.")

    if st.button("Analyze Report"):

        with st.spinner("Analyzing your report... Please wait ⏳"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    files=files
                )

                if response.status_code == 200:

                    data = response.json()

                    if "error" in data:
                        st.error(data["error"])

                    else:

                        st.success("Analysis Complete! ✅")

                        st.markdown("---")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "🔥 Health Risk Score",
                                f"{data.get('risk_score',0)}%"
                            )

                        with col2:

                            if data.get("see_doctor"):
                                st.warning(
                                    "⚠️ Please consult a doctor soon."
                                )
                            else:
                                st.success(
                                    "✅ No immediate doctor visit needed."
                                )

                        st.markdown("---")

                        st.subheader("📋 Summary")

                        st.write(
                            data.get(
                                "summary",
                                "N/A"
                            )
                        )

                        st.markdown("---")

                        col3, col4 = st.columns(2)

                        with col3:

                            st.subheader("🦠 Detected Conditions")

                            conditions = data.get(
                                "conditions",
                                []
                            )

                            if conditions:

                                for c in conditions:
                                    st.error(f"❌ {c}")

                            else:
                                st.success(
                                    "No major conditions detected!"
                                )

                        with col4:

                            st.subheader("⚠️ Abnormal Values")

                            abnormal = data.get(
                                "abnormal_values",
                                {}
                            )

                            if abnormal:

                                for test, detail in abnormal.items():

                                    st.warning(
                                        f"**{test}** : {detail}"
                                    )

                            else:

                                st.success(
                                    "All values are normal!"
                                )

                        st.markdown("---")

                        st.subheader("💡 Recommendations")

                        recommendations = data.get(
                            "recommendations",
                            []
                        )

                        if recommendations:

                            for r in recommendations:

                                st.info(f"➡️ {r}")

                        st.markdown("---")

                        st.caption(
                            "⚠️ This is AI-generated analysis and not a substitute for professional medical advice."
                        )

                else:

                    st.error("Something went wrong. Please try again.")

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Backend server is not running.\n\nRun:\n\nuvicorn backend.main:app --reload"
                )

            except Exception as e:

                st.error(f"Error: {e}")