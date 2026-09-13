# Installer TI-LEX Pro

Depuis la session live, ouvrez **Installer TI-LEX Pro** : l'icône est sur le bureau
et dans le menu, catégorie Système, ainsi que dans les Paramètres TI-LEX.
L'assistant Calamares propose une installation graphique avec le français du Canada,
le clavier canadien, le fuseau `America/Montreal`, le choix du disque, la création du
compte et un résumé de confirmation.

La session live permet d'essayer le matériel — Wi-Fi, son, écrans, veille — avant de
lancer l'installation. L'assistant demande une confirmation avant d'écrire sur le
disque : tant que le résumé n'est pas validé, rien n'est modifié.

## Deux chemins, un seul système
- **Calamares**, depuis la session live, pour une installation guidée au clic.
- **L'installateur Debian**, depuis le menu de démarrage, en mode graphique ou texte.
  Il reste disponible : c'est le filet en cas d'écran noir, de matériel récalcitrant
  ou de partitionnement avancé.

Les deux installent le même système. Le mode texte de l'installateur Debian est le
seul qui fonctionne sans interface graphique.

## Après l'installation
Calamares n'est pas conservé sur le système installé : la configuration Debian le
retire, et le lanceur TI-LEX disparaît alors du menu de lui-même — il déclare
`TryExec=/usr/bin/calamares`, donc il ne laisse pas d'entrée morte.

## Avant d'installer pour de vrai
1. Sauvegardez. L'assistant peut effacer le disque que vous choisissez.
2. Essayez d'abord en machine virtuelle, sur un disque virtuel vide.
3. Suivez [TESTS.md](TESTS.md) : douze étapes, du démarrage au compte installé.

## État
Calamares et sa configuration Debian sont intégrés à l'image et vérifiés à la
construction : paquets présents, lanceur valide, fuseau par défaut en place.
**L'assistant n'a jamais été exécuté et aucune installation n'a été faite.**
Le fuseau `America/Montreal` est le nom québécois du fuseau de l'Est ; tzdata en
fait un lien vers `America/Toronto`, l'heure est donc la même.
