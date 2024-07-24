# Medihacks
Welcome to Cura. A social platform wherein we provide not just social interaction but also support.

# Why 
This application was developed for the medihacks 2024 hackathon

# Who would dare make such a thing
This program is the amalgamation of self-hate, tenacity, intrigue, a week of sleepless nights and caffeine.
Developed by:
  -Uzair Mahomed (multiprocessing, networking and socket programming)
  -Abdur-Rahman Kaka (algorithms for message handling, file handling and io)
  -Yaseen Khan (UI and UX)
  -Sevan Govender (visual components)

# How does it work
The program uses netbird to communicate with other computers over the internet (Read more about netbird at app.netbird.io). Firstly the install script installs netbird and connect the user to the netbird network and starts the netbird service. To start the application run CuraHTTP.py (Windows users need to workaround the maximum allowed sockets.See bugs). The user will then be prompted to open their browser and navigate to http://127.0.0.1:808/home. This will only happen if the user is authenticated with the netbird virtual LAN. The scripts creates a netb.ConnectionHandler object to asynchronously send and receive messages using both the builtin asyncio and multiprocessing libraries. The webpages are then generated dynamically by the template.load method. This is done by resolving templates for requests depending on the nature of the requests. To achieve this we developed our own basic backend framework which computes the outputs of "nests". These nests can call methods and variables stored in the definitions module so long as it is present in the definitions.namespace dictionary.

# How do I run Cura?
*Short answer. YOU CANT* Firstly we have no means to authenticate the identity of our users. Meaning that any body who's installed Cura has a virtual LAN connection to your computer. However any vulnerabilities are on netbirds side , we'd rather not take the risk and so the Virtual LAN was taken down. However you may still use the program.
*Long answer. YOU CAN*This has not been tested but I see no reason why it wouldnt work. If you would like to install Cura on ubuntu simply install netbird by following the instructions on netbirds website and then cloning this repository. Install the pip  requirements using "pip install -r requirements.txt" and then run CuraHTTP.(EDIT: This is infact not all. for the program to work you'll need to create a network of peers. To find out how ,create a new issue request if one isnt already pinned and I'll probably reply). The program currently does not run on windows on its own. To get it to work on windows you'll need to probably use wsl.
