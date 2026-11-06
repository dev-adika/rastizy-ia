from flask import Flask, request, session
import urllib.request, urllib.parse, json, random, os
app = Flask(__name__)
app.secret_key = "rastizy_ia_v5_final"
GROQ_KEY = ""

QUIZ_BAC = [
    {"q": "Cogito Ergo Sum, c'est qui ?", "options": ["Socrate", "Rene Descartes", "Platon", "Newton"], "rep": 1},
    {"q": "2x + 4 = 10, x = ?", "options": ["2", "3", "4", "6"], "rep": 1},
    {"q": "Capitale du Togo ?", "options": ["Atakpame", "Kara", "Lome", "Sokode"], "rep": 2},
    {"q": "F = ?", "options": ["m x v", "m x a", "m / a", "m + a"], "rep": 1},
    {"q": "Qui a ecrit L'Enfant Noir ?", "options": ["Camara Laye", "Senghor", "Cesar", "Achebe"], "rep": 0},
    {"q": "Le Togo est independant en ?", "options": ["1958", "1960", "1963", "1975"], "rep": 1},
    {"q": "Conjugue : Je (aller) a l'ecole", "options": ["vais", "vas", "va", "allons"], "rep": 0},
    {"q": "L'eau c'est ?", "options": ["H2O", "CO2", "O2", "NaCl"], "rep": 0},
]

# COMPTEUR - Pour savoir si tu as atteint 1000 utilisateurs
def compter_visite():
    try:
        if os.path.exists("compteur.txt"):
            with open("compteur.txt", "r") as f:
                n = int(f.read().strip() or 0)
        else:
            n = 0
        n += 1
        with open("compteur.txt", "w") as f:
            f.write(str(n))
        return n
    except:
        return 0

def appel_ia(prompt_system, texte_user):
    if GROQ_KEY and "gsk_" in GROQ_KEY:
        try:
            data = json.dumps({"model": "llama-3.3-70b-versatile","messages": [{"role": "system", "content": prompt_system},{"role": "user", "content": texte_user}]}).encode()
            req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=data, headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())["choices"][0]["message"]["content"]
        except Exception as e:
            print("Groq echoue :", e)
    try:
        url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt_system + " : " + texte_user)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            txt = r.read().decode("utf-8", errors="ignore").strip()
            if txt: return txt
    except Exception as e:
        print(e)
    return "Poto, verifie ta connexion et reessaie !"

def cerveau_universel(texte):
    prompt = """Tu es RAStizy_IA, le prof IA du Togo pour les lyceens. Tu fais TOUT dans une seule case.
Tu dois DETECTER tout seul ce que l'eleve veut :
- Si l'eleve dit "traduis / traduis en / translate" : Tu traduis. Langues possibles : Francais, Anglais, Allemand, Espagnol, Ewe. Donne : ✅ TRADUCTION + 🗣️ EXPLICATION des mots difficiles.
- Si l'eleve dit "corrige / corrige mon texte / fautes" : Tu corriges orthographe, grammaire, conjugaison. Donne : ✅ TEXTE CORRIGE + 📝 TES FAUTES expliquees + 💡 ASTUCE.
- Si l'eleve dit "fiche / fiche de revision / fiche BAC / prepare moi pour le BAC" : Tu fais une FICHE BAC complete : 📌 TITRE + 🎯 CE QU'IL FAUT RETENIR (5 points) + 📖 DEFINITIONS + 🧮 FORMULES/DATES + 💡 ASTUCE BAC + ❓ 3 QUESTIONS TYPE BAC avec reponses + ✅ PIEGES A EVITER.
- Si l'eleve dit "resume / resume mon cours" : Tu resumes en 5 points cles simples + 1 question pour verifier.
- Si l'eleve dit "exercice / aide moi / explique moi / je comprends pas" : Tu expliques etape par etape SANS donner direct la reponse, avec un exemple.
- Sinon : Tu reponds comme un prof genial, francais simple, style poto, drole, 3-4 phrases, avec exemple du Togo.
Regle : Reponds TOUJOURS en francais simple, style poto, encourageant. Ne dis jamais "je ne peux pas"."""
    return appel_ia(prompt, texte)

