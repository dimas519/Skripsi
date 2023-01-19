-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 19 Jan 2023 pada 16.22
-- Versi server: 10.4.24-MariaDB
-- Versi PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


--
-- Database: `skripsi`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `basestasion`
--

CREATE TABLE `basestasion` (
  `id` int(11) NOT NULL,
  `token` varchar(20) NOT NULL,
  `addedTimeStamp` datetime NOT NULL DEFAULT current_timestamp(),
  `lastEditTimeStamp` datetime DEFAULT NULL,
  `idLokasi` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Struktur dari tabel `data_sensing-1-1-23`
--

CREATE TABLE `data_sensing-1-1-23` (
  `timeStamp` datetime NOT NULL DEFAULT current_timestamp(),
  `suhu` float NOT NULL,
  `kelembapan` int(11) NOT NULL,
  `tekanan` int(11) NOT NULL,
  `akselerasi` varchar(20) NOT NULL,
  `idBaseStasion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Struktur dari tabel `kota`
--
CREATE TABLE `kota` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------
--
-- Struktur dari tabel `lokasi`
--
CREATE TABLE `lokasi` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `latitude` varchar(20) NOT NULL,
  `longtitude` varchar(20) NOT NULL,
  `indoor` tinyint(1) NOT NULL COMMENT '0= false, 1=true',
  `idKota` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------
--
-- Struktur dari tabel `nodesensor`
--
CREATE TABLE `nodesensor` (
  `id` int(11) NOT NULL,
  `tipeSensor` varchar(10) NOT NULL,
  `interval` int(11) NOT NULL,
  `idBaseStasion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------
--
-- Struktur dari tabel `user`
--
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(30) NOT NULL,
  `role` smallint(6) NOT NULL COMMENT '0 = user, 1 untuk admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `basestasion`
--
ALTER TABLE `basestasion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `berada` (`idLokasi`);

--
-- Indeks untuk tabel `data_sensing-1-1-23`
--
ALTER TABLE `data_sensing-1-1-23`
  ADD PRIMARY KEY (`timeStamp`);

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
  ADD KEY `idBaseStasion` (`idBaseStasion`);

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
-- AUTO_INCREMENT untuk tabel `basestasion`
--
ALTER TABLE `basestasion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `kota`
--
ALTER TABLE `kota`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT untuk tabel `lokasi`
--
ALTER TABLE `lokasi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `nodesensor`
--
ALTER TABLE `nodesensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

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
  ADD CONSTRAINT `nodesensor_ibfk_1` FOREIGN KEY (`idBaseStasion`) REFERENCES `basestasion` (`id`);
COMMIT;
