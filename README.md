# Audio-Data-Representation

How to install:
1) Download all of the files in the repo.
2) compress into a zip file using (on MacOS) "zip -r zipname.zip foldername -x "__MACOSX*" "*.DS_Store". replace the zipname with whatever you want the name of the compressed folder to be. Replace the foldername with the folder where you have all of these files.
3) Open QGIS and go to "Install Plugin with ZIP"
4) Upload the compressed folder
5) The Plugin should now be successfully installed. Users should be able to choose different raster layers and bands, as well as set their own normalization value range.

How to use:
1) Once the plugin is installed, add some raster layers and then open the plugin.
2) Select the layer and band(s) you want.
3) Update the normalization values.
4) In the background, you must have a MIDI synthesizer process going. I used GarageBand on MacOS. To setup GarageBand, create a new project, select software instrument. Then you also need to setup the Audio MIDI synthesizer. To do this: Open Audio MIDI Setup in MacOs, then go to Window -> Show Midi Studio, double click IAC Driver, then create a new port and name it "Python to GarageBand", select "Device is online" and you should be done.
5) Once Audio MIDI and Garageband are set up, the user should be able to use the plugin.
