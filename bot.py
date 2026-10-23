
import os
import logging
from collections import Counter
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
historique = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue sur Tycho Aviator Crash IA !\n\n"
        "Ce bot enregistre les multiplicateurs que tu saisis "
        "et calcule des statistiques historiques.\n"
        "Il ne prédit pas les prochains résultats.\n\n"
        "Commandes : /ajouter 1.50, /stats, /historique, /analyse, /risques, /aide"
    )

async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/ajouter 1.50 — enregistrer un multiplicateur observé\n"
        "/stats — nombre de résultats et moyenne\n"
        "/historique — derniers résultats\n"
        "/analyse — répartition descriptive\n"
        "/risques — rappel des risques"
    )

async def ajouter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Utilise : /ajouter 1.50")
        return
    try:
        valeur = float(context.args[0].replace(",", "."))
        if valeur < 1 or valeur > 1000000:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Entre un multiplicateur valide, par exemple /ajouter 1.50")
        return
    historique.append(valeur)
    await update.message.reply_text(f"Résultat enregistré : {valeur:.2f}x")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not historique:
        await update.message.reply_text("Aucune donnée. Ajoute un résultat avec /ajouter 1.50")
        return
    moyenne = sum(historique) / len(historique)
    await update.message.reply_text(
        f"Résultats enregistrés : {len(historique)}\n"
        f"Moyenne historique : {moyenne:.2f}x\n"
        f"Minimum : {min(historique):.2f}x\n"
        f"Maximum : {max(historique):.2f}x"
    )

async def afficher_historique(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not historique:
        await update.message.reply_text("Historique vide. Utilise /ajouter 1.50")
        return
    lignes = "\n".join(f"{i+1}. {v:.2f}x" for i, v in enumerate(historique[-20:]))
    await update.message.reply_text("20 derniers résultats au maximum :\n" + lignes)

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not historique:
        await update.message.reply_text("Ajoute d'abord des résultats avec /ajouter 1.50")
        return
    groupes = {
        "< 2x": sum(v < 2 for v in historique),
        "2x à < 5x": sum(2 <= v < 5 for v in historique),
        "5x à < 10x": sum(5 <= v < 10 for v in historique),
        "10x et plus": sum(v >= 10 for v in historique),
    }
    texte = "\n".join(f"{nom} : {n}" for nom, n in groupes.items())
    await update.message.reply_text("Répartition des résultats saisis :\n" + texte)

async def risques(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Attention : les résultats Aviator/Crash ne sont pas prédictibles "
        "de façon fiable par ce bot. Les statistiques passées ne garantissent "
        "pas le prochain résultat. Ne mise jamais de l'argent nécessaire."
    )

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("La variable TELEGRAM_BOT_TOKEN doit être configurée sur l'hébergeur.")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aide", aide))
    app.add_handler(CommandHandler("ajouter", ajouter))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("historique", afficher_historique))
    app.add_handler(CommandHandler("analyse", analyse))
    app.add_handler(CommandHandler("risques", risques))
    app.run_polling()

if __name__ == "__main__":
    main()
