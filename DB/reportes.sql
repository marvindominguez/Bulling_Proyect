-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-04-2023 a las 22:58:54
-- Versión del servidor: 10.4.11-MariaDB
-- Versión de PHP: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `reportes`
--
CREATE DATABASE IF NOT EXISTS `reportes` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `reportes`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login`
--

CREATE TABLE `login` (
  `id_psicologo` int(11) NOT NULL,
  `documento` int(11) NOT NULL,
  `contraseña` int(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `login`
--

INSERT INTO `login` (`id_psicologo`, `documento`, `contraseña`) VALUES
(1, 12345, 12345);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login_profesor`
--

CREATE TABLE `login_profesor` (
  `id_profesor` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(20) NOT NULL,
  `correo` varchar(20) NOT NULL,
  `celular` varchar(10) NOT NULL,
  `documento` int(11) NOT NULL,
  `contraseña` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `login_profesor`
--

INSERT INTO `login_profesor` (`id_profesor`, `nombre`, `apellido`, `correo`, `celular`, `documento`, `contraseña`) VALUES
(1, 'robinson', 'villareal', '', '3004501212', 123456, '123456'),
(2, 'Marvin', 'Dominguez', '112345', '', 1140888950, '1140888950'),
(3, 'pedro', 'ramos', '874587@gmail.com', '45678', 23456789, '23456789');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `r_caso`
--

CREATE TABLE `r_caso` (
  `id_caso` int(11) NOT NULL,
  `semaforo` varchar(10) NOT NULL,
  `observacion` text NOT NULL,
  `id_estudiante` varchar(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(20) NOT NULL,
  `curso` varchar(10) NOT NULL,
  `edad` int(4) NOT NULL,
  `fecha_caso` datetime(6) NOT NULL,
  `genero` varchar(20) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `id_psicologo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `r_caso`
--

INSERT INTO `r_caso` (`id_caso`, `semaforo`, `observacion`, `id_estudiante`, `nombre`, `apellido`, `curso`, `edad`, `fecha_caso`, `genero`, `id_profesor`, `id_psicologo`) VALUES
(1, 'Verde', 'cachon', '1043665653', 'jose', 'duarte', '7°b', 16, '2023-04-18 10:57:00.000000', 'Hombre', 1, 0),
(3, 'Verde', 'cachon', '1043665653', 'jose', 'duarte', '7°b', 16, '2023-04-18 10:57:00.000000', 'Hombre', 2, 0),
(5, 'Amarillo', 'le pegaron 5 compañeros', '1043665653', 'Marvin', 'Dominguez', '7c', 19, '2023-04-19 09:40:00.000000', 'Hombre', 3, 0),
(6, 'Amarillo', 'le pegaron 5 compañeros', '1043665653', 'Marvin', 'Dominguez', '7c', 19, '2023-04-19 09:40:00.000000', 'Hombre', 1, 0),
(7, 'Verde', 'le pegaron', '1043665653', 'jose', 'duarte', '11°', 20, '2023-04-27 11:11:00.000000', 'Hombre', 2, 0),
(8, 'Amarillo', '2', '987654678', 'yoce', 'lin', '99', 65, '2023-04-19 11:22:00.000000', 'Mujer', 1, 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`id_psicologo`);

--
-- Indices de la tabla `login_profesor`
--
ALTER TABLE `login_profesor`
  ADD PRIMARY KEY (`id_profesor`),
  ADD UNIQUE KEY `documento` (`documento`);

--
-- Indices de la tabla `r_caso`
--
ALTER TABLE `r_caso`
  ADD PRIMARY KEY (`id_caso`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `login`
--
ALTER TABLE `login`
  MODIFY `id_psicologo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `login_profesor`
--
ALTER TABLE `login_profesor`
  MODIFY `id_profesor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `r_caso`
--
ALTER TABLE `r_caso`
  MODIFY `id_caso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
