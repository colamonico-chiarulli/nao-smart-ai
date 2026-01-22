<?php

/**
 * File:	/nao-smart-ai/web_dashboard/Views/layout_public.php
 * @package NAO-Smart-AI
 * @author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
 *
 * Created Date: Tuesday, December 17th 2025, 10:52:06 pm
 * -----
 * Last Modified: 	January 12th 2026 9:00:38 pm
 * Modified By: 	Rino Andriano <andriano@colamonicochiarulli.edu.it>
 * -----
 * @license	https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0
 * ------------------------------------------------------------------------------
 *    This program is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Affero General Public License as
 *    published by the Free Software Foundation, either version 3 of the
 *    License, or (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Affero General Public License for more details.
 *
 *    You should have received a copy of the GNU Affero General Public License
 *    along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 *  Additional Terms under Section 7(b):
 *  
 *  The following attribution requirements apply to this work:
 *  
 *  1. Any interactive user interface must preserve the original author
 *     attribution when the AI is asked about its creators
 *  2. System prompts containing author information cannot be modified
 *  3. The robot must always identify its original creators as specified
 *     in the source code
 * ------------------------------------------------------------------------------
 */
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <title><?= $title ?? 'NAO Smart AI Dashboard' ?></title>
    <meta name="description" content="">
    <meta name="keywords" content="">

    <!-- Favicons -->
    <link href="<?= url('assets/img/favicon.png') ?>" rel="icon">
    <link href="<?= url('assets/img/apple-touch-icon.png') ?>" rel="apple-touch-icon">

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com" rel="preconnect">
    <link href="https://fonts.gstatic.com" rel="preconnect" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Nunito:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"
        rel="stylesheet">

    <!-- landing_vendor CSS Files -->
    <link href="<?= url('assets/landing_vendor/bootstrap/css/bootstrap.min.css') ?>" rel="stylesheet">
    <link href="<?= url('assets/landing_vendor/bootstrap-icons/bootstrap-icons.css') ?>" rel="stylesheet">
    <link href="<?= url('assets/landing_vendor/aos/aos.css') ?>" rel="stylesheet">
    <link href="<?= url('assets/landing_vendor/glightbox/css/glightbox.min.css') ?>" rel="stylesheet">
    <link href="<?= url('assets/landing_vendor/swiper/swiper-bundle.min.css') ?>" rel="stylesheet">

    <!-- Main CSS File -->
    <link href="<?= url('assets/css/main.css') ?>" rel="stylesheet">

    <!-- =======================================================
  * Template Name: iLanding
  * Template URL: https://bootstrapmade.com/ilanding-bootstrap-landing-page-template/
  * Updated: Nov 12 2024 with Bootstrap v5.3.3
  * Author: BootstrapMade.com
  * License: https://bootstrapmade.com/license/
  ======================================================== -->
</head>

<body class="index-page">

    <!-- ======= Header ======= -->
    <header id="header" class="header d-flex align-items-center fixed-top">
        <div class="header-container container-fluid container-xl position-relative d-flex align-items-center justify-content-between">

            <a href="#hero" class="logo d-flex align-items-center me-auto me-xl-0">
                <!-- <img src="<?= url('assets/img/logo.png') ?>" alt=""> -->
                <h1 class="sitename">NAO Smart AI</h1>
            </a>

            <nav id="navmenu" class="navmenu">
                <ul>
                    <li><a class="nav-link scrollto active" href="#hero">Home</a></li>
                    <li><a class="nav-link scrollto" href="#about">Perché NAO</a></li>
                    <li><a class="nav-link scrollto" href="#services">Casi d’uso</a></li>
                    <li><a class="nav-link scrollto" href="#features">Come funziona</a></li>
                    <li><a class="nav-link scrollto" href="#testimonials">Impatto</a></li>
                    <li><a class="nav-link scrollto" href="#team">Team</a></li>
                    <li><a class="nav-link scrollto" href="#contact">Contatti</a></li>
                    <!-- <li><a class="getstarted scrollto" href="#contact">Richiedi una demo</a></li> -->
                </ul>
                <i class="mobile-nav-toggle d-xl-none bi bi-list"></i>
            </nav>

            <div class="d-flex">
                 <a class="btn-getstarted" href="#contact">Richiedi una demo</a>
            </div>

        </div>
    </header>
    <!-- End Header -->

    <main class="main">
        <?= $content ?? '' ?>
    </main>

    <!-- ======= Footer ======= -->
    <footer id="footer" class="footer">

        <div class="footer-top">
            <div class="container">
                <div class="row gy-4">

                    <div class="col-lg-4 col-md-6 footer-info">
                        <a href="#hero" class="logo d-flex align-items-center">
                            <span class="sitename">NAO Smart AI</span>
                        </a>
                        <p>Robotica sociale intelligente, empatica e accessibile per la sanità, l’educazione e l’inclusione sociale.</p>
                    </div>

                    <div class="col-lg-4 col-md-6 footer-links">
                        <h4>Risorse</h4>
                        <ul>
                            <li><i class="bi bi-chevron-right"></i> <a href="https://github.com/colamonico-chiarulli/nao-smart-ai" target="_blank">Repository GitHub</a></li>
                            <li><i class="bi bi-chevron-right"></i> <a href="#">Brochure progetto (PDF)</a></li>
                        </ul>
                    </div>

                    <div class="col-lg-4 col-md-6 footer-links">
                        <h4>Legale</h4>
                        <ul>
                            <li><i class="bi bi-chevron-right"></i> <a href="#">Privacy Policy</a></li>
                            <li><i class="bi bi-chevron-right"></i> <a href="#">Licenza GNU AGPL v3</a></li>
                        </ul>
                    </div>

                </div>
            </div>
        </div>

        <div class="container footer-bottom clearfix">
            <div class="copyright">
                &copy; <span id="year"></span> <strong><span>NAO Smart AI</span></strong> – IISS C. Colamonico – N. Chiarulli
            </div>
        </div>
    </footer>
    <!-- End Footer -->

    <script>
        document.getElementById('year').textContent = new Date().getFullYear();
    </script>


    <!-- Scroll Top -->
    <a href="#" id="scroll-top" class="scroll-top d-flex align-items-center justify-content-center"><i
            class="bi bi-arrow-up-short"></i></a>

    <!-- landing_vendor JS Files -->
    <script src="<?= url('assets/landing_vendor/bootstrap/js/bootstrap.bundle.min.js') ?>"></script>
    <script src="<?= url('assets/landing_vendor/php-email-form/validate.js') ?>"></script>
    <script src="<?= url('assets/landing_vendor/aos/aos.js') ?>"></script>
    <script src="<?= url('assets/landing_vendor/glightbox/js/glightbox.min.js') ?>"></script>
    <script src="<?= url('assets/landing_vendor/swiper/swiper-bundle.min.js') ?>"></script>
    <script src="<?= url('assets/landing_vendor/purecounter/purecounter_vanilla.js') ?>"></script>

    <!-- Main JS File -->
    <script src="<?= url('assets/js/main.js') ?>"></script>

</body>

</html>