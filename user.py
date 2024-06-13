class User:
    def __init__(self, username, socket, x_coord, y_coord):
        self.__socket = socket
        self.__username = username
        self.__x_coord = x_coord
        self.__y_coord = y_coord
    
    @property
    def getSocket(self):
        return self.__socket
    
    @property
    def getUsername(self):
        return self.__username
    
    @property
    def getX(self):
        return self.__x_coord
    
    @property
    def getY(self):
        return self.__y_coord
    
    def setX(self, new_x):
        self.__x_coord = new_x

    def setY(self, new_y):
        self.__y_coord = new_y

    