@app.route("/", methods=["GET", "POST"])
def home():
    total_visites = compter_visite()
    reponse=""; quiz=None; score_msg=""
    if request.method=="POST":
        a=request.form.get("action")
        if a=="chat":
            reponse=cerveau_universel(request.form.get("question",""))
        elif a=="quiz":
            quiz=random.sample(QUIZ_BAC,4); session["quiz"]=quiz
        elif a=="corriger":
            quiz=session.get("quiz",[]); score=0
            for i,item in enumerate(quiz):
                rep=request.form.get(f"q{i}")
                if rep is not None and int(rep)==item["rep"]: score+=1
            score_msg=f"TU AS EU {score} / 4 poto ! {'PARFAIT 🏆' if score==4 else 'Continue 💪' if score>=2 else 'On va progresser 📚'}"

    h="<html><head><meta name='viewport' content='width=device-width, initial-scale=1'></head><body style='background:#0f0f0f; text-align:center; font-family:Arial; color:white; padding:15px; margin:0;'><h1>🔥 RAStizy_IA 🔥</h1><p>Le Prof IA du Togo pour les Lyceens ! 🇹🇬</p><div style='background:white; color:black; max-width:700px; margin:auto; padding:25px; border-radius:20px; text-align:left; box-shadow:0 0 20px #00ff88;'>"
    h+="<h3 style='text-align:center; font-size:22px;'>✨ Ecris tout ici poto, RAStizy comprend tout ! ✨</h3><form method='POST'><input type='hidden' name='action' value='chat'><textarea name='question' style='width:100%; height:120px; padding:15px; border-radius:15px; border:3px solid #00ff88; font-size:16px; box-sizing:border-box;' placeholder='Ecris ce que tu veux ici...&#10;&#10;Exemples :&#10;- Traduis en Allemand : Je vais au marche&#10;- Corrige : je suis aller au marche hier&#10;- Fiche BAC : Philosophie, Cogito Ergo Sum&#10;- Resume mon cours : [colle ton cours]&#10;- Explique moi la photosynthese' required></textarea><br><br><button style='width:100%; background:#000; color:#00ff88; padding:16px; border:none; border-radius:15px; font-weight:bold; cursor:pointer; font-size:18px;'>🚀 Demander a RAStizy_IA</button></form>"
    h+="<div style='background:#f8f8f8; padding:12px; border-radius:10px; margin-top:15px; font-size:13px; line-height:1.8;'><b>💡 Tu peux ecrire :</b><br>🌍 <b>Traduis</b> en Anglais / Francais / Allemand / Espagnol / Ewe<br>✍️ <b>Corrige :</b> ton texte avec fautes<br>🎓 <b>Fiche BAC :</b> Matiere + Chapitre<br>📚 <b>Resume :</b> colle ton cours<br>🧮 <b>Explique-moi :</b> n'importe quelle notion<br>💬 <b>Question :</b> n'importe quelle question de cours</div>"
    if reponse: h+=f"<div style='background:#eafff2; padding:18px; border-radius:15px; white-space:pre-wrap; margin-top:20px; line-height:1.7; font-size:15px; border-left:5px solid #00ff88;'>{reponse}</div>"
    h+="<hr><h3 style='text-align:center;'>🎯 Quiz BAC rapide</h3><form method='POST' style='text-align:center;'><input type='hidden' name='action' value='quiz'><button style='background:#00ff88; color:black; padding:12px 25px; border:none; border-radius:10px; font-weight:bold; cursor:pointer;'>🎯 Lancer un Quiz</button></form>"
    if quiz and not score_msg:
        h+="<form method='POST'><input type='hidden' name='action' value='corriger'>"
        for i,item in enumerate(quiz):
            h+=f"<p><b>{i+1}. {item['q']}</b></p>"
            for j,opt in enumerate(item["options"]):
                h+=f"<label style='display:block; padding:5px;'><input type='radio' name='q{i}' value='{j}' required> {opt}</label>"
        h+="<br><button style='background:#000; color:white; padding:12px 25px; border:none; border-radius:10px;'>Corriger</button></form>"
    if score_msg: h+=f"<p style='background:#fff3cd; padding:15px; border-radius:10px; font-weight:bold; text-align:center;'>{score_msg}</p>"
    h+="</div><p>RAStizy_IA - Made in Togo 🇹🇬 | Une seule case, tout faire !</p></body></html>"
    return h

@app.route("/stats-poto")
def stats():
    try:
        with open("compteur.txt", "r") as f:
            total = f.read()
    except:
        total = "0"
    return f"<h1 style='text-align:center; font-family:Arial; margin-top:100px;'>🔥 RAStizy_IA 🔥<br><br>Nombre de visites : {total}<br><br>Objectif : 1000 !<br><br>{'🎉 TU AS REUSSI POTO !' if int(total) >= 1000 else 'Continue poto, tu y es presque ! 💪'}</h1>"

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)