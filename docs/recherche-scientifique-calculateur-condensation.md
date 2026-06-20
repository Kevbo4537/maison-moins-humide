# Recherche scientifique — calculateur point de rosée / condensation MMH

Date : 2026-06-20

Objectif : préparer un calculateur simple pour le grand public, mais fondé sur des bases physiques et sanitaires solides. L’outil doit orienter, pas poser un diagnostic définitif de bâtiment.

---

## 1. Sources retenues

### Sources institutionnelles / santé

1. **WHO — Guidelines for Indoor Air Quality: Dampness and Mould**  
   URL : https://www.who.int/publications/i/item/9789289041683  
   Point clé : l’OMS relie humidité du bâti, moisissures et effets respiratoires. Le document insiste sur la maîtrise de l’humidité comme moyen de prévention.

2. **Institute of Medicine / National Academies — Damp Indoor Spaces and Health**  
   URL : https://www.ncbi.nlm.nih.gov/books/NBK215643/  
   Point clé : les espaces intérieurs humides favorisent moisissures et agents microbiens ; le lien avec plusieurs symptômes respiratoires est suffisamment documenté.

3. **EPA — A Brief Guide to Mold, Moisture and Your Home**  
   URL : https://www.epa.gov/mold/brief-guide-mold-moisture-and-your-home  
   Point clé utilisable grand public : garder l’humidité relative intérieure sous 60 %, idéalement entre 30 et 50 %. Mesurer avec un hygromètre.

4. **CDC / NIOSH — Mold in the Workplace**  
   URL : https://www.cdc.gov/niosh/mold/about/index.html  
   Point clé : l’humidité prolongée et une humidité relative élevée peuvent entraîner une humidité excessive ; l’humidité permet aux moisissures de se développer sur matériaux et surfaces.

5. **Fisk, Lei, Mendell — Association of residential dampness and mold with respiratory tract infections and bronchitis: a meta-analysis**  
   PMID : 21078183  
   Point clé : revue/meta-analyse utile pour rappeler que l’humidité et la moisissure dans l’habitat ne sont pas qu’un problème esthétique.

### Sources physique du calcul

6. **Alduchov & Eskridge — Improved Magnus Form Approximation of Saturation Vapor Pressure**  
   DOI : 10.1175/1520-0450(1996)035<0601:IMFAOS>2.0.CO;2  
   Point clé : formule de Magnus améliorée pour la pression de vapeur saturante, suffisamment précise pour un calculateur grand public.

7. **Littérature bâtiment / hygrothermie**  
   Références utiles repérées : modèles de croissance de moisissures selon humidité relative de surface et température, notamment travaux de type Sedlbauer, Viitanen, et articles Building and Environment.  
   Point clé à retenir prudemment : le risque de moisissure dépend surtout de l’humidité à la surface du matériau, de la température, de la durée, du matériau et de la présence de nutriments. Un seuil de surface autour de 80 % d’humidité relative est souvent utilisé comme repère de vigilance, mais la durée d’exposition compte.

---

## 2. Ce que le calculateur doit expliquer simplement

Un logement peut avoir un taux d’humidité qui semble “moyen”, mais condenser quand même si une surface est froide.

Exemple :

- air de la chambre : 19 °C ;
- humidité relative : 70 % ;
- mur ou vitre : 13 °C.

Calcul :

- point de rosée ≈ 13,4 °C ;
- surface à 13 °C = sous le point de rosée ;
- humidité relative au contact de la surface ≈ 103 %.

Résultat utilisateur : risque élevé de condensation sur cette surface.

Phrase pédagogique :

> L’air de la pièce peut sembler seulement “humide”, mais au contact d’un mur ou d’une vitre froide il atteint presque 100 % d’humidité. L’eau peut alors se déposer sur la surface.

---

## 3. Données à demander à l’utilisateur

Le questionnaire doit rester court. Deux modes : **simple** et **précis**.

### Mode simple — 6 questions

1. **Pièce concernée**
   - chambre ;
   - salle de bain ;
   - cuisine ;
   - cave / sous-sol ;
   - buanderie ;
   - placard ;
   - autre.

2. **Température de l’air dans la pièce**
   - valeur en °C ;
   - aide : lire sur thermomètre/hygromètre.

3. **Humidité relative mesurée**
   - valeur en % ;
   - aide : lire sur hygromètre ; éviter une mesure juste après douche/cuisson si on veut l’état habituel.

4. **Surface froide mesurée ?**
   - oui, j’ai une température de mur/vitre ;
   - non, je ne l’ai pas.

5. **Symptôme principal**
   - vitre embuée ou qui coule ;
   - mur froid / angle noir ;
   - odeur de moisi ;
   - moisissure visible ;
   - linge qui sèche mal ;
   - salpêtre / peinture qui cloque ;
   - eau après pluie ou fuite possible.

6. **Fréquence**
   - ponctuel après douche/cuisson ;
   - surtout le matin ;
   - plusieurs jours par semaine ;
   - presque permanent ;
   - aggravé quand il pleut.

