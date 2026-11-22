-- 1. Crear la tabla de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Crear la tabla de Productos (Inventario)
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- 3. Crear la tabla de Historial de Compras
CREATE TABLE IF NOT EXISTS compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    producto_id INT,
    cantidad INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- 4. Insertar productos de maquillaje y belleza de ejemplo
INSERT INTO productos (nombre, descripcion, precio, stock) VALUES 
('Labial Mate Larga Duración', 'Labial líquido mate de alta pigmentación, tono rojo intenso.', 15.99, 50),
('Paleta de Sombras Glam', 'Paleta con 12 colores altamente pigmentados, acabados mate y brillante.', 25.50, 30),
('Base Líquida Cobertura Total', 'Base de maquillaje de cobertura completa con acabado natural.', 18.00, 40),
('Máscara de Pestañas Extrema', 'Máscara de pestañas a prueba de agua para un volumen máximo.', 12.50, 60),
('Set de Brochas Profesionales', 'Juego de 10 brochas de maquillaje con estuche de cuero.', 35.00, 25),
('Rubor en Polvo', 'Rubor de textura suave con acabado luminoso, tono melocotón.', 14.00, 35);