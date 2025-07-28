import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64


API_URL = "https://e0145e4a5418.ngrok-free.app/generate/"

st.title("Generating Wallpaper")

prompt = st.text_input("Enter your prompt") # 프롬프트 입력받기

if "image_base64_list" not in st.session_state:
    st.session_state.image_base64_list = []

if st.button("Generate"): # 버튼 생성

    st.session_state.image_base64_list = []

    if not prompt:
        st.warning("Please enter your prompt.")

    else :
        with st.spinner("Generating images.. It may take a few seconds."): 

            response = requests.post(API_URL, json= {"prompt": prompt})
            # st.write("API raw response:", response.text)
            
            if response.status_code == 200:
                #json 형식으로 응답 받기
                data = response.json()
                image_url = data.get("image_urls", []) #생성된 이미지 url 받아오기
                # st.write(response)

                if not image_url:
                    st.error("No images returned")
                
                else:
                    st.session_state.image_base64_list = []
                    
                    for i, url in enumerate(image_url):
                        

                        image_resp = requests.get(url) #url에서 이미지 받아오기
                        

                        if image_resp.status_code == 200:
                            try:
                                image = Image.open(BytesIO(image_resp.content)) # 이미지 데이터를 PIL.Image 객체로 변환
                                buf = BytesIO()
                                image.save(buf, format="PNG")
                                byte_data = buf.getvalue()
                                b64_encoded = base64.b64encode(byte_data).decode('utf-8')
                                st.session_state.image_base64_list.append(b64_encoded)
                                
                            except Exception as e:
                                st.error(f"Image {i+1} falied to open: {e}")
                            
                        else :
                            st.warning(f"Image {i+1} failed to load from URL : {url}")

            else :
                st.error(f"API request failed. Status code : {response.status_code}")

# 이미지 출력 + 다운로드 버튼 생성
if st.session_state.image_base64_list:
    st.text("Generated successfully.")

    for i, b64_data in enumerate(st.session_state.image_base64_list):
        byte_data = base64.b64decode(b64_data)
        image = Image.open(BytesIO(byte_data))
        st.image(image, caption=f"Image {i+1}")

        st.download_button(
            label=f"Download Image {i+1}",
            data=byte_data,
            file_name=f"generaged_image_{i+1}.png",
            mime="image/png"
        )