### Mode précis — si l’utilisateur peut mesurer une surface

7. **Température de la surface froide**
   - vitre, mur, angle, plafond, sol de cave ;
   - valeur en °C ;
   - précision : mesure approximative, idéalement avec thermomètre infrarouge, en évitant surface brillante ou en tenant compte de l’émissivité.

8. **Surface concernée**
   - fenêtre ;
   - mur extérieur ;
   - angle ;
   - plafond ;
   - sol ;
   - meuble contre mur ;
   - autre.

9. **Ventilation**
   - VMC présente et fonctionne ;
   - VMC absente ;
   - bouche bouchée / faible aspiration ;
   - aération manuelle seulement ;
   - je ne sais pas.

10. **Signaux d’alerte bâtiment**
   - salpêtre ;
   - mur mouillé au toucher ;
   - trace après pluie ;
   - fuite connue ;
   - moisissure étendue ;
   - aucun.

---

## 4. Calculs à intégrer

### 4.1 Point de rosée

Formule de Magnus, adaptée au grand public :

```text
gamma = ln(RH / 100) + (a × T) / (b + T)
Td = (b × gamma) / (a - gamma)
```

Avec :

- `T` = température de l’air en °C ;
- `RH` = humidité relative en % ;
- `Td` = point de rosée en °C ;
- constantes recommandées : `a = 17,625`, `b = 243,04 °C`.

### 4.2 Humidité absolue approximative

Utile pour expliquer la quantité d’eau dans l’air :

```text
pression_vapeur_hPa = RH/100 × 6,1094 × exp((17,625 × T) / (243,04 + T))
humidité_absolue_g_m3 = 216,7 × pression_vapeur_hPa / (T + 273,15)
```

À afficher en secondaire, pas en résultat principal.

### 4.3 Écart surface / point de rosée

Si l’utilisateur donne une température de surface :

```text
écart = température_surface - point_de_rosée
```

Interprétation :

- écart ≤ 0 °C : condensation possible maintenant ;
- 0 à 2 °C : surface très proche du point de rosée, risque élevé avec marge d’erreur ;
- 2 à 4 °C : à surveiller, surtout si le problème revient souvent ;
- > 4 °C : risque direct plus faible au moment de la mesure.

Pourquoi garder une marge : les hygromètres grand public peuvent avoir plusieurs points d’erreur, et une surface n’a pas une température parfaitement uniforme.

### 4.4 Humidité relative au niveau de la surface

Très utile pour expliquer le risque de moisissure sans attendre la condensation visible :

```text
pression_vapeur_air = pression réelle calculée avec T air + RH air
pression_saturation_surface = saturation calculée à la température de surface
RH_surface = 100 × pression_vapeur_air / pression_saturation_surface
```

Interprétation prudente :

- < 75 % : risque faible au moment de la mesure ;
- 75 à 80 % : zone de vigilance ;
- 80 à 90 % : risque de moisissure si cela dure ou revient souvent ;
- 90 à 100 % : risque fort, surface très humide ;
- ≥ 100 % : condensation possible.

Important : ce n’est pas une preuve de moisissure. C’est un indicateur de conditions favorables.

---

## 5. Grille de résultat simple pour l’utilisateur

Le compte rendu doit sortir 1 résultat principal + 3 explications courtes.

### Niveau A — Situation correcte

Conditions typiques :

- humidité intérieure 40–60 % ;
- pas de symptôme inquiétant ;
- surface > point de rosée + 4 °C ;
- RH surface < 75 %.

Message :

> Le risque de condensation semble faible au moment de la mesure. Continuez à surveiller si le problème revient le matin ou par temps froid.

Actions :

- refaire une mesure matin/soir ;
- garder une aération régulière ;
- ne pas acheter d’appareil lourd sans tendance durable.

### Niveau B — Humidité intérieure élevée

Conditions typiques :

- humidité 60–70 % ;
- point de rosée qui monte ;
- surface pas forcément en condensation ;
- symptômes légers ou ponctuels.

Message :

> L’air contient déjà beaucoup d’humidité. Même si la surface ne condense pas maintenant, une baisse de température peut suffire à créer de la buée ou des traces.

Actions :

- vérifier VMC / aérations ;
- limiter séchage du linge intérieur ;
- aérer après douche/cuisson ;
- mesurer 7 jours ;
- envisager déshumidificateur seulement si durable.

### Niveau C — Risque de condensation

Conditions typiques :

- surface à moins de 2 °C du point de rosée ;
- RH surface ≥ 90 % ;
- buée, vitre qui coule, mur froid.

Message :

> La surface froide est trop proche du point de rosée. L’eau contenue dans l’air peut se déposer dessus, surtout la nuit ou quand la pièce refroidit.

Actions :

- chauffer plus régulièrement si la pièce descend fortement ;
- améliorer ventilation ;
- éloigner meubles du mur froid ;
- traiter pont thermique si localisé ;
- déshumidificateur possible en appoint, mais pas comme seule réponse si mur froid persistant.

### Niveau D — Risque moisissure durable

Conditions typiques :

