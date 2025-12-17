<?php
/**
 * File: src/Controllers/UserController.php
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


namespace App\Controllers;

use App\Models\User;
use App\Core\View;
use App\Core\Router;
use App\Core\Auth;

/*
 * Controller per la gestione degli utenti
 */
class UserController
{
    private $userModel;

    public function __construct()
    {
        Auth::requireAdmin();
        $this->userModel = new User();
    }

    /*
     * Mostra la lista degli utenti
     */
    public function index()
    {
        $page = filter_input(INPUT_GET, 'page', FILTER_VALIDATE_INT) ?? 1;
        if ($page < 1)
            $page = 1;

        $sortCol = $_GET['sort'] ?? 'last_name';
        $sortOrder = $_GET['order'] ?? 'ASC';
        $search = $_GET['search'] ?? '';

        $limit = 10;
        $offset = ($page - 1) * $limit;

        $users = $this->userModel->getPaginated($limit, $offset, $sortCol, $sortOrder, $search);
        $totalUsers = $this->userModel->countAll($search);
        $totalPages = ceil($totalUsers / $limit);
        $nextOrder = ($sortOrder === 'ASC') ? 'DESC' : 'ASC';

        View::render('user/list', [
            'users' => $users,
            'currentPage' => $page,
            'totalPages' => $totalPages,
            'totalUsers' => $totalUsers,
            'currentSort' => $sortCol,
            'currentOrder' => $sortOrder,
            'nextOrder' => $nextOrder,
            'search' => $search
        ]);
    }

    /*
     * Mostra la form per creare un nuovo utente
     */
    public function create()
    {
        View::render('user/form', [
            'action' => 'store',
            'title' => 'Aggiungi Utente',
            'btnText' => 'Salva',
            'btnClass' => 'btn-success',
            'record' => $this->getEmptyRecord(),
            'errors' => []
        ]);
    }

    /*
     * Salva un nuovo utente
     */
    public function store()
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (!verify_csrf_token())
                die("CSRF Invalid");

            $data = $_POST['user'];
            $errors = $this->validateInput($data);

            if (!empty($errors)) {
                View::render('user/form', [
                    'action' => 'store',
                    'title' => 'Aggiungi Utente',
                    'btnText' => 'Salva',
                    'btnClass' => 'btn-success',
                    'record' => $data,
                    'errors' => $errors
                ]);
                return;
            }

            // Hash password
            if (!empty($data['password'])) {
                $data['password'] = password_hash($data['password'], PASSWORD_DEFAULT);
            }

            if ($this->userModel->create($data)) {
                Router::redirect('users');
                exit;
            }
        }
    }

    /*
     * Mostra la form per modificare un utente
     */
    public function edit()
    {
        $id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
        if (!$id)
            die("Invalid ID");

        $user = $this->userModel->getById($id);
        if (!$user)
            die("User not found");

        // Rimuove la password dalla visualizzazione
        $user['password'] = '';

        View::render('user/form', [
            'action' => 'update',
            'title' => 'Modifica Utente',
            'btnText' => 'Aggiorna',
            'btnClass' => 'btn-primary',
            'record' => $user,
            'updateMode' => true,
            'errors' => []
        ]);
    }

    /*
     * Aggiorna un utente
     */
    public function update()
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (!verify_csrf_token())
                die("CSRF Invalid");

            $id = $_POST['id'];
            $data = $_POST['user'];

            $errors = $this->validateInput($data, true);

            if (!empty($errors)) {
                $data['id'] = $id;
                View::render('user/form', [
                    'action' => 'update',
                    'title' => 'Modifica Utente',
                    'btnText' => 'Aggiorna',
                    'btnClass' => 'btn-primary',
                    'record' => $data,
                    'updateMode' => true,
                    'errors' => $errors
                ]);
                return;
            }

            // Gestisce la password
            if (!empty($data['password'])) {
                $data['password'] = password_hash($data['password'], PASSWORD_DEFAULT);
            } else {
                unset($data['password']); // Model will handle this
            }

            if ($this->userModel->update($id, $data)) {
                Router::redirect('users');
                exit;
            }
        }
    }

    /*
     * Mostra la form per eliminare un utente
     */
    public function delete()
    {
        $id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
        if (!$id)
            die("Invalid ID");
        $user = $this->userModel->getById($id);
        View::render('user/delete', ['user' => $user]);
    }

    /*
     * Elimina un utente
     */
    public function destroy()
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (!verify_csrf_token())
                die("CSRF Invalid");
            $id = $_POST['id'];
            $this->userModel->delete($id);
            Router::redirect('users');
            exit;
        }
    }

    /*
     * Restituisce un record vuoto
     */
    private function getEmptyRecord()
    {
        return [
            'id' => '',
            'last_name' => '',
            'first_name' => '',
            'organization' => '',
            'email' => '',
            'password' => '',
            'phone' => '',
            'role' => 'user'
        ];
    }

    /*
     * Validazione input
     */
    private function validateInput($input, $isUpdate = false)
    {
        $errors = [];

        if (empty($input['last_name']))
            $errors['last_name'] = "Cognome obbligatorio";
        if (empty($input['first_name']))
            $errors['first_name'] = "Nome obbligatorio";

        if (empty($input['email']) || !filter_var($input['email'], FILTER_VALIDATE_EMAIL)) {
            $errors['email'] = "Email non valida";
        }

        // Password required on create, optional on update (if empty)
        if (!$isUpdate && empty($input['password'])) {
            $errors['password'] = "Password obbligatoria";
        }

        return $errors;
    }
}
