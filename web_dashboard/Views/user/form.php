<?php
/**
 * File: src/Views/user/form.php
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

// Variabili: $title, $action, $record, $btnText, $btnClass, $errors, $updateMode
$lastName = h($record['last_name']);
$firstName = h($record['first_name']);
$email = h($record['email']);
$organization = h($record['organization']);
$phone = h($record['phone']);
$role = h($record['role']);
?>

<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow border-0 rounded-4">
            <div class="card-header bg-primary text-white py-3 rounded-top-4">
                <h4 class="mb-0"><i class="bi bi-person-badge-fill me-2"></i><?= $title ?></h4>
            </div>
            <div class="card-body p-4">
                <form role="form" method="post" action="<?= $action ?>">
                    <?= csrf_field() ?>
                    <?php if (isset($record['id']) && $record['id']): ?>
                        <input type="hidden" name="id" value="<?= h($record['id']) ?>">
                    <?php endif; ?>

                    <h5 class="text-primary mb-3 text-uppercase fs-6 fw-bold border-bottom pb-2">Dati Utente</h5>

                    <div class="row g-3 mb-4">
                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" name="user[last_name]" value="<?= $lastName ?>"
                                    class="form-control <?= isset($errors['last_name']) ? 'is-invalid' : '' ?>"
                                    id="last_name" placeholder="Cognome">
                                <label for="last_name"><i class="bi bi-person me-1"></i> Cognome *</label>
                                <?= getFormError('last_name', $errors ?? []) ?>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" name="user[first_name]" value="<?= $firstName ?>"
                                    class="form-control <?= isset($errors['first_name']) ? 'is-invalid' : '' ?>"
                                    id="first_name" placeholder="Nome">
                                <label for="first_name"><i class="bi bi-person me-1"></i> Nome *</label>
                                <?= getFormError('first_name', $errors ?? []) ?>
                            </div>
                        </div>
                    </div>

                    <div class="form-floating mb-3">
                        <input type="text" name="user[organization]" value="<?= $organization ?>" class="form-control"
                            id="organization" placeholder="Organizzazione">
                        <label for="organization"><i class="bi bi-building me-1"></i> Organizzazione</label>
                    </div>

                    <h5 class="text-primary mb-3 text-uppercase fs-6 fw-bold border-bottom pb-2">Credenziali e Contatti
                    </h5>

                    <div class="form-floating mb-3">
                        <input type="email" name="user[email]" value="<?= $email ?>"
                            class="form-control <?= isset($errors['email']) ? 'is-invalid' : '' ?>" id="email"
                            placeholder="nome@esempio.com">
                        <label for="email"><i class="bi bi-envelope me-1"></i> E-Mail *</label>
                        <?= getFormError('email', $errors ?? []) ?>
                    </div>

                    <div class="form-floating mb-3">
                        <input type="password" name="user[password]"
                            class="form-control <?= isset($errors['password']) ? 'is-invalid' : '' ?>" id="password"
                            placeholder="Password">
                        <label for="password"><i class="bi bi-key me-1"></i> Password
                            <?= isset($updateMode) ? '(Lascia vuoto per non cambiare)' : '*' ?></label>
                        <?php if (isset($updateMode)): ?>
                            <small class="text-muted">Inserisci solo se vuoi cambiare la password.</small>
                        <?php endif; ?>
                        <?= getFormError('password', $errors ?? []) ?>
                    </div>

                    <div class="row g-3 mb-4">
                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" name="user[phone]" value="<?= $phone ?>" class="form-control"
                                    id="phone" placeholder="Telefono">
                                <label for="phone"><i class="bi bi-phone me-1"></i> Telefono</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-floating">
                                <select name="user[role]" class="form-select" id="role">
                                    <option value="user" <?= $role === 'user' ? 'selected' : '' ?>>User</option>
                                    <option value="admin" <?= $role === 'admin' ? 'selected' : '' ?>>Admin</option>
                                </select>
                                <label for="role"><i class="bi bi-shield-lock me-1"></i> Ruolo</label>
                            </div>
                        </div>
                    </div>

                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <button type="button" class="btn btn-outline-secondary me-md-2" onclick="history.back()">
                            <i class="bi bi-arrow-left me-1"></i> Annulla
                        </button>
                        <button type="submit" class="btn <?= $btnClass ?? 'btn-primary' ?> btn-lg px-5 shadow-sm"
                            name="invia">
                            <i class="bi bi-save me-2"></i><?= $btnText ?>
                        </button>
                    </div>
                </form>
            </div>
            <div class="card-footer bg-light text-muted small text-center py-2 rounded-bottom-4">
                * Campi obbligatori
            </div>
        </div>
    </div>
</div>