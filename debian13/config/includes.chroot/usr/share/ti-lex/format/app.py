#!/usr/bin/python3
"""Graphical entry point to GNOME Disks; never formats a device itself."""
import shutil
import subprocess
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def main():
    dialog = Gtk.MessageDialog(
        message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.NONE,
        text="Formater un disque ou une clé USB")
    dialog.set_title("Formatage — TI-LEX PRO")
    dialog.format_secondary_text(
        "Le formatage efface les données du volume choisi.\n\n"
        "Dans Disques, choisissez le périphérique en vérifiant son nom et sa capacité, "
        "puis la partition à formater. Ouvrez son menu pour choisir le formatage.\n\n"
        "Aucun disque n’est sélectionné ou modifié ici. L’utilitaire Disques vous "
        "demandera de confirmer l’opération.")
    dialog.add_button("Annuler", Gtk.ResponseType.CANCEL)
    dialog.add_button("Ouvrir Disques", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.CANCEL)
    response = dialog.run()
    dialog.destroy()
    if response != Gtk.ResponseType.OK:
        return
    try:
        if shutil.which("gnome-disks") is None:
            raise FileNotFoundError("L’utilitaire Disques n’est pas installé (gnome-disk-utility).")
        subprocess.Popen(["gnome-disks"])
    except OSError as error:
        message = Gtk.MessageDialog(message_type=Gtk.MessageType.ERROR,
                                    buttons=Gtk.ButtonsType.CLOSE,
                                    text="Impossible d’ouvrir Disques")
        message.format_secondary_text(str(error))
        message.run()
        message.destroy()


if __name__ == "__main__":
    main()
