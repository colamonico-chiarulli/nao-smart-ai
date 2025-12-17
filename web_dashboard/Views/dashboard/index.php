<?php
/**
 * File: src/Controllers/AuthController.php
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

<!-- Hero Section -->
<section id="hero" class="hero section">
    <div class="container" data-aos="fade-up" data-aos-delay="100">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <div class="hero-content" data-aos="fade-up" data-aos-delay="200">
                    <div class="company-badge mb-4">
                        <i class="bi bi-gear-fill me-2"></i>
                        Backend Administration
                    </div>
                    <h1 class="mb-4">
                        Welcome Back, <br>
                        <?= h($_SESSION['user_name'] ?? 'User') ?>! <br>
                        <span class="accent-text">NAO Smart AI Dashboard</span>
                    </h1>
                    <p class="mb-4 mb-md-5">
                        Manage your database, users, and AI settings from this central hub.
                        Select a module below or from the navigation menu to get started.
                    </p>
                    <div class="hero-buttons">
                        <a href="<?= url('anagrafe/elenco') ?>" class="btn btn-primary me-0 me-sm-2 mx-1">
                            <i class="bi bi-people-fill me-2"></i> Anagrafe
                        </a>
                        <a href="<?= url('users') ?>" class="btn btn-secondary mt-2 mt-sm-0">
                            <i class="bi bi-person-gear me-2"></i> Users
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="hero-image" data-aos="zoom-out" data-aos-delay="300">
                    <img src="<?= url('assets/img/illustration-1.webp') ?>" alt="Hero Image" class="img-fluid">
                    <div class="customers-badge">
                        <!-- Example stats -->
                        <p class="mb-0 mt-2">Gestione completa del sistema</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row stats-row gy-4 mt-5" data-aos="fade-up" data-aos-delay="500">
            <div class="col-lg-3 col-md-6">
                <div class="stat-item">
                    <div class="stat-icon">
                        <i class="bi bi-people-fill"></i>
                    </div>
                    <div class="stat-content">
                        <h4>Anagrafe</h4>
                        <p class="mb-0">Gestione Contatti</p>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stat-item">
                    <div class="stat-icon">
                        <i class="bi bi-person-gear"></i>
                    </div>
                    <div class="stat-content">
                        <h4>Utenti</h4>
                        <p class="mb-0">Gestione Accessi</p>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stat-item">
                    <div class="stat-icon">
                        <i class="bi bi-database"></i>
                    </div>
                    <div class="stat-content">
                        <h4>Database</h4>
                        <p class="mb-0">MySQL Connected</p>
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="stat-item">
                    <div class="stat-icon">
                        <i class="bi bi-shield-check"></i>
                    </div>
                    <div class="stat-content">
                        <h4>Sicurezza</h4>
                        <p class="mb-0">Session Active</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section><!-- /Hero Section -->

<!-- About Section -->
<section id="about" class="about section">
    <div class="container" data-aos="fade-up" data-aos-delay="100">
        <div class="row gy-4 align-items-center justify-content-between">
            <div class="col-xl-5" data-aos="fade-up" data-aos-delay="200">
                <span class="about-meta">DASHBOARD INFO</span>
                <h2 class="about-title">Gestione Semplificata</h2>
                <p class="about-description">Questa dashboard è progettata per offrire un accesso rapido e intuitivo a
                    tutte le funzionalità amministrative.</p>
            </div>
        </div>
    </div>
</section>