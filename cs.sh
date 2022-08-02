cd ~/projects/lorc
source venv/bin/activate
python orchestra.py && exec ~/projects/csound/build/csound -odac -+rtaudio=auhal --orc csound/sample.orc
