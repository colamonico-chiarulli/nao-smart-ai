<?php
/**
 * File: src/Views/errors/403.php
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

<!-- 403 Forbidden Page -->
<section id="hero" class="hero section" style="min-height: 60vh;">
    <div class="container" data-aos="fade-up" data-aos-delay="100">
        <div class="row align-items-center justify-content-center text-center">
            <div class="col-lg-8">
                <div class="hero-content" data-aos="fade-up" data-aos-delay="200">
                    <div class="company-badge mb-4 bg-danger text-white">
                        <i class="bi bi-shield-x me-2"></i>
                        Accesso Negato
                    </div>
                    <h1 class="mb-4">
                        <span class="text-danger">403</span><br>
                        Forbidden
                    </h1>
                    <p class="mb-4 mb-md-5">
                        Non hai i permessi necessari per accedere a questa risorsa.
                        Contatta l'amministratore se ritieni si tratti di un errore.
                    </p>
                    <div class="hero-buttons">
                        <a href="<?= url('dashboard') ?>" class="btn btn-primary me-2">
                            <i class="bi bi-house-fill me-2"></i>Torna alla Dashboard
                        </a>
                        <a href="<?= url('auth/logout') ?>" class="btn btn-outline-secondary">
                            <i class="bi bi-box-arrow-right me-2"></i>Logout
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>