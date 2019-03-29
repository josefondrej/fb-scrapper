Facebook Scrapper and Profile Viewer
=================

Create the following directories in the root:  
```
- events
- profiles
- static\profile_pics
```

Add your facebook credentials to `credentials.json` file (see `credentials_template.json`). 

You can run some examples using scripts in `examples` directory. Try for example 
```
python parse_profile.py --help
```
To view the profiles belonging to some event run 
```buildoutcfg
python server.py --event-name="some name"
```
