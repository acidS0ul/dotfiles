PM_INSTALL=pacman -S --needed

all: packages dotfiles install aur

packages:
	$(PM_INSTALL) - < packages.txt

dotfiles:
	stow --dotfiles .

install:
	curl -fsSL https://raw.githubusercontent.com/TrustTunnel/TrustTunnelClient/refs/heads/master/scripts/install.sh | sh -s -
	curl -f https://zed.dev/install.sh | sh

aur:
	git clone https://aur.archlinux.org/yay.git /tmp/yay
	cd tmp/yay && makepkg -si
