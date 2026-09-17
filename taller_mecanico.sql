CREATE DATABASE taller_mecanico;

USE taller_mecanico;

CREATE TABLE roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,

    FOREIGN KEY (id_rol)
        REFERENCES roles(id_rol)
);

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(30) NOT NULL UNIQUE,
    telefono VARCHAR(30) NOT NULL,
    email VARCHAR(150)
);
-- para el modelo inicial quedan marca y modelo del vehículo como está, pero se debe de normalizar y hacer como tablas a parte
CREATE TABLE vehiculos (
    id_vehiculo INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    anio INT NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    chasis VARCHAR(50) UNIQUE,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);


CREATE TABLE servicios (
    id_servicio INT PRIMARY KEY AUTO_INCREMENT,
    nombre_servicio VARCHAR(100) NOT NULL,
    descripcion TEXT,
    costo INT NOT NULL,
    horas INT NOT NULL
);

CREATE TABLE proveedores (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(30) NOT NULL UNIQUE,
    telefono VARCHAR(30) NOT NULL,
    email VARCHAR(150)
);

CREATE TABLE repuestos (
    id_repuesto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_pieza VARCHAR(150) NOT NULL,
    costo INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 0
);

CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_proveedor INT NOT NULL,
    fecha_pedido DATE NOT NULL,
    estado VARCHAR(30) NOT NULL,

    FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
);

CREATE TABLE detalle_pedido (
    id_detalle_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_repuesto INT NOT NULL,
    cantidad INT NOT NULL,

    FOREIGN KEY (id_pedido)
        REFERENCES pedidos(id_pedido),

    FOREIGN KEY (id_repuesto)
        REFERENCES repuestos(id_repuesto)
);

CREATE TABLE reparaciones (
    id_reparacion INT PRIMARY KEY AUTO_INCREMENT,
    id_vehiculo INT NOT NULL,
    id_cliente INT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_reparacion DATE,

    FOREIGN KEY (id_vehiculo)
        REFERENCES vehiculos(id_vehiculo),

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);

CREATE TABLE reparacion_servicio (
    id_reparacion INT NOT NULL,
    id_servicio INT NOT NULL,

    PRIMARY KEY (id_reparacion, id_servicio),

    FOREIGN KEY (id_reparacion)
        REFERENCES reparaciones(id_reparacion),

    FOREIGN KEY (id_servicio)
        REFERENCES servicios(id_servicio)
);

CREATE TABLE turnos (
    id_turno INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora TIME,
    id_cliente INT NOT NULL,
    id_vehiculo INT NOT NULL,
    id_reparacion INT,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    FOREIGN KEY (id_vehiculo)
        REFERENCES vehiculos(id_vehiculo),

    FOREIGN KEY (id_reparacion)
        REFERENCES reparaciones(id_reparacion)
);

CREATE TABLE presupuestos (
    id_presupuesto INT PRIMARY KEY AUTO_INCREMENT,
    id_reparacion INT NOT NULL,
    mano_obra INT,
    total INT NOT NULL DEFAULT 0,

    FOREIGN KEY (id_reparacion)
        REFERENCES reparaciones(id_reparacion)
);
