-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Creato il: Dic 17, 2025 alle 22:32
-- Versione del server: 11.8.3-MariaDB-0+deb13u1 from Debian
-- Versione PHP: 8.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `BSGestioneDatabase`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `anagrafe`
--

CREATE TABLE `anagrafe` (
  `idContatto` tinyint(3) UNSIGNED NOT NULL,
  `cognome` varchar(50) DEFAULT NULL,
  `nome` varchar(50) DEFAULT NULL,
  `indirizzo` varchar(50) DEFAULT NULL,
  `com_residenza_id` tinyint(3) UNSIGNED NOT NULL,
  `prov` char(2) DEFAULT NULL,
  `data_nascita` date DEFAULT NULL,
  `com_nascita_id` tinyint(3) UNSIGNED NOT NULL,
  `prov_nascita` char(2) DEFAULT NULL,
  `email` char(30) DEFAULT NULL,
  `cellulare` char(15) DEFAULT NULL,
  `telefono` char(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `anagrafe`
--

INSERT INTO `anagrafe` (`idContatto`, `cognome`, `nome`, `indirizzo`, `com_residenza_id`, `prov`, `data_nascita`, `com_nascita_id`, `prov_nascita`, `email`, `cellulare`, `telefono`) VALUES
(2, 'Garrals', 'Zedekiah', '64836 Corscot Lane', 38, 'BA', '0000-00-00', 42, 'BA', 'zgarrals1@github.com', '601-853-0498', '705-351-0034'),
(3, 'Gullyes', 'Brianne', '35 Stephen Lane', 23, 'BA', '0000-00-00', 31, 'BA', 'bgullyes2@goo.ne.jp', '868-660-7459', '140-366-1188'),
(4, 'Righy', 'Renee', '860 Orin Park', 41, 'BA', '0000-00-00', 19, 'BA', 'rrighy3@flickr.com', '330-580-0323', '339-784-1272'),
(5, 'Laffin', 'Kalil', '14 South Pass', 18, 'BA', '0000-00-00', 22, 'BA', 'klaffin4@latimes.com', '781-819-4805', '895-506-4176'),
(6, 'Bollom', 'Ladonna', '83 Northview Alley', 36, 'BA', '0000-00-00', 22, 'BA', 'lbollom5@pen.io', '751-260-3993', '135-534-9167'),
(7, 'Dumbare', 'Zerk', '9 Valley Edge Hill', 19, 'BA', '0000-00-00', 19, 'BA', 'zdumbare6@netscape.com', '494-700-5259', '687-350-2994'),
(8, 'Eglese', 'Meryl', '20254 Loftsgordon Circle', 36, 'BA', '0000-00-00', 9, 'BA', 'meglese7@reuters.com', '581-311-1417', '531-494-1398'),
(9, 'Zoanetti', 'Sylvia', '4 Village Green Park', 10, 'BA', '0000-00-00', 6, 'BA', 'szoanetti8@google.com.hk', '957-516-7666', '649-864-9393'),
(10, 'Slafford', 'Aguste', '45 East Alley', 44, 'BA', '0000-00-00', 12, 'BA', 'aslafford9@mapquest.com', '886-171-3626', '613-473-5569'),
(11, 'Gravestone', 'Amalee', '08 Vernon Hill', 5, 'BA', '0000-00-00', 22, 'BA', 'agravestonea@opensource.org', '122-111-4074', '970-972-5922'),
(12, 'Pillman', 'Clyve', '166 North Plaza', 38, 'BA', '0000-00-00', 23, 'BA', 'cpillmanb@skype.com', '891-372-9861', '732-979-7460'),
(13, 'Reschke', 'Antin', '685 Brown Street', 28, 'B', NULL, 3, 'BA', 'areschkec@wufoo.com', '601-522-8125', '626-953-6210'),
(14, 'Proffitt', 'Humbert', '66663 Graedel Crossing', 43, 'BA', '0000-00-00', 26, 'BA', 'hproffittd@smh.com.au', '839-595-0287', '697-562-9227'),
(15, 'Minards', 'Nelli', '49 Tennyson Center', 20, 'BA', '0000-00-00', 19, 'BA', 'nminardse@netvibes.com', '466-663-3566', '333-948-7780'),
(16, 'Petroselli', 'Mollie', '76 Dahle Drive', 14, 'BA', '0000-00-00', 35, 'BA', 'mpetrosellif@irs.gov', '903-954-0233', '249-345-6191'),
(17, 'Lumby', 'Reta', '472 Bowman Road', 23, 'BA', '0000-00-00', 31, 'BA', 'rlumbyg@sogou.com', '599-631-3566', '181-506-3596'),
(18, 'O\'Sheils', 'Web', '359 Schurz Road', 5, 'BA', '0000-00-00', 14, 'BA', 'wosheilsh@storify.com', '524-775-8245', '416-101-9292'),
(19, 'Tirrey', 'Tarah', '1401 Waxwing Court', 2, 'BA', '0000-00-00', 23, 'BA', 'ttirreyi@marriott.com', '161-565-5213', '302-474-1959'),
(20, 'Brinsden', 'Koral', '351 Morning Junction', 25, 'BA', '0000-00-00', 9, 'BA', 'kbrinsdenj@sciencedaily.com', '858-264-8851', '651-551-2406'),
(21, 'Ragbourne', 'Taryn', '24 Messerschmidt Street', 24, 'BA', '0000-00-00', 7, 'BA', 'tragbournek@aboutads.info', '196-556-9739', '665-380-0641'),
(22, 'Peart', 'Darrel', '76 Northview Alley', 37, 'BA', '0000-00-00', 46, 'BA', 'dpeartl@is.gd', '812-584-8444', '296-782-2142'),
(23, 'McPartlin', 'Bianca', '7389 Dwight Lane', 31, 'BA', '0000-00-00', 30, 'BA', 'bmcpartlinm@mail.ru', '565-588-9256', '113-179-7890'),
(24, 'Lockhart', 'Deny', '36640 Milwaukee Court', 6, 'BA', '0000-00-00', 48, 'BA', 'dlockhartn@reference.com', '610-957-1931', '957-533-3325'),
(25, 'Worsfold', 'Stephie', '6198 Grim Way', 45, 'BA', '0000-00-00', 22, 'BA', 'sworsfoldo@creativecommons.org', '487-865-3913', '220-484-6650'),
(26, 'Shepley', 'Louise', '0358 Pennsylvania Avenue', 15, 'BA', '0000-00-00', 45, 'BA', 'lshepleyp@themeforest.net', '322-496-0656', '742-502-5795'),
(27, 'Delouch', 'Kare', '50 Oak Valley Junction', 37, 'BA', '0000-00-00', 13, 'BA', 'kdelouchq@instagram.com', '711-737-1894', '668-684-2605'),
(28, 'Iowarch', 'Billy', '509 Cordelia Lane', 41, 'BA', '0000-00-00', 15, 'BA', 'biowarchr@examiner.com', '346-637-1387', '770-997-4214'),
(29, 'Blyth', 'Archie', '704 Rieder Terrace', 37, 'BA', '0000-00-00', 37, 'BA', 'ablyths@upenn.edu', '923-174-1826', '385-274-8127'),
(30, 'Drewson', 'Vincenty', '8 Doe Crossing Circle', 38, 'BA', '0000-00-00', 23, 'BA', 'vdrewsont@privacy.gov.au', '121-491-5049', '160-464-0199'),
(31, 'Humpherson', 'Mommy', '2654 Reinke Drive', 15, 'BA', '0000-00-00', 41, 'BA', 'mhumphersonu@patch.com', '382-526-8209', '971-264-7296'),
(32, 'Allso', 'Min', '50 Oakridge Trail', 7, 'BA', NULL, 3, 'BA', 'mallsov@ebay.co.uk', '193-792-3432', '960-597-5566'),
(33, 'Hamblington', 'Zandra', '25311 Eggendart Way', 2, 'BA', '0000-00-00', 10, 'BA', 'zhamblingtonw@cnbc.com', '176-519-0287', '856-670-8199'),
(34, 'Mougeot', 'Chucho', '3 Dovetail Crossing', 7, 'BA', '0000-00-00', 36, 'BA', 'cmougeotx@spotify.com', '712-417-1474', '782-121-6950'),
(35, 'Lumsdale', 'Bell', '53931 Scofield Hill', 31, 'BA', '0000-00-00', 1, 'BA', 'blumsdaley@mapquest.com', '754-199-6163', '467-347-1475'),
(36, 'Skough', 'Vanna', '62748 Sullivan Trail', 47, 'BA', '0000-00-00', 16, 'BA', 'vskoughz@gmpg.org', '895-268-6877', '683-112-6865'),
(37, 'Collyer', 'Chris', '00339 Straubel Hill', 39, 'BA', '0000-00-00', 41, 'BA', 'ccollyer10@sun.com', '713-737-0804', '337-954-4474'),
(38, 'Paliser', 'Datha', '2624 Eastlawn Terrace', 19, 'BA', '0000-00-00', 27, 'BA', 'dpaliser11@bloomberg.com', '702-317-5337', '594-944-1096'),
(39, 'Camoys', 'Clare', '50 Meadow Valley Trail', 4, 'BA', '0000-00-00', 28, 'BA', 'ccamoys12@php.net', '750-321-2648', '808-174-2390'),
(40, 'Grutchfield', 'Nealy', '41728 Ludington Trail', 3, 'BA', '0000-00-00', 41, 'BA', 'ngrutchfield13@indiatimes.com', '354-951-0416', '887-835-3537'),
(41, 'Bruckenthal', 'Kimberlyn', '484 Hayes Circle', 32, 'BA', '0000-00-00', 7, 'BA', 'kbruckenthal14@va.gov', '944-603-8394', '429-737-8212'),
(42, 'Glasspoole', 'Penelope', '666 Hagan Circle', 24, 'BA', '0000-00-00', 28, 'BA', 'pglasspoole15@posterous.com', '571-431-0378', '596-964-8483'),
(43, 'Lytell', 'Melissa', '576 Barby Trail', 22, 'BA', '0000-00-00', 47, 'BA', 'mlytell16@ebay.co.uk', '595-378-1826', '695-583-0989'),
(44, 'Whitter', 'Deedee', '823 Loeprich Lane', 1, 'BA', '0000-00-00', 42, 'BA', 'dwhitter17@hubpages.com', '303-352-4900', '123-738-5567'),
(45, 'Delph', 'Irvin', '8 Garrison Point', 11, 'BA', '0000-00-00', 13, 'BA', 'idelph18@de.vu', '196-944-6674', '730-451-0303'),
(46, 'Arch', 'Anabel', '2 Sachtjen Plaza', 39, 'BA', '0000-00-00', 38, 'BA', 'aarch19@vimeo.com', '227-742-6312', '521-140-4244'),
(47, 'Commings', 'Jillane', '585 Butternut Center', 43, 'BA', '0000-00-00', 45, 'BA', 'jcommings1a@lycos.com', '700-363-5824', '680-399-0111'),
(48, 'Reucastle', 'Malanie', '9 Macpherson Street', 33, 'BA', '0000-00-00', 19, 'BA', 'mreucastle1b@friendfeed.com', '668-943-8033', '985-921-0200'),
(49, 'Innot', 'Marnia', '493 Harper Pass', 4, 'BA', '0000-00-00', 21, 'BA', 'minnot1c@biblegateway.com', '988-523-9236', '869-961-0611'),
(50, 'Molian', 'Roselia', '62410 Tony Park', 8, 'BA', '0000-00-00', 29, 'BA', 'rmolian1d@tripadvisor.com', '334-985-4210', '573-689-1012'),
(51, 'Davidson', 'Harrie', '0 Dawn Place', 41, 'BA', '0000-00-00', 31, 'BA', 'hdavidson1e@cam.ac.uk', '169-321-5731', '904-957-2192'),
(52, 'Conew', 'Gustaf', '60984 Texas Plaza', 21, 'BA', '0000-00-00', 37, 'BA', 'gconew1f@unesco.org', '696-879-7302', '796-918-3888'),
(53, 'Botfield', 'Micah', '0819 Mcbride Junction', 44, 'BA', '0000-00-00', 40, 'BA', 'mbotfield1g@constantcontact.co', '758-314-1192', '861-242-2943'),
(54, 'Braunfeld', 'Timofei', '082 Granby Lane', 34, 'BA', '0000-00-00', 33, 'BA', 'tbraunfeld1h@dropbox.com', '486-830-1155', '716-551-5797'),
(55, 'Ioan', 'Pace', '8197 Vermont Place', 3, 'BA', '0000-00-00', 9, 'BA', 'pioan1i@dmoz.org', '568-569-6688', '969-817-6286'),
(56, 'Franchi', 'Franklyn', '2 Cordelia Lane', 43, 'BA', '0000-00-00', 36, 'BA', 'ffranchi1j@google.es', '247-405-9897', '112-905-0248'),
(57, 'Askwith', 'Ruddy', '259 Ronald Regan Place', 44, 'BA', '0000-00-00', 13, 'BA', 'raskwith1k@godaddy.com', '699-692-3231', '596-255-6724'),
(58, 'McArdell', 'Olympe', '0 Gale Circle', 38, 'BA', '0000-00-00', 48, 'BA', 'omcardell1l@usda.gov', '165-659-9758', '206-793-2093'),
(59, 'Gellately', 'Kahaleel', '8918 Cody Drive', 1, 'BA', '0000-00-00', 6, 'BA', 'kgellately1m@umn.edu', '761-749-9269', '220-366-7096'),
(60, 'McCoughan', 'Janean', '89694 Fairview Parkway', 11, 'BA', '0000-00-00', 26, 'BA', 'jmccoughan1n@xing.com', '515-928-6975', '424-281-3799'),
(61, 'Hold', 'Giorgio', '58054 Cottonwood Terrace', 37, 'BA', '0000-00-00', 39, 'BA', 'ghold1o@google.fr', '648-971-2131', '548-327-5892'),
(62, 'Maxted', 'Amory', '08 Bunting Hill', 16, 'BA', '0000-00-00', 34, 'BA', 'amaxted1p@psu.edu', '569-765-9594', '140-233-3244'),
(63, 'Pask', 'Nikaniki', '706 Mosinee Drive', 9, 'BA', '0000-00-00', 39, 'BA', 'npask1q@ucoz.com', '448-590-8773', '197-404-1694'),
(64, 'Maddinon', 'Neely', '144 Coleman Road', 7, 'BA', '0000-00-00', 27, 'BA', 'nmaddinon1r@nationalgeographic', '995-387-0965', '378-676-6817'),
(65, 'Mucillo', 'Fionnula', '73614 Hauk Plaza', 2, 'BA', '0000-00-00', 25, 'BA', 'fmucillo1s@lulu.com', '290-260-7351', '285-883-6366'),
(66, 'Woolrich', 'Cymbre', '4510 Scott Point', 1, 'BA', '0000-00-00', 19, 'BA', 'cwoolrich1t@samsung.com', '290-637-2717', '448-437-3197'),
(67, 'Wiltsher', 'Wanda', '2076 Columbus Park', 36, 'BA', '0000-00-00', 41, 'BA', 'wwiltsher1u@dailymotion.com', '738-223-5529', '601-300-5438'),
(68, 'Vardey', 'Filmore', '7 Northridge Lane', 1, 'BA', '0000-00-00', 12, 'BA', 'fvardey1v@artisteer.com', '912-674-9047', '534-935-1922'),
(69, 'Yeowell', 'Bryna', '61 Artisan Street', 26, 'BA', '0000-00-00', 11, 'BA', 'byeowell1w@bluehost.com', '169-799-6458', '528-372-5026'),
(70, 'Colaton', 'Udall', '59201 Gale Circle', 10, 'BA', '0000-00-00', 33, 'BA', 'ucolaton1x@creativecommons.org', '278-542-0274', '875-131-8411'),
(71, 'Althrope', 'Barris', '77 Garrison Drive', 46, 'BA', '0000-00-00', 20, 'BA', 'balthrope1y@auda.org.au', '980-123-3278', '793-824-4917'),
(72, 'Whapple', 'Hymie', '829 Portage Terrace', 45, 'BA', '0000-00-00', 23, 'BA', 'hwhapple1z@addthis.com', '167-496-5480', '271-665-3614'),
(73, 'Shedd', 'Jojo', '49408 Anhalt Road', 25, 'BA', '0000-00-00', 1, 'BA', 'jshedd20@usgs.gov', '200-872-5974', '509-864-6337'),
(74, 'Castletine', 'Tammi', '1232 East Drive', 17, 'BA', '0000-00-00', 45, 'BA', 'tcastletine21@npr.org', '662-579-7571', '197-754-1274'),
(75, 'Kiln', 'Edward', '84 Stang Place', 30, 'BA', '0000-00-00', 46, 'BA', 'ekiln22@icio.us', '444-245-9175', '602-670-0006'),
(76, 'Neylon', 'Fredia', '69749 Ruskin Plaza', 42, 'BA', '0000-00-00', 6, 'BA', 'fneylon23@umn.edu', '982-296-6358', '312-981-8294'),
(77, 'Bechley', 'Renault', '6368 Cascade Hill', 2, 'BA', '0000-00-00', 39, 'BA', 'rbechley24@gov.uk', '436-146-8041', '771-800-4996'),
(78, 'Stanfield', 'Blinnie', '1279 Warbler Avenue', 48, 'BA', '0000-00-00', 40, 'BA', 'bstanfield25@plala.or.jp', '825-194-0829', '641-188-2780'),
(79, 'Scarasbrick', 'Matthieu', '60320 Beilfuss Junction', 38, 'BA', '0000-00-00', 30, 'BA', 'mscarasbrick26@ovh.net', '333-743-5288', '918-909-8846'),
(80, 'Faley', 'Gwendolin', '25379 Victoria Road', 16, 'BA', '0000-00-00', 44, 'BA', 'gfaley27@sina.com.cn', '770-214-9535', '526-931-6833'),
(81, 'Antonoczyk', 'Cesare', '316 Morning Pass', 8, 'BA', '0000-00-00', 43, 'BA', 'cantonoczyk28@usa.gov', '779-975-5419', '330-382-0853'),
(82, 'Delacourt', 'Emmye', '51436 Brentwood Street', 17, 'BA', '0000-00-00', 21, 'BA', 'edelacourt29@artisteer.com', '870-608-8440', '255-321-1091'),
(83, 'Piris', 'Harriot', '03337 Loomis Junction', 42, 'BA', '0000-00-00', 16, 'BA', 'hpiris2a@seattletimes.com', '109-377-1018', '156-272-3307'),
(84, 'Cornelius', 'Ferdinand', '7442 Division Way', 9, 'BA', '0000-00-00', 32, 'BA', 'fcornelius2b@senate.gov', '922-404-2200', '307-500-1463'),
(85, 'Gorick', 'Haily', '53 Kim Court', 12, 'BA', '0000-00-00', 37, 'BA', 'hgorick2c@senate.gov', '711-888-4475', '247-834-3253'),
(86, 'Grabb', 'Kendall', '8 Ridgeway Parkway', 28, 'BA', '0000-00-00', 4, 'BA', 'kgrabb2d@eepurl.com', '798-481-7348', '483-185-7871'),
(87, 'Brightey', 'Kennith', '802 Dixon Crossing', 35, 'BA', '0000-00-00', 20, 'BA', 'kbrightey2e@fotki.com', '691-363-1719', '805-314-9673'),
(88, 'Redpath', 'Dorothea', '908 Brown Point', 46, 'BA', '0000-00-00', 24, 'BA', 'dredpath2f@oaic.gov.au', '829-885-2719', '991-143-3616'),
(89, 'Marchello', 'Katherina', '52306 Thackeray Lane', 22, 'BA', '0000-00-00', 24, 'BA', 'kmarchello2g@meetup.com', '175-523-9304', '159-192-8004'),
(90, 'Raith', 'Vlad', '005 Hooker Road', 31, 'BA', '0000-00-00', 22, 'BA', 'vraith2h@google.com.br', '670-149-5779', '828-652-9720'),
(91, 'Toxell', 'Benedict', '077 Pennsylvania Court', 14, 'BA', '0000-00-00', 16, 'BA', 'btoxell2i@over-blog.com', '770-693-3624', '329-324-7813'),
(92, 'Baroch', 'Ginnifer', '82636 Westerfield Drive', 40, 'BA', '0000-00-00', 44, 'BA', 'gbaroch2j@macromedia.com', '535-125-3699', '445-633-4107'),
(93, 'Burchell', 'Dwight', '5 Carberry Lane', 41, 'BA', '0000-00-00', 23, 'BA', 'dburchell2k@soup.io', '175-204-4784', '699-546-6157'),
(94, 'Strangman', 'Fernande', '634 Cherokee Point', 36, 'BA', '0000-00-00', 33, 'BA', 'fstrangman2l@purevolume.com', '304-372-7833', '654-272-2564'),
(95, 'Dowglass', 'Boy', '63 Northfield Terrace', 16, 'BA', '0000-00-00', 41, 'BA', 'bdowglass2m@psu.edu', '682-930-5915', '676-150-8055'),
(96, 'Cope', 'Teddi', '10 Waywood Street', 25, 'BA', '0000-00-00', 21, 'BA', 'tcope2n@elpais.com', '713-192-0086', '690-215-0291'),
(97, 'Clunie', 'Zed', '265 Waubesa Junction', 31, 'BA', '0000-00-00', 39, 'BA', 'zclunie2o@acquirethisname.com', '542-194-2539', '550-900-8310'),
(98, 'Andrivot', 'Stefa', '086 Leroy Drive', 6, 'BA', '0000-00-00', 37, 'BA', 'sandrivot2p@archive.org', '707-290-9868', '222-884-5739'),
(99, 'Moro', 'Cheri', '33 East Center', 28, 'BA', '0000-00-00', 30, 'BA', 'cmoro2q@cpanel.net', '255-785-8486', '736-206-2855'),
(100, 'Iddenden', 'Zea', '453 2nd Circle', 3, 'BA', '0000-00-00', 7, 'BA', 'ziddenden2r@soundcloud.com', '237-254-9291', '501-773-1643');

-- --------------------------------------------------------

--
-- Struttura della tabella `comuni`
--

CREATE TABLE `comuni` (
  `idComune` tinyint(3) UNSIGNED NOT NULL,
  `comune` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `comuni`
--

INSERT INTO `comuni` (`idComune`, `comune`) VALUES
(1, 'Acquaviva delle Fonti'),
(2, 'Adelfia'),
(3, 'Alberobello'),
(4, 'Altamura'),
(5, 'Andria'),
(6, 'Bari'),
(7, 'Barletta'),
(8, 'Binetto'),
(9, 'Bisceglie'),
(10, 'Bitetto'),
(11, 'Bitonto'),
(12, 'Bitritto'),
(13, 'Canosa di Puglia'),
(14, 'Capurso'),
(15, 'Casamassima'),
(16, 'Cassano delle Murge'),
(17, 'Castellana Grotte'),
(18, 'Cellamare'),
(19, 'Conversano'),
(20, 'Corato'),
(21, 'Gioia del Colle'),
(22, 'Giovinazzo'),
(23, 'Gravina in Puglia'),
(24, 'Grumo Appula'),
(25, 'Locorotondo'),
(26, 'Minervino Murge'),
(27, 'Modugno'),
(28, 'Mola di Bari'),
(29, 'Molfetta'),
(30, 'Monopoli'),
(31, 'Noci'),
(32, 'Noicattaro'),
(33, 'Palo del Colle'),
(34, 'Poggiorsini'),
(35, 'Polignano a Mare'),
(36, 'Putignano'),
(37, 'Rutigliano'),
(38, 'Ruvo di Puglia'),
(39, 'Sammichele di Bari'),
(40, 'Sannicandro di Bari'),
(41, 'Santeramo in Colle'),
(42, 'Spinazzola'),
(43, 'Terlizzi'),
(44, 'Toritto'),
(45, 'Trani'),
(46, 'Triggiano'),
(47, 'Turi'),
(48, 'Valenzano');

-- --------------------------------------------------------

--
-- Struttura della tabella `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `last_name` varchar(120) NOT NULL,
  `first_name` varchar(120) NOT NULL,
  `organization` varchar(120) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `role` enum('admin','user') NOT NULL DEFAULT 'user',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dump dei dati per la tabella `users`
--

INSERT INTO `users` (`id`, `last_name`, `first_name`, `organization`, `email`, `password`, `phone`, `role`, `created_at`, `updated_at`) VALUES
(1, 'Admin', 'Super', 'Colamonico Chiarulli', 'admin@naosmart.ai', '$2y$12$RAnyeBRQsJx1LgQPEo/yweCn1fm20AqoeiPy7qIqgFmdvrtE/vsFa', '', 'admin', '2025-12-17 17:04:42', '2025-12-17 20:56:09'),
(2, 'Utente', 'Normale', 'Colamonico Chiarulli', 'utente@naosmart.ai', '$2y$12$RAnyeBRQsJx1LgQPEo/yweCn1fm20AqoeiPy7qIqgFmdvrtE/vsFa', '0807568978989', 'user', '2025-12-17 21:24:21', '2025-12-17 22:18:35');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `anagrafe`
--
ALTER TABLE `anagrafe`
  ADD PRIMARY KEY (`idContatto`),
  ADD KEY `fk_anagrafe_comuni` (`com_residenza_id`),
  ADD KEY `fk_anagrafe_comuni1` (`com_nascita_id`);

--
-- Indici per le tabelle `comuni`
--
ALTER TABLE `comuni`
  ADD PRIMARY KEY (`idComune`);

--
-- Indici per le tabelle `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `anagrafe`
--
ALTER TABLE `anagrafe`
  MODIFY `idContatto` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT per la tabella `comuni`
--
ALTER TABLE `comuni`
  MODIFY `idComune` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT per la tabella `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `anagrafe`
--
ALTER TABLE `anagrafe`
  ADD CONSTRAINT `fk_anagrafe_comuni` FOREIGN KEY (`com_residenza_id`) REFERENCES `comuni` (`idComune`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_anagrafe_comuni1` FOREIGN KEY (`com_nascita_id`) REFERENCES `comuni` (`idComune`) ON DELETE NO ACTION ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
