
if [ ! -d "/tmp/cfgs" ]; then
    git clone https://github.com/Snowy-Fluffy/zapret.cfgs.git /tmp/cfgs
fi

if [ -f "/tmp/cfgs/configurations/$1" ]; then
    sudo cp /tmp/cfgs/configurations/$1  /opt/zapret/config
    sudo cp /tmp/cfgs/lists/list-basic.txt  /opt/zapret/ipset/zapret-hosts-user.txt
    sudo cp /tmp/cfgs/lists/ipset-discord.txt /opt/zapret/ipset/zapret-ip-user-ipban.txt
    sudo systemctl restart zapret 
else
    ls /tmp/cfgs/configurations
fi
