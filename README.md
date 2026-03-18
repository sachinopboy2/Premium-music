<h2 align="center">
    「 𝕻𝖗𝖊𝖒𝖎𝖚𝖒 𝕸𝖚𝖘𝖎𝖈 」
</h2>

<p align="center">
  <img src="https://i.ibb.co/XbQ3tB6/Nobita-Premium-Banner.png" alt="Nobita Premium Music Banner" width="100%">
</p>

---

### DEPLOYMENT

Aap is bot ko niche diye gaye tarikon se deploy kar sakte hain. VPS use kar rahe hain toh neeche instructions follow karein. Heroku deploy ke liye bhi instructions available hain.

<h3 align="center">
    ─「 DEPLOY ON VPS 」─
</h3>

<details>
<summary><b>Click to see VPS Commands</b></summary>

```console
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3-pip ffmpeg -y
pip3 install -U pip
curl -fssL [https://deb.nodesource.com/setup_20.x](https://deb.nodesource.com/setup_20.x) | sudo -E bash - && sudo apt-get install nodejs -y && npm i -g npm
git clone [https://github.com/sachinopboy2/Premium-music](https://github.com/sachinopboy2/Premium-music) && cd Premium-music
pip3 install -U -r requirements.txt
cp sample.env .env
vi .env
# Edit your .env file with your API_ID, API_HASH, and BOT_TOKEN
python3 -m Premium-music
