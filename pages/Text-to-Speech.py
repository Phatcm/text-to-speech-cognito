import streamlit as st
import requests
import components.authenticate as authenticate

def media_player(url):
    html = f"""
        <audio controls style="width: 100%;">
            <source src={url} type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    """
    st.markdown(html, unsafe_allow_html=True)


# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    authenticate.button_logout()
else:
    authenticate.button_login()

if (st.session_state["authenticated"]):   
    st.markdown("<h1 style='text-align: center; color: red;'>My talking app</h1>", unsafe_allow_html=True)
    text = st.text_area("Input your text")
    st.write(f'You wrote {len(text)} characters.')
    
    if st.button("Let's speech"):
        response = requests.post("https://jekf9dmp49.execute-api.ap-northeast-1.amazonaws.com/prod", json = {"text":text})

        if response.status_code == 200:
            audio_url = response.text  # Assuming the response.text contains the audio URL
            media_player(audio_url)

        else:
            st.write("Error")
            st.write(response.text)
            
else:
    if st.session_state["authenticated"]:
        st.write("You do not have access. Please contact the administrator.")
    else:
        st.write("Please login!")

