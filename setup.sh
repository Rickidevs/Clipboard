#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

echo -e "${BLUE}
⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠙⢦⡀⠀⠀⣰⢶⠀⠀⠀
⠀⠀⠀⠀⠀⢻⠀⠀⠹⣦⠞⠁⢸⠀⠀⠀
⠀⠸⡟⠓⠒⠛⠀⡀⠤⠤⢀⠀⠾⠶⢶⡆
⠀⠀⢻⡀⠀⡐⠁⠀⠀⠀⠀⠑⡀⢀⡞⠀
⣀⡤⠞⠃⢰⠀⠐⠒⠲⡶⠶⠶⢶⠘⠲⣄
⠙⠲⣤⡀⢸⠀⡒⠖⠒⡲⡒⠒⢒⢢⡞⠉
⢀⡴⠋⠀⡸⠀⠌⠀⠈⢀⢉⠤⢽⡈⣳⡄
⠀⠙⢳⠆⠄⡀⠀⠀⠀⣀⣁⠀⢸⢾⡁⠀
⠀⠀⠙⠛⣷⣣⠠⠎⠀⣠⠔⠉⣼⠏⠁⠀
⠀⠀⠀⠀⠉⢉⣳⡤⠀⢀⣤⡞⠁⠀⠀⠀
⠀⠀⠀⡴⠋⠉⡑⠃⠒⠊⣌⠉⢳⡄⠀⠀
⠀⠀⠀⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠃⠀⠀ https://github.com/rickidevs

${NC}Welcome to the Clipboard Monitor Setup!"

for i in {7..1}; do
    echo -ne "\r${YELLOW}Loading${NC} ${GREEN}$(printf '•%.0s' $(seq 1 $((6 - i))))${NC}"
    sleep 1
done
echo -e "\r${GREEN}Done!${NC}\n"

USERNAME=$(whoami)
SCRIPT_DIR=$(pwd)
SCRIPT_NAME="Clipboard.py"
SERVICE_NAME="clipboard_monitor.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"
DEST_DIR="/opt/Clipboard"

REQUIRED_PKG=("pyperclip" "customtkinter" "keyboard")

for pkg in "${REQUIRED_PKG[@]}"; do
    if ! python3 -c "import $pkg" &> /dev/null; then
        echo -e "${RED}$pkg library not found, installing...${NC}"
        sudo apt install python3-pip -y
        pip3 install "$pkg"
    else
        echo -e "${GREEN}$pkg library is already installed.${NC}"
    fi
done

if [ ! -d "$DEST_DIR" ]; then
    sudo mkdir -p $DEST_DIR
    sudo cp -r $SCRIPT_DIR/Clipboard $DEST_DIR/
else
    echo -e "${GREEN}$DEST_DIR already exists, no need to move.${NC}\n"
fi

if [ ! -f "$DEST_DIR/$SCRIPT_NAME" ]; then
    echo -e "${RED}Error: $SCRIPT_NAME not found in $DEST_DIR!${NC}\n"
    exit 1
fi

echo -e "\n${GREEN}Creating service file...${NC}"
sudo bash -c "cat > $SERVICE_PATH <<EOF
[Unit]
Description=Clipboard Monitor Service
After=graphical.target

[Service]
ExecStartPre=/bin/sleep 15
ExecStart=/usr/bin/python3 $DEST_DIR/$SCRIPT_NAME
Restart=always
User=$USERNAME
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USERNAME/.Xauthority
WorkingDirectory=$DEST_DIR

[Install]
WantedBy=default.target
EOF"

echo -e "\n${GREEN}Reloading systemd daemon...${NC}"
sudo systemctl daemon-reload
echo -e "${GREEN}Enabling the service...${NC}"
sudo systemctl enable $SERVICE_NAME
echo -e "${GREEN}Checking service status...${NC}\n"
sudo systemctl start $SERVICE_NAME
sudo systemctl status $SERVICE_NAME --no-pager

echo -e "\n${YELLOW}-------------------------------------------------------${NC}"
echo -e "${GREEN}Service has been successfully classified!${NC}"
echo -e "${YELLOW}-------------------------------------------------------${NC}\n"