- RH surface ≥ 80 % de façon probable ;
- moisissure visible / odeur de moisi ;
- problème plusieurs jours par semaine ;
- chambre, angle, meuble contre mur, cave.

Message :

> Les conditions peuvent favoriser les moisissures si elles durent. Le problème n’est pas forcément une fuite : cela peut être un mélange air humide + surface froide + renouvellement d’air insuffisant.

Actions :

- mesurer sur 7 jours ;
- vérifier ventilation ;
- nettoyer prudemment les petites traces ;
- éviter de coller meubles et cartons au mur ;
- rechercher cause si la trace revient.

### Niveau E — Signal d’alerte technique

Déclencheurs :

- salpêtre ;
- mur mouillé ;
- peinture qui cloque ;
- eau après pluie ;
- fuite possible ;
- moisissure étendue ;
- cave très humide permanente.

Message :

> Le calcul d’humidité ne suffit pas. Ces signes peuvent indiquer une infiltration, une remontée capillaire, une fuite ou un défaut technique. Un appareil peut aider à assécher, mais il ne traite pas la cause.

Actions :

- ne pas masquer avec peinture ou produit anti-moisissure seul ;
- chercher fuite / infiltration / drainage / ventilation ;
- demander un avis pro si durable ou étendu.

---

## 6. Réponse utilisateur à générer

Format recommandé :

1. **Résultat principal**
   - “Risque faible”, “À surveiller”, “Risque élevé de condensation”, “Conditions favorables aux moisissures”, ou “Signal d’alerte technique”.

2. **Chiffres simples**
   - point de rosée ;
   - humidité absolue ;
   - si surface connue : écart surface / point de rosée + humidité relative de surface.

3. **Ce que ça veut dire**
   - 2 à 4 phrases maximum.

4. **Actions prioritaires**
   - 3 actions maximum ;
   - adaptées au symptôme et à la pièce.

5. **Limite claire**
   - mesure approximative ;
   - refaire à froid / matin / soir ;
   - ne remplace pas un diagnostic en cas de fuite ou salpêtre.

---

## 7. Exemples de cas à intégrer dans la page

### Cas 1 — Chambre avec mur froid

Entrée : 19 °C, 70 %, surface 13 °C.  
Sortie : point de rosée ≈ 13,4 °C ; RH surface ≈ 103 %.  
Interprétation : risque élevé de condensation sur ce mur.

### Cas 2 — Salon correct mais mur limite

Entrée : 20 °C, 60 %, surface 15 °C.  
Sortie : point de rosée ≈ 12,0 °C ; écart ≈ 3 °C ; RH surface ≈ 82 %.  
Interprétation : pas forcément de gouttes, mais surface à surveiller si le problème dure.

### Cas 3 — Cave fraîche

Entrée : 10 °C, 80 %, surface 8 °C.  
Sortie : point de rosée ≈ 6,7 °C ; RH surface ≈ 92 %.  
Interprétation : risque de matériaux qui restent humides, même sans condensation visible immédiate.

### Cas 4 — Air plus sec

Entrée : 22 °C, 45 %, surface 16 °C.  
Sortie : point de rosée ≈ 9,5 °C ; RH surface ≈ 65 %.  
Interprétation : risque faible au moment de la mesure.

---

## 8. Décisions de conception pour MMH

### À afficher en gros

- Niveau de risque ;
- point de rosée ;
- “la surface doit rester au-dessus de X °C pour éviter la condensation”.

Exemple :

> Avec vos mesures, la condensation commence autour de 13,4 °C. Une vitre ou un mur à 13 °C peut donc devenir mouillé.

### À afficher en petit / détails

- humidité absolue ;
- humidité relative de surface ;
- marge d’erreur ;
- sources.

### À éviter

- promesse de diagnostic définitif ;
- dire qu’un déshumidificateur règle tout ;
- affirmer “moisissure garantie” uniquement sur un calcul ;
- mélanger infiltration, remontée capillaire et condensation sans distinguer.

---

## 9. Maillage et monétisation sobre

Selon résultat :

- besoin de mesure → page hygromètre ;
- condensation fenêtre → guide condensation fenêtre ;
- humidité durable 60–70 % ou plus → guide taux idéal + déshumidificateur ;
- cave → page cave humide + futur déshumidificateur cave évacuation continue ;
- ventilation douteuse → extracteur / VMC / futur VMI ;
- alerte technique → avertissement diagnostic, pas affiliation agressive.

---

## 10. Spécification finale du calculateur V1

Champs V1 :

- température air ;
- humidité relative ;
- température surface facultative ;
- pièce ;
- symptôme ;
- fréquence ;
- signaux d’alerte.

Calculs V1 :

- point de rosée ;
- humidité absolue ;
- température minimale conseillée des surfaces = point de rosée + 2 à 4 °C ;
- si surface fournie : écart surface/point de rosée ;
- si surface fournie : RH surface.

Résultat V1 :

- un niveau principal ;
- chiffres utiles ;
- explication courte ;
- 3 actions ;
- liens internes.

