<?php
/**
 * File: src/Views/layout_dashboard.php
 * @package NAO-Smart-AI
 * @author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
 *
 * Created Date: Tuesday, December 17th 2025, 10:52:06 pm
 * -----
 * Last Modified: 	December 17th 2025 10:52:06 pm
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

    <!-- Vendor CSS Files -->
    <link href="<?= url('assets/vendor/bootstrap/css/bootstrap.min.css') ?>" rel="stylesheet">
    <link href="<?= url('assets/vendor/bootstrap-icons/bootstrap-icons.css') ?>" rel="stylesheet">
    <link href="<?= url('assets/vendor/aos/aos.css') ?>" rel="stylesheet">
    <link href="<?= url('assets/vendor/glightbox/css/glightbox.min.css') ?>" rel="stylesheet">
    <link href="<?= url('assets/vendor/swiper/swiper-bundle.min.css') ?>" rel="stylesheet">

    <!-- Main CSS File -->
    <link href="<?= url('assets/css/main.css') ?>" rel="stylesheet">
</head>

<body class="index-page">

    <header id="header" class="header d-flex align-items-center fixed-top">
        <div
            class="header-container container-fluid container-xl position-relative d-flex align-items-center justify-content-between">

            <a href="<?= url('dashboard') ?>" class="logo d-flex align-items-center me-auto me-xl-0">
                <h1 class="sitename">NAO Smart AI</h1>
            </a>

            <nav id="navmenu" class="navmenu">
                <ul>
                    <li><a href="<?= url('dashboard') ?>" class="active">Dashboard</a></li>

                    <li class="dropdown"><a href="#"><span>Tabelle</span> <i
                                class="bi bi-chevron-down toggle-dropdown"></i></a>
                        <ul>
                            <li><a href="<?= url('anagrafe/elenco') ?>">Anagrafe</a></li>
                            <!-- Menu riservato agli admin -->
                            <?php if (($_SESSION['user_role'] ?? '') === 'admin'): ?>
                                <li><a href="<?= url('users') ?>">Utenti</a></li>
                            <?php endif; ?>
                        </ul>
                    </li>
                </ul>
                <i class="mobile-nav-toggle d-xl-none bi bi-list"></i>
            </nav>

            <div class="d-flex align-items-center gap-3">
                <div class="d-none d-md-block text-muted small">
                    Benvenuto, <strong><?= htmlspecialchars($_SESSION['user_name'] ?? 'Utente') ?></strong>
                </div>
                <a class="btn-getstarted" href="<?= url('auth/logout') ?>">Esci</a>
            </div>

        </div>
    </header>

    <main class="main" style="padding-top: 100px; min-height: calc(100vh - 100px);">
        <div class="container">
            <div class="row">
                <div class="col">
                    <?= $content ?? '' ?>
                </div>
            </div>
        </div>
    </main>

    <footer id="footer" class="footer">

        <div class="container footer-top">
            <div class="row gy-4">
                <div class="col-lg-4 col-md-6 footer-about">
                    <a href="index.html" class="logo d-flex align-items-center">
                        <span class="sitename">iLanding</span>
                    </a>
                    <div class="footer-contact pt-3">
                        <p>A108 Adam Street</p>
                        <p>New York, NY 535022</p>
                        <p class="mt-3"><strong>Phone:</strong> <span>+1 5589 55488 55</span></p>
                        <p><strong>Email:</strong> <span>info@example.com</span></p>
                    </div>
                </div>

                <div class="col-lg-2 col-md-3 footer-links">
                    <h4>Useful Links</h4>
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">About us</a></li>
                        <li><a href="#">Services</a></li>
                    </ul>
                </div>

            </div>
        </div>

        <div class="container copyright text-center mt-4">
            <p>© <span>Copyright</span> <strong class="px-1 sitename">iLanding</strong> <span>All Rights Reserved</span>
            </p>
            <div class="credits">
                Designed by <a href="https://bootstrapmade.com/">BootstrapMade</a>
            </div>
        </div>

    </footer>

    <!-- Scroll Top -->
    <a href="#" id="scroll-top" class="scroll-top d-flex align-items-center justify-content-center"><i
            class="bi bi-arrow-up-short"></i></a>

    <!-- Vendor JS Files -->
    <script src="<?= url('assets/vendor/bootstrap/js/bootstrap.bundle.min.js') ?>"></script>
    <script src="<?= url('assets/vendor/php-email-form/validate.js') ?>"></script>
    <script src="<?= url('assets/vendor/aos/aos.js') ?>"></script>
    <script src="<?= url('assets/vendor/glightbox/js/glightbox.min.js') ?>"></script>
    <script src="<?= url('assets/vendor/swiper/swiper-bundle.min.js') ?>"></script>
    <script src="<?= url('assets/vendor/purecounter/purecounter_vanilla.js') ?>"></script>

    <!-- Main JS File -->
    <script src="<?= url('assets/js/main.js') ?>"></script>

</body>

</html>