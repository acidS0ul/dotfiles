#!/bin/bash
from typing import NoReturn

import subprocess
import packages
import os
import getopt
import sys 

DOTFILES_PATH = os.path.expanduser(os.path.dirname(os.path.dirname(__file__)))
DOTCONF_PATH  = os.path.expanduser("~/.config/")


FROMTO =  [
    # [DOTFILES_PATH + "/alacritty",                 ""],
    [DOTFILES_PATH + "/redshift",                  ""],   
    [DOTFILES_PATH + "/scripts/getlocale.sh",      "~/.getlocale.sh"],   
    # [DOTFILES_PATH + "/dwm/xinitrc",               "~/.xinitrc"],
    [DOTFILES_PATH + "/tmux/tmux.conf",            "~/.tmux.conf"],
    [DOTFILES_PATH + "/bashrc",                    "~/.bashrc"],
    
]

def _run(cmd)->NoReturn:
    for c in cmd: 
        subprocess.run(c)


def keyboard_setup()->NoReturn:
    cmd = ["setxkbmap", "-model", "pc105", "-layout" "us,ru", "-option",
           "grp:win_space_toggle"]   

    subprocess.run(cmd)


def install_pacman_packages(pkgs) -> NoReturn:
    cmd = ["sudo", "pacman", "-Suy"]
    cmd = cmd + pkgs
    subprocess.run(cmd)

def install_basic_packages() ->NoReturn:
    install_pacman_packages(packages.pacman_basic)

def install_system_packages() ->NoReturn:
    install_pacman_packages(packages.pacman_for_dwm)

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
    git_cmd = ["git", "clone", "https://github.com/bol-van/zapret.git", "/tmp/zapret"]
    subprocess.run(git_cmd)
    git_cmd = ["git", "clone", "https://github.com/Snowy-Fluffy/zapret.cfgs.git", "/tmp/cfgs"]
    subprocess.run(git_cmd)
    subprocess.run(["sudo", "make"], cwd="/tmp/zapret/")

    cmd.append(["/tmp/zapret/install_prereq.sh"]) 
    cmd.append(["/tmp/zapret/install_bin.sh"]) 
    cmd.append(["/tmp/zapret/install_easy.sh"])
    cmd.append(["sudo", "cp", "/tmp/cfgs/configurations/general_ALT",  "/opt/zapret/config"])
    cmd.append(["sudo", "cp", "/tmp/cfgs/lists/list-basic.txt",         "/opt/zapret/ipset/zapret-hosts-user.txt"])
    cmd.append(["sudo", "cp", "/tmp/cfgs/lists/ipset-discord.txt",      "/opt/zapret/ipset/zapret-ip-user-ipban.txt"])
    cmd.append(["sudo", "systemctl", "restart", "zapret"]) 
    _run(cmd) 

def neovim_init()->NoReturn:
    cmd = []
    cmd.append(["rm", "-rf", DOTCONF_PATH + "nvim"]) 
    cmd.append(["git", "clone", "https://github.com/acidS0ul/nvimrc", 
                DOTCONF_PATH + "nvim"])
    _run(cmd) 

def dotfile_init()->NoReturn:
    softlink_cmd =  ["ln", "-s"]
    neovim_init()
    for links in FROMTO:
        if  links[1] == "":
            links[1] = DOTCONF_PATH
        else:
            subprocess.run(["rm", os.path.expanduser(links[1])])
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

def chadw_install()->NoReturn:
    chadwm_patching()
    chadw_compile()

def full_install()->NoReturn:
    install_basic_packages()
    keyboard_setup()
    git_clone_repos()
    install_aur()
    dotfile_init()
    zapret_install()

def full_install_with_dwm()->NoReturn:
    install_system_packages()
    full_install()
    chadw_install()

def print_help()->NoReturn:
    for cmd in COMMANDS:
        print(f"-{cmd[0][0]}/--{cmd[0]}\t\t{cmd[1]}")

COMMANDS = [
    ["help", "this message", print_help],
    ["keyboard", "keyboard settings setup", keyboard_setup],
    ["git", "git repos clone", git_clone_repos],
    ["aur", "aur install", install_aur],
    ["pacman", "pacman packages install", install_basic_packages],
    ["system", "system pacman packages install for dwm", install_system_packages],
    ["dotfiles", "dotfile init", dotfile_init],
    ["zapret", "install and config zapret", zapret_install],
    ["chadwm", "chadwm install and patching", install_system_packages],
    ["full", "full install (without dwm)", full_install],
    ["DWM", "full install (with dwm)", full_install_with_dwm],
]

def usage(code)->NoReturn:
    print_help()
    sys.exit(code)

def get_short_commands_string():
    str = ""
    for cmd in COMMANDS:
        str = str + cmd[0][0]
    return str

def get_long_commands_string():
    str = ""
    for cmd in COMMANDS:
        str = str + cmd[0]
    return str

def processing_commands(opt):
    for cmd in COMMANDS:
        # print(f"{o} / -{cmd[0][0]} / --{cmd[0]}")
        if opt in ("-"+cmd[0][0], "--"+cmd[0]):
            cmd[2]()
            return
    assert False, "unhandled option"
    return

def main(): 
    short_commands = get_short_commands_string()
    long_commands = get_long_commands_string()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_commands, long_commands)
    except getopt.GetoptError as err:
        print(err)
        usage(2)
    
    if len(sys.argv) == 1:
        usage(0)

    for o, a in opts:
        processing_commands(o)

if __name__ == "__main__":
    main()
