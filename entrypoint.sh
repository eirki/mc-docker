echo "Downloading"
python /home/mc/download.py
echo "Rendering"
python /home/mc/Minecraft-Overviewer/overviewer.py --config=/home/mc/renderconfig.py
echo "Generating points of interest"
python /home/mc/Minecraft-Overviewer/overviewer.py --config=/home/mc/renderconfig.py --genpoi
