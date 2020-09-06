@echo HPMS Project Builder - Copyright(c) 2020

blender --background %cd%/HPMSScene.blend --python %cd%/bdata/main.py --log-level 0 -- --logging-level TRACE --output %cd%/HPMS_Project --roomupdate-all yes --render yes --preview yes
pause