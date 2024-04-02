import configparser

try:
    configur = configparser.ConfigParser()
    configur.read('client_config.ini')
    
    IP = configur.get("Networking", "ip")
    PORT = configur.getint("Networking", "port")
    RESOLUTION = (configur.getint("General", "resolution_x"), configur.getint("General", "resolution_y"))
    MID = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)
except:
    config = configparser.ConfigParser()
    config["General"] = {
        "resolution_x" : 1366,
        "resolution_y" : 768
    }
    config["Networking"] = {
        "ip" : "127.0.0.1",
        "port" : 42069,
    }

    IP = "127.0.0.1"
    PORT = 42069
    RESOLUTION = (1366, 708)
    MID = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)

    with open('client_config.ini', 'w') as configfile:
        config.write(configfile)