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
    [DOTFILES_PATH + "../nvimrc",                  ""],
    
]

def _run(cmd)->NoReturn:
    for c in cmd: 
        subprocess.run(c)


def keyboard_setup()->NoReturn:
    cmd = ["localectl", "set-x11-keymap", "--no-convert", "us,ru", "pc105",
           "\"\"", "grp:win_space_toggle"]
    subprocess.run(cmd)

def install_pacman_packages() -> NoReturn:
    cmd = ["sudo", "pacman", "-S"]
    cmd = cmd + packages.pacman
    subprocess.run(cmd)

def install_aur()->NoReturn: 
    subprocess.run(["makepkg", "-si"], cwd=packages.git_repos[0][1])

# def install_aur_packages()->NoReturn:

def git_clone_repos()->NoReturn:
    nvimrc_clone = ["gh", "repo", "clone" "acidS0ul/nvimrc"]
    subprocess.run(nvimrc_clone, cwd=DOTFILES_PATH+"/..")

    git_cmd = ["git", "clone"]
    for rep in packages.git_repos: 
        subprocess.run(git_cmd + rep)

def zapret_install()->NoReturn:
    cmd = []
    ZDIR = "/opt/zapret"
    ZCONFIG = DOTFILES_PATH + "/openwrt" 
    
    cmd.append([DOTFILES_PATH + "../zapret/install_prereq.sh"])
    cmd.append([DOTFILES_PATH + "../zapret/install_bin.sh"])
    cmd.append(["cp", ZCONFIG + "/config", ZDIR]) 
    cmd.append(["cp", ZCONFIG + "/host-auto.txt",
                ZDIR + "/ipset/zapret-host-user.txt"]) 
    _run(cmd) 

def dotfile_init()->NoReturn:
    subprocess.run(["cp", "/wallpapers/wallpapers.png", "~/.wallpaper.png"], cwd=DOTFILES_PATH),   

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
    
    modif_files = [
        "config.def.h"
        "bar.sh"
        "run.sh"
    ]

    cmd = []
    cmd.append(["sudo", "rm", chadwm_dir + "/chadwm/"  + modif_file[0]])
    cmd.append(["sudo", "rm", chadwm_dir + "/scripts/" + modif_file[1]])
    cmd.append(["sudo", "rm", chadwm_dir + "/scripts/" + modif_file[2]])
    
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
    keyboard_setup()
    install_pacman_packages()
    git_clone_repos()
    install_aur()
    dotfile_init()
    chadwm_patching()
    chadw_compile()

if __name__ == "__main__":
    main()
