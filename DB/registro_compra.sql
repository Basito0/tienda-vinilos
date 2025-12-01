CREATE TABLE RegistroCompra (
    CompraID INT AUTO_INCREMENT PRIMARY KEY,
    ProductoID INT,
    CantidadComprada INT,
    FechaCompra DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
);