-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Waktu pembuatan: 08 Feb 2023 pada 11.42
-- Versi server: 8.0.32
-- Versi PHP: 8.0.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+07:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--

--
-- Struktur dari tabel `basestasion`
--

CREATE TABLE `basestasion` (
  `identifier` varchar(4) NOT NULL,
  `token` varchar(20) NOT NULL,
  `addedTimeStamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastEditTimeStamp` datetime DEFAULT NULL,
  `interval` int NOT NULL,
  `idLokasi` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- --------------------------------------------------------

--
-- Struktur dari tabel `kota`
--

CREATE TABLE `kota` (
  `id` int NOT NULL,
  `nama` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- --------------------------------------------------------

--
-- Struktur dari tabel `lokasi`
--

CREATE TABLE `lokasi` (
  `id` int NOT NULL,
  `nama` varchar(50) NOT NULL,
  `latitude` varchar(20) NOT NULL,
  `longtitude` varchar(20) NOT NULL,
  `indoor` tinyint(1) NOT NULL COMMENT '0= false, 1=true',
  `idKota` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- --------------------------------------------------------

--
-- Struktur dari tabel `nodesensor`
--

CREATE TABLE `nodesensor` (
  `id` int NOT NULL,
  `tipeSensor` varchar(10) NOT NULL,
  `identifier` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- --------------------------------------------------------

--
-- Struktur dari tabel `queue_update`
--

CREATE TABLE `queue_update` (
  `id` int NOT NULL,
  `command` varchar(50) NOT NULL,
  `idBS` varchar(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(30) NOT NULL,
  `role` smallint NOT NULL COMMENT '0 = user, 1 untuk admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--
-- Indeks untuk tabel `basestasion`
--
ALTER TABLE `basestasion`
  ADD PRIMARY KEY (`identifier`),
  ADD KEY `berada` (`idLokasi`);

--
-- Indeks untuk tabel `kota`
--
ALTER TABLE `kota`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `lokasi`
--
ALTER TABLE `lokasi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `berada di` (`idKota`);

--
-- Indeks untuk tabel `nodesensor`
--
ALTER TABLE `nodesensor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `IdBS` (`identifier`);

--
-- Indeks untuk tabel `queue_update`
--
ALTER TABLE `queue_update`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk base` (`idBS`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `kota`
--
ALTER TABLE `kota`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `lokasi`
--
ALTER TABLE `lokasi`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `nodesensor`
--
ALTER TABLE `nodesensor`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `queue_update`
--
ALTER TABLE `queue_update`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;


--
-- Ketidakleluasaan untuk tabel `basestasion`
--
ALTER TABLE `basestasion`
  ADD CONSTRAINT `berada` FOREIGN KEY (`idLokasi`) REFERENCES `lokasi` (`id`);

--
-- Ketidakleluasaan untuk tabel `lokasi`
--
ALTER TABLE `lokasi`
  ADD CONSTRAINT `berada di` FOREIGN KEY (`idKota`) REFERENCES `kota` (`id`);

--
-- Ketidakleluasaan untuk tabel `nodesensor`
--
ALTER TABLE `nodesensor`
  ADD CONSTRAINT `nodesensor_ibfk_1` FOREIGN KEY (`identifier`) REFERENCES `basestasion` (`identifier`);

--
-- Ketidakleluasaan untuk tabel `queue_update`
--
ALTER TABLE `queue_update`
  ADD CONSTRAINT `fk base` FOREIGN KEY (`idBS`) REFERENCES `basestasion` (`identifier`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
