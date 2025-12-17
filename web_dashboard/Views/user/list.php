<?php
/**
 * File: src/Views/user/list.php
 * @package NAO-Smart-AI
 * @author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
 *
 * Created Date: Tuesday, December 17th 2025, 10:52:06 pm
 * -----
 * Last Modified: 	December 17th 2025 10:52:06 pm
 * Modified By: <?php	Rino Andriano <andriano@colamonicochiarulli.edu.it>
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

// Variabili disponibili: $users, $currentPage, $totalPages, 
// $totalUsers, $search, $currentSort, $currentOrder, $nextOrder
?>

<div class="row justify-content-center">
    <div class="col-lg-12">
        <div class="card shadow border-0 rounded-4">
            <div
                class="card-header bg-primary text-white py-3 rounded-top-4 d-flex flex-column flex-md-row justify-content-between align-items-center gap-3">
                <h4 class="mb-0"><i class="bi bi-people-fill me-2"></i>Elenco Utenti</h4>
                <div class="d-flex gap-2">
                    <form action="" method="GET" class="d-flex">
                        <div class="input-group">
                            <input type="text" name="search" class="form-control form-control-sm"
                                placeholder="Cerca cognome/email..." value="<?= h($search ?? '') ?>">
                            <?php if (!empty($search)): ?>
                                <a href="?" class="btn btn-light btn-sm" title="Rimuovi filtro"><i
                                        class="bi bi-x-lg text-danger"></i></a>
                            <?php endif; ?>
                            <button class="btn btn-light btn-sm fw-bold text-primary" type="submit"><i
                                    class="bi bi-search"></i></button>
                        </div>
                    </form>
                    <a href="<?= url('users/create') ?>"
                        class="btn btn-light btn-sm fw-bold text-primary shadow-sm text-nowrap">
                        <i class="bi bi-person-plus-fill me-1"></i> Aggiungi
                    </a>
                </div>
            </div>
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0 align-middle">
                        <thead class="table-light">
                            <tr>
                                <th class="text-center" style="width: 100px;">Operazioni</th>
                                <th>
                                    <a href="?page=1&sort=id&order=<?= ($currentSort == 'id') ? $nextOrder : 'ASC' ?>&search=<?= h($search) ?>"
                                        class="text-decoration-none text-dark d-block">
                                        Id
                                        <?php if ($currentSort == 'id'): ?>
                                            <i
                                                class="bi bi-sort-numeric-<?= ($currentOrder == 'ASC') ? 'down' : 'up' ?>"></i>
                                        <?php else: ?>
                                            <i class="bi bi-arrow-down-up text-muted opacity-25"></i>
                                        <?php endif; ?>
                                    </a>
                                </th>
                                <th>
                                    <a href="?page=1&sort=last_name&order=<?= ($currentSort == 'last_name') ? $nextOrder : 'ASC' ?>&search=<?= h($search) ?>"
                                        class="text-decoration-none text-dark d-block">
                                        Cognome
                                        <?php if ($currentSort == 'last_name'): ?>
                                            <i class="bi bi-sort-alpha-<?= ($currentOrder == 'ASC') ? 'down' : 'up' ?>"></i>
                                        <?php else: ?>
                                            <i class="bi bi-arrow-down-up text-muted opacity-25"></i>
                                        <?php endif; ?>
                                    </a>
                                </th>
                                <th>Nome</th>
                                <th>Organizzazione</th>
                                <th>Email</th>
                                <th>Ruolo</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($users)): ?>
                                <tr>
                                    <td colspan="7" class="text-center py-4 text-muted">
                                        <i class="bi bi-inbox fs-4 d-block mb-2"></i>
                                        Nessun utente trovato.
                                    </td>
                                </tr>
                            <?php else: ?>
                                <?php foreach ($users as $user): ?>
                                    <tr>
                                        <?php
                                        $id = h($user['id']);
                                        $last_name = h($user['last_name']);
                                        $first_name = h($user['first_name']);
                                        $org = h($user['organization']);
                                        $email = h($user['email']);
                                        $role = h($user['role']);
                                        ?>
                                        <td class="text-center">
                                            <div class="btn-group btn-group-sm" role="group">
                                                <a href="<?= url('users/edit') ?>?id=<?= $id ?>" class="btn btn-outline-primary"
                                                    title="Modifica">
                                                    <i class="bi bi-pencil"></i>
                                                </a>
                                                <a href="<?= url('users/delete') ?>?id=<?= $id ?>"
                                                    class="btn btn-outline-danger" title="Elimina">
                                                    <i class="bi bi-trash"></i>
                                                </a>
                                            </div>
                                        </td>
                                        <td><span class="badge bg-secondary"><?= $id ?></span></td>
                                        <td class="fw-bold"><?= $last_name ?></td>
                                        <td><?= $first_name ?></td>
                                        <td><?= $org ?></td>
                                        <td>
                                            <a href="mailto:<?= $email ?>" class="text-decoration-none text-body">
                                                <i class="bi bi-envelope text-muted me-1"></i><?= $email ?>
                                            </a>
                                        </td>
                                        <td>
                                            <?php if ($role === 'admin'): ?>
                                                <span class="badge bg-danger">Admin</span>
                                            <?php else: ?>
                                                <span class="badge bg-info text-dark">User</span>
                                            <?php endif; ?>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>

            <?php if (isset($totalPages) && $totalPages > 1): ?>
                <div class="card-footer bg-light py-3 border-top-0 rounded-bottom-4">
                    <nav aria-label="Page navigation">
                        <ul class="pagination justify-content-center mb-0">
                            <li class="page-item <?= ($currentPage <= 1) ? 'disabled' : '' ?>">
                                <a class="page-link"
                                    href="?page=<?= $currentPage - 1 ?>&sort=<?= $currentSort ?>&order=<?= $currentOrder ?>&search=<?= h($search) ?>"
                                    aria-label="Previous">
                                    <span aria-hidden="true">&laquo;</span>
                                </a>
                            </li>

                            <?php for ($i = 1; $i <= $totalPages; $i++): ?>
                                <li class="page-item <?= ($i == $currentPage) ? 'active' : '' ?>">
                                    <a class="page-link"
                                        href="?page=<?= $i ?>&sort=<?= $currentSort ?>&order=<?= $currentOrder ?>&search=<?= h($search) ?>"><?= $i ?></a>
                                </li>
                            <?php endfor; ?>

                            <li class="page-item <?= ($currentPage >= $totalPages) ? 'disabled' : '' ?>">
                                <a class="page-link"
                                    href="?page=<?= $currentPage + 1 ?>&sort=<?= $currentSort ?>&order=<?= $currentOrder ?>&search=<?= h($search) ?>"
                                    aria-label="Next">
                                    <span aria-hidden="true">&raquo;</span>
                                </a>
                            </li>
                        </ul>
                    </nav>
                    <div class="text-center text-muted small mt-2">
                        Totale utenti: <strong><?= $totalUsers ?? 0 ?></strong> - Pagina
                        <strong><?= $currentPage ?></strong> di <strong><?= $totalPages ?></strong>
                    </div>
                </div>
            <?php endif; ?>
        </div>
    </div>
</div>