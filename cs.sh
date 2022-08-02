cd ~/projects/lorc || exit
source venv/bin/activate

python  main.py && csound -odac -+rtaudio=auhal --orc lorc/csound/sample.orc
