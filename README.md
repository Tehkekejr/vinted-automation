> [!CAUTION]
> ## ⚠️ AVERTISSEMENT IMPORTANT - RISQUE DE BAN
>
> **Ce script automatise Vinted et VIOLE leurs conditions d'utilisation.**
>
> **RISQUES :**
> - 🚫 **Suspension ou BAN PERMANENT de votre compte Vinted**
> - 🚫 **Perte définitive de l'accès à vos annonces et messages**
> - 🚫 **Blocage de votre numéro de téléphone et email**
>
> **UTILISEZ CE SCRIPT À VOS PROPRES RISQUES. L'auteur n'est pas responsable des conséquences.**
>
> Ce repository est **privé** et **uniquement à des fins éducatives**.

# vinted-automation

Script Python pour automatiser la description et l'upload de vêtements sur Vinted

## 🎯 Fonctionnalités

- ✅ **Connexion automatique** à Vinted
- ✅ **Génération automatique** de descriptions structurées
- ✅ **Upload de photos** multiples par article
- ✅ **Remplissage automatique** de tous les champs (titre, description, prix, marque, taille, couleur, état)
- ✅ **Upload par lot** : ajoutez plusieurs articles via un fichier JSON
- ✅ **Gestion des erreurs** et logs pour un débogage facile

## 💻 Prérequis

- Python 3.7 ou supérieur
- Chrome ou Chromium installé
- ChromeDriver (téléchargez la version correspondant à votre navigateur)

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/Tehkekejr/vinted-automation.git
cd vinted-automation
```

### 2. Installer les dépendances

```bash
pip install selenium
```

### 3. Configurer vos identifiants

Créez un fichier `config.json` basé sur le fichier d'exemple :

```bash
cp config.example.json config.json
```

Modifiez `config.json` avec vos identifiants Vinted :

```json
{
  "email": "votre-email@exemple.com",
  "password": "votre-mot-de-passe"
}
```

**⚠️ IMPORTANT** : Ne commitez jamais votre fichier `config.json` avec vos vrais identifiants !

### 4. Préparer vos articles

Créez un fichier `items.json` avec vos articles à uploader :

```json
[
  {
    "title": "T-shirt Nike noir taille M",
    "brand": "Nike",
    "type": "T-shirt",
    "size": "M",
    "color": "Noir",
    "condition": "Très bon état",
    "description": "T-shirt Nike en coton, peu porté, comme neuf.",
    "price": 15,
    "photos": [
      "photos/tshirt_nike_1.jpg",
      "photos/tshirt_nike_2.jpg"
    ]
  }
]
```

## 📈 Utilisation

### Lancer le script

```bash
python vinted_automation.py
```

Le script va :
1. Ouvrir Chrome automatiquement
2. Se connecter à votre compte Vinted
3. Lire le fichier `items.json`
4. Uploader chaque article un par un
5. Afficher le résultat dans la console

### Format des données

#### Champs obligatoires :
- `title` : Le titre de l'annonce
- `price` : Le prix en euros

#### Champs recommandés :
- `brand` : La marque du vêtement
- `type` : Type d'article (T-shirt, Jean, Veste, etc.)
- `size` : Taille (S, M, L, XL, 36, 38, etc.)
- `color` : Couleur principale
- `condition` : État (Neuf, Très bon état, Bon état, etc.)
- `description` : Description personnalisée
- `photos` : Liste de chemins vers les photos (au format JPG ou PNG)

## 📝 Template de description

Le script génère automatiquement des descriptions structurées :

```
{Marque} - {Type}

Taille: {Taille}
Couleur: {Couleur}
État: {État}

{Description personnalisée}

Prix: {Prix}€
```

## ⚙️ Configuration avancée

### Mode headless

Pour exécuter le script sans ouvrir la fenêtre du navigateur, décommentez cette ligne dans `vinted_automation.py` :

```python
options.add_argument('--headless')
```

### Modifier le template de description

Éditez la méthode `generate_description()` dans le fichier `vinted_automation.py` pour personnaliser le format.

## 🔒 Sécurité

- **Ne partagez JAMAIS** votre fichier `config.json` avec vos identifiants
- Le fichier `config.json` est déjà ajouté au `.gitignore`
- Utilisez des mots de passe forts et uniques
- **Attention** : L'automatisation peut violer les conditions d'utilisation de Vinted. Utilisez ce script à vos propres risques.

## 🐛 Dépannage

### Le script ne trouve pas ChromeDriver

Téléchargez ChromeDriver depuis : https://chromedriver.chromium.org/
Assurez-vous qu'il est dans votre PATH ou dans le dossier du projet.

### Erreur de connexion

Vérifiez que vos identifiants dans `config.json` sont corrects.

### Les photos ne s'uploadent pas

Vérifiez que les chemins vers les photos sont corrects et que les fichiers existent.

## 📚 Exemple complet

Voici un fichier `items.json` complet avec 3 articles :

```json
[
  {
    "title": "T-shirt Nike noir taille M",
    "brand": "Nike",
    "type": "T-shirt",
    "size": "M",
    "color": "Noir",
    "condition": "Très bon état",
    "description": "T-shirt Nike en coton, peu porté, comme neuf. Parfait pour le sport ou la détente.",
    "price": 15,
    "photos": ["photos/nike1.jpg", "photos/nike2.jpg"]
  },
  {
    "title": "Jean Levi's 501 taille 32",
    "brand": "Levi's",
    "type": "Jean",
    "size": "32",
    "color": "Bleu",
    "condition": "Bon état",
    "description": "Jean Levi's 501 classique, coupe droite. Légères traces d'usure mais encore en excellent état.",
    "price": 35,
    "photos": ["photos/levis1.jpg", "photos/levis2.jpg", "photos/levis3.jpg"]
  },
  {
    "title": "Veste Adidas vintage taille L",
    "brand": "Adidas",
    "type": "Veste",
    "size": "L",
    "color": "Bleu et blanc",
    "condition": "Très bon état",
    "description": "Veste de survêtement Adidas vintage années 90. Pièce de collection en excellent état.",
    "price": 45,
    "photos": ["photos/adidas1.jpg", "photos/adidas2.jpg"]
  }
]
```

## 🔧 Technologies utilisées

- **Python 3** - Langage de programmation
- **Selenium** - Automatisation du navigateur
- **ChromeDriver** - Driver pour Chrome

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Avertissement

Ce script est fourni à des fins éducatives uniquement. L'automatisation de Vinted peut violer leurs conditions d'utilisation. Utilisez-le à vos propres risques. Les auteurs ne sont pas responsables d'une quelconque suspension ou ban de compte.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## ✨ Auteur

Créé avec ❤️ pour faciliter la vente sur Vinted

---

**Note** : Ce projet n'est pas affilié à Vinted.
