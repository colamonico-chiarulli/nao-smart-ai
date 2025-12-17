<?php
/**
 * File: src/Views/contact/form.php
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

// Variabili disponibili: $title, $action, $record, $optionsComuni (o Res/Nasc), $btnText, $btnClass, $errors
// Helper globali: h, csrf_field, getErrorMessage

// Escaping dei dati
$cognome = h($record['cognome']);
$nome = h($record['nome']);
$indirizzo = h($record['indirizzo']);
$prov = h($record['prov']);
$data_nascita = h($record['data_nascita']);
$prov_nascita = h($record['prov_nascita']);
$email = h($record['email']);
$cellulare = h($record['cellulare']);
$telefono = h($record['telefono']);

// Gestione differenziata option comuni
$optionsComuniResid = $optionsComuniResid ?? ($optionsComuni ?? '');
$optionsComuniNasc = $optionsComuniNasc ?? ($optionsComuni ?? '');
?>

<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow border-0 rounded-4">
            <div class="card-header bg-primary text-white py-3 rounded-top-4">
                <h4 class="mb-0"><i class="bi bi-person-lines-fill me-2"></i><?= $title ?></h4>
            </div>
            <div class="card-body p-4">
                <form role="form" method="post" action="<?= $action ?>">
                    <?= csrf_field() ?>
                    <?php if (isset($record['idContatto']) && $record['idContatto']): ?>
                        <input type="hidden" name="idContatto" value="<?= h($record['idContatto']) ?>">
                    <?php endif; ?>

                    <h5 class="text-primary mb-3 text-uppercase fs-6 fw-bold border-bottom pb-2">Dati Anagrafici</h5>

                    <div class="row g-3 mb-4">
                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" name="cliente[cognome]" value="<?= $cognome ?>"
                                    class="form-control <?= isset($errors['cognome']) ? 'is-invalid' : '' ?>"
                                    id="cognome" placeholder="Cognome">
                                <label for="cognome"><i class="bi bi-person me-1"></i> Cognome *</label>
                                <?= getFormError('cognome', $errors ?? []) ?>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" name="cliente[nome]" value="<?= $nome ?>"
                                    class="form-control <?= isset($errors['nome']) ? 'is-invalid' : '' ?>" id="nome"
                                    placeholder="Nome">
                                <label for="nome"><i class="bi bi-person me-1"></i> Nome *</label>
                                <?= getFormError('nome', $errors ?? []) ?>
                            </div>
                        </div>
                    </div>

                    <h5 class="text-primary mb-3 text-uppercase fs-6 fw-bold border-bottom pb-2">Recapiti e Residenza
                    </h5>

                    <div class="form-floating mb-3">
                        <input type="text" name="cliente[indirizzo]" value="<?= $indirizzo ?>"
                            class="form-control <?= isset($errors['indirizzo']) ? 'is-invalid' : '' ?>" id="indirizzo"
                            placeholder="Indirizzo">
                        <label for="indirizzo"><i class="bi bi-geo-alt me-1"></i> Indirizzo</label>
                        <?= getFormError('indirizzo', $errors ?? []) ?>
                    </div>

                    <div class="row g-3 mb-4">
                        <div class="col-md-8">
                            <div class="form-floating">
                                <select name="cliente[com_residenza_id]" class="form-select"
                                    id="com_residenza"><?= $optionsComuniResid ?></select>
                                <label for="com_residenza"><i class="bi bi-buildings me-1"></i> Citta Residenza</label>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-floating">
                                <input type="text" name="cliente[prov]" value="<?= $prov ?>"
                                    class="form-control <?= isset($errors['prov']) ? 'is-invalid' : '' ?>" id="prov"
                                    placeholder="BA" maxlength="2">
                                <label for="prov">Provincia</label>
                                <?= getFormError('prov', $errors ?? []) ?>
                            </div>
                        </div>
                    </div>

                    <h5 class="text-primary mb-3 text-uppercase fs-6 fw-bold border-bottom pb-2">Dati di Nascita</h5>

                    <div class="row g-3 mb-4">
                        <div class="col-md-4">
                            <div class="form-floating">
                                <input type="date" name="cliente[data_nascita]" value="<?= $data_nascita ?>"
                                    class="form-control <?= isset($errors['data_nascita']) ? 'is-invalid' : '' ?>"
                                    id="data_nascita" placeholder="Data Nascita">
                                <label for="data_nascita"><i class="bi bi-calendar-event me-1"></i> Data Nascita</label>
                                <?= getFormError('data_nascita', $errors ?? []) ?>
                            </div>
                        </div>
                        <div class="col-md-5">
                            <div class="form-floating">
                                <select name="cliente[com_nascita_id]" class="form-select"
                                    id="com_nascita"><?= $optionsComuniNasc ?></select>
                                <label for="com_nascita"><i class="bi bi-buildings me-1"></i> Citta Nascita</label>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-floating">
                                <input type="text" name="cliente[prov_nascita]" value="<?= $prov_nascita ?>"
                                    class="form-control" id="prov_nascita" placeholder="BA" maxlength="2">
                                <label for="prov_nascita">Prov. Nascita</label>
                            </div>
                        </div>
                    </div>

                    <h5 class="text-primary mb-3 text-uppercase fs-6 fw-bold border-bottom pb-2">Contatti</h5>

                    <div class="form-floating mb-3">
                        <input type="email" name="cliente[email]" value="<?= $email ?>"
                            class="form-control <?= isset($errors['email']) ? 'is-invalid' : '' ?>" id="email"
                            placeholder="nome@esempio.com">
                        <label for="email"><i class="bi bi-envelope me-1"></i> E-Mail</label>
                        <?= getFormError('email', $errors ?? []) ?>
                    </div>

                    <div class="row g-3 mb-4">
                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" name="cliente[cellulare]" value="<?= $cellulare ?>"
                                    class="form-control" id="cellulare" placeholder="Cellulare">
                                <label for="cellulare"><i class="bi bi-phone me-1"></i> Cellulare</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-floating">
                                <input type="text" name="cliente[telefono]" value="<?= $telefono ?>"
                                    class="form-control" id="telefono" placeholder="Telefono">
                                <label for="telefono"><i class="bi bi-telephone me-1"></i> Telefono</label>
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