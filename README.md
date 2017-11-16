INSEE PCS : Des outils pour utiliser les Professions et Catégories Socioprofessionnelles de l'INSEE
===================================================================================================

**INSEE-PCS** est un module Python permettant d'exploiter facilement les Professions et Catégories Socioprofessionnelles de l'INSEE (version 2003).

Plus d'informations sur les PCS peuvent être trouvées sur le site de l'INSEE : [Nomenclatures des professions et catégories socioprofessionnelles](https://insee.fr/fr/information/2406153).

**Ce code est testé uniquement avec Python 3. L'auteur de ce script n'est en aucune façon relié à l'INSEE, la base de données mise à disposition par ce script a été créée à partir des fichiers CSV fournis sous licence libre sur le site de l'INSEE.**

Voici les différentes nomenclatures actuellement supportées :

- `2003` ;
- `2017-ESE`.

# Installation

Ce module est disponnible sur PyPi. Il nécessite le module `peewee` pour fonctionner.

    $ pip3 install peewee insee-pcs

# Usage

```python
import insee_pcs

# Récupérer les PCS de la nomenclature de 2003
ypcs = insee_pcs.get_year("2003")

# Trouver la PCS "1" du niveau 1.
ypcs.get_PCS(1, "1")
"<PCS '1' (level 1)>"

# Trouver la description de la PCS "382b" du niveau 4.
ypcs.get_PCS(4, "382b").description
"Architectes salariés"
```

Il est aussi possible d'itérer récursivement sur tous les enfants d'une PCS avec la méthode `iter_children()`. Cette méthode accepte un paramètre optionnel, `max_level`, permettant de définir un niveau maximum pour l'itération.

```python
# Affiche récursivement la PCS "38" (niveau 2) et ses enfants.
pcs = ypcs.get_PCS(2, "32")
for p in pcs.iter_children():
    print("{spaces}{code} : {description}...".format(
        spaces=' '*(p.level-2)*2,
        code=p.code,
        description=p.description[:20]
    ))
"""
32 : Cadres de la fonctio...
  33 : Cadres de la fonctio...
    331a : Personnels de direct...
    332a : Ingénieurs de l’État...
    332b : Ingénieurs des colle...
    333a : Magistrats...
    333b : Inspecteurs et autre...
    333c : Cadres de la Poste...
    333d : Cadres administratif...
    333e : Autres personnels ad...
    333f : Personnels administr...
    334a : Officiers des Armées...
    335a : Personnes exerçant u...
  34 : Professeurs, profess...
    341a : Professeurs agrégés ...
    341b : Chefs d’établissemen...
    342a : Enseignants de l’ens...
    342e : Chercheurs de la rec...
    343a : Psychologues spécial...
    344a : Médecins hospitalier...
    344b : Médecins salariés no...
    344c : Internes en médecine...
    344d : Pharmaciens salariés...
  35 : Professions de l’inf...
    351a : Bibliothécaires, arc...
    352a : Journalistes (y. c. ...
    352b : Auteurs littéraires,...
    353a : Directeurs de journa...
    353b : Directeurs, responsa...
    353c : Cadres artistiques e...
    354a : Artistes plasticiens...
    354b : Artistes+B493 de la ...
    354c : Artistes dramatiques...
    354d : Artistes de la danse...
    354g : Professeurs d’art (h...
"""

# Même chose, en limitant l'itération au niveau 3.
pcs = ypcs.get_PCS(1, "3")
for p in pcs.iter_children(max_level=3):
    print("{spaces}{code} : {description}...".format(
        spaces=' '*(p.level-1)*2,
        code=p.code,
        description=p.description[:20]
    ))
"""
3 : Cadres et profession...
  31 : Professions libérale...
    31 : Professions libérale...
  32 : Cadres de la fonctio...
    33 : Cadres de la fonctio...
    34 : Professeurs, profess...
    35 : Professions de l’inf...
  36 : Cadres d’entreprise...
    37 : Cadres administratif...
    38 : Ingénieurs et cadres...
"""
```

La fonction `get_all_PCS_of_level()` prend un niveau (`int`) en paramètre et retourne toutes les PCS du niveau demandé dans un objet `SelectQuery` (convertible en liste).

```python
# Trouver toutes les PCS de niveau 1. Retourne un objet `SelectQuery`.
print(list(ypcs.get_all_PCS_of_level(1)))
[<PCS '1' (level 1)>, <PCS '2' (level 1)>, <PCS '3' (level 1)>, <PCS '4' (level 1)>, <PCS '5' (level 1)>, <PCS '6' (level 1)>, <PCS '7' (level 1)>, <PCS '8' (level 1)>]
```

Les méthodes `get_PCS()` et `get_all_PCS_of_level()` acceptent toutes deux un paramètre `year` (`str`) pour spécifier une nomenclature sans passer par la méthode `get_year()`.

```python
insee_pcs.PCS.get_PCS(1, '1', year="2003")
"<PCS '1' (level 1)>"
```

La liste des nomenclatures disponnibles est accessible via l'attribut `AVAILABLE_YEARS`, qui contient un tuple de strings.

```python
insee_pcs.AVAILABLE_YEARS
("2003", "2017-ESE")
```

L'objet `PCS` est un modèle Peewee classique, vous pouvez donc utiliser toutes les méthodes de Peewee dessus.

```python
# Trouver toutes les PCS 2003 de niveau 4 dont la description contient "Éleveur".
print(list(
    PCS.select().where(PCS.year="2003", PCS.level==4, PCS.description.contains("Éleveur"))
))
[<PCS '111d' (level 4)>, <PCS '111e' (level 4)>, <PCS '121d' (level 4)>, <PCS '121e' (level 4)>, <PCS '131d' (level 4)>, <PCS '131e' (level 4)>]
```

Pour obtenir une aide détaillée hors-ligne, vous pouvez aussi faire `help(<object>)` (par exemple, `help(main_insee)`).

# Dépendances

Ce module nécessite `peewee` (disponnible avec `pip`).

# TODO

- Traduction ?
- Anciennes versions des PCS / CSP ? **[WIP]**

# Licence

Ce module est distribué sous la licence AGPLv3, dont les termes sont disponnibles dans le fichier [LICENCE](LICENCE).
