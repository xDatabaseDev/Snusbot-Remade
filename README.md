# Snusbase Discord Bot (Remake)

🎉 **Bienvenue dans le remake open-source du célèbre bot Discord du serveur [Snusbase](https://discord.gg/snusbase) !** 🎉

Ce projet a pour but de recréer le bot original de Snusbase, tout en le rendant accessible gratuitement et facilement personnalisable. Grâce à cette version, tu pourras gérer ton propre bot avec un système de crédits et d'administration.

---

## 🚀 **Fonctionnalités Principales**

- **💸 Système de Crédits :**  
  Gérez les crédits de vos utilisateurs avec le fichier `credits.json`. Chaque action de l'utilisateur consomme un certain nombre de crédits, que vous pouvez configurer selon vos besoins.

- **🔐 Système d'Administrateurs :**  
  Le fichier `admin.json` permet de définir les administrateurs du bot. Les admins ont accès à des commandes spéciales et peuvent gérer les crédits des utilisateurs.

- **📊 Tableau de Bord avec Emojis :**  
  Le bot utilise des emojis pour rendre l'expérience utilisateur plus agréable et plus claire dans les interactions.

---

## 📁 **Structure du Projet**

- `main.py` : Le fichier principal du bot.
- `credits.json` : Fichier où sont stockés les crédits des utilisateurs.
- `admin.json` : Fichier pour gérer les administrateurs.
- `credit_manager.py` : Fichier qui gère les crédits.


---

## 🛠 **Installation**

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/xDatabaseDev/Snusbot-Remade
   cd Snusbot-Remade
   ```

2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez le fichier `admin.json` avec vos id admins.
   ```json
   {
    "admins": [
        "ton id admin",
        "ton 2eme id admin",
        "ect"
       ]
   }
   ```

5. Lancez le bot :
   ```bash
   python bot.py
   ```


---

## ⚙️ **Configuration**

Le bot peut être configuré selon vos préférences en modifiant quelques lignes de code dans le fichier `bot.py` :

### 1. **Changer le Préfixe des Commandes**

Le préfixe utilisé pour les commandes du bot peut être modifié à la ligne **19** du fichier `bot.py`. Par défaut, le préfixe est défini comme `"-"`, mais vous pouvez le personnaliser à votre convenance.

```python
bot = commands.Bot(command_prefix="-", intents=discord.Intents.all(), help_command=None, activity=discord.Streaming(name="Snusbot by xDatabase", url="https://www.twitch.tv/rickyrollstar"), status=presence_type)
```

- Pour changer le préfixe, remplacez simplement `"-"` par le symbole ou le mot de votre choix.
  - Exemple pour changer le préfixe en `!` :
    ```python
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None, activity=discord.Streaming(name="Snusbot by xDatabase", url="https://www.twitch.tv/rickyrollstar"), status=presence_type)
    ```

### 2. **Configurer le Token du Bot**

Le token de votre bot Discord doit être renseigné à la ligne **462** du fichier `bot.py`. Ce token est requis pour que le bot puisse se connecter à Discord.

```python
bot.run("Ton token")
```

- Remplacez `"Ton token"` par votre propre token de bot Discord.
  - Exemple :
    ```python
    bot.run("VOTRE_TOKEN_DISCORD_ICI")
    ```

⚠️ **Important :**  
Ne partagez jamais votre token publiquement, car il permet à n'importe qui de contrôler votre bot.

---

Avec cette section de configuration, les utilisateurs sauront exactement où et comment modifier les paramètres du bot, notamment le préfixe et le token.

## 🔧 **Utilisation**

- **Commande pour vérifier vos crédits :**
  ```
  -balance
  ```

- **Commande pour ajouter des crédits à un utilisateur (admin uniquement) :**
  ```
  -addcr user_id 100
  ```

- **Commande pour rechercher dans Snusbase :**
  ```
  -snusbase query
  ```

---

## 👥 **Contributions**

Les contributions sont les bienvenues ! Si tu souhaites améliorer le projet, n'hésite pas à soumettre des pull requests, mettre des star ou à ouvrir des issues.

---

## 📜 **Licence**

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## ❤️ **Remerciements**

Merci à [Snusbase](https://discord.gg/snusbase) pour l'inspiration ! Ce projet n'est pas affilié directement à Snusbase, mais vise à rendre leur bot accessible à tous.

---
