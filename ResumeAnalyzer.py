import streamlit as st
import PyPDF2
import io
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
Grok_api_key = "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"
def main():
    st.set_page_config(page_title="AI Resume Analyzer",layout="centered")
    st.title("AI Resume Analyzer")
    st.markdown("Upload your resume and get insights as per your requirements !!")
    uploaded_resume = st.file_uploader("Upload your resume(PDF)",type=["pdf"])
    job_role = st.text_input("Enter the job role you are targetting.")
    analyze = st.button("Analyze Resume.")
    
    def extract_text_from_pdf(pdf_file):
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def extract_text_from_file(uploaded_resume):
        if uploaded_resume.type == "application/pdf":
            return extract_text_from_pdf(io.BytesIO(uploaded_resume.read()))
    
    if analyze and uploaded_resume and job_role:
        try:
            file_content = extract_text_from_file(uploaded_resume)
            
            if not file_content.strip():
                st.error("File does not have any content !!")
                st.stop()

            model = ChatGroq(
                temperature = 0,
                groq_api_key = Grok_api_key,
                model_name = "llama-3.3-70b-versatile"
            )
            
            prompt = PromptTemplate.from_template(f"""
                ###NO PREAMBLE
                You are an expert HR professional and ATS system evaluator.

                Analyze the resume for the following:
                1. Content clarity and overall impact.
                2. Presentation and structure of skills.
                3. Relevance and clarity of work experience.
                4. Tailoring for the specific job role: **{job_role}**.
                5. ATS Compatibility:
                   - Use of standard section headers like "Education", "Experience", etc.
                   - Use of plain formatting (no tables or images).
                   - Presence of keywords relevant to the job role.
                   - Bullet points and consistent structure.
                   - Proper use of fonts, headings, and no graphics.
                
                Resume Content:
                {file_content}

                Please return your analysis in the following format:
                - Section-by-section feedback.
                - ATS Compatibility Score (out of 100).
                - Resume Optimization Score for the job role (out of 100).
                - Final Recommendation Summary.
                """)

            
            chain = prompt | model
            responce = chain.invoke({file_content : job_role})
            st.markdown("### Analysis Result :")
            st.markdown(responce.content)
        except Exception as e:
            st.error(f"Error extracting content : {str(e)}")
            
if __name__ == "__main__":
    main()
