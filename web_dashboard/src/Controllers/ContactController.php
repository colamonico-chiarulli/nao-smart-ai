<?php
/**
 * File: src/Controllers/ContactController.php
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

use App\Models\Contact;
use App\Core\View;
use App\Core\Router;
use App\Core\Auth;

/**
 * Controller per la gestione delle operazioni CRUD sui contatti.
 */
class ContactController
{
    private $contactModel;

    public function __construct()
    {
        Auth::requireAuth();
        $this->contactModel = new Contact();
    }


    /**
     * Mostra l'elenco dei contatti con paginazione, ordinamento e ricerca.
     */
    public function index()
    {
        $page = filter_input(INPUT_GET, 'page', FILTER_VALIDATE_INT) ?? 1;
        if ($page < 1)
            $page = 1;

        // Sorting params
        $sortCol = $_GET['sort'] ?? 'cognome';
        $sortOrder = $_GET['order'] ?? 'ASC';

        // Search param
        $search = $_GET['search'] ?? '';

        $limit = 8;
        $offset = ($page - 1) * $limit;

        $contacts = $this->contactModel->getPaginated($limit, $offset, $sortCol, $sortOrder, $search);
        $totalContacts = $this->contactModel->countAll($search);
        $totalPages = ceil($totalContacts / $limit);

        // Calcola ordine opposto per prossimo click
        $nextOrder = ($sortOrder === 'ASC') ? 'DESC' : 'ASC';

        View::render('contact/list', [
            'contacts' => $contacts,
            'currentPage' => $page,
            'totalPages' => $totalPages,
            'totalContacts' => $totalContacts,
            'currentSort' => $sortCol,
            'currentOrder' => $sortOrder,
            'nextOrder' => $nextOrder,
            'search' => $search
        ]);
    }

    /**
     * Mostra il form di inserimento.
     */
    public function create()
    {
        // Prepara dati per form (comuni)
        $comuniOptions = $this->getComuniOptions();
        View::render('contact/form', [
            'optionsComuni' => $comuniOptions,
            'action' => 'store',
            'title' => 'Aggiungi Cliente',
            'btnText' => 'Salva',
            'btnClass' => 'btn-success',
            'record' => $this->getEmptyRecord()
        ]);
    }

    /**
     * Salva il nuovo contatto nel database (Action).
     */
    public function store()
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (!verify_csrf_token())
                die("CSRF Invalid");

            $data = $_POST['cliente'];
            $errors = $this->validateInput($data);

            if (!empty($errors)) {
                // Ripresenta il form con errori
                $comuniOptions = $this->getComuniOptions();
                View::render('contact/form', [
                    'optionsComuni' => $comuniOptions,
                    'action' => 'store',
                    'title' => 'Aggiungi Cliente',
                    'btnText' => 'Salva',
                    'btnClass' => 'btn-success',
                    'record' => $data, // Dati inseriti
                    'errors' => $errors
                ]);
                return;
            }

            // Normalizzazione dati: trasforma stringhe vuote in NULL per i campi DATE
            if (empty($data['data_nascita'])) {
                $data['data_nascita'] = null;
            }

