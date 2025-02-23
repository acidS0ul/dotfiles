#!/bin/bash
from typing import NoReturn

import subprocess
import packages
import os
import getopt
import sys 

DOTFILES_PATH = os.path.expanduser("~/projects/dotfiles")
DOTCONF_PATH  = os.path.expanduser("~/.config/")

LONG_COMMAND  = [
    "help",
    "keyboard",
    "git",
    "aur",
    "pacman",
    "dotfiles",
    "zapret",
    "systemd",
    "chadwm",
]

FROMTO =  [
    [DOTFILES_PATH + "/alacritty",                 ""],
    [DOTFILES_PATH + "/redshift",                  ""],   
    [DOTFILES_PATH + "/scripts/getlocale.sh",      "~/.getlocale.sh"],   
    [DOTFILES_PATH + "/dwm/xinitrc",               "~/.xinitrc"],
    [DOTFILES_PATH + "../nvimrc",                  "~/.config/nvim"],
    [DOTFILES_PATH + "/tmux/tmux.conf",            "~/.tmux.conf"],
    
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

    subprocess.run(["sudo", "cp", DOTFILES_PATH + "/wallpapers/wallpaper.png", 
                    os.path.expanduser("~/.wallpaper.png")]),   

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

def systemd_init()->NoReturn:
    subprocess.run(["sudo", "systemctl", "enable", "dhcpcd.service"])
    subprocess.run(["sudo", "systemctl", "restart", "zapret"])
def usage()->NoReturn:
    print("-k\t--keyboard\t keyboard settings setup")
    print("-g\t--git\t\t git repos clone")
    print("-a\t--aur\t\t aur install")
    print("-p\t--pacman\t pacman packages install")
    print("-d\t--dotfiles\t dotfile init")
    print("-z\t--zapret\t install and config zapret")
    print("-s\t--systemd\t systemd init")
    print("-c\t--chadwm\t chadwm install and patching")
    print("-f\t--full\t\t full install")
    print("-h\t--help\t\t this message")

def get_short_commands_string():
    str = ""
    for cmd in LONG_COMMAND:
        str = str + cmd[0]
    return str

def get_short(ind):
    return "-" + LONG_COMMAND[ind][0] 

def get_long(ind):
    return "--" + LONG_COMMAND[ind]

def main(): 
    short_commands = get_short_commands_string()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_commands, LONG_COMMAND)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    for o, a in opts:
        if o in (get_short(0), get_long(0)):
            usage()
            sys.exit(0) 
        elif o in (get_short(1), get_long(1)):
            keyboard_setup()
        elif o in (get_short(2), get_long(2)):
            git_clone_repos()
        elif o in (get_short(3), get_long(3)):
            install_aur()
        elif o in (get_short(4), get_long(4)):
            install_pacman_packages()
        elif o in (get_short(5), get_long(5)):
            dotfile_init()
        elif o in (get_short(6), get_long(6)):
            zapret_install()
        elif o in (get_short(7), get_long(7)):
            systemd_init()
        elif o in (get_short(8), get_long(8)):
            chadwm_patching()
            chadw_compile()
        elif o in ("-f", "--full"):
            install_pacman_packages()
            keyboard_setup()
            git_clone_repos()
            install_aur()
            dotfile_init()
            chadwm_patching()
            chadw_compile()
            zapret_install()
            systemd_init()
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()
