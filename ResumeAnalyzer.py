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
    job_role = st.text_input("Enter the job role you are targetting.(Optional)")
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
    
    if analyze and uploaded_resume:
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
                You are an expert resume reviewer with years of experience in HR and recruitment.
                Please analyze this resume and provide constructive feedback.
                Focus on the following aspects:
                1. Content clarity and impact
                2. skills presentation
                3. Experience description
                4. specific improvements for {job_role if job_role else 'general job applications'}
                
                Resume content:
                {file_content}
                
                Please provide your analysis in a clear, structured format with specific recommandations in each section. 
                ###NO PREAMBLE
            """)
            
            chain = prompt | model
            responce = chain.invoke({file_content : job_role})
            st.markdown("### Analysis Result :")
            st.markdown(responce.content)
        except Exception as e:
            st.error(f"Error extracting content : {str(e)}")
            
if __name__ == "__main__":
    main()