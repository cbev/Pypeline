### PYPELINE 
#What is a Pypeline?  </br>
A Pypeline is what the UW Watershed Dynamics Lab uses to refer to a coupled and complex model and data integration workflow.  We are working out how to do that using Jupyter Notebooks and Python scripts. </br>

#Do you want to develop your own Pypeline? Or build one with us? Join our github repository for code-base development </br>
1. Go to https://github.com/cbev/Pypeline and make a new branch. </br>
2. Click on the "branch: Master" menu on the left-side of the screen
Search for the branch to work on, or else start typing-in a new branch name and click enter. (Eventually this will be ported to a HydroShare-JupyterHub Github branch and they can manage it.)
3. Go to HydroShare. There are two ways to open a Jupyter Notebook server.  </br>
    Option A:  Click on Apps. Click on Jupyter Python Notebook at NCSA. This will open a JupyterHub server at the University of Illinois -fondly referred to as ROGER. Fun fact: ROGER is both an acronym and a refernce to a superhero. Resourcing Open Geo-spatial Education and Research = ROGER and also it is named after Roger Tomlinson (Father of GIS).  </br>
    
    Option B: If you are already HydroShare savvy and you have saved a Jupyter Notebook in a Generic Resource, select the Resource from your My Resources tab. Click on the blue "Open With" butoon in the top right in the Resource landing page.  Pick "JupyterHub-USU beta" or "JupyterHub-NCSA". 
    

Click on Jupyter logo (top left)


Click on 'Notebooks' (The home folder is /home/jovyan/work)
Click on "New," make a new folder named "Observatory," then click on Observatory.
Inline image 2

#Clone-in the Pypeline Github repository
Click on "New,"and open a new terminal.

"cd notebooks/Observatory" (change working directory to Observatory).
"git clone https://github.com/cbev/Pypeline.git" (Download the latest Master branch)
"cd Pypeline"(change working directory to Pypeline)

"git checkout <name of branch> (make sure that the changes are not directed at the Master - it gets messy!)
For development, until we have pushed to HydroShare-Jupyter Hub Utilities on Github, copy the scripts to your local utilites/ folder
"cp pypeline_scripts.py ../../utilities" (This saves and overwrites pypeline_scripts.py in the utilities folder.
Work from the Controller_Notebook in the /Observatory/Pypeline/ git folder
if you make changes to scripts, copy them back to the Pypeline folder.  
if you make changes to the the .ipynb, just save it.
When finished, go back to terminal and change directory until you are inside Pypeline/ folder.  Send the changes back to your own branch
To commit your changes locally to the /Observatory/Pypeline git repository as well as remotely on the /cbev/Pypeline github repository, 
"git commit -m <insert short message to explain the changes>" (this commits the changes from the staging environment to the git repository)
"git fetch" to get the latest version from the Master 
"git push" to push the changes to the remote github repository. "git remote" can identify the github that will get affected.
When you're ready to assimilate your changes in your Branch back to Master, do a "git pull" to send a pull request to the Master owner (here, it is cbev)
