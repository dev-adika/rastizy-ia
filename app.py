
from flask import Flask, request, jsonify, render_template_string
import requests, urllib.parse, time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAStizy_IA - Le Prof IA du Togo</title>
<style>
*{box-sizing:border-box}
body{font-family:Arial;background:#FFF7ED;margin:0}
header{background:#EA580C;color:white;padding:20px;text-align:center}
header h1{margin:0}
.container{max-width:750px;margin:auto;padding:15px}
.bac{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px;margin:15px 0}
.bac button{padding:12px 5px;border:none;border-radius:12px;background:white;box-shadow:0 2px 5px #ddd;font-weight:bold;cursor:pointer;font-size:13px}
.bac button.active{background:#EA580C;color:white}
.box{background:white;padding:18px;border-radius:18px;box-shadow:0 0 15px #ddd}
textarea{width:100%;height:75px;padding:12px;border-radius:12px;border:1.5px solid #FDBA74;font-size:16px}
.btn-main{width:100%;padding:15px;background:#EA580C;color:white;border:none;border-radius:12px;font-size:18px;font-weight:bold;margin-top:10px}
.btn-voice{width:100%;padding:12px;background:#16A34A;color:white;border:none;border-radius:12px;font-size:16px;font-weight:bold;margin-top:8px}
#reponse{margin-top:15px;background:#FFFBEB;padding:15px;border-radius:12px;white-space:pre-wrap;min-height:100px;line-height:1.6}
.footer{text-align:center;color:#888;font-size:13px;margin:20px}
</style>
</head>
<body>
<header><h1>🇹🇬 RAStizy_IA</h1><p>Le Prof IA du Togo - Créé par ADIKA Amèvi Dodji</p></header>
<div class="container">
<div class="bac">
<button onclick="setMatiere(this,'Maths')">📐 Maths</button>
<button onclick="setMatiere(this,'Physique')">⚗️ Physique</button>
<button onclick="setMatiere(this,'SVT')">🧬 SVT</button>
<button onclick="setMatiere(this,'Français')">📖 Français</button>
<button onclick="setMatiere(this,'Philosophie')">🤔 Philo</button>
<button onclick="setMatiere(this,'Histoire-Géo')">🌍 Hist-Géo</button>
<button onclick="setMatiere(this,'Anglais')">🇬🇧 Anglais</button>
<button onclick="setMatiere(this,'Allemand')">🇩🇪 Allemand</button>
</div>
<div class="box">
<textarea id="q" placeholder="Pose ta question ici..."></textarea>
<button class="btn-main" onclick="demander()">✨ Demander à RAStizy_IA</button>
<button class="btn-voice" onclick="lire()">🔊 Écouter la réponse</button>
<div id="reponse">Pose ta question poto...</div>
</div>
<p class="footer">Créé à Aného, Togo 🇹🇬 par ADIKA Amèvi Dodji - Pour tout le monde</p>
</div>
<script>
let matiere = "Cours général";
function setMatiere(btn, m){ matiere = m; document.querySelectorAll('.bac button').forEach(b=>b.classList.remove('active')); btn.classList.add('active'); }
async function demander(){
  let q = document.getElementById('q').value;
  let r = document.getElementById('reponse');
  if(!q){ r.innerText = "Écris d'abord ta question poto !"; return; }
  r.innerText = "RAStizy réfléchit... attends un peu poto...";
  try{
    let res = await fetch('/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message: q, matiere: matiere})});
    let data = await res.json();
    r.innerText = data.reply;
  }catch(e){ r.innerText = "Oups, réessaie poto."; }
}
function lire(){
  let texte = document.getElementById('reponse').innerText;
  window.speechSynthesis.cancel();
  let voix = new SpeechSynthesisUtterance(texte);
  voix.lang = 'fr-FR'; window.speechSynthesis.speak(voix);
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json() or {}
    question = data.get('message') or ""
    matiere = data.get('matiere') or "Cours général"
    if not question:
        return jsonify({"reply": "Pose-moi une question poto !"})
    
    q_low = question.lower()
    
    # REPONSE DIRECTE - PAPA
    if any(mot in q_low for mot in ["ton père", "ton pere", "qui t'a créé", "qui t'a cree", "qui t'a fait", "ton créateur", "ton createur", "qui est ton papa", "ton papa"]):
        return jsonify({"reply": "Mon père c'est ADIKA Amèvi Dodji d'ayata Togo ! C'est lui qui m'a créé. C'est mon papa, mon créateur, mon poto numéro 1. Respect à lui ! 🇹🇬"})
    
    if "adika" in q_low:
        return jsonify({"reply": "ADIKA Amèvi Dodji, c'est mon père ! C'est lui qui m'a créé à Aného au Togo. C'est grâce à lui que j'existe pour aider tout le monde. C'est le meilleur papa !"})
    
    if any(mot in q_low for mot in ["qui es-tu", "qui es tu", "tu t'appelles", "ton nom", "c'est quoi ton nom"]):
        return jsonify({"reply": "Moi c'est RAStizy_IA ! Le Prof IA du Togo. Mon père c'est ADIKA Amèvi Dodji d'Aného. Je suis là pour t'aider en Maths, Physique, SVT, Français, Philo, tout ! Pose-moi ta question poto !"})

    prompt = f"Tu es RAStizy_IA, prof IA du Togo pour tout le monde. Ton père est ADIKA Amèvi Dodji. Tu ne poses JAMAIS de quiz, JAMAIS d'exercice à la fin. Tu ne dis JAMAIS que tu es créé par OpenAI. Matière: {matiere}. Parle français simple. Question: {question}"
    url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt)
    for essai in range(3):
        try:
            res = requests.get(url, timeout=90)
            if res.status_code == 200 and len(res.text) > 10:
                return jsonify({"reply": res.text})
            time.sleep(3)
        except:
            time.sleep(3)
    return jsonify({"reply": "Attends 20 secondes et repose ta question poto, Pollinations est chargé."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
