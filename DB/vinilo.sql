CREATE TABLE Productos (
    ProductoID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion VARCHAR(50) NOT NULL,
    Precio INT,
    Cantidad INT
);

INSERT INTO Productos (Nombre, Descripcion, Precio, Cantidad)
VALUES ("disco1", "un disco", 1000, 100000);