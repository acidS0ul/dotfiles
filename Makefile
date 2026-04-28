PM_INSTALL=pacman -S --needed

all: packages dotfiles install aur

packages:
	$(PM_INSTALL) - < packages.txt

dotfiles:
	stow --dotfiles .

install: trusttunnel zed opencode

trusttunnel:
	curl -fsSL https://raw.githubusercontent.com/TrustTunnel/TrustTunnelClient/refs/heads/master/scripts/install.sh | sh -s -
zed:
	curl -f https://zed.dev/install.sh | sh
opencode:
	curl -fsSL https://opencode.ai/install | bash

aur:
	git clone https://aur.archlinux.org/yay.git /tmp/yay
	cd tmp/yay && makepkg -si
