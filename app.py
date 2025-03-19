import requests
from flask import Flask, request
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_opengraph_data(url):
    """ OpenGraph 데이터를 가져와 HTML을 반환 """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
    except requests.exceptions.RequestException as e:
        return f"<p style='text-align:center;'>❌ 정보를 불러올 수 없습니다. 오류: {str(e)}</p>"

    soup = BeautifulSoup(response.text, "html.parser")

    # OpenGraph 데이터 추출
    title = soup.find("meta", property="og:title")
    description = soup.find("meta", property="og:description")
    image = soup.find("meta", property="og:image")
    image_alt = soup.find("meta", property="og:image:alt")

    title = title["content"] if title else "제목 없음"
    description = description["content"] if description else "설명 없음"
    image = image["content"] if image else "https://via.placeholder.com/100"
    image_alt = image_alt["content"] if image_alt else title

    html = f"""
    <div style="display: flex; align-items: center; border: 2px solid #007bff; 
                border-radius: 10px; padding: 15px; background-color: #f8f9fa;
                box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1); width: 100%; max-width: 600px;">
        <img src="{image}" alt="{image_alt}" style="width: 90px; height: 90px; 
                    object-fit: cover; border-radius: 10px; margin-right: 15px; border: 2px solid #007bff;">
        <div>
            <h3 style="font-size: 18px; margin: 0; color: #007bff;">{title}</h3>
            <p style="font-size: 14px; color: #555; margin: 5px 0 0;">{description}</p>
        </div>
    </div>
    """
    
    return html

@app.route("/opengraph", methods=["GET"])
def opengraph():
    url = request.args.get("url")
    if not url:
        return "<p>⚠️ URL이 제공되지 않았습니다.</p>", 400

    return get_opengraph_data(url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
