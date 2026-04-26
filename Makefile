PM_INSTALL=pacman -S --needed

all: packages dotfiles tunnels aur

packages:
	$(PM_INSTALL) - < packages.txt

dotfiles:
	stow --dotfiles .

tunnels:
	curl -fsSL https://raw.githubusercontent.com/TrustTunnel/TrustTunnelClient/refs/heads/master/scripts/install.sh | sh -s -

aur:
	git clone https://aur.archlinux.org/yay.git /tmp/yay
	cd tmp/yay && makepkg -si
