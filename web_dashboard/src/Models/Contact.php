<?php
/**
 * File: src/Models/Contact.php
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


namespace App\Models;

use App\Core\Database;

/**
 * Model per la gestione dei Contatti nel database.
 */
class Contact
{
    private $db;

    /**
     * Costruttore. Ottiene l'istanza del database.
     */
    public function __construct()
    {
        $this->db = Database::getInstance()->getConnection();
    }

    /**
     * Recupera tutti i contatti.
     * 
     * @return array Array di array associativi con i dati dei contatti.
     */
    public function getAll()
    {
        $query = "SELECT idContatto, cognome, nome, email, telefono FROM anagrafe";
        return $this->db->query($query)->fetch_all(MYSQLI_ASSOC);
    }

    /**
     * Recupera un singolo contatto per ID.
     * 
     * @param int $id ID del contatto.
     * @return array|null Dati del contatto o null se non trovato.
     */
    public function getById($id)
    {
        $stmt = $this->db->prepare("SELECT * FROM anagrafe WHERE IdContatto = ?");
        $stmt->bind_param("i", $id);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_assoc();
    }

    /**
     * Crea un nuovo contatto.
     * 
     * @param array $data Dati del form validati.
     * @return bool True se successo, False altrimenti.
     */
    public function create($data)
    {
        $sql = "INSERT INTO anagrafe (cognome, nome, indirizzo, com_residenza_id, prov, data_nascita, com_nascita_id, prov_nascita, email, cellulare, telefono) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param(
            "sssisssssss",
            $data['cognome'],
            $data['nome'],
            $data['indirizzo'],
            $data['com_residenza_id'],
            $data['prov'],
            $data['data_nascita'],
            $data['com_nascita_id'],
            $data['prov_nascita'],
            $data['email'],
            $data['cellulare'],
            $data['telefono']
        );
        return $stmt->execute();
    }

    /**
     * Aggiorna un contatto esistente.
     * 
     * @param int $id ID del contatto.
     * @param array $data Dati aggiornati.
     * @return bool True se successo.
     */
    public function update($id, $data)
    {
        $sql = "UPDATE anagrafe SET cognome=?, nome=?, indirizzo=?, com_residenza_id=?, prov=?, data_nascita=?, com_nascita_id=?, prov_nascita=?, email=?, cellulare=?, telefono=? WHERE idContatto=?";
        $stmt = $this->db->prepare($sql);
        $stmt->bind_param(
            "sssisssssssi",
            $data['cognome'],
            $data['nome'],
            $data['indirizzo'],
            $data['com_residenza_id'],
            $data['prov'],
            $data['data_nascita'],
            $data['com_nascita_id'],
            $data['prov_nascita'],
            $data['email'],
            $data['cellulare'],
            $data['telefono'],
            $id
        );
        return $stmt->execute();
    }

    /**
     * Cancella un contatto.
     * 
     * @param int $id ID del contatto.
     * @return bool True se successo.
     */
    public function delete($id)
    {
        $stmt = $this->db->prepare("DELETE FROM anagrafe WHERE idContatto = ?");
        $stmt->bind_param("i", $id);
        return $stmt->execute();
    }

    /**
     * Recupera l'elenco dei comuni per le select.
     * 
     * @return array Array di comuni.
     */
    public function getComuni()
    {
        return $this->db->query("SELECT idComune, comune FROM comuni ORDER BY comune")->fetch_all(MYSQLI_NUM);
    }

    /**
     * Conta il numero totale di contatti, eventualmente filtrati.
     * 
     * @param string $search Filtro di ricerca per cognome.
     * @return int Numero totale di contatti.
     */
    public function countAll($search = '')
    {
        $sql = "SELECT COUNT(*) as total FROM anagrafe";
        if (!empty($search)) {
            $sql .= " WHERE cognome LIKE ?";
        }

        $stmt = $this->db->prepare($sql);

        if (!empty($search)) {
            $wildcard = "%$search%";
            $stmt->bind_param("s", $wildcard);
        }

        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
        return (int) $row['total'];
    }

    /**
     * Recupera i contatti per la pagina corrente con ordinamento e filtro.
     * 
     * @param int $limit Numero di contatti per pagina.
     * @param int $offset Offset per la query.
     * @param string $sortCol Colonna per ordinamento (allowlist: idContatto, cognome).
     * @param string $sortOrder Ordine (ASC, DESC).
     * @param string $search Filtro di ricerca per cognome.
     * @return array Array di contatti.
     */
    public function getPaginated($limit = 10, $offset = 0, $sortCol = 'cognome', $sortOrder = 'ASC', $search = '')
    {
        // Allowlist per colonne ordinabili per sicurezza
        $allowedCols = ['idContatto', 'cognome'];
        if (!in_array($sortCol, $allowedCols)) {
            $sortCol = 'cognome';
        }

        $sortOrder = strtoupper($sortOrder);
        if (!in_array($sortOrder, ['ASC', 'DESC'])) {
            $sortOrder = 'ASC';
        }

        $sql = "SELECT idContatto, cognome, nome, email, telefono FROM anagrafe";
        if (!empty($search)) {
            $sql .= " WHERE cognome LIKE ?";
        }
        $sql .= " ORDER BY $sortCol $sortOrder LIMIT ? OFFSET ?";

        $stmt = $this->db->prepare($sql);

        if (!empty($search)) {
            $wildcard = "%$search%";
            $stmt->bind_param("sii", $wildcard, $limit, $offset);
        } else {
            $stmt->bind_param("ii", $limit, $offset);
        }

        $stmt->execute();
        return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    }
}
