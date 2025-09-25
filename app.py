# import streamlit as st
# import pandas as pd

# # Title
# st.title("Aluminum Doors/Fences Rules Engine")

# # File upload
# uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

# if uploaded_file:
#     # Read uploaded Excel
#     df = pd.read_excel(uploaded_file)
#     st.subheader("Original Data")
#     st.dataframe(df)

#     # Apply rules (same as Step 1)
#     df['_notes'] = ''
#     for idx, row in df.iterrows():
#         # Rule 1: Default frame color
#         if pd.isna(row['frame_color']) or row['frame_color'].strip() == '':
#             df.at[idx, 'frame_color'] = 'Black'
#             df.at[idx, '_notes'] += 'frame_color_default;'
#         # Rule 2: Hinges based on height
#         if row['height'] > 2000:
#             df.at[idx, 'hinges'] = 4
#             df.at[idx, '_notes'] += 'hinges_4;'
#         else:
#             df.at[idx, 'hinges'] = 3
#             df.at[idx, '_notes'] += 'hinges_3;'

#     st.subheader("Processed Data")
#     st.dataframe(df)

#     # Download processed file
#     output_file = "processed_doors.xlsx"
#     df.to_excel(output_file, index=False)
#     st.download_button(
#         label="Download Processed Excel",
#         data=open(output_file, "rb").read(),
#         file_name="processed_doors.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )


import streamlit as st
import pandas as pd
import openai

# ----------------------
# Setup OpenAI API Key
# ----------------------
# Either set your API key here or use Streamlit secrets
openai.api_key = "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"

# ----------------------
# App Title
# ----------------------
st.title("Aluminum Doors & Fences Automation")

# ----------------------
# Section 1: Upload Excel & Apply Rules
# ----------------------
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Original Data")
    st.dataframe(df)

    # Apply rules (Step 1)
    df['_notes'] = ''
    for idx, row in df.iterrows():
        if pd.isna(row['frame_color']) or row['frame_color'].strip() == '':
            df.at[idx, 'frame_color'] = 'Black'
            df.at[idx, '_notes'] += 'frame_color_default;'
        if row['height'] > 2000:
            df.at[idx, 'hinges'] = 4
            df.at[idx, '_notes'] += 'hinges_4;'
        else:
            df.at[idx, 'hinges'] = 3
            df.at[idx, '_notes'] += 'hinges_3;'

    st.subheader("Processed Data")
    st.dataframe(df)

    # Download processed Excel
    output_file = "processed_doors.xlsx"
    df.to_excel(output_file, index=False)
    st.download_button(
        label="Download Processed Excel",
        data=open(output_file, "rb").read(),
        file_name="processed_doors.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ----------------------
    # Section 2: ChatGPT Query
    # ----------------------
    st.subheader("Ask about your doors/fences")
    question = st.text_input("Type your question here:")

    if st.button("Get Answer") and question:
        context_text = df.head(10).to_string()  # top 10 rows as context
        prompt = f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer concisely."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            answer = response.choices[0].message.content
            st.success(answer)
        except Exception as e:
            st.error(f"Error communicating with OpenAI: {e}")