            if ($this->contactModel->create($data)) {
                header('Location: elenco'); // Redirect to list
                exit;
            }
        }
    }

    /**
     * Mostra il form di modifica per un contatto specifico.
     */
    public function edit()
    {
        $id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
        if (!$id)
            die("Invalid ID");

        $contact = $this->contactModel->getById($id);
        if (!$contact)
            die("Contact not found");

        $comuniOptionsResid = $this->getComuniOptions($contact['com_residenza_id']);
        $comuniOptionsNasc = $this->getComuniOptions($contact['com_nascita_id']);

        View::render('contact/form', [
            'optionsComuniResid' => $comuniOptionsResid,
            'optionsComuniNasc' => $comuniOptionsNasc,
            'action' => 'update',
            'title' => 'Modifica Cliente',
            'btnText' => 'Aggiorna',
            'btnClass' => 'btn-primary',
            'record' => $contact,
            'updateMode' => true
        ]);
    }

    /**
     * Aggiorna il contatto nel database (Action).
     */
    public function update()
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (!verify_csrf_token())
                die("CSRF Invalid");
            $id = $_POST['idContatto'];
            $data = $_POST['cliente'];

            $errors = $this->validateInput($data);

            if (!empty($errors)) {
                // Ripresenta il form con errori
                // Recupera id vecchi per options
                // Ricarichiamo options.
                $comuniOptionsResid = $this->getComuniOptions($data['com_residenza_id']);
                $comuniOptionsNasc = $this->getComuniOptions($data['com_nascita_id']);

                // Merge idContatto in record per hidden field
                $data['idContatto'] = $id;

                View::render('contact/form', [
                    'optionsComuniResid' => $comuniOptionsResid,
                    'optionsComuniNasc' => $comuniOptionsNasc,
                    'action' => 'update',
                    'title' => 'Modifica Cliente',
                    'btnText' => 'Aggiorna',
                    'btnClass' => 'btn-primary',
                    'record' => $data,
                    'errors' => $errors,
                    'updateMode' => true
                ]);
                return;
            }

            // Normalizzazione dati: trasforma stringhe vuote in NULL per i campi DATE
            if (empty($data['data_nascita'])) {
                $data['data_nascita'] = null;
            }

            if ($this->contactModel->update($id, $data)) {
                //header('Location: /anagrafe/elenco'); // Redirect to list
                Router::redirect('/anagrafe/elenco');
                exit;
            }
        }
    }

    /**
     * Mostra la conferma di cancellazione.
     */
    public function delete()
    {
        // Mostra conferma o esegui se POST
        // Per semplicità, se arriviamo qui via GET mostriamo conferma
        $id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
        if (!$id)
            die("Invalid ID");

        $contact = $this->contactModel->getById($id);

        View::render('contact/delete', ['contact' => $contact]);
    }

    /**
     * Esegue la cancellazione fisica dal database (Action).
     */
    public function destroy()
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (!verify_csrf_token())
                die("CSRF Invalid");
            $id = $_POST['idContatto'];
            $this->contactModel->delete($id);
            header('Location: elenco');
            exit;
        }
    }

    // Helpers privati

    /** 
     * Genera le opzioni HTML per la select comuni. 
     */
    private function getComuniOptions($selectedId = null)
    {
        $comuni = $this->contactModel->getComuni();
        $html = '';
        foreach ($comuni as $c) {
            $sel = ($c[0] == $selectedId) ? 'selected' : '';
            $html .= "<option value='{$c[0]}' $sel>{$c[1]}</option>";
        }
        return $html;
    }

    /**
     * Restituisce un array record vuoto per l'inizializzazione del form.
     */
    private function getEmptyRecord()
    {
        return [
            'idContatto' => '',
            'cognome' => '',
            'nome' => '',
            'indirizzo' => '',
            'com_residenza_id' => '',
            'prov' => '',
            'data_nascita' => '',
            'com_nascita_id' => '',
            'prov_nascita' => '',
            'email' => '',
            'cellulare' => '',
            'telefono' => ''
        ];
    }

    /**
     * Valida i dati di input del form.
     * 
     * @param array $input Dati del form ($_POST['cliente']).
     * @return array Array di errori (campo => messaggio).
     */
    private function validateInput($input)
    {
        $errors = [];

        if (empty($input['cognome'])) {
            $errors['cognome'] = "Il cognome è obbligatorio.";
        }

        if (empty($input['nome'])) {
            $errors['nome'] = "Il nome è obbligatorio.";
        }

        if (!empty($input['email']) && !filter_var($input['email'], FILTER_VALIDATE_EMAIL)) {
            $errors['email'] = "Formato email non valido.";
        }

        if (!empty($input['prov']) && strlen($input['prov']) !== 2) {
            $errors['prov'] = "Formato provincia non valido (2 caratteri).";
        }

        if (!empty($input['prov_nascita']) && strlen($input['prov_nascita']) !== 2) {
            $errors['prov_nascita'] = "Formato provincia non valida (2 caratteri).";
        }

        if (!empty($input['data_nascita'])) {
            // Controllo formato data YYYY-MM-DD
            $d = \DateTime::createFromFormat('Y-m-d', $input['data_nascita']);
            if (!$d || $d->format('Y-m-d') !== $input['data_nascita']) {
                $ernrors['data_nascita'] = "Data non valida (Formato richiesto: AAAA-MM-GG)";
            }
        }

        return $errors;
    }
}
