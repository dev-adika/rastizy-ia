from flask import Flask, request, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<script src="https://cdn.counter.dev/script.js" data-id="b8b9f976-5f00-46b8-a3ae-f1bc6f64e648" data-utcoffset="0"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RAStizy_IA - Par ADIKA</title>
<style>
body{font-family:Arial;background:#0f3d1e;color:white;text-align:center;padding:15px;margin:0}
.card{background:white;color:#111;border-radius:20px;padding:20px;max-width:500px;margin:auto}
textarea{width:95%;height:100px;border-radius:10px;padding:10px;font-size:16px;border:2px solid #0f3d1e}
button{background:black;color:#00ff66;border:none;padding:14px 20px;border-radius:12px;font-size:17px;font-weight:bold;width:95%;margin-top:10px;cursor:pointer}
.btn-voice{background:#222;color:white}
.rep{background:#eaffef;border-left:5px solid #00cc66;padding:12px;border-radius:10px;margin-top:15px;text-align:left;min-height:60px;white-space:pre-wrap}
.quiz-btn{background:#00e676;color:black;padding:12px 20px;border-radius:20px;font-weight:bold;border:none;font-size:16px}
</style>
</head>
<body>
<h1>🔥 RAStizy_IA 🔥</h1>
<p>Créé par <b>ADIKA Amèvi Dodji</b> d'Aného au Togo 🇹🇬</p>

<div class="card">
<p><b>Ecris tout ici poto, RAStizy comprend tout !</b><br><br>
Exemples :<br>
- Traduis en Allemand : Je t'aime<br>
- Corrige : Je suis aller a l'école<br>
- Fiche BAC : Maths + Suites</p>

<textarea id="q" placeholder="Ex: C'est qui ton père ?"></textarea><br>
<button onclick="ask()">🚀 Demander a RAStizy_IA</button>
<button class="btn-voice" onclick="speak()">🔊 Écouter la réponse</button>

<div class="rep" id="rep">Ta réponse va s'afficher ici...</div>

<p>💡 <b>Tu peux ecrire :</b><br>
🌍 Traduis en Anglais / Francais / Allemand / Espagnol / Ewe<br>
✍️ Corrige : ton texte avec fautes<br>
🎓 Fiche BAC : Matiere + Chapitre<br>
📚 Resume : colle ton cours<br>
🧠 Explique-moi : n'importe quelle notion<br>
💬 Question : n'importe quelle question de cours</p>

<hr>
<h2>🎯 Quiz BAC rapide</h2>
<button class="quiz-btn" onclick="quiz()">🎯 Lancer un Quiz</button>
<div class="rep" id="quizBox" style="display:none"></div>

</div>
<p style="margin-top:15px">RAStizy_IA - Made in Togo 🇹🇬 | Une seule case, tout faire !</p>

<script>
let last = "";
async function ask(){
  let q = document.getElementById('q').value.trim();
  if(!q) return alert('Ecris quelque chose poto');
  document.getElementById('rep').innerText = 'RAStizy réfléchit...';
  try{
    let r = await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q:q})});
    let d = await r.json();
    last = d.rep;
    document.getElementById('rep').innerText = last;
  }catch(e){
    document.getElementById('rep').innerText = 'Poto, réessaie, la connexion a coupé.';
  }
}
function speak(){
  if(!last) return alert('Demande d’abord poto');
  let u = new SpeechSynthesisUtterance(last);
  u.lang = 'fr-FR';
  speechSynthesis.speak(u);
}
async function quiz(){
  document.getElementById('quizBox').style.display='block';
  document.getElementById('quizBox').innerText='Chargement du Quiz...';
  let r = await fetch('/quiz');
  let d = await r.json();
  document.getElementById('quizBox').innerHTML = '<b>Question :</b><br>'+d.q+'<br><br><button onclick="alert(\\''+d.rep+'\\')">Voir la réponse</button>';
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
    q = data.get('q','')
    q_low = q.lower()

    # 1. REPONSES LOCALES - SANS POLLINATIONS, TOUJOURS MARCHE
    if "ton père" in q_low or "ton pere" in q_low or "qui t'a créé" in q_low or "qui t'a cree" in q_low or "ton createur" in q_low or "ton créateur" in q_low:
        return jsonify({'rep': "Mon père, mon créateur, c'est ADIKA Amèvi Dodji d'Aného au Togo. C'est lui qui m'a créé, c'est mon père !"})
    if "qui es-tu" in q_low or "qui es tu" in q_low or "tu es qui" in q_low or "ton nom" in q_low or "c'est qui rastizy" in q_low:
        return jsonify({'rep': "Je suis RAStizy_IA ! Le Prof IA du Togo. Mon père, mon créateur, c'est ADIKA Amèvi Dodji d'Aného."})
    if "bonjour" in q_low or "salut" in q_low or "yo " in q_low:
        return jsonify({'rep': "Salut poto ! C'est RAStizy, créé par ADIKA Amèvi Dodji. Dis-moi ce que tu veux : Traduis, Corrige, Fiche BAC, Résumé, Explique-moi. Je gère tout !"})

    # 2. SINON ON APPELLE POLLINATIONS
    try:
        prompt = f"Tu es RAStizy_IA, un prof IA du Togo, créé par ADIKA Amèvi Dodji d'Aného. Réponds en français simple, comme un poto, clair et court. Question de l'élève : {q}"
        url = "https://text.pollinations.ai/" + requests.utils.quote(prompt)
        r = requests.get(url, timeout=25)
        if r.status_code == 200 and r.text.strip():
            return jsonify({'rep': r.text.strip()})
        else:
            return jsonify({'rep': "Poto, Pollinations est fatigué. Repose ta question dans 20 secondes, ça va marcher."})
    except Exception as e:
        return jsonify({'rep': "Poto, la connexion a coupé. Repose ta question, je suis là. Si c'est pour ton père, demande : C'est qui ton père ?"})

@app.route('/quiz')
def quiz():
    return jsonify({'q': "Quelle est la capitale du Togo ? A) Lomé B) Aného C) Kara", 'rep': "La réponse est A) Lomé poto !"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
