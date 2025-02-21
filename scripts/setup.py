#!/bin/bash
from typing import NoReturn

import subprocess
import packages
import os

DOTFILES_PATH = os.path.expanduser("~/projects/dotfiles")
DOTCONF_PATH  = os.path.expanduser("~/.config/")

FROMTO =  [
    [DOTFILES_PATH + "/alacritty",                 ""],
    [DOTFILES_PATH + "/redshift",                  ""],   
    [DOTFILES_PATH + "/scripts/getlocale.sh",      "~/.getlocale.sh"],   
    [DOTFILES_PATH + "/dwm/xinitrc",               "~/.xinitrc"],
    [DOTFILES_PATH + "../nvimrc",                  "~/.config/nvim"],
    
]

def _run(cmd)->NoReturn:
    for c in cmd: 
        subprocess.run(c)


def keyboard_setup()->NoReturn:
    cmd = ["setxkbmap", "-model", "pc105", "-layout" "us,ru", "-option",
           "grp:win_space_toggle"]   

    subprocess.run(cmd)

def install_pacman_packages() -> NoReturn:
    cmd = ["sudo", "pacman", "-Suy"]
    cmd = cmd + packages.pacman
    subprocess.run(cmd)

def install_aur()->NoReturn: 
    subprocess.run(["makepkg", "-si"], cwd=packages.git_repos[0][1])

# def install_aur_packages()->NoReturn:

def git_clone_repos()->NoReturn:
    git_cmd = ["git", "clone"]
    for repos in packages.git_repos:
        rep = []
        rep.append(os.path.expanduser(repos[0]))
        rep.append(os.path.expanduser(repos[1]))
        subprocess.run(git_cmd + rep)

def zapret_install()->NoReturn:
    cmd = []
    ZDIR = "/opt/zapret"
    ZCONFIG = DOTFILES_PATH + "/openwrt" 
    
    subprocess.run(["make"], cwd=DOTFILES_PATH + "/../zapret/")
    cmd.append([DOTFILES_PATH + "/../zapret/install_prereq.sh"]) 
    cmd.append([DOTFILES_PATH + "/../zapret/install_bin.sh"])
    cmd.append([DOTFILES_PATH + "/../zapret/install_easy.sh"])
    cmd.append(["sudo", "cp", ZCONFIG + "/config", ZDIR]) 
    cmd.append(["sudo", "cp", ZCONFIG + "/host-auto.txt",
                ZDIR + "/ipset/zapret-host-user.txt"]) 
    _run(cmd) 

def dotfile_init()->NoReturn:
    subprocess.run(["cp", DOTFILES_PATH + "/wallpapers/wallpaper.png", "~/.wallpaper.png"]),   

    softlink_cmd =  ["ln", "-s"]
    for links in FROMTO:
        if  links[1] == "":
            links[1] = DOTCONF_PATH
        else:
            links[1] = os.path.expanduser(links[1])
        subprocess.run(softlink_cmd + links)


def chadwm_patching()->NoReturn:
    dot_chadwm_dir = DOTCONF_PATH  + 'chadwm'
    chadwm_mod_dir = DOTFILES_PATH + '/dwm/chadwm'
    
    modif_file = [
        "config.def.h",
        "bar.sh",
        "run.sh",
    ]

    cmd = []
    cmd.append(["sudo", "rm", dot_chadwm_dir + "/chadwm/"  + modif_file[0]])
    cmd.append(["sudo", "rm", dot_chadwm_dir + "/scripts/" + modif_file[1]])
    cmd.append(["sudo", "rm", dot_chadwm_dir + "/scripts/" + modif_file[2]])
    
    cmd.append(["cp", 
                chadwm_mod_dir + "/"         + modif_file[0], 
                dot_chadwm_dir + "/chadwm/"  + modif_file[0]])
    cmd.append(["cp", 
                chadwm_mod_dir + "/"         + modif_file[1], 
                dot_chadwm_dir + "/scripts/" + modif_file[1]])
    cmd.append(["cp", 
                chadwm_mod_dir + "/"         + modif_file[2], 
                dot_chadwm_dir + "/scripts/" + modif_file[2]])

    _run(cmd) 
    
def chadw_compile()->NoReturn:
    chadwm_dir = DOTCONF_PATH + 'chadwm/chadwm'
    subprocess.run(["sudo", "make", "clean"], cwd=chadwm_dir)
    subprocess.run(["sudo", "make", "install"], cwd=chadwm_dir)

def main():
    # TODO: add c-like getops
    install_pacman_packages()
    keyboard_setup()
    git_clone_repos()
    install_aur()
    dotfile_init()
    chadwm_patching()
    chadw_compile()
    zapret_install()

if __name__ == "__main__":
    main()
