pacman = [
    "xorg",
    "xorg-xinit",
    "wget",
    "firefox",
    "docker",
    "syncthing",
    "obsidian",
    "firacode-ttf",
    "tff-firacode-nerd",
    "flameshot",
    "telegram-desktop",
    "noto-fonts-emoji",
    "openssh",
    "pico",
    "feg",
    "acpi",
    "rofi",
    "fish",
    "qemu-full",
    "dash",
    "tmux",
    "redshift",
    "github-cli",
    "libnetfilter_queue",
]

aur = [

]

git_repos = [
#   [
#       "url/to/git/repos",
#       "/path/to/clone"
#   ]
    [
        "https://aur.archlinux.org/yay.git",
        "/tmp/yay"
    ],
    [
        "https://github.com/wbthomason/packer.nvim", 
        "~/.local/share/nvim/site/pack/packer/start/packer.nvim"
    ],
    [
        "https://github.com/siduck/chadwm", 
        "~/.config/chadwm"
    ],
    [
        "https://github.com/bol-van/zapret.git",
        "~/Projects/zapret"
    ], 
]
